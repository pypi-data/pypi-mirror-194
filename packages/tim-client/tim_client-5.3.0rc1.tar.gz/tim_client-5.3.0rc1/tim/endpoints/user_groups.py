from typing import List, Optional
from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
    ExecuteResponse,
    UserGroup,
    UserGroupPost
)


class UserGroups:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def list_user_group(
        self,
        offset:  Optional[int] = None,
        limit:  Optional[int] = None,
        sort: Optional[str] = None
    ) -> List[UserGroup]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/user-groups',
            params=payload
        )

    def create_user_group(
        self,
        configuration: UserGroupPost
    ) -> UserGroup:
        return execute_request(
            credentials=self._credentials,
            method='post',
            path='/user-groups',
            body=configuration
        )

    def details_user_group(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> UserGroup:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path=f'/user-groups/{id}'
        )

    def update_user_group(
        self,
        id: str,  # pylint: disable=redefined-builtin
        configuration: UserGroupPost
    ) -> UserGroup:
        return execute_request(
            credentials=self._credentials,
            method='put',
            path=f'/user-groups/{id}',
            body=configuration
        )

    def delete_user_group(
        self,
        id: str,  # pylint: disable=redefined-builtin
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method='delete',
            path=f'/user-groups/{id}',
        )
