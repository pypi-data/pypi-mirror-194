# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vocode', 'vocode.input_device', 'vocode.models', 'vocode.output_device']

package_data = \
{'': ['*']}

install_requires = \
['pyaudio==0.2.13',
 'pydantic==1.10.5',
 'python-dotenv==0.21.1',
 'typing-extensions==4.5.0',
 'websockets==10.4']

setup_kwargs = {
    'name': 'vocode',
    'version': '0.1.6',
    'description': 'The all-in-one voice SDK',
    'long_description': '# vocode-python-sdk\n\n```bash\n# set up environment\npython3 -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt\n\n# start talking to an AI\npython simple_conversation.py\n```\n',
    'author': 'Ajay Raj',
    'author_email': 'ajay@vocode.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
