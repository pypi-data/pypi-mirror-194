from .base import _BaseAPI

class MeetingsAPI(_BaseAPI):
    def list_meetings(self, destination_list_id: str):
        res = self._s.get(
            'https://api.umbrella.com/policies/v2/destinationlists/' + destination_list_id
        )
        res.raise_for_status()

        return res.json()

    def get_meeting(self, destination_list_id: str):
        res = self._s.get(
            'https://api.umbrella.com/policies/v2/destinationlists/' + destination_list_id
        )
        res.raise_for_status()

        return res.json()
