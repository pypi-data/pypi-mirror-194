# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eskiz_sms']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'eskiz-sms',
    'version': '0.2.2',
    'description': 'Package for eskiz.uz/sms',
    'long_description': '# eskiz-sms\n\neskiz-sms package for eskiz.uz/sms \n\n[![Downloads](https://pepy.tech/badge/eskiz-sms)](https://pepy.tech/project/eskiz-sms)\n[![Downloads](https://pepy.tech/badge/eskiz-sms/month)](https://pepy.tech/project/eskiz-sms)\n[![Downloads](https://pepy.tech/badge/eskiz-sms/week)](https://pepy.tech/project/eskiz-sms)\n\n> :warning: **Please use the latest version. In previous versions, there are a lot of mistakes, bugs**\n\n# Installation\n\n```\npip install eskiz_sms\n```\n\n# Quickstart\n\n```python\nfrom eskiz_sms import EskizSMS\n\nemail = "your_email@mail.com"\npassword = "your_password"\neskiz = EskizSMS(email=email, password=password)\neskiz.send_sms(\'998991234567\', \'message\', from_whom=\'4546\', callback_url=None)\n```\n\n### Using pre-saved token\n\n```python\nfrom eskiz_sms import EskizSMS\n\nyour_saved_token = \'eySomething9320\'\neskiz = EskizSMS(\'email\', \'password\')\neskiz.token.set(your_saved_token)\n\neskiz.send_sms(\'998901234567\', message=\'message\')\n```\n\n### Saving token to env file\n\nIf you set `save_token=True` it will save the token to env file\n\n```python\nfrom eskiz_sms import EskizSMS\n\neskiz = EskizSMS(\'email\', \'password\', save_token=True, env_file_path=\'.env\')\n# Don\'t forget to add env file to .gitignore!\nresponse = eskiz.send_sms(\'998901234567\', message=\'message\')\n```\n### Async usage\n\n```python\nimport asyncio\n\nfrom eskiz_sms.async_ import EskizSMS\n\n\nasync def main():\n    eskiz = EskizSMS(\'email\', \'password\')\n    response = await eskiz.send_sms(\'998901234567\', \'Hello, World!\')\n\n\nasyncio.run(main())\n```',
    'author': 'Malikov',
    'author_email': 'mlkv.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/malikovss/eskiz-sms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
