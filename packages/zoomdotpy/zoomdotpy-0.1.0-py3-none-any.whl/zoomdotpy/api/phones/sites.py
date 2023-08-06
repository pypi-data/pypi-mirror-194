from dataclasses import dataclass
from zoomdotpy.api.base import _BaseAPI

@dataclass
class SiteEmergencyAddress():
    address_line1   : str
    city            : str
    country         : str
    state_code      : str
    zip             : str

    address_line2   : str = ""

@dataclass
class SiteShortExtension():
    length: int


class SitesAPI(_BaseAPI):
    def list_sites(self, params: dict = {}) -> dict:
        res = self.request('GET', 'phone/sites', params)

        return res.json()

    def get_site(self, site_id: str, params: dict = {}) -> dict:
        res = self.request('GET', f'phone/sites/{site_id}', params)

        return res.json()

    def create_site(
        self, 
        auto_receptionist_name: str,
        default_emergency_address: SiteEmergencyAddress,
        name: str,
        site_code: int = None,
        short_extension: SiteShortExtension = None
    ) -> dict:
        body = {
            'name': name,
            'auto_receptionist_name': auto_receptionist_name,
            'default_emergency_address': default_emergency_address.__dict__
        }

        if site_code: body['site_code'] = site_code
        if short_extension: body['short_extension'] = short_extension.__dict__

        res = self.request('POST', f'phone/sites', json=body)

        return res.json()

    def update_site(
        self,
        site_id: str,
        site_details: dict
    ) -> dict:
        res = self.request('PATCH', f'phone/sites/{site_id}', json=site_details)

        return res.json()

    def delete_site(
        self, 
        site_id: str,
        transfer_site_id: str
    ) -> dict:
        res = self.request(
            'DELETE',
            f'phone/sites/{site_id}',
            params={
                'transfer_site_id': transfer_site_id
            }
        )

        return res.json()
