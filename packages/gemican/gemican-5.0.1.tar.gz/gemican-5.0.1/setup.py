# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gemican',
 'gemican.plugins',
 'gemican.tests',
 'gemican.tests.dummy_plugins.namespace_plugin.gemican.plugins.ns_plugin',
 'gemican.tests.dummy_plugins.normal_plugin.normal_plugin',
 'gemican.tests.dummy_plugins.normal_plugin.normal_submodule_plugin',
 'gemican.tests.dummy_plugins.normal_plugin.normal_submodule_plugin.subpackage',
 'gemican.tools']

package_data = \
{'': ['*'],
 'gemican': ['themes/hyper/templates/*',
             'themes/hyper/templates/partials/*',
             'themes/simple/templates/*',
             'themes/simple/templates/partials/*'],
 'gemican.tests': ['TestPages/*',
                   'content/*',
                   'content/TestCategory/*',
                   'cyclic_intersite_links/*',
                   'mixed_content/*',
                   'mixed_content/subdir/*',
                   'nested_content/maindir/*',
                   'nested_content/maindir/subdir/*',
                   'output/basic/*',
                   'output/basic/author/*',
                   'output/basic/category/*',
                   'output/basic/drafts/*',
                   'output/basic/feeds/*',
                   'output/basic/override/*',
                   'output/basic/pages/*',
                   'output/basic/pictures/*',
                   'output/basic/tag/*',
                   'output/custom/*',
                   'output/custom/author/*',
                   'output/custom/category/*',
                   'output/custom/drafts/*',
                   'output/custom/feeds/*',
                   'output/custom/override/*',
                   'output/custom/pages/*',
                   'output/custom/pictures/*',
                   'output/custom/tag/*',
                   'output/custom_locale/*',
                   'output/custom_locale/author/*',
                   'output/custom_locale/category/*',
                   'output/custom_locale/drafts/*',
                   'output/custom_locale/feeds/*',
                   'output/custom_locale/override/*',
                   'output/custom_locale/pages/*',
                   'output/custom_locale/pictures/*',
                   'output/custom_locale/posts/2010/décembre/02/this-is-a-super-article/*',
                   'output/custom_locale/posts/2010/octobre/15/unbelievable/*',
                   'output/custom_locale/posts/2010/octobre/20/oh-yeah/*',
                   'output/custom_locale/posts/2011/avril/20/a-formerly-markdown-powered-article/*',
                   'output/custom_locale/posts/2011/février/17/article-1/*',
                   'output/custom_locale/posts/2011/février/17/article-2/*',
                   'output/custom_locale/posts/2011/février/17/article-3/*',
                   'output/custom_locale/posts/2012/février/29/second-article/*',
                   'output/custom_locale/posts/2012/novembre/30/filename_metadata-example/*',
                   'output/custom_locale/posts/2021/septembre/24/markdowns-back/*',
                   'output/custom_locale/tag/*',
                   'parse_error/*',
                   'test_theme/static/files/*',
                   'test_theme/static/images/*',
                   'test_theme/templates/*',
                   'theme_overrides/level1/*',
                   'theme_overrides/level2/*'],
 'gemican.tools': ['templates/*']}

install_requires = \
['Twisted>=21.7.0,<22.0.0',
 'blinker>=1.4',
 'docutils>=0.16',
 'feedgenerator>=1.9',
 'jinja2>=2.7',
 'pyOpenSSL>=20.0.1,<21.0.0',
 'python-dateutil>=2.8',
 'python-magic>=0.4.24,<0.5.0',
 'pytz>=2020.1',
 'rich>=10.1',
 'service-identity>=21.1.0,<22.0.0',
 'unidecode>=1.1']

extras_require = \
{'markdown': ['md2gemini>=1.8.1,<2.0.0']}

entry_points = \
{'console_scripts': ['gemican = gemican.__main__:main',
                     'gemican-import = gemican.tools.gemican_import:main',
                     'gemican-plugins = gemican.plugins._utils:list_plugins',
                     'gemican-quickstart = '
                     'gemican.tools.gemican_quickstart:main',
                     'gemican-themes = gemican.tools.pelican_themes:main']}

setup_kwargs = {
    'name': 'gemican',
    'version': '5.0.1',
    'description': 'Static gemini capsule generator supporting Markdown and Gemtext',
    'long_description': '# Gemican\n\nGemican is a static gemini capsule generator, written in [Python](https://www.python.org/), and based on the static site generator [Pelican](https://github.com/getpelican/pelican).\n\n* Write content in [Markdown](https://daringfireball.net/projects/markdown/) or directly in Gemtext using your editor of choice\n* Includes a simple command line tool to (re)generate capsule files\n* Easy to interface with version control systems and web hooks\n* Completely static output is simple to host anywhere\n\n\n## Features\n\nGemican’s feature highlights include:\n\n* Chronological content (e.g., articles, blog posts) as well as static pages\n* Site themes (created using Jinja2_ templates)\n* Publication of articles in multiple languages\n* Generation of Atom and RSS feeds\n* Import existing content from WordPress, Dotclear, or RSS feeds\n* Fast rebuild times due to content caching and selective output writing\n\nCheck out [Gemican\'s documentation](gemini://gemini.hyperlinkyourheart.com/gemicandocs/) for further information.\n\n\n## Source code\n\nGemican\'s source code is [hosted on GitHub](https://github.com/khoulihan/gemican). If you feel like hacking, take a look at [Pelican\'s internals](gemini://gemini.hyperlinkyourheart.com/gemicandocs/pages/gemican-internals.gmi).\n\n\n## Why the name "Gemican"?\n\n"Gemican" is an anagram of *camegin*, which means nothing.\n\nOnly joking - Gemican is based on the Pelican static site generator, and took its name from that.\n',
    'author': 'Kevin Houlihan',
    'author_email': 'kevin@crimsoncookie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khoulihan/gemican',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)
