# hpinterp

A faster (~100x) and more accurate interpolation algorithm for HEALPix maps by Prof. Jonathan Sievers. The code
pre-interpolates the map data in advance, saving time at the evaluation stage. 

## Installation

```
pip install hpinterp
```

## Example

```python
import numpy as np
import healpy as hp

from hpinterp import InterpMap

map_ = hp.read_map("your_map.fits")

# Set nest=True if your map has nested ordering
interp_map = InterpMap(map_)

# Generating example coordinate grid of co-latitude and longitude in radians
npoints = int(1e5)
theta = np.random.rand(npoints) * np.pi
phi = np.random.rand(2 * npoints) * 2 * np.pi

# Get interpolated values. Set lonlat=True if using longitude and latitude in degrees
interp_result = interp_map(theta, phi)
# or
interp_result = interp_map.get_interp_val(theta, phi)
```