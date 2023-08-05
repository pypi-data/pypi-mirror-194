# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai_img_gen']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'openai>=0.25.0,<0.26.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'ai-img-gen',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Wrapper for OpenAI DALL-E Image Generator\nWrapper for Image Generation using DALL-E from OpenAI.\n\n## Prerequisites\n1. `Python 3.7+`\n2. `pip`\n3. Account at [OpenAI](https://beta.openai.com/). Make sure you have a Secret Key.\n\n## Install the code.\n1. Install `poetry`\n```\npython3 -m pip install poetry\n```\n2. Download the codebase and open the folder.\n```\ngit clone\ncd ai_img_gen\n```\n3. Install the necessary packages and environment via `poetry`.\n```\npoetry install\n```\n4. Create a `.env` file by copying the sample.env and filling it up the details.\n```\ncp sample.env .env\nnano .env\n```\n\n## Run the code.\n```\npoetry run python run.py\n```\n',
    'author': 'Neriah "BJ" Ato',
    'author_email': 'n.d.ato@ieee.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
