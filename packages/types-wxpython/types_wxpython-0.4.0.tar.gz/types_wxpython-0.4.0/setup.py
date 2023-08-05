# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wx-stubs']

package_data = \
{'': ['*'],
 'wx-stubs': ['DateTime/*',
              'FileType/*',
              'Image/*',
              'TopLevelWindow/*',
              'Window/*',
              'adv/*',
              'aui/*',
              'dataview/*',
              'glcanvas/*',
              'grid/*',
              'grid/GridBlocks/*',
              'html/*',
              'html2/*',
              'lib/agw/ribbon/buttonbar/*',
              'lib/agw/ribbon/gallery/*',
              'lib/agw/ribbon/toolbar/*',
              'lib/analogclock/lib_setup/fontselect/*',
              'lib/buttons/*',
              'lib/calendar/*',
              'lib/colourselect/*',
              'lib/scrolledpanel/*',
              'lib/wxpTag/*',
              'media/*',
              'propgrid/*',
              'ribbon/*',
              'richtext/*',
              'stc/*',
              'xml/*',
              'xrc/*']}

setup_kwargs = {
    'name': 'types-wxpython',
    'version': '0.4.0',
    'description': 'Typing stubs for wxPython',
    'long_description': '# Typing stubs for wxPython\nVersion: wxPython 4.2.0\n\nThis package contains typings stubs for [wxPython](https://pypi.org/project/wxPython/)\n\nThis package is not maintained by the maintainers of wxPython. This is made by users of wxPython.\n\nAny help is always welcome.\n',
    'author': 'Alexion Software',
    'author_email': 'info@alexion.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlexionSoftware/types-wxpython',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
