from ..base import _BaseAPI

class SettingsAPI(_BaseAPI):
    def get_settings(self ):
        """
            Use this API to return an account's settings.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:**
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/settings'
        )

        return res.json()
        
        def update_settings(self , accountId):
        """
            Account owners can use this API to update Zoom Phone [account settings](https://support.zoom.us/hc/en-us/articles/360025846692).
			
			**Scopes:** `phone:write:admin`
			
			**Prerequisites:** 
			* A Business or Enterprise account
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/settings'
        )

        return res.json()
        
        