# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from time import sleep
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_anomaly_detection(client: Tim, dataset_a: pd.DataFrame):
    # Upload dataset
    new_dataset_configuration = {
        "timestampFormat": "yyyy-mm-dd HH:MM:SS",
        "timestampColumn": "Date",
        "decimalSeparator": ".",
        "timeZone": "Z",
        "name": create_random_string_with_timestamp(prefix="Test-Dataset"),
        "samplingPeriod": {
            "baseUnit": "Hour",
            "value": 1
        }
    }
    new_dataset = client.datasets.upload_dataset(dataset_a, configuration=new_dataset_configuration)
    sleep(5)
    i = 0
    while True:
        new_dataset_status = client.datasets.status_dataset_version(
            new_dataset['id'],
            new_dataset['version']['id']
        )
        status = new_dataset_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Dataset upload failed')
        if i > 90:
            raise ValueError('Dataset upload took too long')
        i += 1
        sleep(2)

    # Create use case with that dataset
    new_use_case_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Use-Case"),
        "dataset": {
            "id": new_dataset['id']
        }
    }
    new_use_case = client.use_cases.create_use_case(new_use_case_configuration)

    # Build model
    new_kpi_build_model_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Anomaly-Detection-KPI-Build-Model-Job"),
        "useCase": {
            "id": new_use_case['id']
        }
    }
    new_kpi_build_model_job = client.detection.build_kpi_model(new_kpi_build_model_job_configuration)

    # Execute and Wait to finish
    new_kpi_build_model_status = client.detection.execute(new_kpi_build_model_job['id'])
    sleep(5)
    i = 0
    while True:
        new_kpi_build_model_status = client.detection.status(new_kpi_build_model_job['id'])
        status = new_kpi_build_model_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Build KPI model job failed')
        if i > 90:
            raise ValueError('Build KPI model job took too long')
        i += 1
        sleep(2)

    # Get job list
    job_list = client.detection.job_list(
        offset=0,
        limit=10,
        use_case_id=new_use_case['id'],
        sort='-createdAt'
    )

    # Get detail
    new_kpi_build_model_job_detail = client.detection.job_details(new_kpi_build_model_job['id'])

    # Get results
    kpi_build_model_job_results = client.detection.results_table(new_kpi_build_model_job['id'])

    # Get model
    kpi_build_model_job_model = client.detection.results_model(new_kpi_build_model_job['id'])

    new_drift_detection_build_model_kolmogorov_smirnov_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Anomaly-Detection-Drift-Build-Model-Job-Kolmogorov-Smirnov"),
        "useCase": {
            "id": new_use_case['id']
        },
        "data": {
            "testRows": {
                "baseUnit": "Hour",
                "value": 1
            }
        }
    }
    new_drift_detection_build_model_kolmogorov_smirnov_job = client.detection.build_drift_model_kolmogorov_smirnov(
        new_drift_detection_build_model_kolmogorov_smirnov_job_configuration
    )
    new_drift_detection_build_model_kolmogorov_smirnov_job_status = client.detection.execute(
        new_drift_detection_build_model_kolmogorov_smirnov_job['id']
    )
    sleep(5)
    i = 0
    while True:
        new_drift_detection_build_model_kolmogorov_smirnov_job_status = client.detection.status(
            new_drift_detection_build_model_kolmogorov_smirnov_job['id']
        )
        status = new_drift_detection_build_model_kolmogorov_smirnov_job_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Build Drift model job failed')
        if i > 90:
            raise ValueError('Build Drift model job took too long')
        i += 1
        sleep(2)

    # Delete Job
    client.detection.delete_job(new_drift_detection_build_model_kolmogorov_smirnov_job['id'])
    client.detection.delete_job(new_kpi_build_model_job['id'])

    # Delete Use Case
    client.use_cases.delete_use_case(new_use_case['id'])

    # Delete Dataset
    client.datasets.delete_dataset(new_dataset['id'])

    assert len(job_list) > 0
    assert new_kpi_build_model_job_detail is not None
    assert kpi_build_model_job_results is not None
    assert kpi_build_model_job_model is not None
