from ..base import _BaseAPI

class PlansAPI(_BaseAPI):
    def get_plans(self ):
        """
            Use this API to return all of an account's Zoom Phone [plan package](https://marketplace.zoom.us/docs/api-reference/other-references/plans#additional-zoom-phone-plans-and-codes), phone number usage and availability.
			
			**Prerequisites:** 
			* A Pro or a higher account 
			* A Zoom Phone license
			
			**Scopes:** `phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/plans'
        )

        return res.json()
        
        