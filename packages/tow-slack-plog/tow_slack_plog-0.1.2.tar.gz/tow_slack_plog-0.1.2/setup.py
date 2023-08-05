# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tow_slack_plog']

package_data = \
{'': ['*']}

install_requires = \
['slack-sdk>=3.20.0,<4.0.0']

setup_kwargs = {
    'name': 'tow-slack-plog',
    'version': '0.1.2',
    'description': '',
    'long_description': "# tow-slack-plog\n\n.. image:: https://img.shields.io/pypi/pyversions/tow-slack-plog.svg?maxAge=2592000?style=flat-square\n:target: https://pypi.python.org/pypi/tow-slack-plog\n\nPython logging handler for Slack webhook integration with simple configuration.\n\n## Installation\n\n.. code-block:: bash\n\n    pip install tow-slack-plog\n\n## Example\n\nSimple\n''''''\n.. code-block:: python\n\nimport logging\nfrom slack_plog import SlackPlog\n\nsh = SlackPlog('YOUR_WEB_HOOK_URL') # url is like 'https://hooks.slack.com/...'\nlogging.basicConfig(handlers=[sh])\nlogging.warning('warn message')\n\nUsing logger\n''''''''''''\n.. code-block:: python\n\nimport logging\nfrom slack_plog import SlackPlog\n\nlogger = logging.getLogger(**name**)\nlogger.setLevel(logging.DEBUG)\n\nsh = SlackPlog(slack_webhook_url='YOUR_WEB_HOOK_URL')\nsh.setLevel(logging.DEBUG)\n\nlogger.addHandler(sh)\n\nlogger.debug('debug message')\nlogger.info('info message')\nlogger.warn('warn message')\nlogger.error('error message')\nlogger.critical('critical message')\n",
    'author': 'Fhuad Balogun',
    'author_email': 'fhuadbalogun@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
