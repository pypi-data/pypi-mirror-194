from ..base import _BaseAPI

class SipTrunkAPI(_BaseAPI):
    def get_sip_trunk(self , ):
        """
            Use this API to return a list of an account's assigned [BYOC (Bring Your Own Carrier) SIP (Session Initiation Protocol) trunks](https://zoom.us/docs/doc/Zoom-Bring%20Your%20Own%20Carrier.pdf).
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/sip_trunk/trunks'
        )

        return res.json()
        
        