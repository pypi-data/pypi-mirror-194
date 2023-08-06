from typing import Union, Callable, Optional, List
from pandas import DataFrame
from tim.core.server import server as server_url
from tim.core.credentials import Credentials
from tim.endpoints import (
    Licenses,
    Users,
    UserGroups,
    Workspaces,
    UseCases,
    Experiments,
    Datasets,
    Forecasting,
    Detection,
    Telemetry,
)
from tim.extended_functions import ExtendedDatasets
from tim.extended_functions import ExtendedForecasting
from tim.extended_functions import ExtendedDetection
from tim.helper_functions import HelperPostProcess
from tim.core.types import (
    UploadDatasetConfiguration,
    DatasetStatusResponse,
    DatasetCreated,
    UploadDatasetResponse,
    UpdateDatasetConfiguration,
    DatasetVersion,
    DatasetOutputs,
    StatusResponse,
    ForecastingBuildModel,
    JobExecuteResponse,
    JobResponse,
    ForecastingResultsOptions,
    ForecastingResultsOutputs,
    ForecastingRebuildModel,
    ForecastingRetrainModel,
    ForecastingPredict,
    ForecastingResultsRCAOptions,
    ForecastingRCAOutput,
    WhatIf,
    WhatIfPanel,
    QuickForecast,
    DetectionResultsOptions,
    DetectionResultsOutputs,
    DetectionBuildKPIModel,
    DetectionBuildSystemModel,
    DetectionBuildOutlierModel,
    DetectionBuildDriftModelKolmogorovSmirnov,
    DetectionBuildDriftModelJensenShannon,
    DetectionRebuildKPIModel,
    DetectionDetect,
    DetectionResultsRCAOptions,
    DetectionRCAOutput
)


class Tim:

    def __init__(
        self,
        email: str,
        password: str,
        server: str = server_url,  # pylint: disable=redefined-builtin
        client_name: str = "Python Client"
    ):
        self._credentials = Credentials(email, password, server, client_name)
        self.licenses = Licenses(self._credentials)
        self.users = Users(self._credentials)
        self.user_groups = UserGroups(self._credentials)
        self.workspaces = Workspaces(self._credentials)
        self.use_cases = UseCases(self._credentials)
        self.experiments = Experiments(self._credentials)
        self.datasets = Datasets(self._credentials)
        self.forecasting = Forecasting(self._credentials)
        self.detection = Detection(self._credentials)
        self.telemetry = Telemetry(self._credentials)
        self.post_process = HelperPostProcess(self._credentials)

        self.extended_datasets = ExtendedDatasets(self._credentials)
        self.extended_forecasting = ExtendedForecasting(self._credentials)
        self.extended_detection = ExtendedDetection(self._credentials)


# ------------------------- Deprecated functions ---------------------------
# -------------------------------- Datasets --------------------------------

    # Deprecated: use self.extended_datasets object instead
    # Deprecated: this function should not be public

    def poll_dataset_version_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        version_id: str,
        status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
        tries_left: int = 300
    ) -> DatasetStatusResponse:
        return self.extended_datasets.poll_dataset_version_status(id, version_id, status_poll, tries_left)

    # Deprecated: use self.extended_datasets object instead
    def upload_dataset(
        self,
        dataset: DataFrame,
        configuration: Optional[UploadDatasetConfiguration] = None,
        wait_to_finish: bool = True,
        outputs: Optional[List[DatasetOutputs]] = None,
        status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[DatasetCreated, UploadDatasetResponse]:
        return self.extended_datasets.upload_dataset(dataset, configuration, wait_to_finish, outputs, status_poll, tries_left)

    # Deprecated: use self.extended_datasets object instead
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
        return self.extended_datasets.update_dataset(
            dataset_id,
            dataset_version,
            configuration,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

# -------------------------------- Forecasting --------------------------------

    # Deprecated: use self.extended_forecasting object instead
    # Deprecated: this function should not be public
    def poll_forecast_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> StatusResponse:
        return self.extended_forecasting.poll_forecast_status(id, status_poll, tries_left)

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_job_results(
        self,
        id: str,  # pylint: disable=redefined-builtin
        outputs: Optional[List[ForecastingResultsOptions]] = None
    ) -> ForecastingResultsOutputs:
        return self.extended_forecasting.results(id, outputs)

    # Deprecated: use self.extended_forecasting object instead
    def execute_forecast_job(
        self,
        id: str,  # pylint: disable=redefined-builtin
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.execute(id, wait_to_finish, outputs, status_poll, tries_left)

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_build_model(
        self,
        configuration: ForecastingBuildModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.build_model(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_predict(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingPredict] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.predict(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_rebuild_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRebuildModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.rebuild_model(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_retrain_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRetrainModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.retrain_model(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_results_rca(
        self,
        id: str,  # pylint: disable=redefined-builtin
        indices_of_model: Optional[List[int]] = None,
        parent_job_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        outputs: Optional[List[ForecastingResultsRCAOptions]] = None,
    ) -> ForecastingRCAOutput:
        return self.extended_forecasting.results_rca(id, indices_of_model, parent_job_id, timestamp, radius, outputs)

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_root_cause_analysis(
        self,
        parent_job_id: str,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsRCAOptions]] = None,
        indices_of_model: Optional[List[int]] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingRCAOutput]:
        return self.extended_forecasting.root_cause_analysis(
            parent_job_id,
            execute,
            wait_to_finish,
            outputs,
            indices_of_model,
            timestamp,
            radius,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def forecasting_what_if_analysis(
        self,
        parent_job_id: str,
        configuration: Union[WhatIf, WhatIfPanel],
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        return self.extended_forecasting.what_if_analysis(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_forecasting object instead
    def quick_forecast(
        self,
        dataset: DataFrame,
        job_configuration: Optional[ForecastingBuildModel] = None,
        workspace_id: Optional[str] = None,
        dataset_configuration: Optional[UploadDatasetConfiguration] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[str]] = None,
        status_poll: Optional[Callable[[Union[DatasetStatusResponse, StatusResponse]], None]] = None,
        tries_left: int = 300,
        delete_items: bool = False
    ) -> QuickForecast:
        return self.extended_forecasting.quick_forecast(
            dataset,
            job_configuration,
            workspace_id,
            dataset_configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left,
            delete_items
        )

# -------------------------------- Detection --------------------------------

    # Deprecated: use self.extended_detection object instead
    # Deprecated: this function should not be public
    def poll_detect_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> StatusResponse:
        return self.extended_detection.poll_detect_status(id, status_poll, tries_left)

    # Deprecated: use self.extended_detection object instead
    def detection_job_results(
        self,
        id: str,  # pylint: disable=redefined-builtin
        outputs: Optional[List[DetectionResultsOptions]] = None
    ) -> DetectionResultsOutputs:
        return self.extended_detection.results(id, outputs)

    # Deprecated: use self.extended_detection object instead
    def execute_detection_job(
        self,
        id: str,  # pylint: disable=redefined-builtin
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.execute(id, wait_to_finish, outputs, status_poll, tries_left)

    # Deprecated: use self.extended_detection object instead
    def detection_build_kpi_model(
        self,
        configuration: DetectionBuildKPIModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.build_kpi_model(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_build_system_model(
        self,
        configuration: DetectionBuildSystemModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.build_system_model(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_build_outlier_model(
        self,
        configuration: DetectionBuildOutlierModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.build_outlier_model(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_build_drift_model_kolmogorov_smirnov(
        self,
        configuration: DetectionBuildDriftModelKolmogorovSmirnov,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.build_drift_model_kolmogorov_smirnov(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_build_drift_model_jensen_shannon(
        self,
        configuration: DetectionBuildDriftModelJensenShannon,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.build_drift_model_jensen_shannon(
            configuration,
            dataset_id,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_rebuild_kpi_model(
        self,
        parent_job_id: str,
        configuration: Optional[DetectionRebuildKPIModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.rebuild_kpi_model(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_detect(
        self,
        parent_job_id: str,
        configuration: DetectionDetect,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.detect(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_results_rca(
        self,
        id: str,  # pylint: disable=redefined-builtin
        index_of_model: Optional[int] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        outputs: Optional[List[DetectionResultsRCAOptions]] = None
    ) -> DetectionRCAOutput:
        return self.extended_detection.results_rca(id, index_of_model, timestamp, radius, outputs)

    # Deprecated: use self.extended_detection object instead
    def detection_root_cause_analysis(
        self,
        parent_job_id: str,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsRCAOptions]] = None,
        index_of_model: Optional[int] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionRCAOutput]:
        return self.extended_detection.root_cause_analysis(
            parent_job_id,
            execute,
            wait_to_finish,
            outputs,
            index_of_model,
            timestamp,
            radius,
            status_poll,
            tries_left
        )

    # Deprecated: use self.extended_detection object instead
    def detection_what_if_analysis(
        self,
        parent_job_id: str,
        configuration: Union[WhatIf, WhatIfPanel],
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        return self.extended_detection.what_if_analysis(
            parent_job_id,
            configuration,
            execute,
            wait_to_finish,
            outputs,
            status_poll,
            tries_left
        )
