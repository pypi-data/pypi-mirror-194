# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cruddy_framework']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'SQLAlchemy>=1.4.40,<2.0.0',
 'fastapi[all]>=0.92.0,<0.93.0',
 'inflect>=6.0.2,<7.0.0',
 'sqlmodel>=0.0.8,<0.0.9',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'fastapi-cruddy-framework',
    'version': '0.0.2',
    'description': 'A holistic CRUD/MVC framework for FastAPI, with endpoint policies and relationships',
    'long_description': '<a name="readme-top"></a>\n\n<!-- PROJECT LOGO -->\n<div align="center">\n  <h2 align="center">FastAPI - Cruddy Framework</h2>\n  <a href="https://github.com/mdconaway/fastapi-cruddy-framework">\n    <img src="https://raw.githubusercontent.com/mdconaway/fastapi-cruddy-framework/master/logo.png" alt="Logo" width="768" height="406">\n  </a>\n  <br/>\n</div>\n\n<!-- ABOUT THE PROJECT -->\n## About Cruddy Framework\n\n[![Product Name Screen Shot][product-screenshot]](https://github.com/mdconaway/fastapi-cruddy-framework)\n\nCruddy Framework is a companion library to FastAPI designed to bring the development productivity of Ruby on Rails, Ember.js or Sails.js to the FastAPI ecosystem. Many of the design patterns base themselves on Sails.js "policies," sails-ember-rest automatic CRUD routing, and Ember.js REST-Adapter feature sets. By default, data sent to and from the auto-magic CRUD routes are expected to conform to the Ember.js Rest Envelope / Linked-data specification. This specification is highly readable for front-end developers, allows for an expressive over-the-wire query syntax, and embeds self-describing relationship URL links in each over-the-wire record to help data stores automatically generate requests to fetch or update related records. This library is still in an alpha/beta phase, so use at your own risk. All CRUD actions and relationship types are currently supported, though there may be unexpected bugs. Please report any bugs under "issues."\n\n\nTODO: All the documentation. See the examples folder for a quick reference of high level setup.\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n<!-- ABOUT THE PROJECT -->\n## Installation\n\nThe fastapi-cruddy-framework module can be install using poetry...\n\n```\npoetry add fastapi-cruddy-framework\n```\n\nOr pip.\n\n```\npip install fastapi-cruddy-framework\n```\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n<!-- LICENSE -->\n## License\n\nDistributed under the MIT License. See `LICENSE` for more information.\n\n<p align="right">(<a href="#readme-top">back to top</a>)</p>\n\n<!-- MARKDOWN LINKS & IMAGES -->\n[product-screenshot]: https://raw.githubusercontent.com/mdconaway/fastapi-cruddy-framework/master/screenshot.png',
    'author': 'mdconaway',
    'author_email': 'mdconaway@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mdconaway/fastapi-cruddy-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
