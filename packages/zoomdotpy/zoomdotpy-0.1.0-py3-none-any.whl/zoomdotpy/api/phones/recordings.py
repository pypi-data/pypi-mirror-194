from ..base import _BaseAPI

class RecordingsAPI(_BaseAPI):
    def delete_recordings(self , recordingId):
        """
            Deletes a call recording.
			
			**Scopes:** `phone:write`, `phone:write:admin`, `phone_recording:write`, `phone_recording:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* User must belong to a Business or Enterprise account 
			* User must have a Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/recordings/{recordingId}'
        )

        return res.json()
        
        