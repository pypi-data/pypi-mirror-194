from ..base import _BaseAPI

class MonitoringGroupsAPI(_BaseAPI):
    def delete_monitoring_groups(self , monitoringGroupId, memberExtensionId):
        """
            Use this API to remove a member from a [Monitoring Group](https://support.zoom.us/hc/en-us/articles/360044804711).
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:**
			 * A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/monitoring_groups/{monitoringGroupId}/monitor_members/{memberExtensionId}'
        )

        return res.json()
        
        