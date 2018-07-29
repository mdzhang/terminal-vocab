# Magoosh Vocab

Like [`sudocabulary`](https://github.com/badarsh2/Sudocabulary) but for GRE words from [Magoosh's](https://gre.magoosh.com/) vocab list, since sudocabulary's vocab list is pretty basic.

## System Requirements

- python 3+ runtime

## Installation

With [basher](https://github.com/basherpm/basher):

  ```sh
  basher install mdzhang/magoosh-vocab
  ```

Manually:

1. Download the `bin/vocab/` executable and move it onto your path e.g.
    ```sh
    export PATH="~/.local/bin:$PATH"
    mv vocab ~/.local/bin
    ```

1. Ensure shell runs script on startup by adding the following to e.g. your `~/.bashrc`
    ```sh
    if which vocab > /dev/null; then
      vocab
    fi
    ```

## Contributing

To regenerate `bin/vocab` after changing the vocab txt file:

1. Install requirements
    ```sh
    pip install -r requirements.txt
    ```

1. Generate the script
    ```sh
    python convert.py > ./bin/vocab
    ```

1. Ensure the script is executable
    ```sh
    chmod u+x ./bin/vocab
    ```

## License

MIT
