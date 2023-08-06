# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_extended_anomaly_detection(client: Tim, dataset_a: pd.DataFrame):
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

    new_kpi_build_model_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Anomaly-Detection-KPI-Build-Model-Job"),
        "useCase": {
            "id": new_use_case['id']
        }
    }
    new_kpi_build_model_job = client.detection_build_kpi_model(
        configuration=new_kpi_build_model_job_configuration,
        execute=True,
        wait_to_finish=True
    )
    new_kpi_build_model_job_id = new_kpi_build_model_job[0]

    new_detect_job_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Anomaly-Detection-Detect-Job")
    }
    new_detect_job = client.detection_detect(
        parent_job_id=new_kpi_build_model_job_id,
        configuration=new_detect_job_configuration,
        execute=False,
        wait_to_finish=False
    )
    new_detect_job_id = new_detect_job['id']

    executed_detection_job = client.execute_detection_job(id=new_detect_job_id, wait_to_finish=True)

    client.detection.delete_job(new_detect_job_id)
    client.detection.delete_job(new_kpi_build_model_job_id)
    client.use_cases.delete_use_case(use_case_id)
    client.datasets.delete_dataset(dataset_id)

    assert new_kpi_build_model_job[0] is not None
    assert new_kpi_build_model_job[1] is None
    assert new_kpi_build_model_job[2] is not None
    assert new_kpi_build_model_job[3] is not None
    assert new_kpi_build_model_job[4] is not None
    assert new_kpi_build_model_job[5] is not None
    assert new_kpi_build_model_job[6] is not None
    assert new_kpi_build_model_job[7] is None
    assert new_kpi_build_model_job[8] is None
    assert executed_detection_job is not None
    assert 'response' in executed_detection_job
    assert 'status' in executed_detection_job
