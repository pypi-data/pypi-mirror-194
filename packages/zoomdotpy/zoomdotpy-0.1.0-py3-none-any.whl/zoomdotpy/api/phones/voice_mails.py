from ..base import _BaseAPI

class VoiceMailsAPI(_BaseAPI):
    def delete_voice_mails(self , voicemailId):
        """
            Use this API to delete an account's [voicemail message](https://support.zoom.us/hc/en-us/articles/360021400211-Managing-voicemail-messages).
			
			**Scopes:** `phone:write:admin`, `phone:write`, `phone_voicemail:write`, `phone_voicemail:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/voice_mails/{voicemailId}'
        )

        return res.json()
        
        def get_voice_mails(self , voicemailId):
        """
            Use this API to return information about a [voicemail message](https://support.zoom.us/hc/en-us/articles/360021400211-Managing-voicemail-messages).
			
			**Scopes:** `phone:read:admin`, `phone:read`, `phone_voicemail:read`, `phone_voicemail:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/voice_mails/{voicemailId}'
        )

        return res.json()
        
        