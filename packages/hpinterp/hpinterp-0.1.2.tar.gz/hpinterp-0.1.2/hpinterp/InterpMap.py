from typing import Callable, List

import healpy as hp
import numba as nb
import numpy as np
from scipy import interpolate


def lonlat2thetaphi(lon, lat):
    return np.pi / 2.0 - np.radians(lat), np.radians(lon)


@nb.njit(parallel=True)
def par_interp(m: np.ndarray, x: np.ndarray, y: np.ndarray, dx: float, dy: float):
    npix = len(x)
    out = np.empty(npix, dtype=np.float64)
    for i in nb.prange(npix):
        while x[i] >= np.pi:
            x[i] -= np.pi
        while y[i] >= 2 * np.pi:
            x[i] -= np.pi
        ix = int(x[i] / dx)
        iy = int(y[i] / dy)
        if ix == m.shape[0]:
            ix = 0
        if iy == m.shape[1]:
            iy = 0
        fx = x[i] / dx - ix
        fy = y[i] / dy - iy
        out[i] = (m[ix, iy] * (1 - fx) * (1 - fy) + m[ix, iy + 1] * (1 - fx) * fy +
                  m[ix + 1, iy] * fx * (1 - fy) + m[ix + 1, iy + 1] * fx * fy)
    return out


class InterpMap:
    """
        A faster (~100x) and more accurate interpolation algorithm for HEALPix maps by Prof. Jonathan Sievers. The code
        pre-interpolates the map data in advance, saving time on the evaluation stage.

        :param m: HEALPix map.
        :param nest: Nested (True) or ring (False) map structure.
        """

    def __init__(self, m: np.ndarray, nest: bool = False):
        self.m = m if not nest else hp.reorder(m, n2r=True)
        self._preinterpolate()

    def _preinterpolate(self):
        npix = self.m.size
        nside = hp.npix2nside(npix)
        th, phi = hp.pix2ang(nside, np.arange(npix))
        edges = np.where(np.diff(th) > 0)[0] + 1
        edges = np.hstack([0, edges, npix])
        ndec = len(edges) - 1

        if not ndec == 4 * nside - 1:
            raise RuntimeError("Incorrect map size")

        splines: List[Callable] = []

        # Number of points used for interpolation
        nth = 4 * nside - 1
        nphi = 2 * nth
        self.interp_map = np.empty([nth, nphi + 1])

        # Interpolating existing rings at theta positions for custom number of phi
        phi_pos, self.d_phi = np.linspace(0, 2 * np.pi, nphi, retstep=True)
        map_tmp = np.empty([ndec, nphi])

        for i in range(ndec):
            ax_len = edges[i + 1] - edges[i] + 1
            phi_xvec = np.empty(ax_len)
            phi_xvec[:-1] = phi[edges[i]:edges[i + 1]]
            phi_xvec[-1] = phi_xvec[-2] + (phi_xvec[1] - phi_xvec[0])

            phi_yvec = np.empty(ax_len)
            phi_yvec[:-1] = self.m[edges[i]:edges[i + 1]]
            phi_yvec[-1] = phi_yvec[0]

            splines.append(interpolate.CubicSpline(phi_xvec, phi_yvec, bc_type='periodic'))
            pp_tmp = phi_pos.copy()
            pp_tmp[pp_tmp < phi_xvec[0]] = pp_tmp[pp_tmp < phi_xvec[0]] + 2 * np.pi
            map_tmp[i, :] = splines[i](pp_tmp)

        # Interpolating at phi positions for custom number of theta
        th_yvec = np.empty(len(edges) + 1)
        th_yvec[0] = np.mean(self.m[:4])
        th_yvec[-1] = np.mean(self.m[-4:])
        th_xvec = np.hstack([0, th[edges[:-1]], np.pi])
        th_pos, self.d_th = np.linspace(0, np.pi, nth, retstep=True)

        for i in range(nphi):
            th_yvec[1:-1] = map_tmp[:, i]
            tmp_spline = interpolate.CubicSpline(th_xvec, th_yvec)
            self.interp_map[:, i] = tmp_spline(th_pos)

        self.interp_map[:, -1] = self.interp_map[:, 0]  # Set up periodic conditions

    def get_interp_val(self, theta: np.ndarray, phi: np.ndarray, lonlat: bool = False):
        """
        :param theta: Co-latitude [rad] / latitude [deg]
        :param phi: Longitude [rad] / longitude [deg]
        :param lonlat: If True, input angles are assumed to be longitude and latitude in degree,
                       otherwise, they are co-latitude and longitude in radians.
        :return: Interpolated values at requested coordinates.
        """
        if not theta.shape == phi.shape:
            raise ValueError("Theta and phi must have the same dimension and shape")

        if lonlat:
            theta, phi = lonlat2thetaphi(theta, phi)

        if theta.ndim == 1:
            return par_interp(self.interp_map, theta, phi, self.d_th, self.d_phi)
        else:
            out = np.empty(theta.shape)
            out.ravel()[:] = par_interp(self.interp_map, theta.ravel(), phi.ravel(), self.d_th, self.d_phi)
            return out

    def __call__(self, theta: np.ndarray, phi: np.ndarray, lonlat: bool = False):
        """
        :param theta: Co-latitude [rad] / latitude [deg]
        :param phi: Longitude [rad] / longitude [deg]
        :param lonlat: If True, input angles are assumed to be longitude and latitude in degree,
                       otherwise, they are co-latitude and longitude in radians.
        :return: Interpolated values at requested coordinates.
        """
        return self.get_interp_val(theta, phi, lonlat)
