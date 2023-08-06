from ..base import _BaseAPI

class RoomsAPI(_BaseAPI):
    def delete_rooms(self , roomId, phoneNumberId):
        """
            Use this API to unassign a [phone number](https://support.zoom.us/hc/en-us/articles/360020808292-Managing-Phone-Numbers#h_38ba8b01-26e3-4b1b-a9b5-0717c00a7ca6) from a [Zoom Room](https://support.zoom.us/hc/en-us/articles/360025153711#h_140e30ba-5a88-40b9-b799-16883fa0a037).
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license 
			* The Zoom Room must have been previously assigned a Zoom Phone number
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/rooms/{roomId}/phone_numbers/{phoneNumberId}'
        )

        return res.json()
        
        