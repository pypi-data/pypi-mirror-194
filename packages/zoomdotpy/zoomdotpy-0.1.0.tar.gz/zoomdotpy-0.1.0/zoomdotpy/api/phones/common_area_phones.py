from ..base import _BaseAPI

class CommonAreaPhonesAPI(_BaseAPI):
    def delete_common_area_phones(self , commonAreaPhoneId, phoneNumberId):
        """
            Use this API to unassign a phone number from a common Area phone.
			
			**Prerequisites:**
			
			* A Pro or a higher account with a Zoom Phone license
			* An account owner or admin permissions
			
			**Scopes:** `phone:write:admin`
			
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/common_area_phones/{commonAreaPhoneId}/phone_numbers/{phoneNumberId}'
        )

        return res.json()
        
        