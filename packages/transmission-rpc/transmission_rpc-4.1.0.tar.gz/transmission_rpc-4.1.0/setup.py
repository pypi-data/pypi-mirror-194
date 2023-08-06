# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transmission_rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

extras_require = \
{'docs': ['sphinx==6.1.3', 'sphinx-rtd-theme==1.2.0']}

setup_kwargs = {
    'name': 'transmission-rpc',
    'version': '4.1.0',
    'description': 'Python module that implements the Transmission bittorent client JSON-RPC protocol',
    'long_description': '# Transmission-rpc Readme\n\n[![PyPI](https://img.shields.io/pypi/v/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Documentation Status](https://readthedocs.org/projects/transmission-rpc/badge/)](https://transmission-rpc.readthedocs.io/)\n[![ci](https://github.com/Trim21/transmission-rpc/workflows/ci/badge.svg)](https://github.com/Trim21/transmission-rpc/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Codecov branch](https://img.shields.io/codecov/c/github/Trim21/transmission-rpc/master)](https://codecov.io/gh/Trim21/transmission-rpc/branch/master)\n\n`transmission-rpc` is a python wrapper of on top of [transmission](https://github.com/transmission/transmission) JSON RPC protocol,\nhosted on GitHub at [github.com/trim21/transmission-rpc](https://github.com/trim21/transmission-rpc)\n\n## Introduction\n\n`transmission-rpc` is a python module implementing the json-rpc client protocol for the BitTorrent client Transmission.\n\nSupport 14 <= rpc version <= 17 (2.40 <= transmission version <= 4.0.1),\nshould works fine with newer rpc version but some new feature may be missing.\n\n## versioning\n\n`transmission-rpc` follow [Semantic Versioning](https://semver.org/),\nreport an issue if you found unexpected API break changes at same major version.\n\n## Install\n\n```console\npip install transmission-rpc -U\n```\n\n## Documents\n\n<https://transmission-rpc.readthedocs.io/>\n\n## Contributing\n\nAll kinds of PRs (docs, feature, bug fixes and eta...) are most welcome.\n\n## License\n\n`transmission-rpc` is licensed under the MIT license.\n',
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Trim21/transmission-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
