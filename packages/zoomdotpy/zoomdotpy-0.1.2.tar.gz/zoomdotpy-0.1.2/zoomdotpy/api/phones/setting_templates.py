from ..base import _BaseAPI

class SettingTemplatesAPI(_BaseAPI):
    def get_setting_templates(self , templateId):
        """
            Returns information about an account's phone template.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/setting_templates/{templateId}'
        )

        return res.json()
        
        def update_setting_templates(self , templateId):
        """
            Updates or modifies a phone template's settings.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/setting_templates/{templateId}'
        )

        return res.json()
        
        