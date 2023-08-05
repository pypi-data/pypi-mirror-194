# ipsum

[![Tests](https://github.com/dtrifuno/ipsum/workflows/check-library/badge.svg)](https://github.com/dtrifuno/ipsum/actions?workflow=check-library)
[![PyPI version](https://badge.fury.io/py/ipsum.svg)](https://badge.fury.io/py/ipsum)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ipsum is a Python library for the generation of international placeholder text.

Unlike most other generators which work by scrambling a
particular text ([e.g. Lorem Ipsum generators with Cicero's "De Finibus Bonorum
et Malorum"](https://loremipsum.io/)), it instead uses Markov models to generate
a vocabulary of meaningless new words that resemble the language it was trained
on. This allows for the generation of text that is typographically similar to a
specified language (i.e. uses the same alphabet and punctuation, in the same manner
and at the same frequency), but is semantically meaningless.

You can read more about how Ipsum works [here](https://trifunovski.me/posts/230225-lorem-ipsum-or-the-procedural-generation-of-typographically-plausible-nonsense).

You can use Ipsum directly from your browser by accessing the web app at
[ipsum.trifunovski.me](https://ipsum.trifunovski.me).

It currently supports the following languages:

- English
- German
- Albanian
- Bulgarian
- Dutch
- English
- French
- German
- Greek
- Italian
- Macedonian
- Serbian
- Spanish
- Swedish

## Installing

Note that `ipsum` requires Python >= 3.8.1.

Run

```
pip install ipsum
```

to install the latest published version of the library, or clone the repo and
use `poetry`

```
git clone git@github.com:dtrifuno/ipsum
cd ipsum/ipsum
poetry install
```

to install a development copy.

## Usage

```python
import ipsum

# Load the English language model
model = ipsum.load_model("en")

# Returns a list of 3 strings, each resembling a paragraph of English
paragraphs = model.generate_paragraphs(3)

# Returns a list of 10 strings, each resembling a full sentence of English
sentences = model.generate_sentences(10)

# Returns a list of 50 words (does not include any punctuation)
words = model.generate_words(50)
```

## Development

### Typechecking, linting and testing

You can run

```
poetry run mypy /src /tests
```

to typecheck,

```
poetry run flake8
```

to lint, or

```
poetry run pytest --cov
```

to test the code.

### Additional scripts

This repository contains several scripts that are useful in development, but are
not included with the PyPI package. If you want to make a change to this library,
please clone the repository instead. You can check out these scripts and what
they do by running `poetry run dev`.

### Adding a language

1. Find out the two-letter [ISO 639-1](https://quickref.me/iso-639-1) code of
   the language you want to add (`xx` for the rest of this subsection). Add the
   full English name and ISO 639-1 code of the language to `supported_languages.py`.
2. Prepare a corpus of texts in the language. The corpus should be packaged as a
   zip archive of `.txt` files.
3. Write a parser for the language (look at `src/ipsum/parse/en_parser.py` for
   an example). Name the `Parser` instance `xx_parser` and save it as
   `src/ipsum/parse/language/xx.py`. Add the parser instance to `load_parser`
   in `src/ipsum/parse/__init__.py`.
4. Run `poetry run dev parser-diagnostics xx`. Ideally, the parser should
   detect around 100,000 sentences and be able to parse into skeletons more
   than 50&ndash;60% of them.
5. Run `poetry run dev build_model xx && poetry run model_diagnostics xx`.
6. Inspect `diagnostics/xx.png`. If it looks good, congrats, you are done!
   Otherwise, return to Step 2 and try to figure out what went wrong.

## Corpora

The models were trained on the following corpora:

- **Albanian**: [Leipzig Corpora Collection - 2020 Albanian News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Albanian)
- **Bulgarian**: [Bulgarian National Corpus - Diachronic corpus for the period of 1951&ndash;2021](https://dcl.bas.bg/bulnc/en/dostap/izteglyane/)
- **Dutch**: [Leipzig Corpora Collection - 2020 Dutch News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Dutch)
- **English**: Selections from [Computational Stylistics Group - 100 English Novels ver. 1.4](https://github.com/computationalstylistics/100_english_novels)
- **French**: [Leipzig Corpora Collection - 2018 French News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/French)
- **German**: [Computational Stylistics Group - 68 German Novels](https://github.com/computationalstylistics/68_german_novels)
- **Greek**: [Monolingual Greek corpus in the culture domain](https://elrc-share.eu/repository/browse/monolingual-greek-corpus-in-the-culture-domain-processed/ab62bd021d5211e9b7d400155d0267069bdba50723a1456cbf1af2dce2201a63/)
- **Italian**: [Leipzig Corpora Collection - 2019 Italian News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Italian)
- **Macedonian**: Selections from [Electronic Corpus of Macedonian Literary Texts - 135 Тома Македонска Книжевност](http://drmj.manu.edu.mk/%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D1%81%D0%BA%D0%B8-%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81-%D0%BD%D0%B0-%D0%BC%D0%B0%D0%BA%D0%B5%D0%B4%D0%BE%D0%BD%D1%81%D0%BA%D0%B8-%D0%BA%D0%BD%D0%B8/)
- **Serbian**: [Leipzig Corpora Collection - 2016 Serbian Wikipedia 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Serbian)
- **Spanish**: [Leipzig Corpora Collection - 2016 Spanish News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Spanish)
- **Swedish**: [Leipzig Corpora Collection - 2019 Swedish News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Swedish)

## License

[MIT](https://github.com/dtrifuno/ipsum/ipsum/blob/main/LICENSE.md)
