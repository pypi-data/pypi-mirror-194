from ..base import _BaseAPI

class CallingPlansAPI(_BaseAPI):
    def get_calling_plans(self ):
        """
            Use this API to return all of an account's Zoom Phone [calling plans](https://marketplace.zoom.us/docs/api-reference/other-references/plans#zoom-phone-calling-plans).
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
			
			**Prerequisites:** 
			* A Pro or a higher account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/calling_plans'
        )

        return res.json()
        
        