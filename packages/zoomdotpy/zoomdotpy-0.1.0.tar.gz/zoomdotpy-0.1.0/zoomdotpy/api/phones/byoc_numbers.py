from ..base import _BaseAPI

class ByocNumbersAPI(_BaseAPI):
    def create_byoc_numbers(self ):
        """
            Use this API to add BYOC (Bring Your Own Carrier) phone numbers to Zoom Phone.
			
			**Scopes:** `phone:write:admin`, `phone:write`, or `phone:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise plan 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/byoc_numbers'
        )

        return res.json()
        
        