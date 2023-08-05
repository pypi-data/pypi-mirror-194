# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['llsubtitles', 'llsubtitles.dictionaries']

package_data = \
{'': ['*'],
 'llsubtitles': ['templates/*'],
 'llsubtitles.dictionaries': ['data/*']}

install_requires = \
['openai-whisper>=20230124,<20230125', 'xpinyin>=0.7.6,<0.8.0']

entry_points = \
{'console_scripts': ['llsubtitles = llsubtitles.__main__:main']}

setup_kwargs = {
    'name': 'llsubtitles',
    'version': '1.0.1',
    'description': "Use OpenAI's whisper to generate subtitles in multiple languages for the purpose of language learning",
    'long_description': "Language learning application that uses openai's whisper to generate foreign language and English subtitles for videos simultaneously to help with language learning.\n\n# Installation\n\n```bash\n> pip install llsubtitles\n```\n\n# Usage\n\nTo use `llsubtitles` first you need a foreign language .mp4 file. I recommend using [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download content for language learning. Once you have a .mp4 file you can use `llsubtitles` to generate subtitles for it.\n\n```bash\n# Using chinese content for this example\n> llsubtitles --language Chinese --model small --combined --definitions --pinyin example.mp4\n```\n\n**--language**: Refers to the language used by openai's whisper to generate subtitles.<br>\n**--model**: The model used by whisper. See [their documentation](https://github.com/openai/whisper) for more options.<br>\n**--combined**: If this flag is used, the subtitles will be generated in both the foreign language and English.<br>\n**--definitions**: If this flag is used, the subtitles will include definitions for the foreign language words.<br>\n**--pinyin**: Optional flag for Chinese learners, if this flag is used, the subtitles will include pinyin for the Chinese words.\n\nNote, you should make sure that you have pytorch set up correctly to use Cuda if you're using an Nvidia GPU. See [pytorch's documentation](https://pytorch.org/get-started/locally/) for more information. This will greatly improve performance.\n\n# Credits\nChinese English dictionary is courtesy of [cedict](https://www.mdbg.net/chinese/dictionary?page=cedict)",
    'author': 'Brian Moody',
    'author_email': 'brian.k.moody@outlook.com',
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
