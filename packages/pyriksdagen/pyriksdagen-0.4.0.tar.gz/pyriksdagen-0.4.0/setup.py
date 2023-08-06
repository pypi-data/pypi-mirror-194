# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pyriksdagen']

package_data = \
{'': ['*'], 'pyriksdagen': ['data/queries/*', 'data/queries_backup/*']}

install_requires = \
['SPARQLWrapper',
 'base58',
 'beautifulsoup4',
 'dateparser',
 'kblab-client',
 'lxml',
 'matplotlib',
 'numpy',
 'pandas',
 'progressbar2',
 'pyparlaclarin',
 'requests',
 'tqdm',
 'unidecode']

setup_kwargs = {
    'name': 'pyriksdagen',
    'version': '0.4.0',
    'description': 'Access the Riksdagen corpus',
    'long_description': '[![Check unchanged](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/check_unchanged.yml/badge.svg)](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/check_unchanged.yml)\n[![Unit tests](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/push.yml/badge.svg)](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/push.yml)\n[![Validate Parla-Clarin XML](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/validate.yml/badge.svg)](https://github.com/welfare-state-analytics/riksdagen-corpus/actions/workflows/validate.yml)\n\n# Swedish parliamentary proceedings - Riksdagens protokoll 1920-2021\n\n_Westac Project, 2020-2021_\n\nThe full data set consists of multiple parts:\n\n- Riksdagens protokoll between from 1920 until today in the [Parla-clarin](https://github.com/clarin-eric/parla-clarin) format\n- Comprehensive list of MPs and cabinet members during this period\n- [Documentation](https://github.com/welfare-state-analytics/riksdagen-corpus/wiki/) of the corpus and the curation process\n- [A Google Colab notebook](https://colab.research.google.com/drive/1C3e2gwi9z83ikXbYXNPfB6RF7spTgzxA?usp=sharing) that demonstrates how the dataset can be used with Python\n\n## Basic use\n\nA full dataset is available under [this download link](https://github.com/welfare-state-analytics/riksdagen-corpus/releases/download/v0.4.3/corpus-0.4.3.zip). It has the following structure\n\n- Annual protocol files in the ```corpus/protocols/``` folder\n- Structured metadata on MPs, speakers, ministers, and governments in the ```corpus/metadata/``` folder\n\nThe workflow to use the data is demonstrated in [this Google Colab notebook](https://colab.research.google.com/drive/1C3e2gwi9z83ikXbYXNPfB6RF7spTgzxA?usp=sharing).\n\n## Design choices of the project\n\nThe Riksdagen corpus is released as an iterative process, where the corpus is curated and expanded. Semantic versioning is used for the whole corpus, following the established major-minor-patch practices as they apply to data. For each major and minor release, a statistical sample is drawn, annotated and quantitatively evaluated. Errors are fixed as they are detected in order of priority. Moreover, the edit history is kept as a traceable git repository.\n\n![Estimate of mapping accuracy](https://raw.githubusercontent.com/welfare-state-analytics/riksdagen-corpus/main/input/accuracy/version_plot.png)\n\nWhile the contents of the corpus will change due to curation and expansion, we aim to keep the deliverable API, the corpus/ folder, as stable as possible. This means we avoid relocating files or folders, changing formats, changing columns in metadata files, or any other changes that might break downstream scripts. Conversely, files outside the corpus/ folder are internal to the project. End users may find utility in them but we make no effort to keep them consistent.\n\nThe data in the corpus is delivered as TEI XML files to follow established practices. The metadata is delivered as CSV files, following a normal form database structure while allowing for a legible git history. A more detailed description of the data and metadata structure and formats can be found in the README files in the corpus/ folder.\n\n## Participate in the curation process\n\nIf you find any errors, it is possible to submit corrections to them. This is documented in the [project wiki](https://github.com/welfare-state-analytics/riksdagen-corpus/wiki/Submit-corrections).\n',
    'author': 'ninpnin',
    'author_email': 'vainoyrjanainen@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/welfare-state-analytics/riksdagen-corpus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
