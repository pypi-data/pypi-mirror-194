from ..base import _BaseAPI

class AutoReceptionistsAPI(_BaseAPI):
    def delete_auto_receptionists(self , autoReceptionistId, phoneNumberId):
        """
            Unassign a specific phone number that was previously assigned to an [auto receptionist](https://support.zoom.us/hc/en-us/articles/360021121312-Managing-Auto-Receptionists-and-Interactive-Voice-Response-IVR-). 
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom Phone License
			* Account owner or admin permissions<br>
			**Scopes:** `phone:write:admin`<br> 
			
			
			 **[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/auto_receptionists/{autoReceptionistId}/phone_numbers/{phoneNumberId}'
        )

        return res.json()
        
        