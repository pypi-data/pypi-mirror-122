# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanchorknit', 'pyanchorknit.cli']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.3,<5.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pyanchorknit = pyanchorknit.cli.main:app()']}

setup_kwargs = {
    'name': 'pyanchorknit',
    'version': '0.1.0',
    'description': 'Weaving algorithm.',
    'long_description': '# PyAnchorKnit\n\n# Dev install\n## Poetry\n### Install pipx\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\npipx completions\n```\n\n### Install poetry\n```bash\npipx install poetry\n```\n\n### Install the project\n```bash\npoetry install\n```\n\n## Install [pre-commit](https://pre-commit.com) hooks\n```bash\npoetry run pre-commit install\npoetry run pre-commit install -t pre-push\n```\n',
    'author': 'CrossNox',
    'author_email': 'ijmermet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
