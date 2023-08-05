# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypka', 'pypka.CHARMM36m', 'pypka.G54A7', 'pypka.clean', 'pypka.mc']

package_data = \
{'': ['*'],
 'pypka.CHARMM36m': ['sts/*'],
 'pypka.G54A7': ['sts/*', 'sts_cphmd/*', 'sts_old/*']}

install_requires = \
['delphi4py>=1.0.1,<2.0.0',
 'numpy',
 'pdbmender>=0.3.0,<0.4.0',
 'psutil',
 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'pypka',
    'version': '2.6.0',
    'description': 'A python module for flexible Poisson-Boltzmann based pKa calculations with proton tautomerism',
    'long_description': '[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mms-fcul/PypKa/blob/master/examples/notebook/pypka.ipynb) [![CircleCI](https://circleci.com/gh/mms-fcul/PypKa.svg?style=svg)](https://circleci.com/gh/mms-fcul/PypKa) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/59a058e4bf0846f18d9d1f6b16a4a0e5)](https://www.codacy.com/gh/mms-fcul/PypKa/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mms-fcul/PypKa&amp;utm_campaign=Badge_Grade) [![Documentation Status](https://readthedocs.org/projects/pypka/badge/?version=latest)](https://pypka.readthedocs.io/en/latest/?badge=latest)\n\n[![PyPI version](https://badge.fury.io/py/pypka.svg)](https://badge.fury.io/py/pypka)  [![PyPI - Downloads](https://img.shields.io/pypi/dm/pypKa)](https://badge.fury.io/py/pypKa)\n\n# PypKa\n\nA python module for flexible Poisson-Boltzmann based pKa calculations with proton tautomerism\nDOI: <a href="https://doi.org/10.1021/acs.jcim.0c00718">10.1021/acs.jcim.0c00718</a>\n\n```bibtex\n@article{reis2020jcim,\nauthor = {Reis, Pedro B. P. S. and Vila-Viçosa, Diogo and Rocchia, Walter and Machuqueiro, Miguel},\ntitle = {PypKa: A Flexible Python Module for Poisson–Boltzmann-Based pKa Calculations},\njournal = {Journal of Chemical Information and Modeling},\nvolume = {60},\nnumber = {10},\npages = {4442-4448},\nyear = {2020},\ndoi = {10.1021/acs.jcim.0c00718}\n}\n```\n\n## Documentation & Basic Usage\n\n  Documentation can be found [here](https://pypka.readthedocs.io/en/latest/)\n\n  Starting templates for the the API and CLI usage can be found [here](https://pypka.readthedocs.io/en/latest/example.html) while a online notebook is hosted at [Google Colab](https://colab.research.google.com/github/mms-fcul/PypKa/blob/master/pypka/example/notebook/pypka.ipynb)\n\n## Installation & Dependencies\n\nPypKa should be installed in a Linux-based system. In Windows please use the [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).\n\n* python2.6>= & python3.5>=\n* libgfortran4\n* gawk\n* pytest\n* numpy\n* delphi4py\n* pdbmender\n\n```bash\n  python3 -m pip install pypka\n  apt install gawk gcc gfortran libgfortran4 python2\n```\n\nA docker image is also [available](https://hub.docker.com/r/pedrishi/pypka). \nA simple way of using it would be to build the image from the [Dockerfile](./Dockerfile) and running it on a local directory which contains the cli parameters file and input structure.\n```bash\ndocker build -t pypka/latest -f Dockerfile .\ndocker run -v ${PWD}:/home/ -w /home -t pypka:latest python3.9 -m pypka <PARAMETERS_FILE>\n```\n\nFunctioning working examples of the API, CLI, docker and notebook can be found under /examples.\n\n## Contributing\n\nContributions are encouraged, and they are greatly appreciated!\n\nYou can contribute in many ways:\n\n* Report Bugs\n* Fix Bugs\n* Implement Features\n* Write Documentation\n* Submit Feedback\n\nFor more info check [CONTRIBUTING](./CONTRIBUTING.rst)\n\n## License\n\n  pypka is distributed under a [LGPL-3.0](./LICENSE), however delphi4py depends on\n  DelPhi which is proprietary. To use DelPhi the user is required to\n  download the DelPhi license\n  [here](https://honiglab.c2b2.columbia.edu/software/cgi-bin/software.pl?input=DelPhi)\n\n## Contacts\n\n  Please submit a github issue to report bugs and to request new features.\n  Alternatively you may find the developer [here](mailto:pdreis@fc.ul.pt). Please visit ou [website](http://mms.rd.ciencias.ulisboa.pt/) for more information.\n',
    'author': 'Pedro Reis',
    'author_email': 'pdreis@fc.ul.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypka.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
