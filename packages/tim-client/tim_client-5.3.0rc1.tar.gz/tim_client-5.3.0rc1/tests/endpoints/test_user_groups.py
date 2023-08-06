# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List
import re
import pytest
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_list_user_group(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_group_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'sort': '-createdAd'
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/user-groups',
        status_code=200,
        json=mocked_api_response_user_group_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.user_groups.list_user_group(
        offset=arguments['offset'],
        limit=arguments['limit'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_user_group_list


def test_create_user_group(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_group_detail: Dict[str, Any]):
    configuration = {
        "name": "ABC DEF",
        "users": []
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/user-groups',
        status_code=200,
        json=mocked_api_response_user_group_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.user_groups.create_user_group(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_user_group_detail


def test_details_user_group(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_group_detail: Dict[str, Any]):
    user_group_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/user-groups/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_user_group_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.user_groups.details_user_group(user_group_id)

    assert result == mocked_api_response_user_group_detail


def test_update_user_group(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_group_detail: Dict[str, Any]):
    user_group_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    configuration = {
        "name": "Test user group 2",
        "description": "XYZ456",
        "users": []
    }

    authenticated_requests_mock.request(
        'PUT',
        re.compile('/api/v5/user-groups/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_user_group_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.user_groups.update_user_group(user_group_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_user_group_detail


def test_delete_user_group(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_group_deleted: Dict[str, Any]):
    user_group_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/user-groups/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_user_group_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.user_groups.delete_user_group(user_group_id)

    assert result == mocked_api_response_user_group_deleted


def test_error_handling_in_user_group_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    user_group_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    configuration = {}

    with pytest.raises(ValueError):
        client.user_groups.list_user_group()

    with pytest.raises(ValueError):
        client.user_groups.create_user_group(configuration)

    with pytest.raises(ValueError):
        client.user_groups.details_user_group(user_group_id)

    with pytest.raises(ValueError):
        client.user_groups.update_user_group(user_group_id, configuration)

    with pytest.raises(ValueError):
        client.user_groups.delete_user_group(user_group_id)
