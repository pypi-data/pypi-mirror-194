from ..base import _BaseAPI

class SipGroupsAPI(_BaseAPI):
    def get_sip_groups(self , ):
        """
            Use this API to list SIP (Session Initiation Protocol) groups.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/sip_groups'
        )

        return res.json()
        
        