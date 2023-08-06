from ..base import _BaseAPI

class ProvisionTemplatesAPI(_BaseAPI):
    def get_provision_templates(self , templateId):
        """
            Use this API to get a specific [provision template](https://support.zoom.us/hc/en-us/articles/360035817952).
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom Phone license
			
			**Scopes:** `phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/provision_templates/{templateId}'
        )

        return res.json()
        
        def update_provision_templates(self , templateId):
        """
            Use this API to update a [provision template](https://support.zoom.us/hc/en-us/articles/360035817952#h_7b34cd1d-5ae6-4a23-bd04-454a6ad8cb3e) in a Zoom account.
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/provision_templates/{templateId}'
        )

        return res.json()
        
        def delete_provision_templates(self , templateId):
        """
            Use this API to [delete a provision template](https://support.zoom.us/hc/en-us/articles/360035817952#h_7b34cd1d-5ae6-4a23-bd04-454a6ad8cb3e) in a Zoom account.
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/provision_templates/{templateId}'
        )

        return res.json()
        
        