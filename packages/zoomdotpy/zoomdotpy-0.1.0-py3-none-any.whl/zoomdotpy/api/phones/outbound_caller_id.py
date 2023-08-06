from ..base import _BaseAPI

class OutboundCallerIdAPI(_BaseAPI):
    def get_outbound_caller_id(self , ):
        """
            Use this API to retrieve phone numbers that can be used as the `account-level` customized outbound caller ID. Note that when multiple sites policy is enabled, users cannot manage the `account-level` configuration. The system will throw an exception. 
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license.
			
			**Scope:** `phone:read:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/outbound_caller_id/customized_numbers'
        )

        return res.json()
        
        def create_outbound_caller_id(self ):
        """
            Use this API to add the `account-level` customized outbound caller ID phone numbers. Note that when multiple sites policy is enabled, users cannot manage the `account-level` configuration. The system will throw an exception.
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license.
			
			**Scope:** `phone:write:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/outbound_caller_id/customized_numbers'
        )

        return res.json()
        
        def delete_outbound_caller_id(self , ):
        """
            Use this API to delete the `account-level` customized outbound caller ID phone numbers. Note that when multiple sites policy is enabled, users cannot manage the `account-level` configuration. The system will throw an exception.
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license.
			
			**Scope:** `phone:write:admin`
			 
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/outbound_caller_id/customized_numbers'
        )

        return res.json()
        
        