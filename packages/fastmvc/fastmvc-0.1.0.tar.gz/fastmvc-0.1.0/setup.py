# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastmvc',
 'fastmvc.extras',
 'fastmvc.models',
 'fastmvc.models.database',
 'fastmvc.templates.core',
 'fastmvc.templates.core.static_pages',
 'fastmvc.templates.scaffold',
 'fastmvc.templates.users']

package_data = \
{'': ['*'],
 'fastmvc': ['templates/core/ignore/*',
             'templates/core/static_pages/static/css/*',
             'templates/core/static_pages/static/img/*',
             'templates/core/static_pages/static/js/*',
             'templates/core/static_pages/templates/*',
             'templates/scaffold/templates/*',
             'templates/scaffold_helpers/*',
             'templates/users/templates/*']}

install_requires = \
['Jinja2',
 'authlib',
 'fastapi',
 'httpx',
 'itsdangerous',
 'passlib[bcrypt]',
 'pyjwt',
 'python-dotenv',
 'python-multipart',
 'typer[all]']

entry_points = \
{'console_scripts': ['fastmvc = fastmvc.main:app']}

setup_kwargs = {
    'name': 'fastmvc',
    'version': '0.1.0',
    'description': 'Rapid application development built for the cloud.',
    'long_description': '# FastMVC\nFastMVC is a modern, fast (high-performance), web framework for building Web Applications\nwith the MVC structure (Model - View - Controller) and effortlessly deploying them to cloud platforms. \n\n- Model is interchangeable depending on the cloud platform you would like to use.\n- View uses Jinja2 to create front end pages\n- Controller is written using FastAPI\n\n\n## FastMVC CLI\n`fastmvc new [PROJECT_NAME]`  \nCreates a new project. Will ask which platform to build towards (GOOGLE_APP_ENGINE, or DETA) and set up the base of the project accordingly.  \n\n`fastmvc scaffold [MODEL_NAME] [ATTRIBUTE]:[DATA_TYPE]`  \nScaffold out a Model, View, and Controller for your object. For example:  \n\nfastmvc scaffold item title:str description:wysiwyg amount:int available:bool  \n\n`fastmvc auth`  \nBuilds an Authentication Framework to easily integrate user sign in for your application.  \n\n`fastmvc s`  \nAlias for `uvicorn main:app --reload` to run your application locally  \n\n## Supported Cloud Platforms\n__Built__\n- Google App Engine (using Firestore database)\n- Deta (using DetaBase)\n\n__Coming Soon__\n- AWS Elastic Beanstalk\n\n\n',
    'author': 'MBeebe',
    'author_email': 'pyn-sol@beebe.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
