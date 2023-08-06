from .sites import SitesAPI
from .devices import DevicesAPI

from zoomdotpy.api.base import _BaseAPI

class PhonesAPI(_BaseAPI):
    devices: DevicesAPI
    sites: SitesAPI

    def __post_init__(self):
        self.devices    = DevicesAPI(self._s)
        self.sites      = SitesAPI(self._s)