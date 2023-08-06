# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voices',
 'voices.cli',
 'voices.functions.slicer',
 'voices.functions.slicer.interactive',
 'voices.functions.slicer.text',
 'voices.functions.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyAudio>=0.2.13,<0.3.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'importlib-metadata>=6.0.0,<7.0.0',
 'librosa>=0.10.0,<0.11.0',
 'matplotlib>=3.7.0,<4.0.0',
 'noneprompt>=0.1.7,<0.2.0',
 'pypinyin>=0.48.0,<0.49.0',
 'soundfile>=0.12.1,<0.13.0']

entry_points = \
{'console_scripts': ['voices = voices.cli:main']}

setup_kwargs = {
    'name': 'voices',
    'version': '1.0.0b2',
    'description': '适用于 diffsinger 的多功能工具集',
    'long_description': '# VoiceS\n\n适用于 diffsinger 的多功能工具集\n\n## 功能与计划\n\n您可以点击对应的功能名查看对应的文档:\n\n- [x] [[slicer]适用于 .ass 的字幕切片工具](docs/字幕切片工具.md)\n- [x] [[uta]openutau 转 .ass(k轴) 工具](docs/utau转k轴工具.md)\n',
    'author': 'Well404',
    'author_email': 'well_404@outlook.com',
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
