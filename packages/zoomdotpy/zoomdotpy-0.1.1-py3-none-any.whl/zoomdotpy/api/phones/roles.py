from ..base import _BaseAPI

class RolesAPI(_BaseAPI):
    def create_roles(self , roleId):
        """
            Use this API to add member(s) to a role.
			
			**Prerequisites:**
			* Business, or Education account
			* Zoom Phone license 
			
			**Scopes:**`phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/roles/{roleId}/members'
        )

        return res.json()
        
        def get_roles(self , roleId):
        """
            Use this API to get members (not) in a [role](https://support.zoom.us/hc/en-us/articles/360042099012-Using-Zoom-Phone-role-management).
			
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
            f'/phone/roles/{roleId}/members'
        )

        return res.json()
        
        def delete_roles(self , roleId):
        """
            Use this API to delete member(s) in a role.
			
			**Prerequisites:**
			* Business, or Education account
			* Zoom Phone license 
			
			**Scopes:**`phone:write:admin`
			
			**Rate Limit Label:** `Light`
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/roles/{roleId}/members'
        )

        return res.json()
        
        