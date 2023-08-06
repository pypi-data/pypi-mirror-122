# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyesaver']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'beepy>=1.0.7,<2.0.0',
 'mss>=6.1.0,<7.0.0',
 'opencv-python>=4.5.3,<5.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'screeninfo>=0.7,<0.8',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['eyesaver = eyesaver.main:app']}

setup_kwargs = {
    'name': 'eyesaver',
    'version': '1.0.0',
    'description': 'Save your eyes with this tool that lets you know when the screen changes a little bit. Excellent for late-night study videos.',
    'long_description': "# EyeSaver\n\nThis CLI-tool will tell you when there is a change happening on the screen by beeping. Now you can close your eyes and give them a rest during those late video-lecture nights, while being sure not to miss a single bullet in the presentation you're watching. 😉\n",
    'author': 'Sinan Morcel',
    'author_email': 'sinan.h.morcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sinan-morcel/eyesaver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
