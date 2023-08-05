# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_imaginary',
 'classy_imaginary.enhancers',
 'classy_imaginary.enhancers.phraselists',
 'classy_imaginary.img_processors',
 'classy_imaginary.modules',
 'classy_imaginary.modules.diffusion',
 'classy_imaginary.modules.midas',
 'classy_imaginary.modules.midas.midas',
 'classy_imaginary.samplers',
 'classy_imaginary.training_tools',
 'classy_imaginary.vendored',
 'classy_imaginary.vendored.basicsr',
 'classy_imaginary.vendored.blip',
 'classy_imaginary.vendored.clip',
 'classy_imaginary.vendored.clipseg',
 'classy_imaginary.vendored.codeformer',
 'classy_imaginary.vendored.k_diffusion',
 'classy_imaginary.vendored.k_diffusion.models']

package_data = \
{'': ['*'],
 'classy_imaginary': ['configs/*', 'data/*'],
 'classy_imaginary.vendored': ['noodle_soup_prompts/*'],
 'classy_imaginary.vendored.blip': ['configs/*']}

install_requires = \
['Pillow>=8.0.0',
 'click-help-colors',
 'click-shell>=2.1',
 'click>=8.0.4',
 'diffusers',
 'einops>=0.3.0',
 'facexlib',
 'fairscale>=0.4.4',
 'ftfy',
 'imageio==2.9.0',
 'kornia>=0.6',
 'numpy',
 'omegaconf>=2.1.1',
 'open-clip-torch',
 'opencv-python',
 'protobuf!=3.20.2,!=3.19.5',
 'psutil',
 'pytorch-lightning>=1.4.2',
 'requests',
 'safetensors',
 'timm>=0.4.12',
 'torch>=1.13.1',
 'torchdiffeq',
 'torchmetrics>=0.6.0',
 'torchvision>=0.13.1',
 'tqdm',
 'transformers>=4.19.2',
 'triton>=2.0.0.dev20221120',
 'xformers>=0.0.16']

setup_kwargs = {
    'name': 'classy-imaginary',
    'version': '0.4.5',
    'description': 'This is not a useful package. It is a wrapper around imaginary to provide a Class interface.',
    'long_description': 'This is not a useful package. It is a wrapper around imaginary to provide a Class interface.\n',
    'author': 'Hanoush',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
