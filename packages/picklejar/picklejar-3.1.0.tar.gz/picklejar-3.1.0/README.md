# Overview
[picklejar] is a python module that allows you to work with multiple pickles while reading/writing them to a single 
file/jar.

## License
[picklejar] is released under the [GNU Lesser General Public License v3.0], see the file LICENSE and LICENSE.lesser 
for the license text.

## Compatibility
As of version 3.0.0, picklejar is compatible with the latest versions of Python3, and PyPy3!

# Installation/Getting Started
The most straightforward way to get the picklejar module working for you is:
```commandline
pip install picklejar
```

# Documentation
All documentation for using picklejar can be found at [ReadTheDocs](http://picklejar.readthedocs.io/)

# Contributing
Comments and enhancements are very welcome. To install [picklejar] for development purposes, first
install [Poetry](https://python-poetry.org) and then run:
```commandline
poetry install --with dev
```

Code contributions are encouraged: please feel free to [fork the
project](https://bitbucket.org/isaiah1112/picklejar) and submit pull requests to the **develop** branch.

Report any issues or feature requests on the [BitBucket bug
tracker](https://bitbucket.org/isaiah1112/picklejar/issues?status=new&status=open). Please include a minimal (not-) 
working example which reproduces the bug and, if appropriate, the traceback information.  Please do not request features 
already being worked towards.

## Building Documentation Locally
To install the packages required and build the Sphinx Documentation simply:
```commandline
make docs
```

This will install all the requirements to work on picklejar and then build the HTML documentation.
To open the docs in your default browser, simply run:
```commandline
open docs/build/html/index.html
```

## Testing
To run the tests for [picklejar] locally with your installed version of python, simply run:
```commandline
make test
```

To run tests across different versions of Python via [Docker](https://www.docker.com), install and start Docker, 
then run:
```commandline
make docker-test-all
```

[GNU Lesser General Public License v3.0]: http://choosealicense.com/licenses/lgpl-3.0/ "LGPL v3"

[picklejar]: https://bitbucket.org/isaiah1112/picklejar "picklejar Module"
