# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['picklejar']
install_requires = \
['dill>=0.3.6,<0.4.0']

setup_kwargs = {
    'name': 'picklejar',
    'version': '3.1.0',
    'description': 'Read and write pickles to a single file',
    'long_description': '# Overview\n[picklejar] is a python module that allows you to work with multiple pickles while reading/writing them to a single \nfile/jar.\n\n## License\n[picklejar] is released under the [GNU Lesser General Public License v3.0], see the file LICENSE and LICENSE.lesser \nfor the license text.\n\n## Compatibility\nAs of version 3.0.0, picklejar is compatible with the latest versions of Python3, and PyPy3!\n\n# Installation/Getting Started\nThe most straightforward way to get the picklejar module working for you is:\n```commandline\npip install picklejar\n```\n\n# Documentation\nAll documentation for using picklejar can be found at [ReadTheDocs](http://picklejar.readthedocs.io/)\n\n# Contributing\nComments and enhancements are very welcome. To install [picklejar] for development purposes, first\ninstall [Poetry](https://python-poetry.org) and then run:\n```commandline\npoetry install --with dev\n```\n\nCode contributions are encouraged: please feel free to [fork the\nproject](https://bitbucket.org/isaiah1112/picklejar) and submit pull requests to the **develop** branch.\n\nReport any issues or feature requests on the [BitBucket bug\ntracker](https://bitbucket.org/isaiah1112/picklejar/issues?status=new&status=open). Please include a minimal (not-) \nworking example which reproduces the bug and, if appropriate, the traceback information.  Please do not request features \nalready being worked towards.\n\n## Building Documentation Locally\nTo install the packages required and build the Sphinx Documentation simply:\n```commandline\nmake docs\n```\n\nThis will install all the requirements to work on picklejar and then build the HTML documentation.\nTo open the docs in your default browser, simply run:\n```commandline\nopen docs/build/html/index.html\n```\n\n## Testing\nTo run the tests for [picklejar] locally with your installed version of python, simply run:\n```commandline\nmake test\n```\n\nTo run tests across different versions of Python via [Docker](https://www.docker.com), install and start Docker, \nthen run:\n```commandline\nmake docker-test-all\n```\n\n[GNU Lesser General Public License v3.0]: http://choosealicense.com/licenses/lgpl-3.0/ "LGPL v3"\n\n[picklejar]: https://bitbucket.org/isaiah1112/picklejar "picklejar Module"\n',
    'author': 'Jesse Almanrode',
    'author_email': 'jesse@almanrode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://picklejar.readthedocs.io/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
