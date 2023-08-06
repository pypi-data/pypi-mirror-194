# type: ignore
from time import sleep
from typing import Union, Callable, Optional, List
from datetime import datetime
from tim.core.credentials import Credentials
from tim.endpoints import (
    UseCases,
    Detection
)
from tim.core.types import (
    Status,
    StatusResponse,
    JobExecuteResponse,
    JobResponse,
    Id,
    UseCasePost,
    WhatIf,
    WhatIfPanel,
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


class ExtendedDetection:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials
        self._use_cases = UseCases(self._credentials)
        self._detection = Detection(self._credentials)

    def poll_detect_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> StatusResponse:
        """Poll for the status and progress of a detection job.

        Parameters
        ----------
        id : str
          The ID of a detection job in the TIM repository.
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the job.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        status : Dict
          Available keys: createdAt (str), status (str), progress (float), memory (int) and CPU (int).
        """
        if tries_left < 1:
            raise ValueError("Timeout error.")
        response = self._detection.status(id)
        if status_poll:
            status_poll(response)
        if Status(response['status']).value == Status.FAILED.value:
            return response
        if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
            sleep(2)
            return self.poll_detect_status(id, status_poll, tries_left - 1)
        return response

    def results(
        self,
        id: str,  # pylint: disable=redefined-builtin
        outputs: Optional[List[DetectionResultsOptions]] = None
    ) -> DetectionResultsOutputs:
        """Retrieve the results of a detection job. You can choose which outputs you want to return by specifying the outputs.
           By default the following outputs are returned.
           ['id','details','logs','status','table','model','accuracies']

        Parameters
        ----------
        id : str
          The ID of a detection job.
        outputs : array | 
          Possible outputs are ['id','details','logs','status','table'
                                ,'model','accuracies','production_table','production_accuracies']
        Returns
        -------
        id : str | None
          The ID of a detection job for tracing.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        production_table : DataFrame | None
          Table result of a sequence.
        production_accuracies : Dict | None
          The performance metrics of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'details',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        details = self._detection.job_details(id) if 'details' in outputs else None
        logs = self._detection.job_logs(id) if 'logs' in outputs else None
        status = self._detection.status(id) if 'status' in outputs else None
        table = self._detection.results_table(id) if 'table' in outputs else None
        if 'model' in outputs:
            model = self._detection.results_model(id)
            if model == {}:
                job_details = self._detection.job_details(id)
                parent_job_id = job_details['parentJob']['id']
                model = self._detection.results_model(parent_job_id)
        else:
            model = None
        accuracies = self._detection.results_accuracies(id) if 'accuracies' in outputs else None
        production_table = self._detection.results_production_table(id) if 'production_table' in outputs else None
        production_accuracies = self._detection.results_production_accuracies(id) if 'production_accuracies' in outputs else None
        return DetectionResultsOutputs(
            id=id,
            details=details,
            logs=logs,
            status=status,
            table=table,
            model=model,
            accuracies=accuracies,
            production_table=production_table,
            production_accuracies=production_accuracies
        )

    def execute(
        self,
        id: str,  # pylint: disable=redefined-builtin
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobExecuteResponse, DetectionResultsOutputs]:
        """Execute a detection job. You can choose which outputs you want to return by specifying the outputs.
           By default none are returned.

        Parameters
        ----------
        id : str
          The ID of a detection job to execute.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job for tracing.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        production_table : DataFrame | None
          Table result of a sequence.
        production_accuracies : Dict | None
          The performance metrics of a sequence.
        """
        response = self._detection.execute(id)
        if wait_to_finish is False:
            return JobExecuteResponse(
                id=id,
                response=response,
                status='Queued'
            )
        status = self.poll_detect_status(
            id=id,
            status_poll=status_poll,
            tries_left=tries_left
        )
        if outputs is None:
            return JobExecuteResponse(
                id=id,
                response=response,
                status=status
            )
        return self.results(
            id=id,
            outputs=outputs
        )

    def build_kpi_model(
        self,
        configuration: DetectionBuildKPIModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        """ Register, execute and collect results of a detection build kpi model job.
            The KPI approach detects anomalies within a target variable.
            The build model job makes a new detection model based on a dataset id and configuration.
            You can choose to only register the job and return a detection job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        configuration : DetectionBuildKPIModel
          TIM Engine KPI model building and detection configuration.
        dataset_id : str
          The ID of a dataset in the TIM repository.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','model','accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        """
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        try:
            if not ('useCase' in configuration and 'id' in configuration['useCase']):
                raise KeyError('Use case missing in configuration')
            job_configuration = DetectionBuildKPIModel(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            create_use_case_configuration = UseCasePost(
                name=f'Quick KPI Detection - {dt_string}',
                dataset=Id(id=dataset_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = DetectionBuildKPIModel(**configuration, useCase=useCase)
        response = self._detection.build_kpi_model(job_configuration)
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def build_system_model(
        self,
        configuration: DetectionBuildSystemModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        """ Register, execute and collect results of a detection build system model job.
            The system-driven approach doesn't require a target value and detects anomalies in the whole system.
            The build model job makes a new detection model based on a dataset id and configuration.
            You can choose to only register the job and return a detection job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        configuration : DetectionBuildSystemModel
          TIM Engine System driven model building and detection configuration.
        dataset_id : str
          The ID of a dataset in the TIM repository.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','model','accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        """
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        try:
            if not ('useCase' in configuration and 'id' in configuration['useCase']):
                raise KeyError('Use case missing in configuration')
            job_configuration = DetectionBuildSystemModel(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            create_use_case_configuration = UseCasePost(
                name=f'Quick System Detection - {dt_string}',
                dataset=Id(id=dataset_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = DetectionBuildSystemModel(**configuration, useCase=useCase)
        response = self._detection.build_system_model(job_configuration)
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def build_outlier_model(
        self,
        configuration: DetectionBuildOutlierModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        try:
            if not ('useCase' in configuration and 'id' in configuration['useCase']):
                raise KeyError('Use case missing in configuration')
            job_configuration = DetectionBuildOutlierModel(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            create_use_case_configuration = UseCasePost(
                name=f'Quick Drift Detection (Kolmogorov Smirnov) - {dt_string}',
                dataset=Id(id=dataset_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = DetectionBuildOutlierModel(**configuration, useCase=useCase)
        response = self._detection.build_outlier_model(job_configuration)
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def build_drift_model_kolmogorov_smirnov(
        self,
        configuration: DetectionBuildDriftModelKolmogorovSmirnov,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        try:
            if not ('useCase' in configuration and 'id' in configuration['useCase']):
                raise KeyError('Use case missing in configuration')
            job_configuration = DetectionBuildDriftModelKolmogorovSmirnov(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            create_use_case_configuration = UseCasePost(
                name=f'Quick Drift Detection (Kolmogorov Smirnov) - {dt_string}',
                dataset=Id(id=dataset_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = DetectionBuildDriftModelKolmogorovSmirnov(**configuration, useCase=useCase)
        response = self._detection.build_drift_model_kolmogorov_smirnov(job_configuration)
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def build_drift_model_jensen_shannon(
        self,
        configuration: DetectionBuildDriftModelJensenShannon,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        try:
            if not ('useCase' in configuration and 'id' in configuration['useCase']):
                raise KeyError('Use case missing in configuration')
            job_configuration = DetectionBuildDriftModelJensenShannon(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            create_use_case_configuration = UseCasePost(
                name=f'Quick Drift Detection (Jensen Shannon) - {dt_string}',
                dataset=Id(id=dataset_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = DetectionBuildDriftModelJensenShannon(**configuration, useCase=useCase)
        response = self._detection.build_drift_model_jensen_shannon(job_configuration)
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def rebuild_kpi_model(
        self,
        parent_job_id: str,
        configuration: Optional[DetectionRebuildKPIModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        """ Register, execute and collect results of a detection rebuild kpi model job.
            The rebuild updates and extends an existing KPI model in the TIM repository.
            You can choose to only register the job and return a detection job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        parent_job_id : str
          The ID of a detection model job in the TIM repository.
        configuration : DetectionRebuildKPIModel
          TIM Engine KPI model rebuilding and detection configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        production_table : DataFrame | None
          Table result of a sequence.
        production_accuracies : Dict | None
          The performance metrics of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
                'model',
                'accuracies',
            ]
        response = self._detection.rebuild_kpi_model(
            parent_job_id=parent_job_id,
            configuration=configuration
        )
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def detect(
        self,
        parent_job_id: str,
        configuration: DetectionDetect,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        """ Register, execute and collect results of a detection detect job.
            The detect job makes a detection based on an existing model job in the TIM repository.
            You can choose to only register the job and return a detection job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table']

        Parameters
        ----------
        parent_job_id : str
          The ID of a detection model job in the TIM repository.
        configuration : DetectionDetect
          TIM Engine detection configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        production_table : DataFrame | None
          Table result of a sequence.
        production_accuracies : Dict | None
          The performance metrics of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
            ]
        response = self._detection.detect(
            parent_job_id=parent_job_id,
            configuration=configuration
        )
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )

    def results_rca(
        self,
        id: str,  # pylint: disable=redefined-builtin
        index_of_model: Optional[int] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        outputs: Optional[List[DetectionResultsRCAOptions]] = None
    ) -> DetectionRCAOutput:
        """ Return the results of a detection root cause analysis job.
            By default all possible outputs are returned: 
            ['id','details','logs','status','results']

        Parameters
        ----------
        id : str
          The ID of a detecion root cause analysis job in the TIM repository.
        index_of_model : int | None
          A model index from the parent job model.
        timestamp : 
          Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
        radius : 
          The maximum number of records to return before and after the timestamp.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','results']

        Returns
        -------
        id : str | None
          The ID of the root cause analysis job.
        details : Dict | None
          Metadata of the root cause analysis job.
        logs : list of Dict | None
          Log messages of the root cause analysis job.
        status : Dict | None
          Final status of the root cause analysis job.
        results : DataFrame | None
          Table result containing all root cause analysis values.
        """
        if outputs is None:
            outputs = [
                'id',
                'details',
                'logs',
                'status',
                'results',
            ]
        results = self._detection.results_rca(
            id=id,
            index_of_model=index_of_model,
            timestamp=timestamp,
            radius=radius
        )
        details = self._detection.job_details(id) if 'details' in outputs else None
        logs = self._detection.job_logs(id) if 'logs' in outputs else None
        status = self._detection.status(id) if 'status' in outputs else None
        return DetectionRCAOutput(
            id=id,
            details=details,
            logs=logs,
            status=status,
            results=results
        )

    def root_cause_analysis(
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
        """ Register, execute and return the results of a detection root cause analysis job.
            You can choose to only register the job and return a job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            By default the following outputs are returned: 
            ['id','results']

        Parameters
        ----------
        parent_job_id : str
          The parent detection job on which the root cause analysis was performed.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','results'].
        index_of_model : int | None
          A model index from the parent job model.
        timestamp : 
          Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
        radius : 
          The maximum number of records to return before and after the timestamp.
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsRCAOptions ->
        id : str | None
          The ID of the root cause analysis job.
        details : Dict | None
          Metadata of the root cause analysis job.
        logs : list of Dict | None
          Log messages of the root cause analysis job.
        status : Dict | None
          Final status of the root cause analysis job.
        results : DataFrame | None
          Table result containing all root cause analysis values.
        """
        if outputs is None:
            outputs = [
                'id',
                'results',
            ]
        response = self._detection.rca(parent_job_id=parent_job_id)
        if execute is False:
            return response
        job_id = response['id']
        execute_response = self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            status_poll=status_poll,
            tries_left=tries_left
        )
        if wait_to_finish is False:
            return execute_response
        return self.results_rca(
            id=job_id,
            index_of_model=index_of_model,
            timestamp=timestamp,
            radius=radius,
            outputs=outputs
        )

    def what_if_analysis(
        self,
        parent_job_id: str,
        configuration: Union[WhatIf, WhatIfPanel],
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[DetectionResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, DetectionResultsOutputs]:
        """ Register, execute and collect results of a detection what-if analysis job.
            The what-if job makes a detection based on an existing model job in the TIM repository and newly provide data.
            You can choose to only register the job and return a detection job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','table']

        Parameters
        ----------
        parent_job_id : str
          The ID of a detection job in the TIM repository.
        configuration : Dict
          TIM Engine what-if configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the detection job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        DetectionResultsOutputs ->
        id : str | None
          The ID of a detection job.
        details : Dict | None
          Metadata of the detection job.
        logs : list of Dict | None
          Log messages of the detection job.
        status : Dict | None
          Final status of the detection job.
        table : DataFrame | None
          Table result containing all predicted values.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          The performance metrics of a detection job.
        production_table : DataFrame | None
          Table result of a sequence.
        production_accuracies : Dict | None
          The performance metrics of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'table'
            ]
        response = self._detection.what_if(
            parent_job_id=parent_job_id,
            configuration=configuration
        )
        if execute is False:
            return response
        job_id = response['id']
        return self.execute(
            id=job_id,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )
