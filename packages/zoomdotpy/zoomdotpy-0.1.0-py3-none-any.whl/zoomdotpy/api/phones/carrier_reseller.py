from ..base import _BaseAPI

class CarrierResellerAPI(_BaseAPI):
    def delete_carrier_reseller(self , number):
        """
            Use this API to delete or unassign a phone number from a carrier reseller account.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/carrier_reseller/numbers/{number}'
        )

        return res.json()
        
        