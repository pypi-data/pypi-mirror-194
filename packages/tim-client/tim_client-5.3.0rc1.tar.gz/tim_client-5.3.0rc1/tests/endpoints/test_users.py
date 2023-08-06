# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any
import pytest
from requests_mock import Mocker
from tim import Tim


def test_get_user_details(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_user_detail: Dict[str, Any]):
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/users/me',
        json=mocked_api_response_user_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.users.details_user()

    assert result == mocked_api_response_user_detail


def test_error_handling_in_user_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    with pytest.raises(ValueError):
        client.users.details_user()
