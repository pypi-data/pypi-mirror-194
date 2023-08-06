# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asciibee']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4,<10.0', 'numpy>=1.24.2,<2.0.0']

entry_points = \
{'console_scripts': ['asciibee = asciibee.main:main']}

setup_kwargs = {
    'name': 'asciibee',
    'version': '0.3.2',
    'description': 'An image-to-ascii-art converter',
    'long_description': "# `<(||')` asciibee `<(||')`\n\nAn image-to-ascii-art converter\n\n## Description\n\nThe default settings are tuned to work best with fine art. Play with different\nshaders, chunk sizes, and value inversion for different results. Remember to\ndecrease your font size if you can't see the whole image.\n\nScaling is accomplished by dividing the image into chunks and converting each\nchunk to a single character. The chunk size can be adjusted with the -c flag.\nThe chunk size defaults to the pixel width of the image divided by 100. The\noutput will tell you what chunk size was used.\n\n## Installation\n\n`$ pip install asciibee`\n\n## Usage\n\nThe best way to learn how to use the app is via the help text:\n\n`$ asciibee --help`\n\nThe most simple command is passing in a path to an image file:\n\n`$ asciibee ~/Downloads/starrynight.png`\n\nYou can use it as an importable module as well.\n\n```python\nfrom asciibee.image import AsciiImage\nimage = AsciiImage('/Users/jnakama/Downloads/port.jpeg')\nimage.convert()  # Converts the image to a matrix of ASCII characters\nimage.ascii_matrix # It's stored here\nimage.show()  # Prints the characters\n```\n\n## Development\n\nThe build system and package manager is [poetry](https://python-poetry.org/).\n\nThe easiest way to run the app locally:\n\n`$ poetry run python -m asciibee.main <path_to_image>`\n\nYou can also install the deps and run it without the `poetry run` prefix.\n\n```text\n                    ...         .....             ......\n                   ..,,-,.         ..,.        ..,,....\n                      ..,-..         .,,.     .,..\n                         .-..         .,-,,..-..             ......\n                          ..,,.      .####+###+..         ..,,,,,,..\n                            ..+-..   -+@@@##@@#+  .....,,,,,.\n                              ..,---.-++++++#+#-.,--,,,....\n                                 ..-#++#######++#+,.\n                        .  ..      ,#++@@@@#@@@#+..            ...\n                    ..,,-,-,-,,,..,-++##@@##@###+++-,,,..,,,,,,,..\n                      ......,,,-++++#+###########+++----,,,... .\n             .....,,,,,,----------+++-###+#++#+++++----------,,,,,,......\n       ...,,,-,,,,,,,,,-,,,,--------+-..#####-..,+-+----,,,-----,-,,,---,,,,....\n    ...,,,,,,,,,,-,,,,,,,,,-,--,,--,.-+########+-,--+-----,,,,,,,---,,--,---,,,,,..\n  ..,,,,,,.,,.,,,,,,,.,,--,,,,-,--..-+####@@@@@##-.,-+-,,,--,,,,,,,,--,,,,,,--,,,,.\n  .,,,,,,.,.,,.,,,..,,-,,,,,,,--+..,++++++++#####+-.,----,,-,,-,,,,,,,,,-,,.,,,-,,.\n  .,,,,,,.,,,.,,,,,,,,,,,,,,-,-+. .+###++#####@###+...---,,,,-,,------,,,,,,,,,..\n    ...,,,,,,,.,,,,,,,,,,,,,,-,.  ,#@@@#-+###@@@@@#,   ,-,,,,,,,,,,,,,,,.,,....\n                ..........,-,...  ,+##++++###@@@##+-.    .,,,.....   .\n                     ..,-,...     ,+##++#++++######-.      ..,..\n                    .,,,...       ,#@@##+##@@#@@@@#-.        .,,.\n                   .,,.           .+####++#@@@@@@#+..         .,.\n                   ...            ..+++++++######+,.          ...\n                                    .+###++####@#-.\n                                     ,+##+######-.\n                                     ...-##@#+-...\n                                        ..--...\n```\n",
    'author': 'Jamey Nakama',
    'author_email': 'nakamajamey@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jameynakama/asciibee/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
