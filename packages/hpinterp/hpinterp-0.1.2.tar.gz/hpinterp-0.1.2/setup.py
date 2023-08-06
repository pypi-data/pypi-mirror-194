# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hpinterp']

package_data = \
{'': ['*']}

install_requires = \
['healpy>=1.16.2,<2.0.0',
 'matplotlib>=3.7.0,<4.0.0',
 'numba>=0.56.4,<0.57.0',
 'scipy>=1.10.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'hpinterp',
    'version': '0.1.2',
    'description': '',
    'long_description': '# hpinterp\n\nA faster (~100x) and more accurate interpolation algorithm for HEALPix maps by Prof. Jonathan Sievers. The code\npre-interpolates the map data in advance, saving time at the evaluation stage. \n\n## Installation\n\n```\npip install hpinterp\n```\n\n## Example\n\n```python\nimport numpy as np\nimport healpy as hp\n\nfrom hpinterp import InterpMap\n\nmap_ = hp.read_map("your_map.fits")\n\n# Set nest=True if your map has nested ordering\ninterp_map = InterpMap(map_)\n\n# Generating example coordinate grid of co-latitude and longitude in radians\nnpoints = int(1e5)\ntheta = np.random.rand(npoints) * np.pi\nphi = np.random.rand(2 * npoints) * 2 * np.pi\n\n# Get interpolated values. Set lonlat=True if using longitude and latitude in degrees\ninterp_result = interp_map(theta, phi)\n# or\ninterp_result = interp_map.get_interp_val(theta, phi)\n```',
    'author': 'lap1dem',
    'author_email': 'vadym.bidula@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
