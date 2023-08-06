from datetime import datetime
import logging
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
import requests
from requests import Response
from typing import Dict, Optional
from urllib.parse import urljoin


class Connection:
    def get(self, path: str, headers: Dict[str, str]) -> Response:
        """Get the resource at ``path`` with the specified ``headers``"""
        raise NotImplementedError()


class AnonymousConnection(Connection):
    host = "auth.galvanize.com"

    def __init__(self, host: str = ""):
        """An anonymous connection to the authentication server"""
        self.log = logging.getLogger(self.__class__.__name__)
        host = host.replace("https://", "")
        self._host = f"https://{host or self.host}"

    def get(self, path: str, headers: Dict[str, str]) -> Response:
        request_url = urljoin(self._host, path)
        self.log.debug(f"Getting {request_url}")
        return requests.get(request_url, headers=headers)


class ClientCredentialConnection(Connection):
    host = "auth.galvanize.com"
    token_path = "/api/oauth/token"
    scope = ["product.read", "user.read", "user.search"]

    def __init__(self, id: str, secret: str, host: Optional[str] = None):
        """A credentialed connection to the authentication server"""
        self.log = logging.getLogger(self.__class__.__name__)
        self._host = f"https://{host or self.host}"
        self._id = id
        self._secret = secret
        self._token = None

    def get(self, path: str, headers: Dict[str, str]) -> Response:
        request_url = urljoin(self._host, path)
        self.log.debug(f"Getting {request_url}")
        try:
            if self._token is None:
                self.fetch_token()
            session = OAuth2Session(self._id, token=self._token)
            return session.get(request_url)
        except TokenExpiredError:
            self.log.debug("Expired token. Fetching a new one.")
            self.fetch_token()
            session = OAuth2Session(self._id, token=self._token)
            return session.get(request_url)

    def fetch_token(self):
        client = BackendApplicationClient(client_id=self._id)
        session = OAuth2Session(client=client, scope=self.scope)
        try:
            self._token = session.fetch_token(
                self.token_url,
                client_id=self._id,
                client_secret=self._secret,
                scope=self.scope,
            )
        except Warning as warning:
            if hasattr(warning, "token"):
                self._token = warning.token
            else:
                raise warning

    @property
    def token(self):
        return self._token

    @property
    def token_url(self):
        return urljoin(self._host, self.token_path)


class AuthenticatedConnection(Connection):
    host = "auth.galvanize.com"
    refresh_token_path = "/api/oauth/token"
    user_info_path = "/api/v1/me"

    def __init__(
        self,
        id: str,
        secret: str,
        access_token: str,
        expires_at: datetime,
        refresh_token: str,
        host: Optional[str] = None,
    ):
        """An authenticated connection to the authentication server"""
        self.log = logging.getLogger(self.__class__.__name__)
        self._host = f"https://{host or self.host}"
        self._id = id
        self._secret = secret
        self._token = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.timestamp(),
        }

    def get(self, path: str, headers: Dict[str, str]) -> Response:
        request_url = urljoin(self._host, path)
        self.log.debug(f"Getting {request_url}")
        refresh_kwargs = {"client_id": self._id, "client_secret": self._secret}
        session = OAuth2Session(
            self._id,
            auto_refresh_url=self.refresh_token_url,
            token=self._token,
            token_updater=self.update_token,
            auto_refresh_kwargs=refresh_kwargs,
        )
        return session.get(request_url)

    def update_token(self, token):
        self.log.debug("Updating token")
        self._token = token

    @property
    def token(self):
        return self._token

    @property
    def refresh_token_url(self):
        return urljoin(self._host, self.refresh_token_path)
