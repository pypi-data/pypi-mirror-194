# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigc', 'bigc.data', 'bigc.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'bigc',
    'version': '0.2.4',
    'description': 'Unofficial client for the BigCommerce API',
    'long_description': "# bigc\n\nAn unofficial Python client for the BigCommerce API.\n\n_This project is currently in an alpha state._\n\n## Installation\n\n```shell\npip install bigc \n```\n\n## Usage\n\nTo authenticate, you'll need the BigCommerce store's hash and an access token.\n\n```python\nfrom bigc import BigCommerceAPI\n\n\nstore_hash = '000000000'\naccess_token = '0000000000000000000000000000000'\nbigcommerce = BigCommerceAPI(store_hash, access_token)\n\norder: dict = bigcommerce.orders.get(101)\norders: list[dict] = list(bigcommerce.orders.all(customer_id=1))\n```\n\nThe following resources are currently supported:\n\n- `carts`\n- `categories`\n- `checkouts`\n- `customer_groups`\n- `customers`\n- `orders`\n- `products`\n- `product_variants`\n- `webhooks`\n\n### Direct API Access\n\nFor resources or parameters that aren't officially supported yet, bigc also includes a flexible API client that can be used to make direct requests to the BigCommerce API.\n\n```python\nbigcommerce = BigCommerceAPI(store_hash, access_token)\n\nproduct = bigcommerce.api.v3.get('/products/77', params={'include': 'videos'})\norder_messages = bigcommerce.api.v2.get_many('/orders/101/messages')\n```\n\n### Utilities\n\nSome extra utility functions that don't interact with the BigCommerce API are available in `bigc.utils`.\n\n- `bigc.utils.parse_rfc2822_date`: Convert an [RFC-2822 date] (used by some BigCommerce APIs) to a `datetime`\n\n[RFC-2822 date]: https://www.rfc-editor.org/rfc/rfc2822#section-3.3\n\n### Constants\n\nFor convenience, some constants are made available in `bigc.data`.\n\n- `bigc.data.BigCommerceOrderStatus`: An `Enum` of order statuses and their IDs\n",
    'author': 'Ryan Thomson',
    'author_email': 'ryan@medshift.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MedShift/bigc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
