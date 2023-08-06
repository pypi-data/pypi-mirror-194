from ..base import _BaseAPI

class CommonAreasAPI(_BaseAPI):
    def create_common_areas(self , commonAreaId, settingType):
        """
            Use this API to add the common area setting according to the setting type, specifically for desk phones.
			
			**Note**: For use by customers who opted for `Common Area Optimization`  
			
			**Prerequisites:**
			* Pro or a higher account with Zoom Phone license.
			* Account owner or admin permissions.
			
			**Scope:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/common_areas/{commonAreaId}/settings/{settingType}'
        )

        return res.json()
        
        def delete_common_areas(self , commonAreaId, settingType):
        """
            Use this API to remove the common area subsetting from desk phones. 
			
			**Note**: For use by customers who opted for `Common Area Optimization`  
			
			**Prerequisites:**
			* Pro or a higher account with Zoom Phone license.
			* Account owner or admin permissions.
			
			**Scopes:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/common_areas/{commonAreaId}/settings/{settingType}'
        )

        return res.json()
        
        def update_common_areas(self , commonAreaId, settingType):
        """
            Use this API to update the common area setting according to the setting type, specifically for desk phones.
			
			**Note**: For use by customers who opted for `Common Area Optimization`  
			
			**Prerequisites:**
			* Pro or a higher account with Zoom Phone license.
			* Account owner or admin permissions.
			
			**Scope:** `phone:write:admin`
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/common_areas/{commonAreaId}/settings/{settingType}'
        )

        return res.json()
        
        