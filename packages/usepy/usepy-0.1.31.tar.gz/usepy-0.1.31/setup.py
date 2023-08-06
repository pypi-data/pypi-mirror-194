# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['usepy', 'usepy.data', 'usepy.decorator', 'usepy.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usepy',
    'version': '0.1.31',
    'description': 'usepy',
    'long_description': '# UsePy\n\n<a href="https://github.com/mic1on/usepy/actions/workflows/test.yml?query=event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/mic1on/usepy/workflows/test%20suite/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://pypi.org/project/usepy" target="_blank">\n    <img src="https://img.shields.io/pypi/v/usepy.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/usepy" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/usepy.svg" alt="Supported Python versions">\n</a>\n\n`usepy`是一个简单易用的Python工具库，包含了一些常用的工具函数。\n\n### 安装\n\n```bash\npip install usepy -U\n```\n\n### 示例及文档\n\n[官方文档](https://usepy.code05.com/)',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://usepy.code05.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
