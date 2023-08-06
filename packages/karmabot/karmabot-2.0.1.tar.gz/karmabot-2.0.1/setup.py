# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['karmabot', 'karmabot.commands', 'karmabot.db']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.20,<2.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'freezegun>=1.1.0,<2.0.0',
 'humanize>=3.10.0,<4.0.0',
 'importlib-metadata>=3.7.3,<4.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'pyjokes>=0.6.0,<0.7.0',
 'python-dotenv>=0.18.0,<0.19.0',
 'requests>=2.25.1,<3.0.0',
 'slack-bolt>=1.6.1,<2.0.0',
 'slack-sdk>=3.7.0,<4.0.0']

entry_points = \
{'console_scripts': ['karmabot = karmabot.main:main']}

setup_kwargs = {
    'name': 'karmabot',
    'version': '2.0.1',
    'description': 'PyBites Karmabot - A Python based Slack Chatbot for Community interaction',
    'long_description': '# PyBites Karmabot - A Python based Slack Chatbot\n\n[![Tests](https://github.com/PyBites-Open-Source/karmabot/workflows/Tests/badge.svg)](https://github.com/PyBites-Open-Source/karmabot/actions?workflow=Tests) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![codecov.io](https://codecov.io/github/PyBites-Open-Source/karmabot/coverage.svg?branch=master)](https://codecov.io/github/PyBites-Open-Source/karmabot?branch=master)\n\n**A Python based Slack Chatbot for Community interaction**\n\n## Features\n\nKarmabot\'s main features is the management of Karma within the slack community server. You can give karma, reduce karma, check your current karma points and manage your karma related username.\n\n![karma example](https://www.pogross.de/uploads/karmabot.png)\n\n[Demo Youtube Video](https://www.youtube.com/watch?v=Yx9qYl6lmzM&amp;t=2s)\n\nAdditional commands / features are:\n\n- Jokes powered by [PyJokes](https://github.com/pyjokes/pyjokes)\n- Overview on top channels of the slack server\n- Random Python tip, quote or nugget from CodeChalleng.es\n- Browse and search python documentation, "pydoc help"\n\n## Installation\n\n`pip install karmabot`\n\n## Basic Usage\n\nAfter installing you can start karmabot by using the command\n\n```bash\nkarmabot\n```\n\nHowever, you need to some setup and supply some settings prior to this.\n\n### Setup\n\nFor app creation and tokens please follow the [slack-bolt guide](https://slack.dev/bolt-python/tutorial/getting-started) and enable [socket mode](https://slack.dev/bolt-python/concepts#socket-mode).\n\n#### Settings\n\nBy default we will look for a `.karmabot` file in the directory you used the `karmabot` command. The file should supply the following information.\n\n```env\n# Slack bot app\nKARMABOT_SLACK_BOT_TOKEN=\nKARMABOT_SLACK_APP_TOKEN=\n\n# Workspace\nKARMABOT_SLACK_USER=\nKARMABOT_GENERAL_CHANNEL=\nKARMABOT_ADMINS=\n\n# Backend\nKARMABOT_DATABASE_URL=\n\n# Testing\nKARMABOT_TEST_MODE=\n```\n\nKARMABOT_SLACK_BOT_TOKEN\n:   The [SLACK_BOT_TOKEN](https://slack.dev/bolt-python/tutorial/getting-started) for your bot. You will find it under **OAuth & Permission 🠊 Bot User OAuth Access Token** in your [app](https://api.slack.com/apps/). The token starts with `xoxb-`.\n\nKARMABOT_SLACK_APP_TOKEN\n: The SLACK_APP_TOKEN used for running the bot in [Socket Mode](https://slack.dev/bolt-python/concepts#socket-mode). You will find it under **Basic Information 🠊 App-Level Tokens** in your [app](https://api.slack.com/apps/).\n  The token starts with `xapp-`.\n\nKARMABOT_SLACK_USER\n: The bot\'s user id. Initially, you can fill in a placeholder. Once you\'ve run your own Karmabot for the first time, you can ask it as admin in private chat via `@Karmabot your_id`. This will return a value starting with `U`, e.g., `U0123XYZ`. Replace your placeholder with this value.\n\nKARMABOT_GENERAL_CHANNEL\n: The channel id of your main channel in slack. Initially, you can fill in a placeholder. Once you\'ve run your own Karmabot for the first time, you can ask it as admin in private chat via `@Karmabot general_channel_id`. This will return a value starting with `C`, e.g., `C0123XYZ`. Replace your placeholder with this value.\n\nKARMABOT_ADMINS\n: The [slack user ids](https://api.slack.com/methods/users.identity) of the users that should have admin command access separated by commas.\n\nKARMABOT_DATABASE_URL\n  : The database url which should be compatible with SqlAlchemy. For the provided docker file use `postgresql://user42:pw42@localhost:5432/karmabot`.\n  :heavy_exclamation_mark: To start the provided Docker-based Postgres server, be sure you have Docker Compose [installed](https://docs.docker.com/compose/install/) and run `docker-compose up -d` from the karmabot directory.\n\nKARMABOT_TEST_MODE=\n  : Determines if the code is run in test mode. User `KARMABOT_TEST_MODE=true` to enable testing mode. Everything else will default to `false`. This setting has to be provided as `true`, if you want run tests without a valid `KARMABOT_SLACK_BOT_TOKEN`. Otherwise, you will receive an exceptions with `slack_bolt.error.BoltError: token is invalid ...`.\n\nIf you do not want to use a file you have to provide environment variables with the above names. If no file is present we default to environment variables.\n\n#### Permissions\n\nGo to your [slack app](https://api.slack.com/apps/) and click on **Add features and functionality**. Then go into the following categories and set permissions.\n\n- Event Subscriptions\n  - Enable Events 🠊 Toggle the slider to on\n  - Subscribe to bot events 🠊 Add via the **Add Bot User Event** button\n    - team_join\n    - channel_create\n    - message.channels\n    - message.groups\n    - message.im\n- Permissions\n  - Scopes 🠊 Add the following permissions via the **Add an OAuth Scope** button\n    - app_mentions:read\n    - channels:history\n    - channels:join\n    - channels:read\n    - chat:write\n    - groups:history\n    - groups:read\n    - groups:write\n    - im:history\n    - im:read\n    - im:write\n    - users.profile:read\n    - users:read\n\n## Development pattern for contributors\n\nWe use [poetry](https://github.com/python-poetry/poetry) and `pyproject.toml` for managing packages, dependencies and some settings.\n\n### Setup virtual environment for development\n\nYou should follow the [instructions](https://github.com/python-poetry/poetry) to get poetry up and running for your system. We recommend to use a UNIX-based development system (Linux, Mac, WSL). After setting up poetry you can use `poetry install` within the project folder to install all dependencies.\n\nThe poetry virtual environment should be available in the the project folder as `.venv` folder as specified in `poetry.toml`. This helps with `.venv` detection in IDEs.\n\n#### Conda users\n\nIf you use the Anaconda Python distribution (strongly recommended for Windows users) and `conda create` for your virtual environments, then you will not be able to use the `.venv` environment created by poetry because it is not a conda environment. If you want to use `poetry` disable poetry\'s behavior of creating a new virtual environment with the following command: `poetry config virtualenvs.create false`. You can add `--local` if you don\'t want to change this setting globally but only for the current project. See the [poetry configuration docs](https://python-poetry.org/docs/configuration/) for more details.\n\nNow, when you run `poetry install`, poetry will install all dependencies to your conda environment. You can verify this by running `pip freeze` after `poetry install`.\n\n### Testing and linting\n\nFor testing you need to install [nox](https://nox.thea.codes/en/stable/) separately from the project venv created by poetry. For testing just use the `nox` command within the project folder. You can run all the nox sessions separately if need, e.g.,\n\n- only linting `nox -rs lint`\n- only testing `nox -rs tests`\n\nIf `nox` cannot be found, use `python -m nox` instead.\n\nFor different sessions see the `nox.py` file. You can run `nox --list` to see a list of all available sessions.\n\nIf you want to run tests locally via `pytest` you have to provide a valid `.karmabot` settings file or the respective enviroment variables.\n\nPlease make sure all tests and checks pass before opening pull requests!\n\n#### Using nox under Windows and Linux (WSL)\n\nMake sure to delete the `.nox` folder when you switch from Windows to WSL and vice versa, because the environments are not compatible.\n\n### [pre-commit](https://pre-commit.com/)\n\nTo ensure consistency you can use pre-commit. `pip install pre-commit` and after cloning the karmabot repo run `pre-commit install` within the project folder.\n\nThis will enable pre-commit hooks for checking before every commit.\n',
    'author': 'PyBites',
    'author_email': 'info@pybit.es',
    'maintainer': 'Patrick-Oliver Groß',
    'maintainer_email': 'mail@pogross.de',
    'url': 'https://github.com/PyBites-Open-Source/karmabot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
