from ..base import _BaseAPI

class SharedLineGroupsAPI(_BaseAPI):
    def create_shared_line_groups(self , sharedLineGroupId, policyType):
        """
            Use this API to add the policy sub-setting for a specific [shared line group](https://support.zoom.us/hc/en-us/articles/360038850792) according to the `policyType`. For example, you can use this API to set up shared access members. 
			
			**Prerequisites:** 
			* Pro or higher account with Zoom Phone license.
			* Account owner or admin privileges 
			
			**Scopes:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/shared_line_groups/{sharedLineGroupId}/policy/{policyType}'
        )

        return res.json()
        
        def update_shared_line_groups(self , sharedLineGroupId, policyType):
        """
            Use this API to update the policy sub-setting for a specific [shared line group](https://support.zoom.us/hc/en-us/articles/360038850792) according to the `policyType`. For example, you can use this API to update shared access members. 
			
			**Prerequisites:** 
			* Pro or higher account with Zoom Phone license.
			* Account owner or admin privileges 
			
			**Scopes:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/shared_line_groups/{sharedLineGroupId}/policy/{policyType}'
        )

        return res.json()
        
        def delete_shared_line_groups(self , sharedLineGroupId, policyType):
        """
            Use this API to remove the policy sub-setting for a specific [shared line group](https://support.zoom.us/hc/en-us/articles/360038850792) according to the `policyType`. For example, you can use this API to remove shared access members. 
			
			**Prerequisites:** 
			* Pro or higher account with Zoom Phone license.
			* Account owner or admin privileges 
			
			**Scopes:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/shared_line_groups/{sharedLineGroupId}/policy/{policyType}'
        )

        return res.json()
        
        