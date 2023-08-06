from ..base import _BaseAPI

class ExtensionAPI(_BaseAPI):
    def delete_extension(self , extensionId, lineKeyId):
        """
            Use this API to delete the Zoom Phone [line key settings](https://support.zoom.us/hc/en-us/articles/360040587552) information.
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
			
			**Scopes:** `phone:write:admin` or `phone:write`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/extension/{extensionId}/line_keys/{lineKeyId}'
        )

        return res.json()
        
        