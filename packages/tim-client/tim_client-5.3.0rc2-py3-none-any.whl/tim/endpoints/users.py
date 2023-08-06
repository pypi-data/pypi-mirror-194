from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import User


class Users:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def details_user(
        self,
    ) -> User:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/users/me'
        )
