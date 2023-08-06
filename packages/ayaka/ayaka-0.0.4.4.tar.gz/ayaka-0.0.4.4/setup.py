# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka', 'ayaka.adapters', 'ayaka.adapters.nb1', 'ayaka.adapters.nb2']

package_data = \
{'': ['*']}

install_requires = \
['ayaka-db>=0.0.3',
 'ayaka-utils>=0.0.4',
 'fastapi>=0.87.0,!=0.89.0,<1.0.0',
 'httpx>=0.20.0,<1.0.0',
 'pydantic>=1.10.0',
 'uvicorn[standard]>=0.20.0,<1.0.0']

extras_require = \
{'nb2ob11': ['nonebot2>=2.0.0b5', 'nonebot-adapter-onebot>=2.2.0'],
 'playwright': ['playwright>=1.17.2']}

setup_kwargs = {
    'name': 'ayaka',
    'version': '0.0.4.4',
    'description': '猫猫，猫猫！',
    'long_description': '<div align="center">\n\n# Ayaka - 猫猫，猫猫！ - 0.0.4.4\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ayaka)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/ayaka)\n![PyPI - License](https://img.shields.io/pypi/l/ayaka)\n![PyPI](https://img.shields.io/pypi/v/ayaka)\n\n通过ayaka开发多框架下的、多人互动的群聊插件\n\n</div>\n\n根据py包的导入情况，猜测当前插件工作在哪个机器人框架下，已支持\n\n- [nonebot2](https://github.com/nonebot/nonebot2)(使用[onebotv11](https://github.com/nonebot/adapter-onebot)适配器，借助[qqguild_patch](https://github.com/mnixry/nonebot-plugin-guild-patch)同时可适配qqguild)\n- [hoshino](https://github.com/Ice-Cirno/HoshinoBot)\n- [nonebot1](https://github.com/nonebot/nonebot)\n\n也可将其\n\n- 作为console程序离线运行，便于调试\n- 直接通过反向ws连接到gocq上\n\n## 文档\n\nhttps://bridgel.github.io/ayaka/\n\n## 安装\n\n```\npip install ayaka\n```\n\n## 作为console程序离线运行\n\n```py\n# run.py\nimport ayaka.adapters.console as cat\n\n# 加载插件\n# do something\n\nif __name__ == "__main__":\n    cat.run()\n```\n\n```\npython run.py\n```\n\n## 直接连接到gocq上\n\n```py\n# run2.py\nimport ayaka.adapters.gocq as cat\n\n# 加载插件\n# do something\n\nif __name__ == "__main__":\n    cat.run()\n```\n\n```\npython run2.py\n```\n\n## 其他\n\n本插件的前身：[nonebot_plugin_ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
