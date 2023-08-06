from ..base import _BaseAPI

class CompanyNumberAPI(_BaseAPI):
    def update_company_number(self ):
        """
            Use this API to [change an account's main company number](https://support.zoom.us/hc/en-us/articles/360028553691#h_82414c34-9df2-428a-85a4-efcf7f9e0d72).
			
			External users can use the [main company number](https://support.zoom.us/hc/en-us/articles/360028553691) to reach your Zoom Phone users by dialing the main company number and the user's extension. It can also be used by your account's Zoom Phone users as their caller ID when making calls.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'PUT',
            f'/phone/company_number'
        )

        return res.json()
        
        