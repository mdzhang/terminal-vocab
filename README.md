# Command Line Vocab

Like [`sudocabulary`](https://github.com/badarsh2/Sudocabulary) but allows for loading custom vocab lists based on environment variables.
Uses "Advanced" GRE words from [Magoosh's](https://gre.magoosh.com/) vocab list, as an example.

## Screenshot

<img width="1422" alt="screenshot 2018-07-31 09 46 12" src="https://user-images.githubusercontent.com/3429763/43463460-9a315672-94a6-11e8-92b4-10f7c15d083b.png">

## Installation

With [basher][basher]

  ```sh
  basher install mdzhang/magoosh-vocab
  ```

Manually:

1. Download the `bin/vocab` executable and move it onto your path e.g.
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

### Custom Vocab Lists

1. Make a JSON file where each entry in a top level array has the keys:
  - `word`: the vocab word
  - `meaning`: the definition of the word
  - `pos`: aka part of speech
  - `example`: a sentence using the word in an example
1. Add the file under `$VOCAB_HOME/data/<file name>.json`
  - by default, `VOCAB_HOME` is the `data` directory alongside the `vocab` executable; if you used [basher][basher] to install this, then it would be e.g. `~/.basher/cellar/packages/mdzhang/magoosh-vocab/data`
  - you can override this to point to some other directory on your host
1. Change your environment variable `VOCAB_SET` to match `<file name>`
1. Profit

## License

MIT

[basher]: https://github.com/basherpm/basher
