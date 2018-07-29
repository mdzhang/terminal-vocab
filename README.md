# Magoosh Vocab

Like [`sudocabulary`](https://github.com/badarsh2/Sudocabulary) but for GRE words from [Magoosh's](https://gre.magoosh.com/) vocab list, since sudocabulary's vocab list is pretty basic.


## System Requirements

- python 3+ runtime


## Usage

1. Install requirements

  ```sh
  pip install -r requirements.txt
  ```

1. Generate the script

  ```sh
  python convert.py > vocab
  ```

1. Ensure the script is executable

  ```sh
  chmod u+x vocab
  ```

1. Move the executable onto your path

  ```sh
  export PATH="~/.local/bin:$PATH"
  mv vocab ~/.local/bin
  ```

1. Ensure shell runs script on startup by adding the following to e.g. your `~/.bashrc`

  ```sh
  if [ -f ~/.local/bin/vocab ]; then
    ~/.local/bin/vocab
  fi
  ```
