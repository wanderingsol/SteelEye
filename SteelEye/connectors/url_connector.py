import requests
from util.singleton import Singleton


@Singleton
class UrlConnector(object):
    def __init__(self, url, headers=None, user=None, password=None):
        self.url = url
        self._session = requests.Session()
        self.user = user
        self.header = headers
        self.password = password
        self._set_session_params()

    def _set_session_params(self):
        if self.header:
            self._session.headers.update(self.header)
        if self.user and self.password:
            self._session.auth = (self.user, self.password)

    def rest_connection(self, headers=None, user=None, password=None):
        self._session = requests.Session()
        self.header = headers
        self.user = user
        self.password = password
        self._set_session_params()

    def get_url_text(self):
        resp = self._session.get(self.url)
        if resp.status_code == 200:
            return resp.content
        else:
            raise ConnectionError(f"Observed error code {resp.status_code}. Error message: {resp.content}")

    def is_downloadable(self, url=None):
        url = url or self.url
        with self._session.head(url) as resp:
            content_type = resp.headers.get('content-type').lower()
            if 'text' in content_type or 'html' in content_type:
                return False
        return True

    def download_data(self, url, chunk_size):
        url = url or self.url
        with self._session.get(url, stream=True, allow_redirects=True) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    yield chunk

    def get(self):
        pass

    def post(self):
        pass
