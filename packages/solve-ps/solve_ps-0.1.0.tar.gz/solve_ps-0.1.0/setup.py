# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solve_ps', 'solve_ps.subs']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['solve = solve_ps:main.cli']}

setup_kwargs = {
    'name': 'solve-ps',
    'version': '0.1.0',
    'description': 'a small cli tool for ps',
    'long_description': '# solve\n\na small cli tool for ps\n\n---\n\n## install\n\n```bash\ngit clone https://github.com/ganghe74/solve\ncd solve\npip install .\n```\n\n## Usage\n\n```bash\nsolve get boj 1000\nsolve tc 2 -p 1000\nsolve run 1000.cpp\nsolve diff\n```\n',
    'author': 'KH',
    'author_email': 'ganghe74@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
