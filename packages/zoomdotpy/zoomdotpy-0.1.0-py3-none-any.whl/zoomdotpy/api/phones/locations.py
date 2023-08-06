from ..base import _BaseAPI

class LocationsAPI(_BaseAPI):
    def delete_locations(self , locationId):
        """
            Removes an emergency location.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/locations/{locationId}'
        )

        return res.json()
        
        def get_locations(self , locationId):
        """
            Returns an emergency service location's information.
			
			**Scopes:** `phone:read:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/locations/{locationId}'
        )

        return res.json()
        
        def update_locations(self , locationId):
        """
            Updates an emergency location's information.
			
			**Scopes:** `phone:write:admin`
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:** 
			* Pro or a higher account with Zoom Phone license 
			* Account owner or admin permissions
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/locations/{locationId}'
        )

        return res.json()
        
        