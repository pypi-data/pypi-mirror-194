# type: ignore
from time import sleep
from typing import Union, Callable, Optional, List
from pandas import DataFrame
from tim.core.credentials import Credentials
from tim.endpoints import Datasets

from tim.core.types import (
    UploadDatasetConfiguration,
    DatasetStatusResponse,
    DatasetCreated,
    UploadDatasetResponse,
    Status,
    UpdateDatasetConfiguration,
    DatasetVersion,
    DatasetOutputs
)


class ExtendedDatasets:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials
        self._datasets = Datasets(self._credentials)

    def poll_dataset_version_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version_id: str,
        status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
        tries_left: int = 300
    ) -> DatasetStatusResponse:
        """Poll for the status and progress of the dataset upload or dataset version update.

        Parameters
        ----------
        id : str
          The ID of a dataset in the TIM repository.
        version_id : str
          The ID of a dataset version in the TIM repository of the dataset above.
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the dataset version.
        tries_left : int
          Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

        Returns
        -------
        status : Dict
          Available keys: createdAt (str), status (str) and progress (int)
        """
        if tries_left < 1:
            raise ValueError("Timeout error.")
        response = self._datasets.status_dataset_version(id, version_id)
        if status_poll:
            status_poll(response)
        if Status(response['status']).value == Status.FAILED.value:  # pyright: reportUnnecessaryComparison=false
            return response
        if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
            sleep(2)
            return self.poll_dataset_version_status(
                id,
                version_id,
                status_poll,
                tries_left - 1
            )
        return response

    def upload_dataset(
        self,
        dataset: DataFrame,
        configuration: Optional[UploadDatasetConfiguration] = None,
        wait_to_finish: bool = True,
        outputs: Optional[List[DatasetOutputs]] = None,
        status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[DatasetCreated, UploadDatasetResponse]:
        """Upload a dataset to the TIM repository.

          Parameters
          ----------
          dataset : DataFrame
            The dataset containing time-series data.
          configuration : Dict, Optional
            Metadata of the dataset
            Available keys are: 
            timestampFormat, timestampColumn, decimalSeparator, csvSeparator, timeZone,
            timeZoneName, groupKeys, name, description, samplingPeriod and workspace.
            The value of samplingPeriod is a Dict containing the keys baseUnit and value.
          wait_to_finish : bool, Optional
            Wait for the dataset to be uploaded before returning.
            If set to False, the function will return once the dataset upload process has started.
          status_poll : Callable, Optional
            A callback function to poll for the status and progress of the dataset upload.
          tries_left : int
            Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

          Returns
          -------
          response : Dict
          details : Dict | None
            Dict when successful; None when unsuccessful
          logs : list of Dict
          """
        if configuration is None:
            configuration = UploadDatasetConfiguration()
        if outputs is None:
            outputs = [
                'response',
                'logs',
                'details',
            ]
        response = self._datasets.upload_dataset(dataset, configuration)
        if wait_to_finish is False:
            return response
        dataset_id = response['id']
        version_id = response['version']['id']
        status_result = self.poll_dataset_version_status(
            id=dataset_id,
            version_id=version_id,
            status_poll=status_poll,
            tries_left=tries_left
        )
        if Status(status_result['status']).value != Status.FAILED.value:
            details = self._datasets.details_dataset(dataset_id) if 'details' in outputs else None
        else:
            details = None
        logs = self._datasets.dataset_logs(dataset_id) if 'logs' in outputs else None
        return UploadDatasetResponse(response, details, logs)

    def update_dataset(
        self,
        dataset_id: str,
        dataset_version: DataFrame,
        configuration: Optional[UpdateDatasetConfiguration] = None,
        wait_to_finish: bool = True,
        outputs: Optional[List[DatasetOutputs]] = None,
        status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[DatasetVersion, UploadDatasetResponse]:
        """Update a dataset in the TIM repository.

          Parameters
          ----------
          dataset_id : str
            The ID of a dataset in the TIM repository.
          dataset : DataFrame
            The dataset containing time-series data.
          configuration : Dict, Optional
            Metadata of the dataset version
            Available keys are:
            timestampFormat, timestampColumn, decimalSeparator, csvSeparator.
          wait_to_finish : bool, Optional
            Wait for the dataset to be updated before returning.
            If set to False, the function will return once the dataset update process has started.
          status_poll : Callable, Optional
            A callback function to poll for the status and progress of the dataset update.
          tries_left : int
            Number of iterations the function will loop to fetch the dataset version status before sending a timeout error.

          Returns
          -------
          response : Dict
          details : Dict | None
            Dict when successful; None when unsuccessful
          logs : list of Dict
          """
        if configuration is None:
            configuration = UpdateDatasetConfiguration()
        if outputs is None:
            outputs = [
                'response',
                'logs',
                'details',
            ]
        response = self._datasets.update_dataset(dataset_id, dataset_version, configuration)
        if wait_to_finish is False:
            return response
        status_result = self.poll_dataset_version_status(
            id=dataset_id,
            version_id=response['version']['id'],
            status_poll=status_poll,
            tries_left=tries_left
        )
        if Status(status_result['status']).value != Status.FAILED.value:
            details = self._datasets.details_dataset(dataset_id) if 'details' in outputs else None
        else:
            details = None
        details = self._datasets.details_dataset(dataset_id) if 'details' in outputs else None
        logs = self._datasets.dataset_logs(dataset_id) if 'logs' in outputs else None
        return UploadDatasetResponse(response, details, logs)
