# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yak_server',
 'yak_server.cli',
 'yak_server.database',
 'yak_server.database.migrations',
 'yak_server.database.migrations.versions',
 'yak_server.helpers',
 'yak_server.v1',
 'yak_server.v1.utils',
 'yak_server.v2',
 'yak_server.v2.utils']

package_data = \
{'': ['*'], 'yak_server': ['data/world_cup_2022/*']}

install_requires = \
['Flask-SQLAlchemy>=3.0.3,<4.0.0',
 'PyJWT>=2.6.0,<3.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'flask-cors>=3.0.10,<4.0.0',
 'flask-migrate>=4.0.4,<5.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'strawberry-graphql>=0.155.3,<0.156.0']

entry_points = \
{'console_scripts': ['yak = yak_server.cli:main']}

setup_kwargs = {
    'name': 'yak-server',
    'version': '0.4.0',
    'description': 'Football bet rest/graphql server',
    'long_description': "# Yak-toto\n\n## Requisites\n\n- Ubuntu 22.04\n- Python 3.10.4\n- MySQL 8.0.30\n\n## How to build the project\n\n### Database\n\nInstall and start mysql server on port 3306. Add a database named `yak_toto`. In root folder, create a dotenv file named `.flaskenv` and fill your MySQL user name, password and database. When backend start, this configuration is automaticaly loaded.\n\n```text\nMYSQL_USER_NAME=my_user_name\nMYSQL_PASSWORD=my_password\nMYSQL_DB=my_database_name\n```\n\nYou can also set MySQL port by adding `MYSQL_PORT=my_port` to `.flaskenv` file. If not set, it will be 3306 by default.\n\n### Backend\n\nRun your project in a Python env is highly recommend. You can use `venv` with the following command:\n\n```bash\npython3 -m venv <my_env_name>\n```\n\nThen activate it with:\n\n```bash\nsource <my_env_name>/bin/activate\n```\n\nFetch all packages using poetry with the following command:\n\n```bash\npoetry install\n```\n\nBefore starting the backend, add `JWT_SECRET_KEY` in `.flaskenv` same as the MySQL user name and password. As\nlogin system is using JSON Web Token, a secret key is required. To generate one, you can use the python built-in `secrets` module.\n\n```py\n>>> import secrets\n>>> secrets.token_hex(16)\n'9292f79e10ed7ed03ffad66d196217c4'\n```\n\n```text\nJWT_SECRET_KEY=9292f79e10ed7ed03ffad66d196217c4\n```\n\nAlso, automatic backup can be done through `yak_server/cli/backup_database` script. It can be run using `flask db backup`.\n\nFinally, flask needs some configuration to start. Please add `FLASK_APP=yak_server` variable to indicate main location. Last thing, for development environment, debug needs to be activated with a addditional environment variable:\n\n```text\nFLASK_DEBUG=1\n```\n\nAnd then start backend with:\n\n```bash\nflask run\n```\n\n### Data initialization\n\nTo run local testing, you can use the script `create_database.py`, `initialize_database.py` and `create_admin.py` located in `yak_server/cli` folder. To select, set `COMPETITION` environment variable in `.flaskenv`. It will read data from `yak_server/data/{COMPETITION}/`.\n\n### Testing\n\nTo set up test, please add a MySQL database named `yak_toto_test`. It will contain all the records created during unit tests. This database is cleaned everytime you run test. That's why a different database is created to avoid deleting records you use for your local testing.\n\nYak-server is using `pytest` to run tests and can run them using `poetry run pytest` command into root folder.\n\nTo generate xml report, run `pytest --cov-report=xml --cov=yak_server tests/ -vv`.\n",
    'author': 'Guillaume Le Pape',
    'author_email': 'gui.lepape25@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yak-toto/yak-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
