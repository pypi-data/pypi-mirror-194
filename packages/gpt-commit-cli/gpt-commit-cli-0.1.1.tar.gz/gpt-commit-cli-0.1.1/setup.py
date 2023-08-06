# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpt_commit']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.26.5,<0.27.0']

entry_points = \
{'console_scripts': ['gpt-commit = gpt_commit.cli:main']}

setup_kwargs = {
    'name': 'gpt-commit-cli',
    'version': '0.1.1',
    'description': 'Generate commit messages using GPT-3.',
    'long_description': "# gpt-commit\n\nGenerate commit messages using GPT-3. To use `gpt-commit`, simply invoke it whenever you'd use `git commit`. Git will prompt you to edit the generated commit message.\n\n```bash\ngit add .\ngpt-commit\n```\n\nBased on Markus' [gpt-commit](https://github.com/markuswt/gpt-commit).\n\n- [gpt-commit](#gpt-commit)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Getting Started](#getting-started)\n  - [Develop](#develop)\n\n\n## Installation\n\nMinimum Python version required: 3.10.\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install gpt-commit-cli\n```\n\n### [pip](https://pypi.org/project/gpt-commit-cli/)\n\n```\n$ pip install gpt-commit-cli\n```\n\n\n## Getting Started\n\nSet the environment variable `OPENAI_API_KEY` to your [OpenAI API key](https://platform.openai.com/account/api-keys), e.g. by adding the following line to your `.bashrc`.\n\n```bash\nexport OPENAI_API_KEY=<YOUR API KEY>\nexport OPENAI_ORG_ID=<YOUR ORG ID> # optional\n```\n\n<!-- ### Modify `git commit` (optional)\n\nIf you want `git commit` to automatically invoke `gpt-commit`, copy `gpt-commit.py` and `prepare-commit-msg` to the `.git/hooks` directory in any project where you want to modify `git commit`.\n -->\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/gpt-commit-cli.git\n$ cd gpt-commit-cli\n$ poetry install\n```",
    'author': 'Teddy Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/gpt-commit-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
