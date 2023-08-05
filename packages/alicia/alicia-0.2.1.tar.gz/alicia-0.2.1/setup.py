# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'dependencies': 'src/dependencies',
 'features': 'src/features',
 'features.comparer': 'src/features/comparer',
 'features.torchvision_downloader': 'src/features/torchvision_downloader',
 'features.trainer': 'src/features/trainer',
 'libs': 'src/libs',
 'models': 'src/modules/models',
 'modules': 'src/modules',
 'modules.models': 'src/modules/models',
 'modules.transforms': 'src/modules/transforms',
 'transforms': 'src/modules/transforms'}

packages = \
['commands',
 'dependencies',
 'features',
 'features.comparer',
 'features.torchvision_downloader',
 'features.trainer',
 'libs',
 'models',
 'modules',
 'modules.models',
 'modules.transforms',
 'transforms']

package_data = \
{'': ['*']}

modules = \
['main']
install_requires = \
['better-abc>=0.0.3,<0.0.4',
 'click>=8.1,<9.0',
 'loading-display>=0.2,<0.3',
 'matplotlib>=3.6,<4.0',
 'numpy>=1.24,<2.0',
 'pillow>=9.4,<10.0',
 'plotext>=5.2,<6.0',
 'scipy>=1.10,<2.0',
 'termcolor>=2.2,<3.0',
 'torch>=1.13,<2.0',
 'torchvision>=0.14,<0.15',
 'wcmatch>=8.4,<9.0']

entry_points = \
{'console_scripts': ['alicia = main:call']}

setup_kwargs = {
    'name': 'alicia',
    'version': '0.2.1',
    'description': 'A CLI to download, create, modify, train, test, predict and compare an image classifiers.',
    'long_description': '\n.. image:: https://github.com/aemonge/alicia/raw/main/docs/DallE-Alicia-logo.jpg\n   :width: 75px\n   :align: left\n\n.. image:: https://img.shields.io/badge/badges-awesome-green.svg\n   :target: https://github.com/Naereen/badges\n\n.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/\n\n.. image:: https://img.shields.io/pypi/v/ansicolortags.svg\n   :target: https://pypi.python.org/pypi/alicia/\n\n.. image:: https://img.shields.io/pypi/dm/ansicolortags.svg\n   :target: https://pypi.python.org/pypi/alicia/\n\n.. image:: https://img.shields.io/pypi/l/ansicolortags.svg\n   :target: https://pypi.python.org/pypi/ansicolortags/\n\n.. image:: https://img.shields.io/badge/say-thanks-ff69b4.svg\n   :target: https://saythanks.io/to/kennethreitz\n\n================================================\n                   AlicIA\n================================================\n::\n\n  Usage: alicia [OPTIONS] COMMAND [ARGS]...\n\n    A CLI to download, create, modify, train, test, predict and compare an image classifiers.\n\n    Supporting mostly all torch-vision neural networks and datasets.\n\n    This will also identify cute 🐱 or a fierce 🐶, also flowers or what type of\n    🏘️ you should be.\n\n  Options:\n    -v, --verbose\n    -g, --gpu\n    --version      Show the version and exit.\n    --help         Show this message and exit.\n\n  Commands:\n    compare   Compare the info, accuracy, and step speed two (or more by...\n    create    Creates a new model for a given architecture.\n    download  Download a MNIST dataset with PyTorch and split it into...\n    info      Display information about a model architecture.\n    modify    Changes the hyper parameters of a model.\n    predict   Predict images using a pre trained model, for a given folder...\n    test      Test a pre trained model.\n    train     Train a given architecture with a data directory containing a...\n\nView a FashionMNIST demo\n-----------------------------------------------\n\n.. image:: https://asciinema.org/a/561138.png\n   :target: https://asciinema.org/a/561138?autoplay=1"\n\nInstall and usage\n================================================\n::\n\n    pip install alicia\n    alicia --help\n\n\nIf you just want to see a quick showcase of the tool, download and run `showcase.sh` https://github.com/aemonge/alicia/raw/main/docs/showcase.sh\n\nFeatures\n-----------------------------------------------\n\nTo see the full list of features, and option please refer to `alicia --help`\n\n* Download common torchvision datasets (tested with the following):\n    - MNIST\n    - FashionMNIST\n    - Flowers102\n    - EMNIST\n    - StanfordCars\n    - KMNIST and CIFAR10\n* Select different transforms to train.\n* Train, test and predict using different custom-made and torch-vision models:\n    - SqueezeNet\n    - AlexNet\n    - MNASNet\n* Get information about each model.\n* Compare models training speed, accuracy, and meta information.\n* View test prediction results in the console, or with matplotlib.\n* Adds the network training history log, to the model. To enhance the info and compare.\n* Supports pre-trained models, with weights settings.\n* Automatically set the input size based on the image resolution.\n\nReferences\n-----------------------------------------------\n\nUseful links found and used while developing this\n\n* https://medium.com/analytics-vidhya/creating-a-custom-dataset-and-dataloader-in-pytorch-76f210a1df5d\n* https://stackoverflow.com/questions/51911749/what-is-the-difference-between-torch-tensor-and-torch-tensor\n* https://deepai.org/dataset/mnist\n* https://medium.com/fenwicks/tutorial-1-mnist-the-hello-world-of-deep-learning-abd252c47709\n',
    'author': 'aemonge',
    'author_email': 'andres@aemonge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/alicia/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
