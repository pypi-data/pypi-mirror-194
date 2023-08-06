# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h3daemon']

package_data = \
{'': ['*']}

install_requires = \
['hmmer>=0.2.1',
 'pidlockfile>=0.3',
 'psutil>=5.9.4',
 'python-daemon>=2.3.2',
 'typer[all]>=0.7.0']

entry_points = \
{'console_scripts': ['h3daemon = h3daemon.cli:app']}

setup_kwargs = {
    'name': 'h3daemon',
    'version': '0.9.3',
    'description': 'HMMER server',
    'long_description': '# Welcome to h3daemon 👋\n\n> Command-line for running HMMER server on arm64 and amd64 machines.\n\n### 🏠 [Homepage](https://github.com/EBI-Metagenomics/h3daemon)\n\n## ⚡️ Requirements\n\n- Python >= 3.9\n- Pip\n- [Homebrew](https://brew.sh) on MacOS (recommended)\n- [Pipx](https://pypa.github.io/pipx/) for Python package management (recommended)\n\n### MacOS\n\nInstall Python and Pipx:\n\n```sh\nbrew update && brew install python pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n### Ubuntu (and Debian-based distros)\n\nInstall Python and Pipx:\n\n```sh\nsudo apt update && \\\n    sudo apt install python3 python3-pip python3-venv --yes && \\\n    python3 -m pip install --user pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npython3 -m pipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n## 📦 Install\n\n```sh\npipx install h3daemon\n```\n\n## Usage\n\n```\n Usage: h3daemon [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ─────────────────────────────────────────────────────╮\n│ --version                                                     │\n│ --help             Show this message and exit.                │\n╰───────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────╮\n│ start                 Start daemon.                           │\n│ stop                  Stop daemon.                            │\n╰───────────────────────────────────────────────────────────────╯\n```\n\n### Example\n\nDownload `minifam.hmm` database:\n\n```sh\npipx run blx get \\\n  fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960 \\\n  minifam.hmm\n```\n\nPress it:\n\n```sh\npipx run --spec hmmer hmmpress minifam.hmm\n```\n\nStart the daemon to listen on a random (available) port:\n\n```sh\nh3daemon start minifam.hmm\n```\n\nAnd stop it:\n\n```sh\nh3daemon stop minifam.hmm\n```\n\n## 👤 Author\n\n- [Danilo Horta](https://github.com/horta)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
