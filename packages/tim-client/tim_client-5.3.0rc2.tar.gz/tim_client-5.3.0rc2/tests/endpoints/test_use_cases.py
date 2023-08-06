# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List
import re
import pytest
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_list_use_case(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_use_case_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'userGroupId': '94cb6f31-371c-4885-98cf-c3a4c5423769',
        'workspaceId': 'afe4bf18-8fce-495d-884e-b8fd463f685a',
        'datasetId': '11c82fc4-dbcd-4cce-bc36-c5dd73842dfd',
        'sort': '-createdAd',
        'isPanelData': False,
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/use-cases',
        status_code=200,
        json=mocked_api_response_use_case_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.use_cases.list_use_case(
        offset=arguments['offset'],
        limit=arguments['limit'],
        user_group_id=arguments['userGroupId'],
        workspace_id=arguments['workspaceId'],
        dataset_id=arguments['datasetId'],
        sort=arguments['sort'],
        is_panel_data=arguments['isPanelData']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_use_case_list


def test_create_use_case(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_use_case_detail: Dict[str, Any]):
    configuration = {
        "name": "Use case 123",
        "description": "Description ABC",
        "businessValue": "xyz",
        "businessObjective": "abc",
        "businessKpi": "def",
        "workspace": {
            "id": "ef47117c-5408-4603-9d6f-735f45a74ff3"
        },
        "dataset": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "isFavorite": True
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/use-cases',
        status_code=200,
        json=mocked_api_response_use_case_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.use_cases.create_use_case(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_use_case_detail


def test_details_use_case(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_use_case_detail: Dict[str, Any]):
    use_case_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/use-cases/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_use_case_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.use_cases.details_use_case(use_case_id)

    assert result == mocked_api_response_use_case_detail


def test_update_use_case(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_use_case_detail: Dict[str, Any]):
    use_case_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    configuration = {
        "name": "Use case 456"
    }

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/use-cases/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_use_case_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.use_cases.edit_use_case(use_case_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_use_case_detail


def test_delete_use_case(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_use_case_deleted: Dict[str, Any]):
    use_case_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/use-cases/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_use_case_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.use_cases.delete_use_case(use_case_id)

    assert result == mocked_api_response_use_case_deleted


def test_error_handling_in_use_case_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    use_case_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    configuration = {}

    with pytest.raises(ValueError):
        client.use_cases.list_use_case()

    with pytest.raises(ValueError):
        client.use_cases.create_use_case(configuration)

    with pytest.raises(ValueError):
        client.use_cases.details_use_case(use_case_id)

    with pytest.raises(ValueError):
        client.use_cases.edit_use_case(use_case_id, configuration)

    with pytest.raises(ValueError):
        client.use_cases.delete_use_case(use_case_id)
