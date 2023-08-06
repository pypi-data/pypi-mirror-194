from ..base import _BaseAPI

class PortedNumbersAPI(_BaseAPI):
    def get_ported_numbers(self , orderId):
        """
            Use this API to get details on the ported numbers by specifying `order_id`.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Pro or higher account plan 
			* A Zoom phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/ported_numbers/orders/{orderId}'
        )

        return res.json()
        
        