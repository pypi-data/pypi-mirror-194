from ..base import _BaseAPI

class CallLogsAPI(_BaseAPI):
    def get_call_logs(self , id):
        """
            Gets an account's call recording(https://support.zoom.us/hc/en-us/articles/360038521091-Accessing-and-sharing-call-recordings) by the recording's `callId` or `callLogId` ID.
			
			**Prerequisites:** 
			* A Pro or higher account with Zoom Phone license. 
			* Account owner or admin privileges
			
			**Scopes:** `phone:read:admin`<br>
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/call_logs/{id}/recordings'
        )

        return res.json()
        
        