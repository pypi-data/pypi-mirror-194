# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List
import re
import pytest
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_list_workspace(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_workspace_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'userGroupId': '94cb6f31-371c-4885-98cf-c3a4c5423769',
        'sort': '-createdAd'
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/workspaces',
        status_code=200,
        json=mocked_api_response_workspace_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.workspaces.list_workspace(
        offset=arguments['offset'],
        limit=arguments['limit'],
        user_group_id=arguments['userGroupId'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_workspace_list


def test_create_workspace(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_workspace_detail: Dict[str, Any]):
    configuration = {
        "name": "Test workspace 123",
        "description": "Some interesting description",
        "userGroup": {
                "id": "9a7e960b-5071-4eb5-a372-913f7d426a2c"
        }
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/workspaces',
        status_code=200,
        json=mocked_api_response_workspace_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.workspaces.create_workspace(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_workspace_detail


def test_details_workspace(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_workspace_detail: Dict[str, Any]):
    workspace_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/workspaces/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_workspace_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.workspaces.details_workspace(workspace_id)

    assert result == mocked_api_response_workspace_detail


def test_update_workspace(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_workspace_detail: Dict[str, Any]):
    workspace_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    configuration = {
        "name": "Test workspace 456",
        "description": "Another interesting description",
        "isFavorite": False
    }

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/workspaces/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_workspace_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.workspaces.edit_workspace(workspace_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_workspace_detail


def test_delete_workspace(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_workspace_deleted: Dict[str, Any]):
    workspace_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/workspaces/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_workspace_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.workspaces.delete_workspace(workspace_id)

    assert result == mocked_api_response_workspace_deleted


def test_error_handling_in_workspace_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    workspace_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    configuration = {}

    with pytest.raises(ValueError):
        client.workspaces.list_workspace()

    with pytest.raises(ValueError):
        client.workspaces.create_workspace(configuration)

    with pytest.raises(ValueError):
        client.workspaces.details_workspace(workspace_id)

    with pytest.raises(ValueError):
        client.workspaces.edit_workspace(workspace_id, configuration)

    with pytest.raises(ValueError):
        client.workspaces.delete_workspace(workspace_id)
