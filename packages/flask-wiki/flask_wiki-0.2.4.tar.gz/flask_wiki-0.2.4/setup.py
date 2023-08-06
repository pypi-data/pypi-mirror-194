# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_wiki']

package_data = \
{'': ['*'],
 'flask_wiki': ['static/*',
                'static/css/*',
                'static/fonts/*',
                'static/js/*',
                'static/less/*',
                'static/scss/*',
                'templates/*',
                'templates/wiki/*',
                'translations/*',
                'translations/de/LC_MESSAGES/*',
                'translations/en/LC_MESSAGES/*',
                'translations/fr/LC_MESSAGES/*',
                'translations/hu/LC_MESSAGES/*',
                'translations/it/LC_MESSAGES/*']}

install_requires = \
['babel>=2.9.1',
 'bootstrap-flask',
 'flask-babelex',
 'flask-wtf',
 'flask<3.0.0',
 'jinja2>=3.0.0',
 'markdown<3.4.0',
 'werkzeug>=0.15',
 'wtforms<3.0.0']

setup_kwargs = {
    'name': 'flask-wiki',
    'version': '0.2.4',
    'description': 'Simple file-based wiki for Flask',
    'long_description': "# Flask-Wiki\n\n## About\n\nSimple file based wiki for Flask.\n\n## Getting started\n\n### Requirements\n\n* Python >=3.6.2\n* [Poetry](https://python-poetry.org/)\n\n### Install\n\n- Clone the git repository\n- run `poetry install`\n- If you want to enable debug mode, run `export FLASK_ENV=development`\n- `cd examples`, then `poetry run flask run`\n- go to http://localhost:5000/wiki\n\n## Configuration\n\n### Templates\n\n- WIKI_BASE_TEMPLATE = 'wiki/base.html'\n- WIKI_SEARCH_TEMPLATE = 'wiki/search.html'\n- WIKI_NOT_FOUND_TEMPLATE = 'wiki/404.html'\n- WIKI_FORBIDDEN_TEMPLATE = 'wiki/403.html'\n- WIKI_EDITOR_TEMPLATE = 'wiki/editor.html'\n- WIKI_FILES_TEMPLATE = 'wiki/files.html'\n- WIKI_PAGE_TEMPLATE = 'wiki/page.html'\n\n### Miscs\n\n- WIKI_HOME = 'home'\n- WIKI_CURRENT_LANGUAGE = lambda: 'en'\n- WIKI_LANGUAGES = ['en']\n- WIKI_URL_PREFIX = '/wiki'\n- WIKI_CONTENT_DIR = './data'\n- WIKI_UPLOAD_FOLDER = os.path.join(WIKI_CONTENT_DIR, 'files')\n- WIKI_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}\n- WIKI_MARKDOWN_EXTENSIONS = set(('codehilite', 'fenced_code'))\n\n### Permssions\n\n- WIKI_EDIT_VIEW_PERMISSION = lambda: True\n- WIKI_READ_VIEW_PERMISSION = lambda: True\n- WIKI_EDIT_UI_PERMISSION = WIKI_EDIT_VIEW_PERMISSION\n- WIKI_READ_UI_PERMISSION = WIKI_READ_VIEW_PERMISSION\n",
    'author': 'rero',
    'author_email': 'info@rero.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
