# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buffalo',
 'buffalo.algo',
 'buffalo.data',
 'buffalo.evaluate',
 'buffalo.misc',
 'buffalo.parallel']

package_data = \
{'': ['*'], 'buffalo.algo': ['cuda/*']}

install_requires = \
['absl-py>=1.3.0,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'h5py>=3.7.0,<4.0.0',
 'numpy>=1.21.6,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'scipy>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['Buffalo = buffalo.cli:_cli_buffalo']}

setup_kwargs = {
    'name': 'buffalo',
    'version': '2.0.1',
    'description': 'TOROS Buffalo: A fast and scalable production-ready open source project for recommender systems',
    'long_description': '[![Linux/Mac Build Status](https://travis-ci.org/kakao/buffalo.svg?branch=master)](https://travis-ci.org/kakao/buffalo)\n\n<center><img src="./docs/buffalo.png" width="320px"></center>\n\n\n# Buffalo\nBuffalo is a fast and scalable production-ready open source project for recommender systems. Buffalo effectively utilizes system resources, enabling high performance even on low-spec machines. The implementation is optimized for CPU and SSD. Even so, it shows good performance with GPU accelerator, too. Buffalo, developed by Kakao, has been reliably used in production for various Kakao services.\n\nFor more information see the [documentation](https://buffalo-recsys.readthedocs.io)\n\n## Requirements\n- Python 3.8+\n- cmake 3.17+\n- gcc/g++ (with std=c++14)\n\n\n## License\n\nThis software is licensed under the [Apache 2 license](LICENSE), quoted below.\n\nCopyright 2020 Kakao Corp. <http://www.kakaocorp.com>\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not\nuse this project except in compliance with the License. You may obtain a copy\nof the License at http://www.apache.org/licenses/LICENSE-2.0.\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS, WITHOUT\nWARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the\nLicense for the specific language governing permissions and limitations under\nthe License.\n',
    'author': 'recoteam',
    'author_email': 'recoteam@kakaocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
