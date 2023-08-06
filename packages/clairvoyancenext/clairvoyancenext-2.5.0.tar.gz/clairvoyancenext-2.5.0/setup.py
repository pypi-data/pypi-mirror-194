# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clairvoyance', 'clairvoyance.entities']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['clairvoyance = clairvoyance:cli']}

setup_kwargs = {
    'name': 'clairvoyancenext',
    'version': '2.5.0',
    'description': 'Obtain GraphQL API Schema even if the introspection is not enabled',
    'long_description': "# Clairvoyance\n\nObtain GraphQL API Schema even if the introspection is disabled.\n\n[![PyPI](https://img.shields.io/pypi/v/clairvoyance)](https://pypi.org/project/clairvoyance/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clairvoyance)](https://pypi.org/project/clairvoyance/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/clairvoyance)](https://pypi.org/project/clairvoyance/)\n[![GitHub](https://img.shields.io/github/license/nikitastupin/clairvoyance)](https://github.com/nikitastupin/clairvoyance/blob/main/LICENSE)\n\n## Introduction\n\nSome GraphQL APIs have disabled introspection. For example, [Apollo Server disables introspection automatically if the `NODE_ENV` environment variable is set to `production`](https://www.apollographql.com/docs/tutorial/schema/#explore-your-schema).\n\nClairvoyance allows us to get GraphQL API schema when introspection is disabled. It produces schema in JSON format suitable for other tools like [GraphQL Voyager](https://github.com/APIs-guru/graphql-voyager), [InQL](https://github.com/doyensec/inql) or [graphql-path-enum](https://gitlab.com/dee-see/graphql-path-enum).\n\n## Contributors\n\nThanks to the [contributers](#contributors) for their work.\n\n- [nikitastupin](https://github.com/nikitastupin)\n- [Escape](https://escape.tech) team :\n  - [iCarossio](https://github.com/iCarossio)\n  - [Swan](https://github.com/c3b5aw)\n  - [QuentinN42](https://github.com/QuentinN42)\n  - [Nohehf](https://github.com/Nohehf)\n- [i-tsaturov](https://github.com/i-tsaturov)\n- [EONRaider](https://github.com/EONRaider)\n- [noraj](https://github.com/noraj)\n- [belane](https://github.com/belane)\n\n## Getting started\n\n```bash\npip install clairvoyance\nclairvoyance https://rickandmortyapi.com/graphql -o schema.json\n# should take about 2 minute\n```\n\n## Docker Image\n\n```bash\ndocker run --rm nikitastupin/clairvoyance --help\n```\n\n## Advanced Usage\n\n### Which wordlist should I use?\n\nThere are at least two approaches:\n\n- Use general English words (e.g. [google-10000-english](https://github.com/first20hours/google-10000-english)).\n- Create target specific wordlist by extracting all valid GraphQL names from application HTTP traffic, from mobile application static files, etc. Regex for GraphQL name is [`[_A-Za-z][_0-9A-Za-z]*`](http://spec.graphql.org/June2018/#sec-Names).\n\n### Environment Variables\n\n```bash\nLOG_FMT=`%(asctime)s \\t%(levelname)s\\t| %(message)s` # A string format for logging.\nLOG_DATEFMT=`%Y-%m-%d %H:%M:%S` # A string format for logging date.\nLOG_LEVEL=`INFO` # A string level for logging.\n```\n\n## Support\n\n> Due to time constraints @nikitastupin won't be able to answer all the issues for some time but he'll do his best to review & merge PRs\n\nIn case of question or issue with clairvoyance please refer to [wiki](https://github.com/nikitastupin/clairvoyance/wiki) or [issues](https://github.com/nikitastupin/clairvoyance/issues). If this doesn't solve your problem feel free to open a [new issue](https://github.com/nikitastupin/clairvoyance/issues/new).\n\n## Contributing\n\nPull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. For more information about tests, internal project structure and so on refer to [Development](https://github.com/nikitastupin/clairvoyance/wiki/Development) wiki page.\n\n## Documentation\n\n- You may find more details on how the tool works in the second half of the [GraphQL APIs from bug hunter's perspective by Nikita Stupin](https://youtu.be/nPB8o0cSnvM) talk.\n",
    'author': 'Nikita Stupin',
    'author_email': 'nikitastupin@protonmail.com',
    'maintainer': 'Nikita Stupin',
    'maintainer_email': 'nikitastupin@protonmail.com',
    'url': 'https://github.com/nikitastupin/clairvoyance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
