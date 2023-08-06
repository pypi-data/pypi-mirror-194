from ..base import _BaseAPI

class EmergencyAddressesAPI(_BaseAPI):
    def delete_emergency_addresses(self , emergencyAddressId):
        """
            Removes an emergency address.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Heavy`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/emergency_addresses/{emergencyAddressId}'
        )

        return res.json()
        
        def get_emergency_addresses(self , emergencyAddressId):
        """
            Gets the emergency address information.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions<br>
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/emergency_addresses/{emergencyAddressId}'
        )

        return res.json()
        
        def update_emergency_addresses(self , emergencyAddressId):
        """
            Updates an emergency address information. If the address provided is not an exact match, the system generated corrected address will be used. 
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/emergency_addresses/{emergencyAddressId}'
        )

        return res.json()
        
        