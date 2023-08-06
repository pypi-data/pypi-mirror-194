# Genomic References
OncoDNA library to handle genomic reference directory
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Git repository
origin git@gitlab.oncoworkers.oncodna.com:bioinfo/libraries/dna_utils.git

## Installation

```sh
pip install 
--index-url http://devpi.oncoworkers.oncodna.com/root/pypi/+simple
--extra-index-url http://devpi.oncoworkers.oncodna.com/root/public/+simple
--trusted-host devpi.oncoworkers.oncodna.com

dna_utils
```

## Usage

```python
from dna_utils import DNAUtils

print(DNAUtils.complement("AAG"))
```


## 🛠️ DEV 🛠️

### Environment Setup
1. First install [poetry](https://python-poetry.org/docs/)
2. `git clone github repo`
3. `cd DNAUtils`
4. `poetry init`
5. `poetry install --with dev`
6. `poetry run pre-commit install`

### Before pushing
* Each new implementation should be unitested. (`poetry run pytest`)
* Run precommit (`poetry run pre-commit run --all-files`)