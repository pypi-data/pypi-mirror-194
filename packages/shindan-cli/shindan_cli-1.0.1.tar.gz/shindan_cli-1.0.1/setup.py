# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shindan_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['shindan = shindan_cli.main:main']}

setup_kwargs = {
    'name': 'shindan-cli',
    'version': '1.0.1',
    'description': 'ShindanMaker (https://shindanmaker.com) CLI',
    'long_description': "# shindan-cli\n\n[![PyPI]](https://pypi.org/project/shindan-cli\n) [![PyPI - Python Version]](https://pypi.org/project/shindan-cli\n)\n\n[![Release Package]](https://github.com/eggplants/shindan-cli/actions/workflows/release.yml\n) [![Maintainability]](https://codeclimate.com/github/eggplants/shindan-cli/maintainability\n)\n\nShindanMaker (<https://shindanmaker.com>) CLI\n\n## Install\n\n```bash\npip install shindan-cli\n```\n\n## Usage\n\n### CLI\n\n```shellsession\n$ shindan -h\nusage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME\n\nShindanMaker (https://shindanmaker.com) CLI\n\npositional arguments:\n  ID             shindan page id\n  NAME           shindan name\n\noptional arguments:\n  -h, --help     show this help message and exit\n  -w, --wait     insert random wait\n  -H, --hashtag  add hashtag `#shindanmaker`\n  -l, --link     add link to last of output\n  -V, --version  show program's version number and exit\n\n$ shindan 1036646 hoge\nねこって、むしだ。\n\n𝙐𝙉𝙄𝙌𝙇𝙊\n\n$ shindan 1036646 huga -l\nねこって、むしだ。\n\n𝙉𝙄𝙎𝙎𝙄𝙉\nhttps://shindanmaker.com/1036646\n\n$ shindan 1036646 huga -l -H\nねこって、むしだ。\n\n𝙁𝙐𝙅𝙄𝙏𝙎𝙐\n#shindanmaker\nhttps://shindanmaker.com/1036646\n```\n\n### Library\n\n```python\nfrom shindan_cli import shindan\n# type: (int, str, optional[bool]) -> ShindanResults\nshindan(1036646, 'hoge', wait=False)\n```\n\nReturns:\n\n```python\n{\n  'results': ['ねこって、むしだ。', '', '𝙏𝙊𝙆𝙔𝙊 𝙈𝙀𝙏𝙍𝙊'],\n  'hashtags': ['#shindanmaker'],\n  'shindan_url': 'https://shindanmaker.com/1036646'\n}\n```\n\n## License\n\nMIT\n\n---\n\n## Similar Imprementations\n\n- C#\n  - [misodengaku/ShindanMaker](https://github.com/misodengaku/ShindanMaker)\n    - Library\n- Go\n  - [kakakaya/goshindan](https://github.com/kakakaya/goshindan)\n    - Library + CLI\n    - <https://pkg.go.dev/github.com/kakakaya/goshindan>\n- Java\n  - [shibafu528/shindan4j](https://github.com/shibafu528/shindan4j)\n    - Library\n    - <https://jitpack.io/#shibafu528/shindan4j>\n- JavaScript\n  - [asawo/shindan-scraper](https://github.com/asawo/shindan-scraper)\n    - Library\n  - [stawberri/shindan](https://github.com/stawberri/shindan)\n    - Library (Archived)\n    - <https://www.npmjs.com/package/shindan>\n- Perl\n  - [Likk/WebService-ShindanMaker](https://github.com/Likk/WebService-ShindanMaker)\n    - Library\n- PHP\n  - [moroya/php-shindanmaker](https://github.com/moroya/php-shindanmaker)\n    - Library\n    - <https://packagist.org/packages/moroya/php-shindanmaker>\n- Python\n  - [Le96/auto_shindanmaker](https://github.com/Le96/auto_shindanmaker)\n    - Bot Server\n  - [tanitanin/shindan-python](https://github.com/tanitanin/shindan-python)\n    - CLI (Script)\n- Ruby\n  - [osak/shindanmaker](https://github.com/osak/shindanmaker)\n    - [Mikutter](https://github.com/mikutter/mikutter) Plugin\n  - [gouf/shindan](https://github.com/gouf/shindan)\n    - Library\n  - [ikaruga777/shindan-cli](https://github.com/ikaruga777/shindan-cli)\n    - CLI\n  - [yasuhito/shindan](https://github.com/yasuhito/shindan)\n    - CLI\n    - <https://rubygems.org/gems/shindan>\n- TypeScript\n  - [dqn/shindanmaker-js](https://github.com/dqn/shindanmaker-js)\n    - Library\n\n[Release Package]: https://github.com/eggplants/shindan-cli/actions/workflows/release.yml/badge.svg\n[PyPI]: https://img.shields.io/pypi/v/shindan-cli?color=blue\n[PyPI - Python Version]: https://img.shields.io/pypi/pyversions/shindan-cli\n[Maintainability]: https://api.codeclimate.com/v1/badges/9134b56a4241e91dfa01/maintainability\n",
    'author': 'eggplants',
    'author_email': 'w10776e8w@yahoo.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eggplants/shindan-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
