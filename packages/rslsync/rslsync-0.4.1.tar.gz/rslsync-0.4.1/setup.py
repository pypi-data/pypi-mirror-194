# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rslsync', 'rslsync.commands']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rsl = rslsync.cli:main']}

setup_kwargs = {
    'name': 'rslsync',
    'version': '0.4.1',
    'description': 'A Python client library and CLI of unofficial Resilio Sync API',
    'long_description': 'A Python client library and CLI of unofficial Resilio Sync (BTSync) API. No API Key is needed.\n\n## Installation\n\nInstall from pypi\n\n```\npip install rslsync\n```\n\nInstall from repo\n```\npip install .\n```\n\n## Usage\n\nAs a command line tool\n```\n$ rsl --help\n$ rsl general get-settings\n$ rsl folder list\n\n```\n\nAs a library\n```\n$ from rslsync import RslClient\n$ c = RslClient("http://localhost:8888/", "user", "pass")\n\n# general commands\n$ c.general.get_settings()     # get all settings\n\n# folder commands\n$ c.folder.list()  # list all shared folders\n\n# file commands\n$ c.file.list()  # list all shared files\n$ share_id = c.file.share(path, days)   # share a single file\n$ c.file.get_link(share_id)   # create a share link\n$ c.file.unshare(share_id)   # unshare a file\n\n# stat commands\n$ c.stat.get_peers_stat()  # get the stats of peers\n\n# fs (file system) commands\n# c.fs.get_attr("/")\n```\n\n## Related Projects\n\n * https://github.com/kevinjqiu/btsync.py\n * https://github.com/dlawregiets/btsync_status\n * https://github.com/ywrac/btsync-api-python\n * https://github.com/jminardi/python-btsync\n * https://github.com/icy/btsync\n * https://github.com/PythonNut/resilio-sync-cli\n * https://github.com/lxiange/ResilioSync-py\n ',
    'author': 'Zhongke Chen',
    'author_email': 'github@ch3n2k.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zhongkechen/python-resilio-sync-unofficial',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
