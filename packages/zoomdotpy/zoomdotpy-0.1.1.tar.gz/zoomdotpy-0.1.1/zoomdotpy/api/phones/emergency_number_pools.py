from ..base import _BaseAPI

class EmergencyNumberPoolsAPI(_BaseAPI):
    def delete_emergency_number_pools(self , phoneNumberId):
        """
            Use this API to unassign phone numbers from the [Emergency Number Pool](https://support.zoom.us/hc/en-us/articles/360062110192-Routing-emergency-calls).
			
			**Scopes:** `phone:write`, `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/emergency_number_pools/phone_numbers/{phoneNumberId}'
        )

        return res.json()
        
        