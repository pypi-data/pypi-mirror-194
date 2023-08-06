from ..base import _BaseAPI

class CarrierPeeringAPI(_BaseAPI):
    def get_carrier_peering(self , ):
        """
            Returns phone numbers pushed by the carrier to different customers.
			To become a peering provider/ carrier, submit your [request](https://docs.google.com/forms/d/e/1FAIpQLSewkY6ixVyKVNkWC-vgmejC16gigxsJWXji3dWzE3XlWtjsgg/viewform).
			
			**Scopes:** `phone_peering:read:admin`, `phone_peering:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/carrier_peering/numbers'
        )

        return res.json()
        
        