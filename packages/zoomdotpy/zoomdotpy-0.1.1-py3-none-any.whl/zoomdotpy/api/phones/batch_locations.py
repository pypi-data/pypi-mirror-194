from ..base import _BaseAPI

class BatchLocationsAPI(_BaseAPI):
    def create_batch_locations(self ):
        """
            Batches the add emergency service locations.
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			* Account owner or admin permissions
			
			**Scope:** `phone:write:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
        """

        # TBD
        return

        res = self.request(
            'POST',
            f'/phone/batch_locations'
        )

        return res.json()
        
        