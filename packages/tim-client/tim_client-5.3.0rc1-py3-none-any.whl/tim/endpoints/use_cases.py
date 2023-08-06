from typing import List, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import (
    UseCase,
    UseCasePost,
    UseCasePut,
    ExecuteResponse
)


class UseCases:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def list_use_case(
        self,
        offset:  Optional[int] = None,
        limit:  Optional[int] = None,
        user_group_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        sort: Optional[str] = None,
        is_panel_data: Optional[bool] = None,
    ) -> List[UseCase]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "userGroupId": user_group_id,
            "workspaceId": workspace_id,
            "datasetId": dataset_id,
            "isPanelData": is_panel_data
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/use-cases',
            params=payload
        )

    def create_use_case(
        self,
        configuration: UseCasePost
    ) -> UseCase:
        return execute_request(
            credentials=self._credentials,
            method='post',
            path='/use-cases',
            body=configuration
        )

    def details_use_case(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> UseCase:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path=f'/use-cases/{id}'
        )

    def edit_use_case(
        self,
        id: str,  # pylint: disable=redefined-builtin
        configuration: UseCasePut
    ) -> UseCase:
        return execute_request(
            credentials=self._credentials,
            method='patch',
            path=f'/use-cases/{id}',
            body=configuration
        )

    def delete_use_case(
        self,
        id: str,  # pylint: disable=redefined-builtin
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method='delete',
            path=f'/use-cases/{id}',
        )
