from requests import Session, Request, Response
from urllib import parse as urlparse

class _BaseAPI():
    _s : Session

    def __init__(self, session: Session):
        self._s = session

        self.__post_init__()

    def __post_init__(self): pass

    def _try(func: callable, *args, **kwargs):
        def inner():
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(err)

        return inner

    def _endpoint_to_absolute_path(self, endpoint: str) -> str:
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]

        return urlparse.urljoin('https://api.zoom.us/v2/', endpoint)

    def request(self, method: str, endpoint: str, *args, **kwargs) -> Response:
        endpoint = self._endpoint_to_absolute_path(endpoint)

        # Update args with method and endpoint
        args = ( method, endpoint, *args )

        # Invoke request
        res = self._s.request(
            *args,
            **kwargs
        )

        return res

    def get(self, endpoint: str, *args, **kwargs):
        endpoint = self._endpoint_to_absolute_path(endpoint)

        res = self._s.get(endpoint, *args, **kwargs)
        res.raise_for_status()

        return res