# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List, Tuple
import re
import pytest
import pandas as pd
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_upload_dataset(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_uploaded: Dict[str, Any]):
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

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/datasets/csv',
        status_code=200,
        json=mocked_api_response_dataset_uploaded,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.upload_dataset(
        mocked_dataset_df,
        configuration=configuration
    )

    latest_api_request = authenticated_requests_mock.request_history[-1]
    request_body = latest_api_request.text.replace('\r', '').replace('\n', '')

    assert latest_api_request.headers['content-type'].startswith('multipart/form-data; boundary=')
    assert 'Content-Disposition: form-data; name="configuration"; filename="configuration"{"timestampFormat": "yyyy-mm-ddTHH:MM:SSZ", "timestampColumn": "timestamp", "decimalSeparator": ".", "timeZone": "Z", "name": "Random dataset", "description": "Random dataset 123", "samplingPeriod": {"baseUnit": "Hour", "value": 1}, "workspace": {"id": "ef47117c-5408-4603-9d6f-735f45a74ff3"}, "csvSeparator": ";"}' in request_body
    assert 'Content-Disposition: form-data; name="file"; filename="file"timestamp;value2020-01-01T00:00:00Z;12020-01-01T01:00:00Z;22020-01-01T02:00:00Z;3' in request_body
    assert result == mocked_api_response_dataset_uploaded


def test_update_dataset(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_updated: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'
    mocked_dataset_df = pd.DataFrame(
        [['2020-01-01T00:00:00Z', 1], ['2020-01-01T01:00:00Z', 2], ['2020-01-01T02:00:00Z', 3]],
        columns=['timestamp', 'value']
    )
    configuration = {
        "timestampFormat": "yyyy-mm-ddTHH:MM:SSZ",
        "timestampColumn": "timestamp",
        "decimalSeparator": "."
    }

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/csv'),
        status_code=200,
        json=mocked_api_response_dataset_updated,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.update_dataset(
        dataset_id,
        mocked_dataset_df,
        configuration=configuration
    )

    latest_api_request = authenticated_requests_mock.request_history[-1]
    request_body = latest_api_request.text.replace('\r', '').replace('\n', '')

    assert latest_api_request.headers['content-type'].startswith('multipart/form-data; boundary=')
    assert 'Content-Disposition: form-data; name="configuration"; filename="configuration"{"timestampFormat": "yyyy-mm-ddTHH:MM:SSZ", "timestampColumn": "timestamp", "decimalSeparator": ".", "csvSeparator": ";"}' in request_body
    assert 'Content-Disposition: form-data; name="file"; filename="file"timestamp;value2020-01-01T00:00:00Z;12020-01-01T01:00:00Z;22020-01-01T02:00:00Z;3' in request_body
    assert result == mocked_api_response_dataset_updated


def test_list_dataset(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'workspaceId': 'afe4bf18-8fce-495d-884e-b8fd463f685a',
        'sort': '-createdAd',
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/datasets',
        status_code=200,
        json=mocked_api_response_dataset_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.list_dataset(
        offset=arguments['offset'],
        limit=arguments['limit'],
        workspace_id=arguments['workspaceId'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_dataset_list


def test_delete_dataset_list(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_deleted: Dict[str, Any]):
    arguments = {
        'from': '2020-01-01 01:02:03.000Z',
        'to': '2021-02-03 04:05:01.000Z',
        'workspaceId': 'afe4bf18-8fce-495d-884e-b8fd463f685a'
    }

    authenticated_requests_mock.request(
        'DELETE',
        '/api/v5/datasets',
        status_code=200,
        json=mocked_api_response_dataset_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.delete_dataset_list(
        workspace_id=arguments['workspaceId'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_dataset_deleted


def test_details_dataset(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_detail: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.details_dataset(dataset_id)

    assert result == mocked_api_response_dataset_detail


def test_edit_dataset_details(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_detail: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    configuration = {
        "name": "Dataset 456 XYZ",
        "description": "Description description..."
    }

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.edit_dataset_details(dataset_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_dataset_detail


def test_delete_dataset(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_deleted: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.delete_dataset(dataset_id)

    assert result == mocked_api_response_dataset_deleted


def test_dataset_logs(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_log: List[Dict[str, Any]]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.dataset_logs(dataset_id)

    assert result == mocked_api_response_dataset_log


def test_logs_dataset_version(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_log: List[Dict[str, Any]]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    dataset_version_id = '64d94106-efd6-4247-82d0-1c3dfdcc6c56'
    arguments = {
        'offset': 10,
        'limit': 20
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_dataset_log,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.logs_dataset_version(
        dataset_id,
        dataset_version_id,
        offset=arguments['offset'],
        limit=arguments['limit']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_dataset_log


def test_list_dataset_versions(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_versions_list: List[Dict[str, Any]]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    arguments = {
        'offset': 10,
        'limit': 20
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions'),
        status_code=200,
        json=mocked_api_response_dataset_versions_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.list_dataset_versions(
        dataset_id,
        offset=arguments['offset'],
        limit=arguments['limit']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_dataset_versions_list


def test_details_dataset_version(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_versions_detail: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    dataset_version_id = '64d94106-efd6-4247-82d0-1c3dfdcc6c56'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_versions_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.details_dataset_version(
        dataset_id,
        dataset_version_id
    )

    assert result == mocked_api_response_dataset_versions_detail


def test_delete_dataset_version(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_deleted: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    dataset_version_id = '64d94106-efd6-4247-82d0-1c3dfdcc6c56'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_dataset_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.delete_dataset_version(
        dataset_id,
        dataset_version_id
    )

    assert result == mocked_api_response_dataset_deleted


def test_status_dataset_version(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_dataset_version_status_running: Dict[str, Any]):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    dataset_version_id = '64d94106-efd6-4247-82d0-1c3dfdcc6c56'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.datasets.status_dataset_version(
        dataset_id,
        dataset_version_id
    )

    assert result == mocked_api_response_dataset_version_status_running


def test_slice_dataset_version(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_slice_table: Tuple[pd.DataFrame, str]
):
    dataset_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    dataset_version_id = '64d94106-efd6-4247-82d0-1c3dfdcc6c56'
    configuration = {
        "outputFormat": "ZIP",
        "rows": [
            {
                "from": "2021-01-01 00:00:00Z",
                "to": "2021-01-31 00:00:00Z"
            }
        ],
        "columns": [
            1,
            3,
            "wind"
        ],
        "targetColumn": "y",
        "imputation": {
            "type": "Linear",
            "maxGapLength": 0
        },
        "timeScale": {
            "baseUnit": "Hour",
            "value": 1
        },
        "aggregation": "Mean",
        "preprocessors": [
            {
                "type": "CategoryFilter"
            }
        ],
        "plotlyFriendly": True,
        "includeWasImputed": True
    }

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/slice'),
        status_code=200,
        text=mocked_api_response_dataset_slice_table[1],
        headers={'Content-Type': 'text/csv'}
    )

    result = client.datasets.slice_dataset_version(
        dataset_id,
        dataset_version_id,
        configuration=configuration
    )

    assert mocked_api_response_dataset_slice_table[0].equals(result)


def test_error_handling_in_dataset_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    dataset_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    dataset_version_id = '1cd40909-c572-44ad-812e-74ef800758d9'
    dataset_df = pd.DataFrame()
    configuration = {}

    with pytest.raises(ValueError):
        client.datasets.upload_dataset(dataset_df, configuration)

    with pytest.raises(ValueError):
        client.datasets.update_dataset(dataset_id, dataset_df, configuration)

    with pytest.raises(ValueError):
        client.datasets.list_dataset()

    with pytest.raises(ValueError):
        client.datasets.delete_dataset_list(dataset_id)

    with pytest.raises(ValueError):
        client.datasets.details_dataset(dataset_id)

    with pytest.raises(ValueError):
        client.datasets.edit_dataset_details(dataset_id, configuration)

    with pytest.raises(ValueError):
        client.datasets.delete_dataset(dataset_id)

    with pytest.raises(ValueError):
        client.datasets.dataset_logs(dataset_id)

    with pytest.raises(ValueError):
        client.datasets.logs_dataset_version(dataset_id, dataset_version_id)

    with pytest.raises(ValueError):
        client.datasets.list_dataset_versions(dataset_id)

    with pytest.raises(ValueError):
        client.datasets.details_dataset_version(dataset_id, dataset_version_id)

    with pytest.raises(ValueError):
        client.datasets.delete_dataset_version(dataset_id, dataset_version_id)

    with pytest.raises(ValueError):
        client.datasets.status_dataset_version(dataset_id, dataset_version_id)

    with pytest.raises(ValueError):
        client.datasets.slice_dataset_version(dataset_id, dataset_version_id)
