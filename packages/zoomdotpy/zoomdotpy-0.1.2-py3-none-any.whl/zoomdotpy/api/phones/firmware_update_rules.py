from ..base import _BaseAPI

class FirmwareUpdateRulesAPI(_BaseAPI):
    def get_firmware_update_rules(self , ruleId):
        """
            Use this API to get the [firmware update rule](https://support.zoom.us/hc/en-us/articles/360054198852-Setting-up-firmware-update-rules) information.
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:**`phone:read:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/firmware_update_rules/{ruleId}'
        )

        return res.json()
        
        def delete_firmware_update_rules(self , ruleId):
        """
            Use this API to delete the [firmware update rule](https://support.zoom.us/hc/en-us/articles/360054198852-Setting-up-firmware-update-rules).
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/firmware_update_rules/{ruleId}'
        )

        return res.json()
        
        def update_firmware_update_rules(self , ruleId):
        """
            Use this API to update a specific [firmware update rule](https://support.zoom.us/hc/en-us/articles/360054198852-Setting-up-firmware-update-rules).
			
			**Prerequisites:**
			* Business, or Education account
			* Zoom Phone license 
			
			**Scopes:**`phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/firmware_update_rules/{ruleId}'
        )

        return res.json()
        
        