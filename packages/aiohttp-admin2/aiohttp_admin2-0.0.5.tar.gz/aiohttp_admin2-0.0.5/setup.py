# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_admin2',
 'aiohttp_admin2.controllers',
 'aiohttp_admin2.mappers',
 'aiohttp_admin2.mappers.fields',
 'aiohttp_admin2.mappers.validators',
 'aiohttp_admin2.resources',
 'aiohttp_admin2.resources.dict_resource',
 'aiohttp_admin2.resources.mongo_resource',
 'aiohttp_admin2.resources.mysql_resource',
 'aiohttp_admin2.resources.postgres_resource',
 'aiohttp_admin2.views',
 'aiohttp_admin2.views.aiohttp',
 'aiohttp_admin2.views.aiohttp.views']

package_data = \
{'': ['*'],
 'aiohttp_admin2.views.aiohttp': ['static/css/*',
                                  'static/js/*',
                                  'templates/aiohttp_admin/blocks/*',
                                  'templates/aiohttp_admin/blocks/filters/*',
                                  'templates/aiohttp_admin/blocks/form/*',
                                  'templates/aiohttp_admin/blocks/form/fields/*',
                                  'templates/aiohttp_admin/layouts/*']}

install_requires = \
['SQLAlchemy>=1.4.20,<2.0.0',
 'aiohttp-jinja2>=1.4.2,<2.0.0',
 'aiohttp>=3.6.3,<4.0.0',
 'aiomysql>=0.0.21,<0.0.22',
 'aiopg>=1.3.0,<2.0.0',
 'motor>=2.4.0,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'sqlalchemy-stubs>=0.4,<0.5',
 'umongo>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-admin2',
    'version': '0.0.5',
    'description': 'Generator an admin interface based on aiohttp.',
    'long_description': '.. image:: https://img.shields.io/pypi/v/aiohttp_admin2.svg\n        :target: https://pypi.python.org/pypi/aiohttp_admin2\n\n.. image:: https://github.com/Arfey/aiohttp_admin2/actions/workflows/tests.yaml/badge.svg?branch=master\n        :target: https://github.com/Arfey/aiohttp_admin2/actions/workflows/tests.yaml\n\n.. image:: https://readthedocs.org/projects/aiohttp-admin2/badge/?version=latest\n        :target: https://aiohttp-admin2.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/arfey/aiohttp_admin2/shield.svg\n     :target: https://pyup.io/repos/github/arfey/aiohttp_admin2/\n     :alt: Updates\n\n.. image:: https://img.shields.io/badge/PRs-welcome-green.svg\n     :target: https://github.com/Arfey/aiohttp_admin2/issues\n     :alt: PRs Welcome\n\n=============\nAiohttp admin\n=============\n\n`Demo site\n<https://shrouded-stream-28595.herokuapp.com/>`_ | `Demo source code\n<https://github.com/Arfey/aiohttp_admin2/tree/master/demo/main>`_.\n\nThe aiohttp admin is a library for build admin interface for applications based\non the aiohttp. With this library you can ease to generate CRUD views for your\ndata (for data storages which support by aiohttp admin) and flexibly customize\nrepresentation and access to these.\n\n* Free software: MIT license\n* Documentation: https://aiohttp-admin2.readthedocs.io.\n\nInstallation\n------------\n\nThe first step which you need to do it’s installing library\n\n.. code-block:: bash\n\n   pip install aiohttp_admin2\n\n.. image:: https://github.com/Arfey/aiohttp_admin2/blob/master/docs/images/index.png?raw=true\n\n=======\nHistory\n=======\n\n0.1.0 (2020-04-28)\n------------------\n\n* First release on PyPI.\n',
    'author': 'Mykhailo Havelia',
    'author_email': 'misha.gavela@gmail.com',
    'maintainer': 'Mykhailo Havelia',
    'maintainer_email': 'misha.gavela@gmail.com',
    'url': 'https://github.com/arfey/aiohttp_admin2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
