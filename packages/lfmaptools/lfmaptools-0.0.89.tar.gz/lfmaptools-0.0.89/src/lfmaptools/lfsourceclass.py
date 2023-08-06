from typing import Optional

import numpy as np


class LFSource(object):
    def __init__(
        self,
        *,
        x: Optional[float] = None,
        y: Optional[float] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius: float,
        time: np.ndarray,
        flux: np.ndarray,
        conc: np.ndarray,
    ):
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.time = time
        self.flux = flux
        self.conc = conc

    def volume(self) -> np.float64:
        return np.trapz(self.flux, self.time)

    def peak_flux(self) -> np.float64:
        return np.amax(self.flux)

    def peak_time(self) -> np.float64:
        i = np.argmax(self.flux)
        return self.time[i]

    def duration(self) -> np.float64:
        return self.time[-1] - self.time[0]
