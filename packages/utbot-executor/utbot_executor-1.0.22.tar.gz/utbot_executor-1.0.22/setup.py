# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utbot_executor', 'utbot_executor.deep_serialization']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=6.5.0,<7.0.0']

entry_points = \
{'console_scripts': ['utbot-executor = utbot_executor:utbot_executor']}

setup_kwargs = {
    'name': 'utbot-executor',
    'version': '1.0.22',
    'description': '',
    'long_description': "# UtBot Executor\n\nUtil for python code execution and state serialization.\n\n## Installation\n\nYou can install module from [https://pypi.org/project/utbot-executor/](PyPI):\n\n```bash\npython -m pip install utbot-executor\n```\n\n## Usage\n\n### From console with socket listener\n\nRun with your `<hostname>` and `<port>` for socket connection\n```bash\n$ python -m utbot_executor <hostname> <port>\n```\n\n### From code\n\nMain method is `executor.run_calculate_function_value`.\n\nResult format:\n\n```json\n{\n        'status': 'success',\n        'isException': bool,\n        'statements': list[int],\n        'missedStatements': list[int],\n        'stateBefore': memory json dump,\n        'stateAfter': memory json dump,\n        'argsIds': list[str],\n        'kwargs': list[str],\n        'resultId': str,\n}\n```\n\nStates format: see [deep_serialization]()\n",
    'author': 'Vyacheslav Tamarin',
    'author_email': 'vyacheslav.tamarin@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
