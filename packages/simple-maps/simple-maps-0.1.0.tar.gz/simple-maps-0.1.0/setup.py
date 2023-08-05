# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_maps']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['simple_maps = simple_maps.cli:app']}

setup_kwargs = {
    'name': 'simple-maps',
    'version': '0.1.0',
    'description': 'Tool to create maps with markers using cartes.io API',
    'long_description': "# Simple Maps\n\n[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)\n[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)\n\nThis program allows the creation of maps with markers directly from the command\nline.\n\n\n## Installation\n\n```console\n$ pip install simple-maps\n```\n\n## Features\n\nSimple Maps interacts with the cartes.io API to provide the following\nfunctionality:\n\n- Create a map with parameters: `map create`\n- Get information about a map: `map get`\n- Delete a map: `map delete`\n- Create a marker on a map: `marker create`\n- List all markers on a map: `marker list`\n- Edit marker description: `marker edit`\n- Delete a marker: `marker delete`\n\n\n**Usage**:\n\n```console\n$ simple_maps [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `map`\n* `marker`\n\n## `simple_maps map`\n\n**Usage**:\n\n```console\n$ simple_maps map [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a map.\n* `delete`: Delete a single map.\n* `get`: Get a single map.\n\n### `simple_maps map create`\n\nCreate a map.\n\n**Usage**:\n\n```console\n$ simple_maps map create [OPTIONS]\n```\n\n**Options**:\n\n* `--title TEXT`: The title of the map\n* `--slug TEXT`: The map slug. Currently un-used\n* `--description TEXT`: The description of the map and its purpose\n* `--privacy [public|unlisted|private]`: The privacy level of the map: public, unlisted, private\n* `--users-can-create-markers [yes|no|only_logged_in]`: The setting that defines who can create markers\n* `--help`: Show this message and exit.\n\n### `simple_maps map delete`\n\nDelete a single map.\n\n**Usage**:\n\n```console\n$ simple_maps map delete [OPTIONS]\n```\n\n**Options**:\n\n* `--token TEXT`: Token  [required]\n* `--map-id TEXT`: Map id  [required]\n* `--help`: Show this message and exit.\n\n### `simple_maps map get`\n\nGet a single map.\n\n**Usage**:\n\n```console\n$ simple_maps map get [OPTIONS]\n```\n\n**Options**:\n\n* `--map-id TEXT`: Id of the map  [required]\n* `--help`: Show this message and exit.\n\n## `simple_maps marker`\n\n**Usage**:\n\n```console\n$ simple_maps marker [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a marker on a map.\n* `delete`: Delete a marker on a map.\n* `edit`: Edit a marker on a map.\n* `list`: Get all markers on a map.\n\n### `simple_maps marker create`\n\nCreate a marker on a map.\n\n**Usage**:\n\n```console\n$ simple_maps marker create [OPTIONS]\n```\n\n**Options**:\n\n* `--map-token TEXT`: Map token  [required]\n* `--map-id TEXT`: Map id  [required]\n* `--lat FLOAT RANGE`: The lat position of the marker  [required]\n* `--lng FLOAT RANGE`: The lng position of the marker  [required]\n* `--category INTEGER`: Category ID. Use category_name if you don't know the ID\n* `--category-name TEXT`: Category name\n* `--description TEXT`: Marker description\n* `--help`: Show this message and exit.\n\n### `simple_maps marker delete`\n\nDelete a marker on a map.\n\n**Usage**:\n\n```console\n$ simple_maps marker delete [OPTIONS]\n```\n\n**Options**:\n\n* `--token TEXT`: Token  [required]\n* `--map-id TEXT`: Map id  [required]\n* `--marker-id TEXT`: Marker id  [required]\n* `--help`: Show this message and exit.\n\n### `simple_maps marker edit`\n\nEdit a marker on a map.\n\n**Usage**:\n\n```console\n$ simple_maps marker edit [OPTIONS]\n```\n\n**Options**:\n\n* `--token TEXT`: Marker token  [required]\n* `--map-id TEXT`: Map id  [required]\n* `--marker-id TEXT`: Marker id  [required]\n* `--description TEXT`: Marker description\n* `--help`: Show this message and exit.\n\n### `simple_maps marker list`\n\nGet all markers on a map.\n\n**Usage**:\n\n```console\n$ simple_maps marker list [OPTIONS]\n```\n\n**Options**:\n\n* `--map-id TEXT`: Map id  [required]\n* `--show-expired / --no-show-expired`: Show markers that have already expired\n* `--help`: Show this message and exit.\n",
    'author': 'Julio Batista Silva',
    'author_email': 'julio@juliobs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jbsilva/simple-maps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
