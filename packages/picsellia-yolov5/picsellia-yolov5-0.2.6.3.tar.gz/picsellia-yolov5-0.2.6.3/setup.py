# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picsellia_yolov5',
 'picsellia_yolov5.yolov5',
 'picsellia_yolov5.yolov5.classify',
 'picsellia_yolov5.yolov5.models',
 'picsellia_yolov5.yolov5.segment',
 'picsellia_yolov5.yolov5.utils',
 'picsellia_yolov5.yolov5.utils.aws',
 'picsellia_yolov5.yolov5.utils.flask_rest_api',
 'picsellia_yolov5.yolov5.utils.loggers',
 'picsellia_yolov5.yolov5.utils.loggers.clearml',
 'picsellia_yolov5.yolov5.utils.loggers.comet',
 'picsellia_yolov5.yolov5.utils.loggers.wandb',
 'picsellia_yolov5.yolov5.utils.segment']

package_data = \
{'': ['*'],
 'picsellia_yolov5.yolov5': ['.github/*',
                             '.github/ISSUE_TEMPLATE/*',
                             '.github/workflows/*',
                             '.idea/*',
                             '.idea/inspectionProfiles/*',
                             'data/*',
                             'data/hyps/*',
                             'data/images/*',
                             'data/scripts/*'],
 'picsellia_yolov5.yolov5.models': ['hub/*', 'segment/*'],
 'picsellia_yolov5.yolov5.utils': ['docker/*', 'google_app_engine/*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'gitpython>=3.1.30,<4.0.0',
 'ipython>=8.10.0,<9.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.1.1,<5.0.0',
 'pandas>=1.1.4,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pycocotools>=2.0.6,<3.0.0',
 'scipy>=1.10.0,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'tensorboard>=2.12.0,<3.0.0',
 'thop>=0.1.1,<0.2.0',
 'torch>=1.8.0,<2.0.0',
 'torchvision>=0.9.0,<0.10.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'picsellia-yolov5',
    'version': '0.2.6.3',
    'description': "'Picsellia wrapper for pytorch implementation of Yolov5'",
    'long_description': 'None',
    'author': 'PN-picsell',
    'author_email': 'pierre-nicolas@picsellia.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
