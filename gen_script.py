import os

from jinja2 import Template


def generate_script(**kwargs):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    tmpl_path = os.path.join(dir_path, 'script.sh.j2')

    with open(tmpl_path) as f:
        tmpl = Template(f.read())

    rendered_template = tmpl.render(**kwargs)
    return rendered_template


def read_csv(filename: str='vocab.csv'):
    pass


if __name__ == '__main__':
    words = read_csv()

    # TODO
    words, parts_of_speech, defns, examples = []

    # mdzhang: hack to circumvent bash script quote escape rules
    exs = tuple(map(lambda x: x.replace("'", ''), examples))
    script_str = generate_script(words=tuple(words),
                                 parts_of_speech=tuple(parts_of_speech),
                                 definitions=tuple(defns),
                                 examples=exs)
    print(script_str)
