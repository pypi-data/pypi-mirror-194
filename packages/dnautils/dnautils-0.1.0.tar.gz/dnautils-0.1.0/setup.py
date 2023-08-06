# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dna_utils']

package_data = \
{'': ['*']}

install_requires = \
['pyfaidx>=0.7.2.1,<0.8.0.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'dnautils',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Genomic References\nOncoDNA library to handle genomic reference directory\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Git repository\norigin git@gitlab.oncoworkers.oncodna.com:bioinfo/libraries/dna_utils.git\n\n## Installation\n\n```sh\npip install \n--index-url http://devpi.oncoworkers.oncodna.com/root/pypi/+simple\n--extra-index-url http://devpi.oncoworkers.oncodna.com/root/public/+simple\n--trusted-host devpi.oncoworkers.oncodna.com\n\ndna_utils\n```\n\n## Usage\n\n```python\nfrom dna_utils import DNAUtils\n\nprint(DNAUtils.complement("AAG"))\n```\n\n\n## 🛠️ DEV 🛠️\n\n### Environment Setup\n1. First install [poetry](https://python-poetry.org/docs/)\n2. `git clone github repo`\n3. `cd DNAUtils`\n4. `poetry init`\n5. `poetry install --with dev`\n6. `poetry run pre-commit install`\n\n### Before pushing\n* Each new implementation should be unitested. (`poetry run pytest`)\n* Run precommit (`poetry run pre-commit run --all-files`)',
    'author': 'Benoitdw',
    'author_email': 'bw@oncodna.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
