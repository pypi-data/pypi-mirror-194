# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elm_framework_helpers',
 'elm_framework_helpers.ccxt',
 'elm_framework_helpers.ccxt.models',
 'elm_framework_helpers.ccxt.orderbook',
 'elm_framework_helpers.http',
 'elm_framework_helpers.json',
 'elm_framework_helpers.operators',
 'elm_framework_helpers.output',
 'elm_framework_helpers.schedulers',
 'elm_framework_helpers.strategies.grid',
 'elm_framework_helpers.websockets.models']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.92.0,<0.93.0',
 'orjson>=3.8.6,<4.0.0',
 'reactivex>=4.0.4,<5.0.0',
 'uvicorn>=0.20.0,<0.21.0',
 'websocket-client>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'elm-framework-helpers',
    'version': '0.2.3',
    'description': '',
    'long_description': '# Helpers for the ELM framework scripts\n\n## Logging\n\nPrefer dict based config.\n\n## HTTP\n\nThe `http` module contains a Uvicorn server which can be run outside of the main thread.\n\n## Json\n\nThe `json` module contains an implementation of `dumps` which handles Decimal (turns into string)\n\n## Output\n\n### never_ending_observer\n\nReturns an `OnNext` only observer which logs an error to `logger` if it ever completes or errors.',
    'author': 'Mat',
    'author_email': 'mathieu@redapesolutions.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TechSpaceAsia/elm-framework-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
