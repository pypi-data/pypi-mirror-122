# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_same_dir']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.0.3,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['same-dir = mkdocs_same_dir.plugin:SameDirPlugin']}

setup_kwargs = {
    'name': 'mkdocs-same-dir',
    'version': '0.1.1',
    'description': 'MkDocs plugin to allow placing mkdocs.yml in the same directory as documentation',
    'long_description': "# mkdocs-same-dir\n\n**[Plugin][] for [MkDocs][] to allow placing *mkdocs.yml* in the same directory as documentation**\n\n[![PyPI](https://img.shields.io/pypi/v/mkdocs-same-dir)](https://pypi.org/project/mkdocs-same-dir/)\n[![GitHub](https://img.shields.io/github/license/oprypin/mkdocs-same-dir)](https://github.com/oprypin/mkdocs-same-dir/blob/master/LICENSE.md)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/mkdocs-same-dir/CI)](https://github.com/oprypin/mkdocs-same-dir/actions?query=event%3Apush+branch%3Amaster)\n\n```shell\npip install mkdocs-same-dir\n```\n\n[mkdocs]: https://www.mkdocs.org/\n[plugin]: https://www.mkdocs.org/user-guide/plugins/\n\n## Usage\n\nActivate the plugin in **mkdocs.yml**, along with actually changing `docs_dir`  \n(normally, MkDocs *absolutely wouldn't* let you set it to `.`):\n\n```yaml\nsite_name: foo\ndocs_dir: .\nsite_dir: ../site\n\nplugins:\n  - search\n  - same-dir\n```\n\nand now you can move this **mkdocs.yml** into your **docs** directory, or move your docs alongside **mkdocs.yml**.\n\n[**See example layout**](https://github.com/oprypin/mkdocs-same-dir/tree/master/example)\n\n### Important notes\n\nAnother necessary effect of this plugin is that files *directly at the root* of the **docs** dir will no longer be picked up, unless they are Markdown files.\n\nAnd note that the [implementation](https://github.com/oprypin/mkdocs-same-dir/blob/master/mkdocs_same_dir/plugin.py) of this plugin is a huge hack that monkeypatches MkDocs' internals. But I pledge to keep up with MkDocs updates and keep it working as long as that's still possible.\n",
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-same-dir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
