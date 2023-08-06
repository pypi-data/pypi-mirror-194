# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sspeedup', 'sspeedup.cache', 'sspeedup.logging', 'sspeedup.word_split']

package_data = \
{'': ['*']}

install_requires = \
['jieba[word-split-jieba]>=0.42.1,<0.43.0', 'pymongo[logging]>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'sspeedup',
    'version': '0.1.0',
    'description': '开发工具箱',
    'long_description': '# sspeedup\n\n开发工具箱。\n\n- 缓存\n    - 过期缓存\n- 日志\n    - 运行日志\n- 终端彩色输出\n- 可选模块加载\n- 分词\n    - jieba\n        - 普通分词\n        - 搜索引擎分词\n        - 词性分词',
    'author': 'yezi',
    'author_email': 'yehaowei20060411@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FHU-yezi/sspeedup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
