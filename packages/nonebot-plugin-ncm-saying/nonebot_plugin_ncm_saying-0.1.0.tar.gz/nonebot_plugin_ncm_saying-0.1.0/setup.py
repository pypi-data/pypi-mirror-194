# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_ncm_saying']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ncm-saying',
    'version': '0.1.0',
    'description': '一开口就老网抑云了',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-ncm-saying\n\n_✨ 一开口就老网抑云了 ✨_\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/A-kirami/nonebot-plugin-moyu.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-ncm-saying">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ncm-saying.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n\n</div>\n\n## 📖 介绍\n\n如果有一天，我决定删了你，并不代表你对我不再重要，而是我怕我自己越陷越深，原来真的有那么一个人，我无数次的想要放弃，但终究还是舍不得，我知道忘记你很难，但我决定试试。 ——网易云音乐热评《可惜没有如果》\n\n## 💿 安装\n\n<details>\n<summary>使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-ncm-saying\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n<details>\n<summary>pip</summary>\n\n    pip install nonebot-plugin-ncm-saying\n</details>\n<details>\n<summary>pdm</summary>\n\n    pdm add nonebot-plugin-ncm-saying\n</details>\n<details>\n<summary>poetry</summary>\n\n    poetry add nonebot-plugin-ncm-saying\n</details>\n<details>\n<summary>conda</summary>\n\n    conda install nonebot-plugin-ncm-saying\n</details>\n\n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n\n    nonebot.load_plugin(\'nonebot_plugin_ncm-saying\')\n\n</details>\n\n## 🎉 使用\n/网抑云|网易云热评：随机一条网易云热评\n\n## 💡 鸣谢\n\n### [夏柔网易云热评API](https://api.aa1.cn/doc/api-wenan-wangyiyunreping.html)\n\n### [A-kirami一言](https://github.com/A-kirami/nonebot-plugin-hitokoto)：本项目就是用大佬的项目改了几行代码，连说明文档也是（）',
    'author': 'Ananovo',
    'author_email': 'techotaku39@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
