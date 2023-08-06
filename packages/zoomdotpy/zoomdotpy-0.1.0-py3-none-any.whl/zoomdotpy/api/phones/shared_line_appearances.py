from ..base import _BaseAPI

class SharedLineAppearancesAPI(_BaseAPI):
    def get_shared_line_appearances(self , ):
        """
            Use this API to list [shared line appearance](https://support.zoom.us/hc/en-us/articles/4406753208461-Enabling-or-disabling-shared-lines-privacy-mode) instances.
			
			**Prerequisites:** 
			* Pro or higher account with Zoom Phone license 
			* Account owner or admin privileges  
			
			**Scopes:** `phone:read:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/shared_line_appearances'
        )

        return res.json()
        
        