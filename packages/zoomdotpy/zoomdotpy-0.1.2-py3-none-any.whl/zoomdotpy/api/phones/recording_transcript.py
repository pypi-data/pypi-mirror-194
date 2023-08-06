from ..base import _BaseAPI

class RecordingTranscriptAPI(_BaseAPI):
    def get_recording_transcript(self , recordingId):
        """
            Downloads the phone recording transcript. 
			
			**Prerequisites:**
			
			* A Business or Enterprise account
			* A Zoom Phone license
			
			**Scopes:** `phone:read`, `phone:read:admin`, `phone_recording:read`, `phone_recording:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			
			
			
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/recording_transcript/download/{recordingId}'
        )

        return res.json()
        
        