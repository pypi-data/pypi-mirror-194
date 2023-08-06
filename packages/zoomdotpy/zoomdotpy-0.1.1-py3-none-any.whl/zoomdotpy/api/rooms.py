from .base import _BaseAPI

class RoomsAPI(_BaseAPI):
    def list_rooms(self, params: dict = {}):
        req_params = {'page_size': 300}
        req_params.update(params)

        res = self.request("GET", "rooms", req_params)

        return res.json()

    def get_room(self, room_id: str):
        res = self.request("GET", f"rooms/{room_id}")

        return res.json()

    def get_room_devices(self, room_id: str):
        res = self.request("GET", f"rooms/{room_id}/devices")

        return res.json()['devices']