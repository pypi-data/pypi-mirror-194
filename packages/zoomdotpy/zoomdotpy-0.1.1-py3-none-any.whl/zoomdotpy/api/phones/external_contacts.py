from ..base import _BaseAPI

class ExternalContactsAPI(_BaseAPI):
    def delete_external_contacts(self , externalContactId):
        """
            Removes an external contact.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/external_contacts/{externalContactId}'
        )

        return res.json()
        
        def get_external_contacts(self , externalContactId):
        """
            Gets an external contact's information.
			
			**Scopes:** `phone:read:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions<br>
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/external_contacts/{externalContactId}'
        )

        return res.json()
        
        def update_external_contacts(self , externalContactId):
        """
            Updates an external contact's information.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/external_contacts/{externalContactId}'
        )

        return res.json()
        
        