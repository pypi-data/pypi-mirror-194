# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['askitsu', 'askitsu.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.0,<4.0.0', 'colorama>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'askitsu',
    'version': '1.0.0',
    'description': 'An async API wrapper for Kitsu.io',
    'long_description': '<h1  align="center">\naskitsu\n</h1>\n\n[![TwitterShomy](https://img.shields.io/badge/-shomykohai-1DA1F2?style=flat&logo=twitter&logoColor=white&labelColor=1DA1F2)](https://twitter.com/shomykohai)\n[![askitsu](https://img.shields.io/pypi/v/askitsu?label=askitsu&logo=pypi&logoColor=white&labelColor=blue&color=9cf)](https://pypi.org/project/askitsu/)\n[![Documentation Status](https://readthedocs.org/projects/askitsu/badge/?version=master)](https://askitsu.readthedocs.io/en/master/?badge=master)\n\n<p align="center">\n  An async wrapper for Kitsu.io API written in Python\n</p>\n\n![askitsu](https://github.com/ShomyKohai/askitsu/blob/master/docs/images/dark.png?raw=true "askitsu")\n  \n\n# IMPORTANT\n\n💡 UPDATE:<br>\nThe master branch is now in a status where it can be used.<br>\nFor any issue you may encounter, please make a new [issue](https://github.com/ShomyKohai/askitsu/issues).<br>\nYou can check the [projects](https://github.com/ShomyKohai/askitsu/projects?type=classic) tab to see current progress.\n\n# Key features\n\n- Fully typed\n- Use of `async`/`await`\n- Support most of primary Kitsu entries -- Anime, Manga, Characters and much more\n- Can be used with discord bots\n\n# Currently avaiable endpoints\n\n- 🎞️ Anime (Anime, Episodes and Streaming Links)\n- 📖 Manga (Manga and Chapters)\n- 👥 Characters\n- 📰 Reviews\n- 👤 User (Profile and Profile Links)\n- 🗞️ Posts\n- 📚 User Libraries\n\nComing soon:\n\n- 🗨️ Comments\n\n# Installing\n\nRequires python 3.8+\n\nTo install the package, you can simply run\n\n```py\n\n#Linux/MacOS\npython3 -m pip install askitsu\n\n\n#Windows\npy -3 -m pip install askitsu\n\n```\n\nOr to get the latest dev version\n\n```py\n\n#Linux/MacOS\npython3 -m pip install git+https://github.com/ShomyKohai/askitsu.git\n\n  \n\n#Windows\npy -3 -m pip install git+https://github.com/ShomyKohai/askitsu.git\n\n```\n\n## Requirements\n\n- [aiohttp](https://pypi.org/project/aiohttp/)\n- [colorama](https://pypi.org/project/colorama/)\n\n# Examples\n\n```py\nimport askitsu\nimport asyncio\n\nasync def search():\n    client = askitsu.Client()\n    anime = await client.search_anime("attack on titan")\n    print(anime.episode_count)\n    print(anime.status)\n    await client.close()\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(search())\n\n```\n\nMore examples can be found inside the example directory -> [Here](https://github.com/ShomyKohai/askitsu/tree/master/examples)\n\n# Links & Credits\n\n- [Docs](https://askitsu.readthedocs.io/)\n- [PyPi](https://pypi.org/project/askitsu/)\n- [Kitsu.io Docs](https://kitsu.io/api/playground)\n- [discord.py](https://github.com/Rapptz/discord.py) (bot example)\n\n__"Kitsu" name and the "Kitsu logo" are property of [Kitsu](https://kitsu.io/)__\n',
    'author': 'ShomyKohai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ShomyKohai/askitsu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
