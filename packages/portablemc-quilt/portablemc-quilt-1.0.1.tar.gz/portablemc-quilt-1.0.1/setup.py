# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portablemc_quilt']

package_data = \
{'': ['*']}

install_requires = \
['portablemc>=3,<4']

setup_kwargs = {
    'name': 'portablemc-quilt',
    'version': '1.0.1',
    'description': "Start Minecraft using the Quilt mod loader using '<exec> start quilt:[<mc-version>[:<loader-version>]]'.",
    'long_description': '# Quilt add-on\nThe quilt add-on allows you to install and run Minecraft with quilt mod loader in a single command \nline!\n\n![PyPI - Version](https://img.shields.io/pypi/v/portablemc-quilt?label=PyPI%20version&style=flat-square) &nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/portablemc-quilt?label=PyPI%20downloads&style=flat-square)\n\n```console\npip install --user portablemc-quilt\n```\n\n## Usage\nThis add-on extends the syntax accepted by the [start](/README.md#start-the-game) sub-command, by \nprepending the version with `quilt:`. Almost all releases since 1.14 are supported by quilt,\nyou can find more information on [quilt website](https://github.com/QuiltMC/quilt-template-mod), note the snapshots\nare currently not supported by this addon, but this could be the case in the future because quilt\nprovides support for them. You can also use version aliases like `release` or equivalent empty version \n(just `quilt:`). This addon also provides a way of specifying the loader version, you just have to \nadd `:<loader_version>` after the game version (the game version is still allowed to be aliases \nor empty, the following syntax is valid: `quilt::<loader_version>`).\n\nThis addon requires external HTTP accesses if:\n- the game version is an alias.\n- if the loader version is unspecified.\n- if the specified version is not installed.\n\n## Examples\n```sh\nportablemc start quilt:                # Start latest quilt loader version for latest release\nportablemc start quilt:release         # Same as above\nportablemc start quilt:1.19            # Start latest quilt loader version for 1.19\nportablemc start quilt:1.19:0.14.8     # Start quilt loader 0.14.8 for game version 1.19\nportablemc start quilt::0.14.8         # Start quilt loader 0.14.8 for the latest release\nportablemc start --dry quilt:          # Install (and exit) the latest quilt loader version for latest release\n```\n\n<!-- ![fabric animation](/doc/assets/fabricmc.gif) -->\n\n## Credits\n- [Quilt Website](https://quiltmc.org)\n',
    'author': 'MisileLaboratory',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
