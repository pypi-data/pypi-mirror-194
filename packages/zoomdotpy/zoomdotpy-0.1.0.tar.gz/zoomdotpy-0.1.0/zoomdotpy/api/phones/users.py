from ..base import _BaseAPI

class UsersAPI(_BaseAPI):
    def get_users(self , userId):
        """
            Use this API to retrieve a user's Zoom Phone voicemails in descending order. For user-level apps, pass [the `me` value](https://marketplace.zoom.us/docs/api-reference/using-zoom-apis#mekeyword) instead of the `userId` parameter.
			
			**Scopes:** `phone:read`, `phone:read:admin`, `phone_voicemail:read`, `phone_voicemail:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/users/{userId}/voice_mails/sync'
        )

        return res.json()
        
        