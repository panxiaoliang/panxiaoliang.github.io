#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

# Site settings
SITENAME = '潘晓亮的博客'
SITEURL = ''
AUTHOR = '潘晓亮'

TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh_CN'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

PATH = ''
PAGE_PATHS = ['content/pages']
ARTICLE_PATHS = ['content/posts']
STATIC_PATHS = ['static', 'images', 'theme/images', 'extra/_redirects', 'code']
OUTPUT_PATH = 'docs'

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = ''
DEFAULT_PAGINATION = False

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}.html'

CATEGORIES_URL = 'categories.html'
TAGS_URL = 'tags.html'
ARCHIVES_URL = 'archives.html'
SEARCH_URL = 'search.html'

# Theme settings
THEME = 'themes/elegant'
TYPOGRIFY = True

# Elegant theme
EXTRA_PATH_METADATA = {'extra/_redirects': {'path': '_redirects'}}

if os.environ.get('CONTEXT') == 'production':
    STATIC_PATHS.append('extra/robots.txt')
    EXTRA_PATH_METADATA['extra/robots.txt'] = {'path': 'robots.txt'}
else:
    STATIC_PATHS.append('extra/robots_deny.txt')
    EXTRA_PATH_METADATA['extra/robots_deny.txt'] = {'path': 'robots.txt'}

DIRECT_TEMPLATES = ['index', 'categories', 'tags', 'archives', 'search', '404']
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
USE_SHORTCUT_ICONS = True

# Elegant Labels
SOCIAL_PROFILE_LABEL = 'Stay in Touch'
RELATED_POSTS_LABEL = 'Keep Reading'
SHARE_POST_INTRO = 'Like this post? Share on:'
COMMENTS_INTRO = 'So what do you think? Did I miss something? Is any part unclear? Leave your comments below.'

# Landing page
LANDING_PAGE_TITLE = "Pan Xiaoliang's Blog"

AUTHORS = {
    '潘晓亮': {
        'blurb': """江湖人称亮哥，计算机技术爱好者。""",
        'url': 'https://panxiaoliang.github.io',
    }
}

PROJECTS_TITLE = '项目列表'
PROJECTS = [
    {
        'name': 'panxiaoliang.github.io',
        'url': 'https://github.com/panxiaoliang/panxiaoliang.github.io',
        'description': "Pan Xiaoliang's Blog",
    },
]

# Legal
SITE_LICENSE = """Pan Xiaoliang's Blog is licensed under the
    <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">
        Creative Commons Attribution 4.0 International License
    </a>.
    """

# Plugin and extensions
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'extract_toc',
    'liquid_tags.img',
    'liquid_tags.include_code',
    'neighbors',
    'sitemap',
    'tipue_search']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {'permalink': ''},
    }
}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = 'feeds/all-{lang}.atom.xml'
AUTHOR_FEED_ATOM = 'feeds/{slug}.atom.xml'
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
    ('You can modify those links in your config file', '#'),
)

# Social widget
SOCIAL = (
    ('RSS', SITEURL + '/feeds/all.atom.xml'),
    ('Email', 'pxl@baihesoftware.com'),
)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
