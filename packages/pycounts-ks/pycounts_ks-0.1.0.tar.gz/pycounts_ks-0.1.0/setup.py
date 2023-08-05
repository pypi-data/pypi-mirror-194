# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycounts_ks']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0']

setup_kwargs = {
    'name': 'pycounts-ks',
    'version': '0.1.0',
    'description': 'Calculate word counts in a text file!',
    'long_description': '# `pycounts_ks`\n\nCalculate word counts in a text file!\n\n## Installation\n\n```bash\n$ pip install pycounts_ks\n```\n\n## Usage\n\n`pycounts_ks` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pycounts_ks.pycounts_ks import count_words\nfrom pycounts_ks.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. \nPlease note that this project is released with a Code of Conduct. \nBy contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycounts_ks` was created by [Shafayet Khan Shafee](https://github.com/shafayetShafee). It is licensed under the terms\nof the MIT license.\n\n## Credits\n\n`pycounts_ks` was created with \n[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and \nthe `py-pkgs-cookiecutter` \n[template](https://github.com/py-pkgs/py-pkgs-cookiecutter).',
    'author': 'Shafayet Khan Shafee',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
