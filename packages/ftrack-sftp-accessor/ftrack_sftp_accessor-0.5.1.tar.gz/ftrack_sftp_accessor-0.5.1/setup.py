# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftrack_sftp_accessor']

package_data = \
{'': ['*']}

install_requires = \
['ftrack-python-api>=2.3.3,<3.0.0', 'paramiko>=2.11.0,<3.0.0']

setup_kwargs = {
    'name': 'ftrack-sftp-accessor',
    'version': '0.5.1',
    'description': 'A ftrack sftp accessor',
    'long_description': '# ftrack-sftp-accessor\n\nAn ftrack sftp [accessor](https://ftrack-python-api.readthedocs.io/en/backlog-threading-story/locations/overview.html?highlight=accessor#accessors). \n\n\n**Note**\n> To see paths resolved in Studio, the [resolver listener](https://github.com/ftrackhq/ftrack-connect/blob/main/resource/hook/resolver.py) need to be running, either through [ftrack-connect](https://github.com/ftrackhq/ftrack-connect) or manually.\n\n# Installation\n\nInstall using pip:\n\n    $ pip install ftrack-sftp-accessor\n\nInstall from sources:\n\n    $ git clone https://github.com/ftrackhq/ftrack-sftp-accessor.git\n    $ pip install poetry\n    $ poetry build\n    $ pip install dist/ftrack_sftp_accessor-<VERSION>-py3-none-any.whl\n\n\n## Documentation\n\nFull documentation, including installation and setup guides can be found at https://ftrack-sftp-accessor.readthedocs.io/en/latest/\n\n## Usage\n\nThe main plugin can be found in the plugins folder. This folder may be registered using the FTRACK_EVENT_PLUGIN_PATH ftrack environment variable so that it is picked up when ftrack is started.\n\nExamples of how to use the plugin can be found in the scripts folder. The simplest way to launch ftrack with the accessor is scripts/start_ftrack_with_sftp.py. \n\n# Contributing\n\nPlease refer to the [CONTRIBUTING.md](./CONTRIBUTING.md) ',
    'author': 'Ian Wootten',
    'author_email': 'hi@niftydigits.com',
    'maintainer': 'ftrack support',
    'maintainer_email': 'support@ftrack.com',
    'url': 'https://github.com/ftrackhq/ftrack-sftp-accessor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<3.10',
}


setup(**setup_kwargs)
