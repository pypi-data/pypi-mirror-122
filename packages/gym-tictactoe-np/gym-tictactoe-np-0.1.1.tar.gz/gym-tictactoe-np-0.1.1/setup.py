# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_tictactoe_np', 'gym_tictactoe_np.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.20.0,<0.21.0', 'numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'gym-tictactoe-np',
    'version': '0.1.1',
    'description': "3D TicTacToe environment for OpenAI's gym written with Numpy.",
    'long_description': "# gym-tictactoe-np\n\n3D TicTacToe environment for OpenAI's gym. Optimized and written using numpy for parallel gameplay and rapid training\n",
    'author': 'Ishan Manchanda',
    'author_email': 'ishanmanchanda70@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IshanManchanda/gym-tictactoe-np',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
