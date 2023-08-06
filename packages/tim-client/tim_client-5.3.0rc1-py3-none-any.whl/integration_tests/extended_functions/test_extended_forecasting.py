# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_extended_forecasting(client: Tim, dataset_a: pd.DataFrame):
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

    new_dataset = client.upload_dataset(
        dataset=dataset_a,
        configuration=new_dataset_configuration,
        wait_to_finish=True
    )
    dataset_id = new_dataset[0]['id']

    new_use_case_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Use-Case"),
        "dataset": {
            "id": dataset_id
        }
    }
    new_use_case = client.use_cases.create_use_case(new_use_case_configuration)
    use_case_id = new_use_case['id']

    new_build_model_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Forecasting-Build-Model-Job"),
        "useCase": {
            "id": new_use_case['id']
        }
    }

    new_build_model_job = client.forecasting_build_model(
        configuration=new_build_model_job_configuration,
        execute=True,
        wait_to_finish=True
    )
    new_build_model_job_id = new_build_model_job[0]

    new_predict_job = client.forecasting_predict(
        parent_job_id=new_build_model_job_id,
        execute=False,
        wait_to_finish=False
    )
    new_predict_job_id = new_predict_job['id']

    executed_predict_job = client.execute_forecast_job(new_predict_job_id, wait_to_finish=True)

    client.forecasting.delete_job(new_predict_job_id)
    client.forecasting.delete_job(new_build_model_job_id)
    client.use_cases.delete_use_case(use_case_id)
    client.datasets.delete_dataset(dataset_id)

    assert new_build_model_job[0] is not None
    assert new_build_model_job[1] is None
    assert new_build_model_job[2] is not None
    assert new_build_model_job[3] is not None
    assert new_build_model_job[4] is not None
    assert new_build_model_job[5] is None
    assert new_build_model_job[6] is not None
    assert new_build_model_job[7] is not None
    assert new_build_model_job[8] is None
    assert new_build_model_job[9] is None
    assert executed_predict_job is not None
    assert 'response' in executed_predict_job
    assert 'status' in executed_predict_job


def test_extended_quick_forecasting(client: Tim, dataset_a: pd.DataFrame):
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

    new_quick_forecast = client.quick_forecast(
        dataset=dataset_a,
        dataset_configuration=new_dataset_configuration,
        execute=True,
        wait_to_finish=True,
        delete_items=True
    )

    assert new_quick_forecast is not None
    assert new_quick_forecast[0] is not None
    assert new_quick_forecast[1] is not None
    assert new_quick_forecast[2] is not None
