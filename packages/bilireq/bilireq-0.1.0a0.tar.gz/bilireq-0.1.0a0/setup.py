# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bilireq',
 'bilireq.auth',
 'bilireq.dynamic',
 'bilireq.live',
 'bilireq.login',
 'bilireq.user',
 'bilireq.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0', 'rsa>=4.7.2,<5.0.0']

extras_require = \
{'qrcode': ['qrcode[pil]>=7.1,<8.0']}

setup_kwargs = {
    'name': 'bilireq',
    'version': '0.1.0a0',
    'description': 'Another Bilibili request lib.',
    'long_description': '# BiliReq\n\n## 简介\n\n原 [HarukaBot](https://github.com/SK-415/HarukaBot) 的哔哩哔哩请求库。\n\n因为现有的 Bilibili API 库无法满足需求，所以单独拆分出来方便其他项目复用。\n\n## 文档\n\n这个项目还处于起步阶段，等基本功能完善后会更新文档。\n\n## 功能\n\n目前只支持了一些我会用到的 API，有兴趣可以查看源码。\n\n如果你希望添加更多 API 欢迎在 Issue 区提出请求。\n\n## 开源协议\n\nMIT',
    'author': 'SK-415',
    'author_email': '2967923486@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SK-415/bilireq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
