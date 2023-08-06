# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['instrumentum',
 'instrumentum.features',
 'instrumentum.image_processing',
 'instrumentum.time_series']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'instrumentum',
    'version': '0.4.1',
    'description': 'General utilities for data science projects',
    'long_description': '# instrumentum\n\nGeneral utilities for data science projects\n\n## Installation\n\n```bash\n$ pip install instrumentum\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`instrumentum` was created by Federico Montanana. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`instrumentum` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Federico Montanana',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
