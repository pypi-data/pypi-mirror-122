# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanchorknit', 'pyanchorknit.cli']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.3,<5.0.0',
 'pycairo>=1.20.1,<2.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pyanchorknit = pyanchorknit.cli.main:app()']}

setup_kwargs = {
    'name': 'pyanchorknit',
    'version': '0.3.0',
    'description': 'Weaving algorithm.',
    'long_description': '# PyAnchorKnit\nInspired by the work of [Petros Vrellis](https://www.instagram.com/pvrellis/). Based on [Weaver](https://github.com/alyyousuf7/Weaver).\n\n## Installation\n### Prerequisites\n`pyanchorknit` uses `pycairo`, which requires `pkg-config` and `cairo`. Check [here](https://pycairo.readthedocs.io/en/latest/getting_started.html) for installation commands for your platform.\n\n### Install `pyanchorknit`\nUsage of [pipx](https://pypa.github.io/pipx/) is encouraged.\n\n```bash\npipx install pyanchorknit\n```\n\n## Example usage\n```bash\npyanchorknit imgs/Johannes-Vermeer-Girl-With-a-Pearl-Earring.jpg --n-jobs 16 --n-edges 512 --maxlines 2000 --img-out imgs/\n```\n\n### Output image\n<img src="imgs/Johannes-Vermeer-Girl-With-a-Pearl-Earring-weave.png" alt="drawing" width="400"/>\n\n### Output JSON\n```json\n{\n  "points": {\n    "0": [\n      799,\n      400\n    ],\n    "1": [\n      682,\n      682\n    ],\n    ...,\n    "7": [\n      682,\n      117\n    ]\n  },\n  "traces": [\n    [\n      [\n        0,\n        4\n      ],\n      145236\n    ],\n    [\n      [\n        4,\n        1\n      ],\n      113064\n    ],\n    ...,\n    [\n      [\n        2,\n        6\n      ],\n      130755\n    ]\n  ]\n}\n```\n\nWhich indicates the position of anchor points and traces (along with their distance).\n\n# Dev install\n## Poetry\n### Install poetry\n```bash\npipx install poetry\n```\n\n### Install the project\n```bash\npoetry install\n```\n\n## Install [pre-commit](https://pre-commit.com) hooks\n```bash\npoetry run pre-commit install\npoetry run pre-commit install -t pre-push\n```\n\n## Publish\n```bash\npoetry publish --build\n```\n',
    'author': 'CrossNox',
    'author_email': 'ijmermet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CrossNox/pyanchorknit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
