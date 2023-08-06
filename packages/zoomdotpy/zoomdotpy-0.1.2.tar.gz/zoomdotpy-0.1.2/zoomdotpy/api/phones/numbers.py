from ..base import _BaseAPI

class NumbersAPI(_BaseAPI):
    def update_numbers(self ):
        """
            Use this API to update a site's unassigned [phone numbers](https://support.zoom.us/hc/en-us/articles/360020808292-Managing-Phone-Numbers#h_38ba8b01-26e3-4b1b-a9b5-0717c00a7ca6). Up to 20 phone numbers can be updated in a single request. 
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom Phone license
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/numbers/sites/{siteId}'
        )

        return res.json()
        
        