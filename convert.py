import logging
import os
import re
import typing as T

from jinja2 import Template

logger = logging.getLogger()

INPUT_FILE_NAME = 'vocab.txt'
DEFN_LINE_PATT = re.compile(r'^(\w+) \((\w+)\): (.+)\n$')


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


def parse_txt(filename: str) -> T.Tuple:
    """Parse the magoosh vocab txt export file to a list of

    :return: tuple of (words, parts_of_speech, definitions, examples)
    """
    words = []
    parts_of_speech = []
    definitions = []
    examples = []

    with open(filename, 'r') as f:
        it = iter(f)
        long_defn = next(it)

        while long_defn:
            long_defn, (word, pos, defn, full_example) = \
                parse_txt_inner(it, long_defn)

            words.append(word.lower())
            parts_of_speech.append(pos)
            definitions.append(defn)
            examples.append(full_example)

    return words, parts_of_speech, definitions, examples


def generate_script(**kwargs):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    tmpl_path = os.path.join(dir_path, 'script.sh.j2')

    with open(tmpl_path) as f:
        tmpl = Template(f.read())

    rendered_template = tmpl.render(**kwargs)
    return rendered_template


if __name__ == '__main__':
    words, parts_of_speech, defns, examples = parse_txt(INPUT_FILE_NAME)
    exs = tuple(map(lambda x: x.replace("'", ''), examples))
    script_str = generate_script(words=tuple(words),
                                 parts_of_speech=tuple(parts_of_speech),
                                 definitions=tuple(defns),
                                 examples=exs)
    print(script_str)
