# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xitorch',
 'xitorch._core',
 'xitorch._docstr',
 'xitorch._impls',
 'xitorch._impls.integrate',
 'xitorch._impls.integrate.ivp',
 'xitorch._impls.integrate.mcsamples',
 'xitorch._impls.interpolate',
 'xitorch._impls.linalg',
 'xitorch._impls.optimize',
 'xitorch._impls.optimize.root',
 'xitorch._tests',
 'xitorch._utils',
 'xitorch.debug',
 'xitorch.grad',
 'xitorch.integrate',
 'xitorch.interpolate',
 'xitorch.linalg',
 'xitorch.optimize']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1', 'scipy>=1.10.0', 'torch>=1.13.1']

setup_kwargs = {
    'name': 'xitorch',
    'version': '0.5.1',
    'description': 'Differentiable scientific computing library',
    'long_description': '# `xitorch`: differentiable scientific computing library\n\n![Build](https://img.shields.io/github/workflow/status/xitorch/xitorch/CI)\n[![Docs](https://img.shields.io/readthedocs/xitorch)](https://xitorch.readthedocs.io/)\n[![Code coverage](https://img.shields.io/codecov/c/github/xitorch/xitorch)](https://codecov.io/gh/xitorch/xitorch)\n\n`xitorch` is a PyTorch-based library of differentiable functions and functionals that\ncan be widely used in scientific computing applications as well as deep learning.\n\nThe documentation can be found at: https://xitorch.readthedocs.io/\n\n## Example\n\nFinding root of a function:\n\n```python\nimport torch\nfrom xitorch.optimize import rootfinder\n\ndef func1(y, A):  # example function\n    return torch.tanh(A @ y + 0.1) + y / 2.0\n\n# set up the parameters and the initial guess\nA = torch.tensor([[1.1, 0.4], [0.3, 0.8]]).requires_grad_()\ny0 = torch.zeros((2, 1))  # zeros as the initial guess\n\n# finding a root\nyroot = rootfinder(func1, y0, params=(A,))\n\n# calculate the derivatives\ndydA, = torch.autograd.grad(yroot.sum(), (A,), create_graph=True)\ngrad2A, = torch.autograd.grad(dydA.sum(), (A,), create_graph=True)\n```\n\n## Modules\n\n* [`linalg`](xitorch/linalg/): Linear algebra and sparse linear algebra module\n* [`optimize`](xitorch/optimize/): Optimization and root finder module\n* [`integrate`](xitorch/integrate/): Quadrature and integration module\n* [`interpolate`](xitorch/interpolate/): Interpolation\n\n## Requirements\n\n* python >=3.8.1,<3.12\n* pytorch 1.13.1 or higher (install [here](https://pytorch.org/))\n\n## Getting started\n\nAfter fulfilling all the requirements, type the commands below to install `xitorch`\n\n    python -m pip install xitorch\n\nOr to install from GitHub:\n\n    python -m pip install git+https://github.com/xitorch/xitorch.git\n\nFinally, if you want to make an editable install from source:\n\n    git clone https://github.com/xitorch/xitorch.git\n    cd xitorch\n    python -m pip install -e .\n\nNote that the last option is only available per [PEP 660](https://peps.python.org/pep-0660/), so you will require [pip >= 23.1](https://pip.pypa.io/en/stable/news/#v21-3)\n    \n## Used in\n\n* Differentiable Quantum Chemistry (DQC): https://dqc.readthedocs.io/\n\n## Gallery\n\nNeural mirror design ([example 01](examples/01-mirror-design/)):\n\n![neural mirror design](examples/01-mirror-design/images/mirror.gif)\n\nInitial velocity optimization in molecular dynamics ([example 02](examples/02-molecular-dynamics/)):\n\n![molecular dynamics](examples/02-molecular-dynamics/images/md.gif)\n',
    'author': 'mfkasim1',
    'author_email': 'firman.kasim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://xitorch.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
