# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shiny_api',
 'shiny_api.classes',
 'shiny_api.config',
 'shiny_api.modules',
 'shiny_api.modules.cogs']

package_data = \
{'': ['*'], 'shiny_api': ['applescript/*']}

install_requires = \
['Flask>=2.2.3,<3.0.0',
 'beautifulsoup4>=4.11.2,<5.0.0',
 'discord>=2.1.0,<3.0.0',
 'kivy>=2.1.0,<3.0.0',
 'luddite>=1.0.2,<2.0.0',
 'numpi>=0.3.1,<0.4.0',
 'openai>=0.26.5,<0.27.0',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'pandas>=1.5.3,<2.0.0',
 'py-applescript>=1.0.3,<2.0.0',
 'py-trello>=0.19.0,<0.20.0',
 'pygsheets>=2.0.6,<3.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'selenium>=4.8.2,<5.0.0',
 'simple-zpl2>=0.3.0,<0.4.0',
 'sqlalchemy>=2.0.4,<3.0.0',
 'waitress>=2.1.2,<3.0.0']

extras_require = \
{':sys_platform == "darwin"': ['python-dotenv>=0.21.1,<0.22.0'],
 ':sys_platform == "windows"': ['dotenv>=0.0.5,<0.0.6']}

entry_points = \
{'console_scripts': ['shiny_serial_camera = '
                     'shiny_api.shiny_serial_camera:start_gui',
                     'shiny_start_gui = shiny_api.main:start_gui']}

setup_kwargs = {
    'name': 'shiny-api',
    'version': '0.2.42',
    'description': 'Interface with LS and Camera Scanner',
    'long_description': 'None',
    'author': 'Chris Busillo',
    'author_email': 'info@shinycomputers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
