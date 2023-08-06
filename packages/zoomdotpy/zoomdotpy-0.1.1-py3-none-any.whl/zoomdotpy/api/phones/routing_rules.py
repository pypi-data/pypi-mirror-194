from ..base import _BaseAPI

class RoutingRulesAPI(_BaseAPI):
    def delete_routing_rules(self , routingRuleId):
        """
            Use this API to delete directory backup routing rule. The directory backup routing rules are a series of predefined Regular Expressions. These rules are used to route outgoing calls. If a dialed number does not match a Zoom Phone user, and does not match a defined External Contact, these rules are tested next. If a dialed number does not match any rules, the call will be routed via the PSTN.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:**
			 * A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'DELETE',
            f'/phone/routing_rules/{routingRuleId}'
        )

        return res.json()
        
        def get_routing_rules(self , routingRuleId):
        """
            Use this API to get directory backup routing rule. The directory backup routing rules are a series of predefined Regular Expressions. These rules are used to route outgoing calls. If a dialed number does not match a Zoom Phone user, and does not match a defined External Contact, these rules are tested next. If a dialed number does not match any rules, the call will be routed via the PSTN.
			
			**Scopes:** `phone:read:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Medium`
			
			**Prerequisites:**
			 * A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'GET',
            f'/phone/routing_rules/{routingRuleId}'
        )

        return res.json()
        
        def update_routing_rules(self , routingRuleId):
        """
            Use this API to update directory backup routing rule. The directory backup routing rules are a series of predefined Regular Expressions. These rules are used to route outgoing calls. If a dialed number does not match a Zoom Phone user, and does not match a defined External Contact, these rules are tested next. If a dialed number does not match any rules, the call will be routed via the PSTN.
			
			**Scopes:** `phone:write:admin`<br>**[Rate Limit Label](https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits):** `Light`
			
			**Prerequisites:**
			 * A Business or Enterprise account 
			* A Zoom Phone license
        """

        # TBD
        return

        res = self.request(
            'PATCH',
            f'/phone/routing_rules/{routingRuleId}'
        )

        return res.json()
        
        