from requests.sessions import session, Session
from requests.auth import HTTPBasicAuth
from . import api

class ZoomClient():
    s : Session = session()

    rooms   : api.RoomsAPI
    meetings: api.MeetingsAPI
    phones  : api.PhonesAPI

    def _get_token(self, account_id: str, username: str, password: str) -> str:
        self.s.auth = HTTPBasicAuth(username, password)
        
        res = self.s.post(
            'https://zoom.us/oauth/token',
            params={
                'grant_type': 'account_credentials',
                'account_id': account_id
            }
        )
        res.raise_for_status()

        self.s.auth = None

        return res.json()['access_token']

    def __init__(self, account_id: str, api_key: str, api_secret: str):
        token = self._get_token( account_id, api_key, api_secret )

        new_headers = {
            "authorization" : f'Bearer {token}',
            "content-type"  : "application/json",
            "accept"        : "application/json"
        }

        self.s.headers.update( new_headers )

        self.rooms      = api.RoomsAPI(self.s)
        self.meetings   = api.MeetingsAPI(self.s)
        self.phones     = api.PhonesAPI(self.s)
