# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thu_learn_downloader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'hydra-core>=1.3.1,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.1,<14.0.0']

setup_kwargs = {
    'name': 'thu-learn-downloader',
    'version': '0.1.3',
    'description': 'Download everything from Web Learning of Tsinghua University',
    'long_description': '# thu-learn-downloader\n\nDownload everything from Web Learning of Tsinghua University\n\n## Demo\n\n![Demo](https://res.cloudinary.com/liblaf/image/upload/v1677213088/2023/02/24/20230224-1677213085.gif)\n\nThe resulting file structure looks like:\n\n```\nthu-learn\n└── Quantum Mechanics(1)\n   ├── docs\n   │  └── 电子教案\n   │     ├── 01-0量子力学介绍1.pdf\n   │     └── 04-0量子力学介绍2.pdf\n   └── work\n      └── 01-第一周作业\n         ├── attach-第一周作业.pdf\n         ├── submit-第一周作业.pdf\n         └── README.md\n```\n\n## Features\n\n- pretty TUI powered by [rich](https://github.com/Textualize/rich)\n- auto set `mtime` of downloaded files according to timestamp of remote file\n- auto skip download when local file is newer\n- dump homework details into `README.md` in each homework folder\n- pretty markdown files powered by [prettier](https://prettier.io) (require `prettier` installed)\n\n## Usage\n\n1. Download pre-built binary from [releases](https://github.com/liblaf/thu-learn-downloader/releases).\n2. Prepare a `config.yaml` like [config.yaml](https://github.com/liblaf/thu-learn-downloader/blob/main/config.yaml).\n3. Run `thu-learn-downloader password="***"` and wait for the sync to finish.\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/liblaf/thu-learn-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
