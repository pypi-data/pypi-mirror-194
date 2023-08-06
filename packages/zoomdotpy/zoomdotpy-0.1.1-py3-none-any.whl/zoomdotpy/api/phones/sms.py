from ..base import _BaseAPI

class SmsAPI(_BaseAPI):
    def get_sms(self , sessionId, messageId):
        """
            Get details about a specific message in an SMS session.
			
			**Scopes:** `phone_sms:read`, `phone_sms:read:admin`, `phone_sms:master`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Heavy`
			
			**Prerequisites**
			* Paid account
			* User-enabled Zoom phone
			
			
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/sms/sessions/{sessionId}/messages/{messageId}'
        )

        return res.json()
        
        