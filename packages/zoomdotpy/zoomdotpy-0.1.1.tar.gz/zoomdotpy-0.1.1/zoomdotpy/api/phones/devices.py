from ..base import _BaseAPI

class DevicesAPI(_BaseAPI):
    def list_phones(self, params: dict = {}):
        """
            Retrieves a list of phones in zoom
        """

        res = self.request("GET", "phone/devices", params)

        return res.json()

    def get_phone(self, phone_id: str):
        """
            Retreives information on a specific phone
        """

        res = self.request("GET", f"phone/devices/{phone_id}")

        return res.json()

    def list_phone_numbers(self, params: dict = {}):
        """
            Retrieves a list of all phone numbers
        """

        res = self.request("GET", "phone/numbers", params)

        return res.json()
    
    def get_phone_number(self, number_id: str):
        """
            Retreives information on a specific phone number
        """

        res = self.request("GET", f"phone/numbers/{number_id}")

        return res.json()