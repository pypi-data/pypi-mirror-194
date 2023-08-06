from requests.exceptions import HTTPError
from typing import Protocol, Union
from .connections import Connection
from .errors import NotFoundError, UnauthorizedError
from .models import ProductInfo, TokenInfo, UserInfo

Id = Union[str, int]


class ConnectionProtocol(Protocol):
    def __init__(self, connection: Connection):
        pass


class BaseApi:
    def __init__(self, connection: Connection):
        pass


class TokenMixin(ConnectionProtocol):
    token_info_path = "/api/oauth/token/info"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.auth_connection = connection

    def validate_token(self, token: str):
        response = self.auth_connection.get(
            path=self.token_info_path,
            headers={"Authorization": f"Bearer {token}"},
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            code = (
                response.status
                if hasattr(response, "status")
                else response.status_code
            )
            if code == 401:
                raise UnauthorizedError(e)
        value = response.json() or {"attributes": {}}
        result = TokenInfo.from_dict(value, has_attributes=False)
        return result


class UsersMixin(ConnectionProtocol):
    user_info_path = "/api/v1/me"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.auth_connection = connection

    def get_current_user_info(self):
        response = self.auth_connection.get(self.user_info_path)
        try:
            response.raise_for_status()
        except HTTPError as e:
            code = (
                response.status
                if hasattr(response, "status")
                else response.status_code
            )
            if code == 404:
                raise NotFoundError(e)
        value = response.json() or {"attributes": {}}
        user_info = UserInfo.from_dict(value)
        return user_info


class ProductsMixin(ConnectionProtocol):
    product_info_path = "/api/v1/products/:id"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.auth_connection = connection

    def get_product_info(self, id: Id):
        path = self.product_info_path.replace(":id", str(id))
        response = self.auth_connection.get(path, {})
        try:
            response.raise_for_status()
        except HTTPError as e:
            code = (
                response.status
                if hasattr(response, "status")
                else response.status_code
            )
            if code == 404:
                raise NotFoundError(e)
        value = response.json() or {"attributes": {}}
        result = ProductInfo.from_dict(value)
        return result


class Api(ProductsMixin, UsersMixin, TokenMixin, BaseApi):
    pass
