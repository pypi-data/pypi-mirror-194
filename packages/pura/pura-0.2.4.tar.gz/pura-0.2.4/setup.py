# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pura', 'pura.services']

package_data = \
{'': ['*'], 'pura': ['data/*']}

install_requires = \
['Pint>=0.19.2,<0.20.0',
 'aiohttp>=3.8.1,<4.0.0',
 'databases[aiosqlite]>=0.7.0,<0.8.0',
 'lxml>=4.9.0,<5.0.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rdkit-pypi>=2022.3.3,<2023.0.0',
 'stqdm>=0.0.4,<0.0.5',
 'streamlit>=1.16.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

extras_require = \
{'stout': ['unicodedata2>=14.0.0,<15.0.0',
           'pystow>=0.4.5,<0.5.0',
           'tensorflow-gpu==2.7.2']}

setup_kwargs = {
    'name': 'pura',
    'version': '0.2.4',
    'description': 'Clean chemical data quickly',
    'long_description': 'None',
    'author': 'Kobi Felton',
    'author_email': 'kobi.c.f@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.11.*',
}


setup(**setup_kwargs)
