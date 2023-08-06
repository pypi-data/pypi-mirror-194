from io import StringIO
from copy import copy
from typing import List, Optional
import pandas as pd
from pandas import DataFrame
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.helper import is_valid_csv_configuration
from tim.core.types import (
    CSVSeparator,
    ExecuteResponse,
    UploadDatasetConfiguration,
    UpdateDatasetConfiguration,
    DatasetCreated,
    DatasetVersion,
    DatasetDetails,
    DatasetVersionDetails,
    DatasetStatusResponse,
    DatasetLog,
    DatasetVersionLog,
    DatasetPut,
    DatasetSliceConfiguration
)


class Datasets:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def upload_dataset(
        self,
        dataset: DataFrame,
        configuration: Optional[UploadDatasetConfiguration] = None,
    ) -> DatasetCreated:
        if configuration is None:
            configuration = UploadDatasetConfiguration()
        else:
            if 'csvSeparator' in configuration:
                del configuration['csvSeparator']
            if not is_valid_csv_configuration(configuration):
                raise ValueError("Invalid configuration input.")
        conf_with_csv_separator: UploadDatasetConfiguration = copy(configuration)
        conf_with_csv_separator["csvSeparator"] = CSVSeparator.SEMICOLON.value
        return execute_request(
            credentials=self._credentials,
            method="post",
            path="/datasets/csv",
            body=conf_with_csv_separator,
            file=dataset.to_csv(sep=conf_with_csv_separator["csvSeparator"], index=False),
        )

    def update_dataset(
        self,
        id: str,  # pylint: disable=redefined-builtin
        dataset: DataFrame,
        configuration: Optional[UpdateDatasetConfiguration] = None,
    ) -> DatasetVersion:
        if configuration is None:
            configuration = UploadDatasetConfiguration()
        else:
            if 'csvSeparator' in configuration:
                del configuration['csvSeparator']
            if not is_valid_csv_configuration(configuration):
                raise ValueError("Invalid configuration input.")
        conf_with_csv_separator: UpdateDatasetConfiguration = copy(configuration)
        conf_with_csv_separator["csvSeparator"] = CSVSeparator.SEMICOLON.value
        return execute_request(
            credentials=self._credentials,
            method="patch",
            path=f"/datasets/{id}/csv",
            body=conf_with_csv_separator,
            file=dataset.to_csv(sep=conf_with_csv_separator["csvSeparator"], index=False),
        )

    def list_dataset(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        workspace_id: Optional[str] = None,
        sort: Optional[str] = None
    ) -> List[DatasetDetails]:
        payload = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "workspaceId": workspace_id
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/datasets',
            params=payload
        )

    def delete_dataset_list(
        self,
        workspace_id: str,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None
    ) -> ExecuteResponse:
        payload = {
            "from": from_datetime,
            "to": to_datetime,
            "workspaceId": workspace_id
        }
        return execute_request(
            credentials=self._credentials,
            method='delete',
            path='/datasets',
            params=payload
        )

    def details_dataset(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> DatasetDetails:
        return execute_request(
            credentials=self._credentials,
            method="get",
            path=f"/datasets/{id}"
        )

    def edit_dataset_details(
        self,
        id: str,  # pylint: disable=redefined-builtin
        configuration: DatasetPut
    ) -> DatasetDetails:
        return execute_request(
            credentials=self._credentials,
            method="patch",
            path=f"/datasets/{id}",
            body=configuration
        )

    def delete_dataset(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method="delete",
            path=f"/datasets/{id}"
        )

    def dataset_logs(
        self,
        id: str  # pylint: disable=redefined-builtin
    ) -> List[DatasetLog]:
        return execute_request(
            credentials=self._credentials,
            method="get",
            path=f"/datasets/{id}/log",
        )

    def logs_dataset_version(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> DatasetVersionLog:
        payload = {
            "offset": offset,
            "limit": limit
        }
        return execute_request(
            credentials=self._credentials,
            method="get",
            path=f"/datasets/{id}/versions/{version}/log",
            params=payload
        )

    def list_dataset_versions(
        self,
        id: str,  # pylint: disable=redefined-builtin
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[DatasetVersionDetails]:
        payload = {
            "offset": offset,
            "limit": limit
        }
        return execute_request(
            credentials=self._credentials,
            method='get',
            path=f'/datasets/{id}/versions',
            params=payload
        )

    def details_dataset_version(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version: str
    ) -> DatasetVersionDetails:
        return execute_request(
            credentials=self._credentials,
            method="get",
            path=f"/datasets/{id}/versions/{version}"
        )

    def delete_dataset_version(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version: str
    ) -> ExecuteResponse:
        return execute_request(
            credentials=self._credentials,
            method="delete",
            path=f"/datasets/{id}/versions/{version}"
        )

    def status_dataset_version(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version_id: str
    ) -> DatasetStatusResponse:
        return execute_request(
            credentials=self._credentials,
            method="get",
            path=f"/datasets/{id}/versions/{version_id}/status",
        )

    def slice_dataset_version(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version_id: str,
        configuration: Optional[DatasetSliceConfiguration] = None
    ) -> DataFrame:
        if configuration is None:
            configuration = DatasetSliceConfiguration()
        configuration['outputFormat'] = 'CSV'

        response = execute_request(
            credentials=self._credentials,
            method="post",
            path=f"/datasets/{id}/versions/{version_id}/slice",
            body=configuration
        )

        data_string = StringIO(response)
        return pd.read_csv(data_string)
