from ..base import _BaseAPI

class DialByNameDirectoryAPI(_BaseAPI):
    def create_dial_by_name_directory(self ):
        """
            Use this API to add users to a [directory](https://support.zoom.us/hc/en-us/articles/4404938949389-Using-a-dial-by-name-directory).
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/dial_by_name_directory/extensions'
        )

        return res.json()
        
        def get_dial_by_name_directory(self , ):
        """
            Use this API to get users that are in or not in a [directory](https://support.zoom.us/hc/en-us/articles/4404938949389-Using-a-dial-by-name-directory).
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:**`phone:read:admin`
			
			**Rate Limit Label:** `Medium`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/dial_by_name_directory/extensions'
        )

        return res.json()
        
        def delete_dial_by_name_directory(self , ):
        """
            Use this API to delete users from the [directory](https://support.zoom.us/hc/en-us/articles/4404938949389-Using-a-dial-by-name-directory).
			
			**Prerequisites:**
			* Business or Education account
			* Zoom Phone license 
			
			**Scopes:** `phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/dial_by_name_directory/extensions'
        )

        return res.json()
        
        