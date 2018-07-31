import logging
import os
import re
import typing as T
from collections import namedtuple
from enum import Enum

logger = logging.getLogger()

Word = namedtuple('Word', ['name', 'definition', 'part_of_speech', 'example'])
INPUT_FILE_NAME = 'magoosh-gre-1000-words_oct01.txt'
DEFN_LINE_PATT = re.compile(r'^(\w+) \((\w+)\): (.+)\n$')

IGNORE_LINES = [
    'This word has other definitions but this is the most important one for the GRE',
    'gre.magoosh.com/flashcards',
    '---'
]


class LineType(Enum):
    SKIP = 'SKIP'
    DEFN = 'DEFINITION'
    CONT = 'CONTINUATION'
    EXMP = 'EXAMPLE'


def parse_txt_inner(it, long_defn: str):
    """Given a file iterator, parse the next word with its definition,
    part of speech, and example

    Helper for parse_txt

    :param it: iterator over lines in a filee
    :param long_defn: next line in file, expected to match the DEFN_LINE_PATT
    :return: line for _next_ words definition, and a tuple
        (word, definition, part of speech, example usage)
    """
    # first line starts to define a word
    match = re.match(DEFN_LINE_PATT, long_defn)

    if not match:
        msg = "Line didn't match pattern: {}".format(long_defn)
        logger.error(msg)
        raise ValueError(msg)

    word, pos, defn = match.groups()
    full_example = ''
    long_defn = None

    # ensuing lines may result from a long definition if they don't
    # start with a capital letter
    # mdzhang: this is not a great estimator
    end_of_cont_defn = False
    while not end_of_cont_defn:
        try:
            cont_defn = next(it)
        except StopIteration:
            end_of_cont_defn = True
            continue

        if cont_defn[0].isupper():
            full_example = cont_defn
            end_of_cont_defn = True
        else:
            defn += ' ' + cont_defn.rstrip('\n')

    # examples may also consist of multiple lines
    # we know they end when the next line to look at looks like the
    # start of the definition for a new word
    end_of_example = False
    while not end_of_example:
        try:
            example = next(it)
        except StopIteration:
            end_of_example = True
            continue

        if re.match(DEFN_LINE_PATT, example):
            long_defn = example
            end_of_example = True
        else:
            full_example += ' ' + example.rstrip('\n')

    return long_defn, (word, pos, defn, full_example.strip())


def parse_next_definition(it):
    # skip over cruft
    type_, *contents = next_line(it)

    while type_ == LineType.SKIP:
        type_, *contents = next_line(it)

    if type_ != LineType.DEFN:
        raise ValueError(f'Definition must come first; got {type_.value}')

    # parse word definition
    name = contents['name']
    part_of_speech = contents['part_of_speech']
    defn = contents['definition']

    type_, *contents = next_line(it)

    while type_ == LineType.CONT:
        line = next(it)
        type_, *contents = eval_line(line)

    # parse word example


def parse_txt(filename: str) -> T.Tuple:
    """Parse the magoosh vocab txt export file to a list of

    :return: tuple of (words, parts_of_speech, definitions, examples)
    """
    words = []
    should_continue = True

    with open(filename, 'r') as f:
        it = iter(f)
        while should_continue:
            word = parse_next_definition(it)

            if not word:
                should_continue = False
            else:
                words.append(word)

    return words


def write_csv(words: T.Iterable[Word]):
    pass


if __name__ == '__main__':
    words = parse_txt(INPUT_FILE_NAME)
    write_csv(words)
