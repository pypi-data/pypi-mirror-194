# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ailab', 'ailab.hub.huggingface.transformers.text_classification.wrapper']

package_data = \
{'': ['*'],
 'ailab': ['hub/huggingface/transformers/text_classification/*'],
 'ailab.hub.huggingface.transformers.text_classification.wrapper': ['test_data/*']}

setup_kwargs = {
    'name': 'ifly-ailab',
    'version': '0.1.0',
    'description': 'a iflytek ailab library ...',
    'long_description': None,
    'author': 'ybyang',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.7',
}


setup(**setup_kwargs)
