from ..base import _BaseAPI

class GroupCallPickupAPI(_BaseAPI):
    def delete_group_call_pickup(self , groupId, extensionId):
        """
            Use this API to remove member from the [Group Call Pickup](https://support.zoom.us/hc/en-us/articles/360060107472-Setting-up-and-using-group-call-pickup) object. 
			
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
            f'/phone/group_call_pickup/{groupId}/members/{extensionId}'
        )

        return res.json()
        
        