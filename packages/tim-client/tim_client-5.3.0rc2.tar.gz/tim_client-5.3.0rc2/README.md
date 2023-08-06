# TIM Python Client

TIM, or Tangent Information Modeler, is Tangent Works’ automatic model building engine. It is designed specifically for time-series forecasting and anomaly detection.

The TIM Python client introduces an easy and fast way to use TIM in any Python project. As an abstraction over [TIM's API](https://tim-platform.tangent.works/api/v5/swagger-ui.html), it encapsulates the logic into useful and performant functions helping users go from time-series data to insights that can generate business value.

## Usage

### Installation

To install the package run: `pip install tim-client`

### Initialization

```python
import tim

client = tim.Tim(email='',password='')
```

### Error handling

Minimal validation is performed by the Tim client, errors will be raised by the server.

### Documentation

Full documentation of the API can be found at: [https://docs.tangent.works](https://docs.tangent.works)

### Examples

For examples, code templates and case studies using the Python Client, please visit the Tangent Works GitHub page here: [https://github.com/Tangent-Works](https://github.com/Tangent-Works)

### Methods

The TIM Python client is a Python SDK to use the TIM Platform (v5) and is organized around the TIM API which can be found here: [https://tim-platform.tangent.works/api/v5/swagger-ui.html#/](https://tim-platform.tangent.works/api/v5/swagger-ui.html#/)
Its exists in two levels. The first level consists of methods that call the API endpoints directly. This includes the following:

```python
client.user_groups.list_user_group
client.user_groups.create_user_group
client.user_groups.details_user_group
client.user_groups.update_user_group
client.user_groups.delete_user_group

client.workspaces.list_workspace
client.workspaces.create_workspace
client.workspaces.details_workspace
client.workspaces.edit_workspace
client.workspaces.delete_workspace

client.datasets.upload_dataset
client.datasets.update_dataset
client.datasets.list_dataset
client.datasets.delete_dataset_list
client.datasets.details_dataset
client.datasets.edit_dataset_details
client.datasets.delete_dataset
client.datasets.dataset_logs
client.datasets.logs_dataset_version
client.datasets.list_dataset_versions
client.datasets.details_dataset_version
client.datasets.delete_dataset_version
client.datasets.status_dataset_version
client.datasets.slice_dataset_version

client.use_cases.list_use_case
client.use_cases.create_use_case
client.use_cases.details_use_case
client.use_cases.edit_use_case
client.use_cases.delete_use_case

client.experiments.list_experiment
client.experiments.create_experiment
client.experiments.details_experiment
client.experiments.edit_experiment
client.experiments.delete_experiment

client.forecasting.build_model
client.forecasting.upload_model
client.forecasting.rebuild_model
client.forecasting.retrain_model
client.forecasting.predict
client.forecasting.rca
client.forecasting.what_if
client.forecasting.job_list
client.forecasting.delete_job_list
client.forecasting.job_details
client.forecasting.delete_job
client.forecasting.copy_job
client.forecasting.execute
client.forecasting.job_logs
client.forecasting.status
client.forecasting.status_collect
client.forecasting.results_table
client.forecasting.results_production_forecast
client.forecasting.results_model
client.forecasting.results_accuracies
client.forecasting.results_rca
client.forecasting.results_production_table
client.forecasting.results_production_accuracies

client.detection.build_kpi_model
client.detection.build_system_model
client.detection.build_outlier_model
client.detection.build_drift_model_kolmogorov_smirnov
client.detection.build_drift_model_jensen_shannon
client.detection.upload_model
client.detection.rebuild_kpi_model
client.detection.detect
client.detection.rca
client.detection.what_if
client.detection.jobs_list
client.detection.delete_job_list
client.detection.job_details
client.detection.delete_job
client.detection.copy_job
client.detection.execute
client.detection.job_logs
client.detection.status
client.detection.status_collect
client.detection.results_table
client.detection.results_model
client.detection.results_accuracies
client.detection.results_rca
client.detection.results_production_table
client.detection.results_production_accuracies

client.licenses.details_license
client.licenses.storage_license

client.users.details_user

client.telemetry.dataset_calls
client.telemetry.job_calls
```

Secondly, higher level functions exist to facilitate the use of TIM and setting up MLOps pipelines through Python. This includes the following methods:

```python
client.poll_dataset_version_status
client.poll_dataset_version_status
client.upload_dataset
client.update_dataset

client.poll_forecast_status
client.forecasting_job_results
client.execute_forecast_job
client.forecasting_build_model
client.forecasting_predict
client.forecasting_rebuild_model
client.forecasting_retrain_model
client.forecasting_results_rca
client.forecasting_root_cause_analysis
client.forecasting_what_if_analysis
client.quick_forecast

client.poll_detect_status
client.detection_job_results
client.execute_detection_job
client.detection_build_kpi_model
client.detection_build_system_model
client.detection_build_outlier_model
client.detection_build_drift_model_kolmogorov_smirnov
client.detection_build_drift_model_jensen_shannon
client.detection_rebuild_kpi_model
client.detection_detect
client.detection_results_rca
client.detection_root_cause_analysis
client.detection_what_if_analysis
```

## About Tangent Works

Tangent Works delivers forecasting and anomaly detection capabilities for time series data in a fast, accurate and explainable way. This enables users to drive business value from predictive analytics, empowers them to take informed decisions and helps them improve processes.

TIM has already been recognized as a winner in multiple competitions, including GEFCom 2017 and the 2017 ANDRITZ Hackathon.
