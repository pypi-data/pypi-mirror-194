from typing import List, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import (
    Experiment,
    ExperimentPost,
    ExperimentPut,
    ExecuteResponse
)


class Experiments:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def list_experiment(
        self,
        offset:  Optional[int] = None,
        limit:  Optional[int] = None,
        workspace_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        sort: Optional[str] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> List[Experiment]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "workspaceId": workspace_id,
            "useCaseId": use_case_id,
            "datasetId": dataset_id,
            "type": type
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/experiments',
            params=payload
        )

    def create_experiment(
        self,
        configuration: ExperimentPost
    ) -> Experiment:
        return execute_request(
            credentials=self._credentials,
            method='post',
            path='/experiments',
            body=configuration
        )

    def details_experiment(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> Experiment:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path=f'/experiments/{id}'
        )

    def edit_experiment(
        self,
        id: str,  # pylint: disable=redefined-builtin
        configuration: ExperimentPut
    ) -> Experiment:
        return execute_request(
            credentials=self._credentials,
            method='patch',
            path=f'/experiments/{id}',
            body=configuration
        )

    def delete_experiment(
        self,
        id: str,  # pylint: disable=redefined-builtin
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method='delete',
            path=f'/experiments/{id}',
        )
