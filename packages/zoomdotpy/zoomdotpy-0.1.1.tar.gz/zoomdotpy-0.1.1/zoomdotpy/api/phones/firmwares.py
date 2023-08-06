from ..base import _BaseAPI

class FirmwaresAPI(_BaseAPI):
    def get_firmwares(self , ):
        """
            Use this API to get updatable [firmwares](https://support.zoom.us/hc/en-us/articles/360054198852-Setting-up-firmware-update-rules).
			
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
            f'/phone/firmwares'
        )

        return res.json()
        
        