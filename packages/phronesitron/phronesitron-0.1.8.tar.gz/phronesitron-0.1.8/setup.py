# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phronesitron']

package_data = \
{'': ['*']}

install_requires = \
['argparse', 'openai', 'paper2txt', 'pyperclip', 'termcolor']

entry_points = \
{'console_scripts': ['ph = phronesitron.executables:ph_main']}

setup_kwargs = {
    'name': 'phronesitron',
    'version': '0.1.8',
    'description': 'Interact with ML language models from the commandline',
    'long_description': "[![check](https://github.com/retospect/phronesitron/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/phronesitron/actions/workflows/check.yml)\n\n# Phronesitron\n\nPhronesitron is a set of tools to interact with textual AI\ntools like OpenAI's models.\n\nExample use:\n\n```\n> ph explain quantum physics in 10 words\nMysterious particles with probabilistic behavior in complex systems.\n```\n\nCurrently, openAI models are supported.\n\n# Setup\n\nSet the openAI API key (get it from here: https://platform.openai.com/account/api-keys)\n\n```\nexport OPENAIKEY=<put key here>\n```\n\n# Versioning\n\nUses semantic versioning. https://semver.org/\n\n",
    'author': 'Reto Stamm',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retospect/phronesitron',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
