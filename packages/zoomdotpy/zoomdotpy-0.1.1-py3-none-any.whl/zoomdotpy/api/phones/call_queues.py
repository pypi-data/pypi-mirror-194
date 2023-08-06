from ..base import _BaseAPI

class CallQueuesAPI(_BaseAPI):
    def create_call_queues(self , callQueueId, policyType):
        """
            Use this API to add the policy sub-setting for a specific [call queue](https://support.zoom.us/hc/en-us/articles/360021524831) according to the `policyType`. For example, you can use this API to set up shared access members. 
			
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
            f'/phone/call_queues/{callQueueId}/policies/{policyType}'
        )

        return res.json()
        
        def update_call_queues(self , callQueueId, policyType):
        """
            Use this API to update the policy sub-setting for a specific [call queue](https://support.zoom.us/hc/en-us/articles/360021524831) according to the `policyType`. For example, you can use this API to update shared access members.
			
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
            f'/phone/call_queues/{callQueueId}/policies/{policyType}'
        )

        return res.json()
        
        def delete_call_queues(self , callQueueId, policyType):
        """
            Use this API to remove the policy sub-setting for a specific [call queue](https://support.zoom.us/hc/en-us/articles/360021524831) according to the `policyType`. For example, you can use this API to remove shared access members. 
			
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
            f'/phone/call_queues/{callQueueId}/policies/{policyType}'
        )

        return res.json()
        
        