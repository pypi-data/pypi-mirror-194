from typing import List, Optional
from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
    ExecuteResponse,
    Workspace,
    WorkspacePost,
    WorkspacePut
)


class Workspaces:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def list_workspace(
        self,
        offset:  Optional[int] = None,
        limit:  Optional[int] = None,
        user_group_id: Optional[str] = None,
        sort: Optional[str] = None
    ) -> List[Workspace]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "userGroupId": user_group_id
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/workspaces',
            params=payload
        )

    def create_workspace(
        self,
        configuration: WorkspacePost
    ) -> Workspace:
        return execute_request(
            credentials=self._credentials,
            method='post',
            path='/workspaces',
            body=configuration
        )

    def details_workspace(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> Workspace:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path=f'/workspaces/{id}'
        )

    def edit_workspace(
        self,
        id: str,  # pylint: disable=redefined-builtin
        configuration: WorkspacePut
    ) -> Workspace:
        return execute_request(
            credentials=self._credentials,
            method='patch',
            path=f'/workspaces/{id}',
            body=configuration
        )

    def delete_workspace(
        self,
        id: str,  # pylint: disable=redefined-builtin
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method='delete',
            path=f'/workspaces/{id}',
        )
