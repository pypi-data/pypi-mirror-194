# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lunni_cli', 'lunni_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['lun = lunni_cli.app:app', 'lunni = lunni_cli.app:app']}

setup_kwargs = {
    'name': 'lunni-cli',
    'version': '0.1.0',
    'description': "Lunni's CLI companion",
    'long_description': "# Lunni CLI\n\nLunni's command line interface lets you set up projects ready for continuous\ndeployment with Lunni, straight from the command line.\n\n## Installation\n\nTo install Lunni CLI, make sure you have Python version 3.11 or later. You'll\nalso want to [have pipx](https://github.com/pypa/pipx#install-pipx), a package\nmanager for installing Python CLI tools.\n\n```\npipx install lunni-cli\nlunni --install-completion [bash|zsh|fish|powershell]\n```\n\nThis installs Lunni CLI globally, so you can run `lunni` commands from any\ndirectory. You can check the version and find out some basic information about\nthe tool with the following command:\n\n```\nlunni version\n```\n\n\n## CLI commands\n\nTo get a list of commands, run `lunni --help`. To get a list of command\narguments & flags run `lunni COMMAND --help`.\n\n\n## lunni create\n\nSet up projects ready for deployment on Lunni (or Docker Swarm).\n\nWe provide some templates you can use:\n\n- [Modern Python setup]() with Poetry, FastAPI or Flask, CI/CD, code quality\n  and testing\n\n- more coming soon!\n\n\n## lunni dev & run\n\nRun an app locally. This just wraps `docker-compose up` and `docker-compose\nrun` respectively, but it allows you to save some keystrokes.\n",
    'author': 'Alexander Pushkov',
    'author_email': 'ale@aedge.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lunni.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
