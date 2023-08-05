# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sportradar_api', 'sportradar_api.soccer_extended']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.28.2']

setup_kwargs = {
    'name': 'sportradar-api',
    'version': '0.1.5',
    'description': 'Lightweight wrapper for Sportradar API',
    'long_description': "# Sportradar API\nLightweight wrapper for [Sportradar API](https://developer.sportradar.com/docs/read/Home)\n\n## Set up\n1. Register on [Sportradar Developer](https://developer.sportradar.com/member/register)\n2. Generate an API Key\n\n## Installation\n````bash\npip install sportradar-api\n````\n\n## Usage\n\n````python\nfrom sportradar_api import SoccerExtended\n\nsportradar = SoccerExtended(api_key='SPORTRADAR_API_KEY')\n````",
    'author': 'Felipe Allegretti',
    'author_email': 'felipe@allegretti.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipeall/sportradar-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
