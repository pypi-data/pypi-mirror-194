# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipsum', 'ipsum.model', 'ipsum.parse', 'ipsum.parse.language']

package_data = \
{'': ['*'], 'ipsum': ['trained_models/*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['dev = ipsum.dev.main:app']}

setup_kwargs = {
    'name': 'ipsum',
    'version': '0.1.1',
    'description': 'Library for procedurally-generating text that resembles a particular language.',
    'long_description': '# ipsum\n\n[![Tests](https://github.com/dtrifuno/ipsum/workflows/check-library/badge.svg)](https://github.com/dtrifuno/ipsum/actions?workflow=check-library)\n[![PyPI version](https://badge.fury.io/py/ipsum.svg)](https://badge.fury.io/py/ipsum)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nIpsum is a Python library for the generation of international placeholder text.\n\nUnlike most other generators which work by scrambling a\nparticular text ([e.g. Lorem Ipsum generators with Cicero\'s "De Finibus Bonorum\net Malorum"](https://loremipsum.io/)), it instead uses Markov models to generate\na vocabulary of meaningless new words that resemble the language it was trained\non. This allows for the generation of text that is typographically similar to a\nspecified language (i.e. uses the same alphabet and punctuation, in the same manner\nand at the same frequency), but is semantically meaningless.\n\nYou can read more about how Ipsum works [here](https://trifunovski.me/posts/230225-lorem-ipsum-or-the-procedural-generation-of-typographically-plausible-nonsense).\n\nYou can use Ipsum directly from your browser by accessing the web app at\n[ipsum.trifunovski.me](https://ipsum.trifunovski.me).\n\nIt currently supports the following languages:\n\n- English\n- German\n- Albanian\n- Bulgarian\n- Dutch\n- English\n- French\n- German\n- Greek\n- Italian\n- Macedonian\n- Serbian\n- Spanish\n- Swedish\n\n## Installing\n\nNote that `ipsum` requires Python >= 3.8.1.\n\nRun\n\n```\npip install ipsum\n```\n\nto install the latest published version of the library, or clone the repo and\nuse `poetry`\n\n```\ngit clone git@github.com:dtrifuno/ipsum\ncd ipsum/ipsum\npoetry install\n```\n\nto install a development copy.\n\n## Usage\n\n```python\nimport ipsum\n\n# Load the English language model\nmodel = ipsum.load_model("en")\n\n# Returns a list of 3 strings, each resembling a paragraph of English\nparagraphs = model.generate_paragraphs(3)\n\n# Returns a list of 10 strings, each resembling a full sentence of English\nsentences = model.generate_sentences(10)\n\n# Returns a list of 50 words (does not include any punctuation)\nwords = model.generate_words(50)\n```\n\n## Development\n\n### Typechecking, linting and testing\n\nYou can run\n\n```\npoetry run mypy /src /tests\n```\n\nto typecheck,\n\n```\npoetry run flake8\n```\n\nto lint, or\n\n```\npoetry run pytest --cov\n```\n\nto test the code.\n\n### Additional scripts\n\nThis repository contains several scripts that are useful in development, but are\nnot included with the PyPI package. If you want to make a change to this library,\nplease clone the repository instead. You can check out these scripts and what\nthey do by running `poetry run dev`.\n\n### Adding a language\n\n1. Find out the two-letter [ISO 639-1](https://quickref.me/iso-639-1) code of\n   the language you want to add (`xx` for the rest of this subsection). Add the\n   full English name and ISO 639-1 code of the language to `supported_languages.py`.\n2. Prepare a corpus of texts in the language. The corpus should be packaged as a\n   zip archive of `.txt` files.\n3. Write a parser for the language (look at `src/ipsum/parse/en_parser.py` for\n   an example). Name the `Parser` instance `xx_parser` and save it as\n   `src/ipsum/parse/language/xx.py`. Add the parser instance to `load_parser`\n   in `src/ipsum/parse/__init__.py`.\n4. Run `poetry run dev parser-diagnostics xx`. Ideally, the parser should\n   detect around 100,000 sentences and be able to parse into skeletons more\n   than 50&ndash;60% of them.\n5. Run `poetry run dev build_model xx && poetry run model_diagnostics xx`.\n6. Inspect `diagnostics/xx.png`. If it looks good, congrats, you are done!\n   Otherwise, return to Step 2 and try to figure out what went wrong.\n\n## Corpora\n\nThe models were trained on the following corpora:\n\n- **Albanian**: [Leipzig Corpora Collection - 2020 Albanian News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Albanian)\n- **Bulgarian**: [Bulgarian National Corpus - Diachronic corpus for the period of 1951&ndash;2021](https://dcl.bas.bg/bulnc/en/dostap/izteglyane/)\n- **Dutch**: [Leipzig Corpora Collection - 2020 Dutch News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Dutch)\n- **English**: Selections from [Computational Stylistics Group - 100 English Novels ver. 1.4](https://github.com/computationalstylistics/100_english_novels)\n- **French**: [Leipzig Corpora Collection - 2018 French News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/French)\n- **German**: [Computational Stylistics Group - 68 German Novels](https://github.com/computationalstylistics/68_german_novels)\n- **Greek**: [Monolingual Greek corpus in the culture domain](https://elrc-share.eu/repository/browse/monolingual-greek-corpus-in-the-culture-domain-processed/ab62bd021d5211e9b7d400155d0267069bdba50723a1456cbf1af2dce2201a63/)\n- **Italian**: [Leipzig Corpora Collection - 2019 Italian News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Italian)\n- **Macedonian**: Selections from [Electronic Corpus of Macedonian Literary Texts - 135 Тома Македонска Книжевност](http://drmj.manu.edu.mk/%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D1%81%D0%BA%D0%B8-%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81-%D0%BD%D0%B0-%D0%BC%D0%B0%D0%BA%D0%B5%D0%B4%D0%BE%D0%BD%D1%81%D0%BA%D0%B8-%D0%BA%D0%BD%D0%B8/)\n- **Serbian**: [Leipzig Corpora Collection - 2016 Serbian Wikipedia 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Serbian)\n- **Spanish**: [Leipzig Corpora Collection - 2016 Spanish News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Spanish)\n- **Swedish**: [Leipzig Corpora Collection - 2019 Swedish News 100k Sentences](https://wortschatz.uni-leipzig.de/en/download/Swedish)\n\n## License\n\n[MIT](https://github.com/dtrifuno/ipsum/ipsum/blob/main/LICENSE.md)\n',
    'author': 'Darko Trifunovski',
    'author_email': 'darko@trifunovski.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
