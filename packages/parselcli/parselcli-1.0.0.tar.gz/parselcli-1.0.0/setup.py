# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parselcli']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'parsel>=1.6.0,<2.0.0',
 'prompt-toolkit>=3.0.20,<4.0.0',
 'requests-cache>=0.8.1,<0.9.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['parsel = parselcli.cli:cli']}

setup_kwargs = {
    'name': 'parselcli',
    'version': '1.0.0',
    'description': 'CLI interpreter for xpath/css selectors',
    'long_description': '\n# About parselcli ![PyPI](https://img.shields.io/pypi/v/parselcli.svg?style=popout)\n\n`parselcli` is a command line interface wrapper for [parsel](https://github.com/scrapy/parsel) package for evaluating css and xpath selection real time against web urls or local html files.  \n\n> Parsel is a library to extract data from HTML and XML using XPath and CSS selectors\n\n## Example Usage\n\nCalling command `parsel` with any http url will drop terminal into prompt. \nIn the prompt css and xpath selector can be entered together with commands and processing options\n\n```\n$ parsel "https://github.com/granitosaurus/parsel-cli"\n> h1::text\n[\'\\n    \', \'\\n  \', \'\\n  \', \'\\n  \', \'\\n\\n  \', \'\\n\', \'About parselcli \']\n> --xpath\n> //h1/text()\n[\'\\n    \', \'\\n  \', \'\\n  \', \'\\n  \', \'\\n\\n  \', \'\\n\', \'About parselcli \']\n> --css\n> --join --strip\ndefault processors: [Join, Strip]\n> h1::text\nAbout parselcli\n> h1::text --len\n7\n> --xpath\nswitched to xpath\ndefault processors: [Join, Strip]\n> //h1/text()\nAbout parselcli\n> --css\nswitched to css\ndefault processors: [Join, Strip]\n```\n \n\n#### Features:\n\n* Supports css and xpath expression.\n* Interactive shell with autocomplete.\n* Css and xpath hints based on current webpage DOM.\n* Input history tracking\n* Cache support for repeated usage.\n* Extensive and instant text processing via text processor flags.\n\n## Details\n\n    $ parsel --help                                                                                                      \n    Usage: parsel [OPTIONS] [URL]\n\n      Interactive shell for css and xpath selectors\n\n    Options:\n      -h TEXT                         request headers, e.g. -h "user-agent=cat\n                                      bot"\n      -xpath                          start in xpath mode instead of css\n      -p, --processors TEXT           comma separated processors: {}\n      -f, --file FILENAME             input from html file instead of url\n      -c TEXT                         compile css and return it\n      -x TEXT                         compile xpath and return it\n      --cache                         cache requests\n      --config TEXT                   config file  [default:\n                                      /home/dex/.config/parsel.toml]\n      --embed                         start in embedded python shell\n      --shell [ptpython|ipython|bpython|python]\n                                      preferred embedded shell; default auto\n                                      resolve in order\n      --help                          Show this message and exit.\n\n\n`parselcli` reads XML or HTML file from url or disk and starts interpreter for xpath or css selectors.\nBy default it starts in css interpreter mode but can be switched to xpath by `-xpath` command and switched back with `-css`.\nInterpreter also has auto complete and suggestions for selectors \\[in progress\\]\n\nThe interpreter also supports commands and embedding of `python`, `ptpython`, `ipython` and `bpython` shells.\nCommand can be called with `-` prefix. List of available commands can be found by calling `-help` command (see Example section).\n\n\n\n### Processors and Commands\n\n`parsecli` supports processors and commands in shell for advance usage:\n\n    $ parsel "https://github.com/granitosaurus/parsel-cli"                                                               \n    > --help                                                                                                              \n    Commands:\n    --help                   print help\n    --embed                  embed repl\n    --info                   show context info\n    --css                    switch to css input\n    --xpath                  siwtch to xpath input\n    --open                   open current url in web browser\n    --view                   open current doc in web browser\n    Processors:\n    --first, -1              take only 1st value\n    --len, -l                return total length\n    --strip, -s              strip away trailing chars\n    --absolute, -a           turn relative urls to absolute ones\n    --collapse, -c           collapse single element lists\n    --join, -j               join results\n    --join-with, -J          join results with specified character\n    -n                       take n-th element\n\nCommands can be called at any point in the prompter:\n\n    > -fetch "http://some-other-url.com"\n    downloading "http://some-other-url.com"\n    > -view\n    opening document in browser\n\nProcessor options can be either activated for specific prompt:\n\n    > h1::text --first\n    # will take first element\n\nOr can be set for current session:\n    > --first\n    default processors: [First]\n    # will process every following command with new processors\n\n## Install\n    \n    pip install parselcli\n    \nor install from github:\n\n    pip install --user git+https://github.com/Granitosaurus/parsel-cli@v0.33\n    \n## Config\n\n`parselcli` can be configured via `toml` configuration file found in `$XDG_HOME/parsel.toml` (usually `~/.config/parsel.toml`):\n\n    # default processors (the +flags)\n    processors = [ "collapse", "strip",]\n    # where ptpython history is located\n    history_file_css = "/home/user/.cache/parsel/history_css"\n    history_file_xpath = "/home/user/.cache/parsel/history_xpath"\n    history_file_embed = "/home/user/.cache/parsel/history_embed"\n    \n    [requests]\n    # when using --cache flag for using cached responses\n    cache_expire = 86400\n    # where sqlite cache file is stored for cache\n    cache_file = "/home/user/.cache/parsel/requests.cache"\n\n    [requests.headers]\n    # here headers can be defined for requests to avoid bot detection etc.\n    User-Agent = "parselcli web inspector"\n    # e.g. chrome on windows use\n    # User-Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"\n\n \n',
    'author': 'granitosaurus',
    'author_email': 'bernardas.alisauskas@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://scrapecrow.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
