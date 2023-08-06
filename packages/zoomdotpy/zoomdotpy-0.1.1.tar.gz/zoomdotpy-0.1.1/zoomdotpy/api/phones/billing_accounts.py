from ..base import _BaseAPI

class BillingAccountsAPI(_BaseAPI):
    def get_billing_accounts(self , billingAccountId):
        """
            A Zoom account owner or a user with admin privilege can use this API to get information about a billing account.
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			
			**Scope:** `phone:read:admin` 
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/billing_accounts/{billingAccountId}'
        )

        return res.json()
        
        