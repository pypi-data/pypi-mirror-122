# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'click>=8.0.1,<9.0.0',
 'more-itertools>=8.10.0,<9.0.0',
 'mtgsdk>=1.3.1,<2.0.0',
 'reportlab>=3.6.1,<4.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['mtgproxy = src.command:main']}

setup_kwargs = {
    'name': 'mtgproxy',
    'version': '0.1.0',
    'description': 'This is the scripts for automatically creating a proxy from the deck list.',
    'long_description': '# MTGPROXY\n\nThis is the scripts for automatically creating a proxy from the deck list.\n\n## Getting Started\n\n### Dependencies\n\nOS:\n\n- MacOS Big Sur(11.6)\n\nPython modules:\n\n- python ≧ 3.9\n- mtgsdk ≧ 1.3.1\n- tqdm ≧ 4.62.3\n- more-itertools ≧ 8.10.0\n- click ≧ 8.0.1\n- reportlab ≧ 3.6.1\n- Pillow ≧ 8.3.2\n\nPlease check [poetry.lock](https://github.com/reonyanarticle/mtg_proxy/blob/main/poetry.lock)for more details.\n\n#### Note\n\nI only checked it on Mac OS, so if there is a problem on Windows or Linux, I would appreciate it if you could issue a report.\n\n### Installing\n\nUsing pip:\n\n```sh\npip install mtgproxy\n```\n\nUsing poetry:\n\n```sh\ngit clone git@github.com:reonyanarticle/mtg_proxy.git\ncd mtg_proxy\npoetry install\n```\n\nPlease check [here](https://github.com/python-poetry/poetry) for how to use poetry.\n\n### Executing program\n\nTo run directly from a file:\n\n```sh\npython src/commamd.py --decklist foo.txt\n```\n\nTo run with poetry:\n\n```sh\npoetry run mtgproxy --decklist foo.txt\n```\n\n## Help\n\nPlease use `--help` to check the details of the execution command.\n\n```sh\npoetry run mtgproxy --help\n# Usage: mtgproxy [OPTIONS]\n\n#   Program for printing proxy cards from a deck list.\n\n# Options:\n#   --decklist TEXT  Deck list for which you want to create a proxy\n#                    [required]\n#   --output TEXT    File name to print the proxy card\n#   --help           Show this message and exit.\n```\n\n## Authors\n\nContributors names and contact info\n\n- Reona [@reonaarticlemtg](https://twitter.com/reonaarticleMtG)\n\n## Version History\n\n- 0.1\n  - Initial Release\n\n## License\n\nMIT Lisence.\n\n## Acknowledgments\n\nInspiration, code snippets, etc.\n\n- [Magic: The Gathering SDK](https://github.com/MagicTheGathering/mtg-sdk-python)\n',
    'author': 'reonyanarticle',
    'author_email': 'reonaarticles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reonyanarticle/mtg_proxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
