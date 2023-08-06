# type: ignore
from time import sleep
from typing import Union, Callable, Optional, List
from datetime import datetime
from pandas import DataFrame
from tim.core.credentials import Credentials
from tim.endpoints import (
    UseCases,
    Datasets,
    Forecasting
)
from tim.extended_functions.extended_datasets import ExtendedDatasets
from tim.core.types import (
    UploadDatasetConfiguration,
    DatasetStatusResponse,
    Status,
    StatusResponse,
    ForecastingBuildModel,
    JobExecuteResponse,
    JobResponse,
    ForecastingResultsOptions,
    ForecastingResultsOutputs,
    Id,
    UseCasePost,
    ForecastingRebuildModel,
    ForecastingRetrainModel,
    ForecastingPredict,
    ForecastingResultsRCAOptions,
    RCAResults,
    ForecastingRCAOutput,
    WhatIf,
    WhatIfPanel,
    QuickForecast
)


class ExtendedForecasting:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials
        self._use_cases = UseCases(self._credentials)
        self._datasets = Datasets(self._credentials)
        self._forecasting = Forecasting(self._credentials)
        self._extended_datasets = ExtendedDatasets(self._credentials)

    def poll_forecast_status(
        self,
        id: str,  # pylint: disable=redefined-builtin
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> StatusResponse:
        """Poll for the status and progress of a forecasting job.

        Parameters
        ----------
        id : str
          The ID of a forecasting job in the TIM repository.
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
        response = self._forecasting.status(id)
        if status_poll:
            status_poll(response)
        if Status(response['status']).value == Status.FAILED.value:
            return response
        if Status(response['status']).value != Status.FINISHED.value and Status(response['status']).value != Status.FINISHED_WITH_WARNING.value:
            sleep(2)
            return self.poll_forecast_status(
                id,
                status_poll,
                tries_left - 1
            )
        return response

    def results(
        self,
        id: str,  # pylint: disable=redefined-builtin
        outputs: Optional[List[ForecastingResultsOptions]] = None
    ) -> ForecastingResultsOutputs:
        """Retrieve the results of a forecast job. You can choose which outputs you want to return by specifying the outputs.
           By default all possible outputs are returned.

        Parameters
        ----------
        id : str
          The ID of a forecast job.
        outputs : array | 
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        Returns
        -------
        id : str | None
          The ID of a forecast job for tracing.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'details',
                'logs',
                'status',
                'table',
                'production_forecast',
                'model',
                'accuracies',
                'production_table',
                'production_accuracies'
            ]
        details = self._forecasting.job_details(id) if 'details' in outputs else None
        logs = self._forecasting.job_logs(id) if 'logs' in outputs else None
        status = self._forecasting.status(id) if 'status' in outputs else None
        table = self._forecasting.results_table(id) if 'table' in outputs else None
        production_forecast = self._forecasting.results_production_forecast(id) if 'production_forecast' in outputs else None
        if 'model' in outputs:
            model = self._forecasting.results_model(id)
            if model == {}:
                job_details = self._forecasting.job_details(id)
                parent_job_id = job_details['parentJob']['id']
                model = self._forecasting.results_model(parent_job_id)
        else:
            model = None
        accuracies = self._forecasting.results_accuracies(id) if 'accuracies' in outputs else None
        production_table = self._forecasting.results_production_table(id) if 'production_table' in outputs else None
        production_accuracies = self._forecasting.results_production_accuracies(id) if 'production_accuracies' in outputs else None
        return ForecastingResultsOutputs(
            id=id,
            details=details,
            logs=logs,
            status=status,
            table=table,
            production_forecast=production_forecast,
            model=model,
            accuracies=accuracies,
            production_table=production_table,
            production_accuracies=production_accuracies
        )

    def execute(
        self,
        id: str,  # pylint: disable=redefined-builtin
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobExecuteResponse, ForecastingResultsOutputs]:
        """Execute a forecast job. You can choose which outputs you want to return by specifying the outputs.
           By default none are returned.

        Parameters
        ----------
        id : str
          The ID of a forecast job to execute.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
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
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job for tracing.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
        """
        response = self._forecasting.execute(id)
        if wait_to_finish is False:
            return JobExecuteResponse(
                id=id,
                response=response,
                status='Queued'
            )
        status = self.poll_forecast_status(
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

    def build_model(
        self,
        configuration: ForecastingBuildModel,
        dataset_id: Optional[str] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        """ Register, execute and collect results of a forecasting build model job.
            The build model job makes a new forecasting model based on a dataset id and configuration.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        configuration : ForecastingBuildModel
          TIM Engine model building and forecasting configuration.
        dataset_id : str
          The ID of a dataset in the TIM repository.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
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
            job_configuration = ForecastingBuildModel(**configuration)
        except Exception as err:
            if dataset_id is None:
                raise ValueError(
                    "'No dataset provided, please add a dataset id or link to an existing use case with data, in the configuration.'"
                ) from err
            try:
                use_case_name = configuration['name']
            except Exception:
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                use_case_name = f'Quick Forecast - {dt_string}'
            dataset_details = self._datasets.details_dataset(dataset_id)
            workspace_id = dataset_details['workspace']['id']
            create_use_case_configuration = UseCasePost(
                name=use_case_name,
                dataset=Id(id=dataset_id),
                workspace=Id(id=workspace_id)
            )
            useCase = self._use_cases.create_use_case(create_use_case_configuration)
            job_configuration = ForecastingBuildModel(**configuration, useCase=useCase)
        response = self._forecasting.build_model(job_configuration)
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

    def predict(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingPredict] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        """ Register, execute and collect results of a forecasting predict job.
            The predict job makes a prediction based on an existing model job in the TIM repository.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table']

        Parameters
        ----------
        parent_job_id : str
          The ID of a forecasting model job in the TIM repository.
        configuration : ForecastingPredict
          TIM Engine forecasting prediction configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
        """
        if outputs is None:
            outputs = [
                'id',
                'logs',
                'status',
                'table',
            ]
        response = self._forecasting.predict(
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

    def rebuild_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRebuildModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        """ Register, execute and collect results of a forecasting rebuild model job.
            The rebuild model job updates and extends an existing model in the TIM repository.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        parent_job_id : str
          The ID of a forecasting model job in the TIM repository.
        configuration : ForecastingRebuildModel
          TIM Engine forecasting rebuild configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
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
        response = self._forecasting.rebuild_model(
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

    def retrain_model(
        self,
        parent_job_id: str,
        configuration: Optional[ForecastingRetrainModel] = None,
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        """ Register, execute and collect results of a forecasting retrain model job.
            The retrain model job updates the coefficients of an existing model in the TIM repository.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','logs','status','table','model','accuracies']

        Parameters
        ----------
        parent_job_id : str
          The ID of a forecasting model job in the TIM repository.
        configuration : ForecastingRetrainModel
          TIM Engine forecasting retrain configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        production_table : DataFrame | None
          Table result containing the predicted values of a sequence.
        production_accuracies : Dict | None
          Accuracy metrics calculated by TIM on predicted values of a sequence.
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
        response = self._forecasting.retrain_model(
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
        indices_of_model: Optional[List[int]] = None,
        parent_job_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        outputs: Optional[List[ForecastingResultsRCAOptions]] = None,
    ) -> ForecastingRCAOutput:
        """ Return the results of a root cause analysis job.
            By default all possible outputs are returned:
            ['id','details','logs','status','results']

        Parameters
        ----------
        id : str
          The ID of a forecasting root cause analysis job in the TIM repository.
        indices_of_model : list of int
          The model indices from the parent job model.
        parent_job_id : str | None
          The parent forecasting job on which the root cause analysis was performed.
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
                'status'
                'results',
            ]
        if indices_of_model is None:
            if parent_job_id is None:
                job_details = self._forecasting.job_details(id=id)
                parent_job_id = job_details['parentJob']['id']
            parent_job_details = self._forecasting.job_details(id=parent_job_id)
            model_id = parent_job_details['parentJob'] if parent_job_details['type'] in ['predict', 'what-if'] else parent_job_id
            results_model = self._forecasting.results_model(model_id)
            indices_of_model = [f['index'] for f in results_model['model']['modelZoo']['models']]

        results = []
        for index_of_model in indices_of_model:
            result = self._forecasting.results_rca(
                id=id,
                index_of_model=index_of_model,
                timestamp=timestamp,
                radius=radius
            )
            results.append(RCAResults(indexOfModel=index_of_model, results=result))
        details = self._forecasting.job_details(id) if 'details' in outputs else None
        logs = self._forecasting.job_logs(id) if 'logs' in outputs else None
        status = self._forecasting.status(id) if 'status' in outputs else None
        return ForecastingRCAOutput(
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
        outputs: Optional[List[ForecastingResultsRCAOptions]] = None,
        indices_of_model: Optional[List[int]] = None,
        timestamp: Optional[str] = None,
        radius: Optional[int] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingRCAOutput]:
        """ Register, execute and return the results of a root cause analysis job.
            You can choose to only register the job and return a job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            By default the following outputs are returned: 
            ['id','results']

        Parameters
        ----------
        parent_job_id : str
          The parent forecasting job on which the root cause analysis was performed.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','results'].
        indices_of_model : list of int
          The model indices from the parent job model.
        timestamp : 
          Selected timestamp to retrieve RCA results for; if not provided, the last timestamp of the results table is taken.
        radius : 
          The maximum number of records to return before and after the timestamp.
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingRCAOutput ->
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
        response = self._forecasting.rca(parent_job_id=parent_job_id)
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
            indices_of_model=indices_of_model,
            timestamp=timestamp,
            radius=radius,
            parent_job_id=parent_job_id,
            outputs=outputs
        )

    def what_if_analysis(
        self,
        parent_job_id: str,
        configuration: Union[WhatIf, WhatIfPanel],
        execute: bool = True,
        wait_to_finish: bool = True,
        outputs: Optional[List[ForecastingResultsOptions]] = None,
        status_poll: Optional[Callable[[StatusResponse], None]] = None,
        tries_left: int = 300
    ) -> Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]:
        """ Register, execute and collect results of a forecasting what-if analysis job.
            The what-if job makes a prediction based on an existing model job in the TIM repository and newly provide data.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','table']

        Parameters
        ----------
        parent_job_id : str
          The ID of a forecasting job in the TIM repository.
        configuration : Dict
          TIM Engine what-if configuration.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast','model','accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.

        Returns
        -------
        if execute is false:
        JobResponse : Dict | None

        if wait_to_finish is false:
        JobExecuteResponse : Dict | None

        else:
        ForecastingResultsOutputs ->
        id : str | None
          The ID of a forecast job.
        details : Dict | None
          Metadata of the forecasting job.
        logs : list of Dict | None
          Log messages of the forecasting job.
        status : Dict | None
          Final status of the forecasting job.
        table : DataFrame | None
          Table result containing all predicted values.
        production_forecast : DataFrame | None
          Table result containing only the production forecast.
        model :  Dict | None
          Contains the model and contextual information about the model.
        accuracies : Dict | None
          Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
        """
        if outputs is None:
            outputs = [
                'id',
                'table'
            ]
        response = self._forecasting.what_if(
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
        """ Register, execute and collect results of a forecasting build model job from a new dataset.
            The quick forecast offers much flexibility in setting up a forecasting job within TIM and easily clean up afterwards.
            You can choose to only register the job and return a forecasting job ID.
            You can also choose to already start the execution of the registered job.
            You can also choose to wait for the job to finish.
            Lastly you can choose which outputs are returned by the function.
            By default the following outputs are returned: 
            ['id','status','table']

        Parameters
        ----------
        dataset : DataFrame
        job_configuration : ForecastingBuildModel
          TIM Engine model building and forecasting configuration.
        workspace_id : str
          The ID of a workspace in the TIM repository.
        dataset_configuration : UploadDatasetConfiguration
            Metadata of the dataset
            Available keys are: 
            timestampFormat, timestampColumn, decimalSeparator, csvSeparator, timeZone,
            timeZoneName, groupKeys, name, description, samplingPeriod and workspace.
        execute : bool, Optional
          If set to False, the function will return once the job has been registered.
        wait_to_finish : bool, Optional
          Wait for all results to be calculated before returning. This parameter is used only if execute is set to True.
          If set to False, the function will return once the job has started the execution process.
        outputs : array, Optional
          Possible outputs are ['id','details','logs','status','table','production_forecast'
                                ,'model','accuracies','production_table','production_accuracies']
        status_poll : Callable, Optional
          A callback function to poll for the status and progress of the forecasting job execution.
        tries_left: int
          Number of iterations the function will loop to fetch the job status before sending a timeout error.
        delete_items: bool
          Removes all content within TIM after returning the results.

        Returns
        -------
        upload_response: Dict | None
        forecasting_response: NamedTuple
          if execute is false:
          JobResponse : Dict | None

          if wait_to_finish is false:
          JobExecuteResponse : Dict | None

          else:
          ForecastingResultsOutputs ->
          id : str | None
            The ID of a forecast job.
          details : Dict | None
            Metadata of the forecasting job.
          logs : list of Dict | None
            Log messages of the forecasting job.
          status : Dict | None
            Final status of the forecasting job.
          table : DataFrame | None
            Table result containing all predicted values.
          production_forecast : DataFrame | None
            Table result containing only the production forecast.
          model :  Dict | None
            Contains the model and contextual information about the model.
          accuracies : Dict | None
            Accuracy metrics calculated by TIM in case of inSample or outOfSample results.
          production_table : DataFrame | None
            Table result containing the predicted values of a sequence.
          production_accuracies : Dict | None
            Accuracy metrics calculated by TIM on predicted values of a sequence.
        delete_response: Dict | None
        """
        if job_configuration is None:
            job_configuration = ForecastingBuildModel()
        if dataset_configuration is None:
            dataset_configuration = UploadDatasetConfiguration()
        if outputs is None:
            outputs = [
                'id',
                'status',
                'table',
            ]
        if delete_items is True and (wait_to_finish is False or execute is False):
            raise ValueError("'Delete_items' can only be True when both 'wait_to_finish' and 'execute' are True. Change 'wait_to_finish' and 'execute' to True to use the 'delete_items' parameter.")
        configuration = job_configuration.copy()
        try:
            use_case_name = job_configuration['name']
        except Exception:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            use_case_name = f'Quick Forecast - {dt_string}'
            configuration['name'] = use_case_name
        upload_dataset_configuration = dataset_configuration.copy()
        if workspace_id is not None:
            upload_dataset_configuration['workspace'] = Id(id=workspace_id)
        try:
            upload_dataset_configuration['name']
        except Exception:
            upload_dataset_configuration['name'] = use_case_name
        upload_dataset = self._extended_datasets.upload_dataset(
            dataset=dataset,
            configuration=upload_dataset_configuration,
            wait_to_finish=True,
            status_poll=status_poll,
            tries_left=tries_left
        )
        upload_response = upload_dataset.response
        dataset_id = upload_response['id']
        forecasting_build_model = self.build_model(
            configuration=configuration,
            dataset_id=dataset_id,
            execute=execute,
            wait_to_finish=wait_to_finish,
            outputs=outputs,
            status_poll=status_poll,
            tries_left=tries_left
        )
        delete_response = self._datasets.delete_dataset(id=dataset_id) if delete_items else None
        return QuickForecast(
            upload_response=upload_response,
            forecast_response=forecasting_build_model,
            delete_response=delete_response
        )
