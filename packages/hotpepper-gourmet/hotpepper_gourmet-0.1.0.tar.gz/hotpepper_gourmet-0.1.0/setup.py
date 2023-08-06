# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygourmet']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28,<3.0']

setup_kwargs = {
    'name': 'hotpepper-gourmet',
    'version': '0.1.0',
    'description': 'A simple Python wrapper for Hotpepper API',
    'long_description': '# hotpepper-gourmet\n\n## About\n\n[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルなクライアントライブラリです\n\n## How To Use\n\n### keyidの取得\n\nホットペッパーグルメAPIに登録し, token(keyid)を取得\n\n### サンプル\n\n``` python\nimport pygourmet\n\napi = pygourmet.Api(keyid=YOUR_KEYID)\nresults = api.get_restaurants(lat=35.170915, lng=136.8793482, radius=400)\nprint(results)\n```\n\n### シーケンス図\n\n![sequence](out/diagrams/sequence/sequence.png)\n\n___\n\nPowered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)\n',
    'author': 'paperlefthand',
    'author_email': 'being.paperlefthand@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/paperlefthand/hotpepper-gourmet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
