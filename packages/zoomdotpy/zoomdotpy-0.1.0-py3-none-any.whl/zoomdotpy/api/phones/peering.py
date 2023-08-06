from ..base import _BaseAPI

class PeeringAPI(_BaseAPI):
    def delete_peering(self ):
        """
            Removes phone numbers added to Zoom through the Provider Exchange.
			
			**Note**: Phone peering API and events are for partners who have completed the MoU to peer with Zoom. To become a peering provider/ carrier, submit your [request](https://docs.google.com/forms/d/e/1FAIpQLSewkY6ixVyKVNkWC-vgmejC16gigxsJWXji3dWzE3XlWtjsgg/viewform).
			
			**Scopes**: `phone_peering:write:admin`, `phone_peering:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/peering/numbers'
        )

        return res.json()
        
        def get_peering(self , ):
        """
            Returns phone numbers to Zoom through the Provider Exchange.
			
			**Note**: Phone peering API and events are for partners who have completed the MoU to peer with Zoom. To become a peering provider/ carrier, submit your [request](https://docs.google.com/forms/d/e/1FAIpQLSewkY6ixVyKVNkWC-vgmejC16gigxsJWXji3dWzE3XlWtjsgg/viewform).
			
			**Scopes:** `phone_peering:read:admin`, `phone_peering:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/peering/numbers'
        )

        return res.json()
        
        def update_peering(self ):
        """
            Updates phone numbers to Zoom through the Provider Exchange.
			
			**Note**: Phone peering API and events are for partners that have completed the MoU to peer with Zoom. To become a peering provider/ carrier, submit your [request](https://docs.google.com/forms/d/e/1FAIpQLSewkY6ixVyKVNkWC-vgmejC16gigxsJWXji3dWzE3XlWtjsgg/viewform).
			
			**Scopes:** `phone_peering:write:admin`, `phone_peering:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/peering/numbers'
        )

        return res.json()
        
        def create_peering(self ):
        """
            Adds phone numbers to Zoom through the Provider Exchange.
			
			**Note**: Phone peering API and events are for partners who have completed the MoU to peer with Zoom. To become a peering provider/ carrier, submit your [request](https://docs.google.com/forms/d/e/1FAIpQLSewkY6ixVyKVNkWC-vgmejC16gigxsJWXji3dWzE3XlWtjsgg/viewform).
			
			**Scopes:** `phone_peering:write:admin`, `phone_peering:master`</br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/peering/numbers'
        )

        return res.json()
        
        