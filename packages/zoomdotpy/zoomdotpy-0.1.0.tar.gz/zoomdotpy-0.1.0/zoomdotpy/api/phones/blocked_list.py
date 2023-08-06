from ..base import _BaseAPI

class BlockedListAPI(_BaseAPI):
    def delete_blocked_list(self , blockedListId):
        """
            A Zoom account owner or a user with admin privilege can block phone numbers for phone users in an account. Blocked numbers can be inbound (numbers will be blocked from calling in) and outbound (phone users in your account won't be able to dial those numbers).
			
			Use this API to delete a blocked list and therefore removing the associated number from the blocked list. The number will be unblocked after the deletion.
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			
			**Scope:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/blocked_list/{blockedListId}'
        )

        return res.json()
        
        def get_blocked_list(self , blockedListId):
        """
            A Zoom account owner or a user with admin privilege can block phone numbers for phone users in an account. Blocked numbers can be inbound (numbers will be blocked from calling in) and outbound (phone users in your account won't be able to dial those numbers). Blocked callers will hear a generic message stating that the person they are calling is not available.
			Use this API to get information about a specific blocked list.
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			
			**Scope:** `phone:read:admin`
			 
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/blocked_list/{blockedListId}'
        )

        return res.json()
        
        def update_blocked_list(self , blockedListId):
        """
            A Zoom account owner or a user with admin privilege can block phone numbers for phone users in an account. Blocked numbers can be inbound (numbers will be blocked from calling in) and outbound (phone users in your account won't be able to dial those numbers). Blocked callers will hear a generic message stating that the person they are calling is not available.
			Use this API to update the information on the blocked list.
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			
			**Scope:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/blocked_list/{blockedListId}'
        )

        return res.json()
        
        