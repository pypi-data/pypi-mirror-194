# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from time import sleep
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_forecasting(client: Tim, dataset_a: pd.DataFrame):
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
    new_build_model_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Forecasting-Build-Model-Job"),
        "useCase": {
            "id": new_use_case['id']
        }
    }
    new_build_model_job = client.forecasting.build_model(new_build_model_job_configuration)

    # Execute and Wait to finish
    new_build_model_status = client.forecasting.execute(new_build_model_job['id'])
    sleep(5)
    i = 0
    while True:
        new_build_model_status = client.forecasting.status(new_build_model_job['id'])
        status = new_build_model_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Build model job failed')
        if i > 90:
            raise ValueError('Build model job took too long')
        i += 1
        sleep(2)

    # Get job list
    job_list = client.forecasting.job_list(
        offset=0,
        limit=10,
        use_case_id=new_use_case['id'],
        sort='-createdAt'
    )

    # Get detail
    new_build_model_job_detail = client.forecasting.job_details(new_build_model_job['id'])

    # Get results
    build_model_job_results = client.forecasting.results_table(new_build_model_job['id'])

    # Get model
    build_model_job_model = client.forecasting.results_model(new_build_model_job['id'])

    # Delete Job
    client.forecasting.delete_job(new_build_model_job['id'])

    # Delete Use Case
    client.use_cases.delete_use_case(new_use_case['id'])

    # Delete Dataset
    client.datasets.delete_dataset(new_dataset['id'])

    assert len(job_list) > 0
    assert new_build_model_job_detail is not None
    assert build_model_job_results is not None
    assert build_model_job_model is not None
