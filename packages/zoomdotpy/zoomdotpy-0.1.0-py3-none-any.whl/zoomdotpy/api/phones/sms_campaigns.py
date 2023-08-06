from ..base import _BaseAPI

class SmsCampaignsAPI(_BaseAPI):
    def delete_sms_campaigns(self , smsCampaignId, phoneNumberId):
        """
            Use this API to [unassign a phone number from the SMS campaign](https://support.zoom.us/hc/en-us/articles/5016496738445-SMS-MMS-10DLC-Compliance-for-Zoom-Phone-and-Zoom-Contact-Center#h_01FYVVSPVM8MZN4Y9EW5690QHH).
			Remove the assigned phone number from the campaign.
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license 
			* The campaign must have been previously assigned a Zoom Phone number
			
			**Scopes:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/sms_campaigns/{smsCampaignId}/phone_numbers/{phoneNumberId}'
        )

        return res.json()
        
        