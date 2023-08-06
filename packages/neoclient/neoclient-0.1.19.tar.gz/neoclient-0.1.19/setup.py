# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neoclient']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'mediate>=0.1.7,<0.2.0',
 'pydantic>=1.10.0,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'neoclient',
    'version': '0.1.19',
    'description': 'Fast API Clients for Python',
    'long_description': '# neoclient\n🚀 Fast API Clients for Python\n\n## Installation\n```console\npip install neoclient\n```\n\n## Introduction\nThe simplest `neoclient` file might look like this:\n```python\nfrom neoclient import get\n\n@get("https://httpbin.org/ip")\ndef ip():\n    ...\n```\n```python\n>>> ip()\n{\'origin\': \'1.2.3.4\'}\n```\n\nHowever, it\'s almost always better to create a `NeoClient` instance:\n```python\nfrom neoclient import NeoClient\n\nclient = NeoClient("https://httpbin.org/")\n\n@client.get("/ip")\ndef ip():\n    ...\n```\n```python\n>>> ip()\n{\'origin\': \'1.2.3.4\'}\n```',
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tombulled/neoclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
