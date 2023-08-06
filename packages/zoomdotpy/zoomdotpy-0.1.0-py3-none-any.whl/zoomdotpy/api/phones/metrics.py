from ..base import _BaseAPI

class MetricsAPI(_BaseAPI):
    def get_metrics(self , ):
        """
            Lists the tracked locations. 
			
			**Prerequisites:**
			* Pro or higher account plan with Zoom phone license
			* Account owner or admin permissions
			
			**Scope:** `phone:read:admin`
			
			**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/metrics/location_tracking'
        )

        return res.json()
        
        