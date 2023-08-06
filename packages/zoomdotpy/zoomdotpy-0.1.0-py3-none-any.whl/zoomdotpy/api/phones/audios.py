from ..base import _BaseAPI

class AudiosAPI(_BaseAPI):
    def delete_audios(self , audioId):
        """
            Deletes an audio item.
			
			**Prerequisites:**
			* Business, or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:write`,`phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/audios/{audioId}'
        )

        return res.json()
        
        def get_audios(self , audioId):
        """
            Gets an audio item.
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:read`,`phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/audios/{audioId}'
        )

        return res.json()
        
        def update_audios(self , audioId):
        """
            Updates an audio item.
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/audios/{audioId}'
        )

        return res.json()
        
        