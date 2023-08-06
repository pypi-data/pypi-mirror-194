# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jintegral']

package_data = \
{'': ['*']}

install_requires = \
['csaps>=1.1.0,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'plotly>=5.13.1,<6.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'jintegral',
    'version': '1.0.0a2',
    'description': 'A Python implementation of J-integral data reduction for translaminar toughness of compact tension specimens',
    'long_description': '[![DOI](https://zenodo.org/badge/563768686.svg)](https://zenodo.org/badge/latestdoi/563768686)\n\n# Jintegral\nA Python implementation of J-integral data reduction for translaminar toughness of compact tension specimens\n\n# Roadmap \nCurrently, this repository contains only (functional) raw code as a support for paper doi: .\nIt will be cleaned and (hopefully) packaged for a future release. \n\n# Documentation\nTo be done\n\n# Related works on github\n\n- https://github.com/smrg-uob/OUR-OMA\n- https://github.com/irfancn/Matlab-J-integral\n\n# Acknowledgement\n\nThe research leading to this software has been carried out within the framework of [HyFiSyn project](https://www.hyfisyn.eu/) and has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 765881. \n',
    'author': 'Guillaume Broggi',
    'author_email': '25569517+GuillaumeBroggi@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
