# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List, Tuple
import re
import pytest
import pandas as pd
from requests_mock import Mocker
from tim import Tim


@pytest.fixture
def mocked_dataset_df_and_configuration() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    mocked_dataset_df = pd.DataFrame(
        [['2020-01-01T00:00:00Z', 1], ['2020-01-01T01:00:00Z', 2], ['2020-01-01T02:00:00Z', 3]],
        columns=['timestamp', 'value']
    )
    configuration = {
        "timestampFormat": "yyyy-mm-ddTHH:MM:SSZ",
        "timestampColumn": "timestamp",
        "decimalSeparator": ".",
        "timeZone": "Z",
        "name": "Random dataset",
        "description": "Random dataset 123",
        "samplingPeriod": {
            "baseUnit": "Hour",
            "value": 1
        },
        "workspace": {
            "id": "ef47117c-5408-4603-9d6f-735f45a74ff3"
        }
    }
    return mocked_dataset_df, configuration


def test_extended_upload_dataset_without_wait_to_finish(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_uploaded: Dict[str, Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration
    authenticated_requests_mock.request(
        'POST',
        '/api/v5/datasets/csv',
        status_code=200,
        json=mocked_api_response_dataset_uploaded,
        headers={'Content-Type': 'application/json'}
    )

    result = client.upload_dataset(
        dataset=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=False
    )

    post_datasets_csv_api_request = authenticated_requests_mock.request_history[1]
    post_datasets_csv_request_body = post_datasets_csv_api_request.text.replace('\r', '').replace('\n', '')

    assert post_datasets_csv_api_request.headers['content-type'].startswith('multipart/form-data; boundary=')
    assert 'Content-Disposition: form-data; name="configuration"; filename="configuration"{"timestampFormat": "yyyy-mm-ddTHH:MM:SSZ", "timestampColumn": "timestamp", "decimalSeparator": ".", "timeZone": "Z", "name": "Random dataset", "description": "Random dataset 123", "samplingPeriod": {"baseUnit": "Hour", "value": 1}, "workspace": {"id": "ef47117c-5408-4603-9d6f-735f45a74ff3"}, "csvSeparator": ";"}' in post_datasets_csv_request_body
    assert 'Content-Disposition: form-data; name="file"; filename="file"timestamp;value2020-01-01T00:00:00Z;12020-01-01T01:00:00Z;22020-01-01T02:00:00Z;3' in post_datasets_csv_request_body

    assert result == mocked_api_response_dataset_uploaded


def test_extended_upload_dataset_with_wait_to_finish_and_finished_upload(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_uploaded: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_api_response_dataset_version_status_finished: Dict[str, Any],
    mocked_api_response_dataset_detail: Dict[str, Any],
    mocked_api_response_dataset_log: List[Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/datasets/csv',
        status_code=200,
        json=mocked_api_response_dataset_uploaded,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.upload_dataset(
        dataset=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_dataset_version_status_finished,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result[0] == mocked_api_response_dataset_uploaded
    assert result[1] == mocked_api_response_dataset_detail
    assert result[2] == mocked_api_response_dataset_log


def test_extended_upload_dataset_with_wait_to_finish_and_failed_upload(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_uploaded: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_api_response_dataset_version_status_failed: Dict[str, Any],
    mocked_api_response_dataset_log: List[Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/datasets/csv',
        status_code=200,
        json=mocked_api_response_dataset_uploaded,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.upload_dataset(
        dataset=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_dataset_version_status_failed,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result[0] == mocked_api_response_dataset_uploaded
    assert result[1] is None
    assert result[2] == mocked_api_response_dataset_log


def test_extended_upload_dataset_with_wait_to_finish_and_timeout_reached(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_uploaded: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/datasets/csv',
        status_code=200,
        json=mocked_api_response_dataset_uploaded,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    with pytest.raises(ValueError):
        client.upload_dataset(
            dataset=mocked_dataset_df,
            configuration=configuration,
            wait_to_finish=True,
            tries_left=2
        )


def test_extended_update_dataset_without_wait_to_finish(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_updated: Dict[str, Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/csv'),
        status_code=200,
        json=mocked_api_response_dataset_updated,
        headers={'Content-Type': 'application/json'}
    )

    result = client.update_dataset(
        dataset_id=dataset_id,
        dataset_version=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=False
    )

    patch_datasets_csv_api_request = authenticated_requests_mock.request_history[1]
    patch_datasets_csv_request_body = patch_datasets_csv_api_request.text.replace('\r', '').replace('\n', '')

    assert patch_datasets_csv_api_request.headers['content-type'].startswith('multipart/form-data; boundary=')
    assert 'Content-Disposition: form-data; name="configuration"; filename="configuration"{"timestampFormat": "yyyy-mm-ddTHH:MM:SSZ", "timestampColumn": "timestamp", "decimalSeparator": ".", "timeZone": "Z", "name": "Random dataset", "description": "Random dataset 123", "samplingPeriod": {"baseUnit": "Hour", "value": 1}, "workspace": {"id": "ef47117c-5408-4603-9d6f-735f45a74ff3"}, "csvSeparator": ";"}' in patch_datasets_csv_request_body
    assert 'Content-Disposition: form-data; name="file"; filename="file"timestamp;value2020-01-01T00:00:00Z;12020-01-01T01:00:00Z;22020-01-01T02:00:00Z;3' in patch_datasets_csv_request_body

    assert result == mocked_api_response_dataset_updated


def test_extended_update_dataset_with_wait_to_finish_and_finished_update(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_updated: Dict[str, Any],
    mocked_api_response_dataset_detail: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_api_response_dataset_version_status_finished: Dict[str, Any],
    mocked_api_response_dataset_log: List[Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/csv'),
        status_code=200,
        json=mocked_api_response_dataset_updated,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.update_dataset(
        dataset_id=dataset_id,
        dataset_version=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_dataset_version_status_finished,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result[0] == mocked_api_response_dataset_updated
    assert result[1] == mocked_api_response_dataset_detail
    assert result[2] == mocked_api_response_dataset_log


def test_extended_update_dataset_with_wait_to_finish_and_failed_update(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_updated: Dict[str, Any],
    mocked_api_response_dataset_detail: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_api_response_dataset_version_status_failed: Dict[str, Any],
    mocked_api_response_dataset_log: List[Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/csv'),
        status_code=200,
        json=mocked_api_response_dataset_updated,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.update_dataset(
        dataset_id=dataset_id,
        dataset_version=mocked_dataset_df,
        configuration=configuration,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_dataset_version_status_failed,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result[0] == mocked_api_response_dataset_updated
    assert result[1] == mocked_api_response_dataset_detail
    assert result[2] == mocked_api_response_dataset_log


def test_extended_update_dataset_with_wait_to_finish_and_timeout_reached(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_updated: Dict[str, Any],
    mocked_api_response_dataset_version_status_running: Dict[str, Any],
    mocked_dataset_df_and_configuration: Tuple[pd.DataFrame, Dict[str, Any]]
):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'
    mocked_dataset_df, configuration = mocked_dataset_df_and_configuration

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/csv'),
        status_code=200,
        json=mocked_api_response_dataset_updated,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    with pytest.raises(ValueError):
        client.update_dataset(
            dataset_id=dataset_id,
            dataset_version=mocked_dataset_df,
            configuration=configuration,
            wait_to_finish=True,
            tries_left=2
        )
