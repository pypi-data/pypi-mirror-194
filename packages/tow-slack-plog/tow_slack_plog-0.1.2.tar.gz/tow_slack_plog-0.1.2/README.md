# tow-slack-plog

.. image:: https://img.shields.io/pypi/pyversions/tow-slack-plog.svg?maxAge=2592000?style=flat-square
:target: https://pypi.python.org/pypi/tow-slack-plog

Python logging handler for Slack webhook integration with simple configuration.

## Installation

.. code-block:: bash

    pip install tow-slack-plog

## Example

Simple
''''''
.. code-block:: python

import logging
from slack_plog import SlackPlog

sh = SlackPlog('YOUR_WEB_HOOK_URL') # url is like 'https://hooks.slack.com/...'
logging.basicConfig(handlers=[sh])
logging.warning('warn message')

Using logger
''''''''''''
.. code-block:: python

import logging
from slack_plog import SlackPlog

logger = logging.getLogger(**name**)
logger.setLevel(logging.DEBUG)

sh = SlackPlog(slack_webhook_url='YOUR_WEB_HOOK_URL')
sh.setLevel(logging.DEBUG)

logger.addHandler(sh)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
