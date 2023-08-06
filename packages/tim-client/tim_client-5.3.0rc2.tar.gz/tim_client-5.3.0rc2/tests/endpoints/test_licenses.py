# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any
import pytest
from requests_mock import Mocker
from tim import Tim


def test_get_license_details(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_license_detail: Dict[str, Any]):
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/licenses',
        json=mocked_api_response_license_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.licenses.details_license()

    assert result == mocked_api_response_license_detail


def test_unauthenticated_get_license_details(client: Tim, not_authenticated_requests_mock: Mocker):
    with pytest.raises(ValueError):
        client.licenses.details_license()


def test_get_license_storage(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_license_storage: Dict[str, Any]):
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/licenses/storage',
        json=mocked_api_response_license_storage,
        headers={'Content-Type': 'application/json'}
    )

    result = client.licenses.storage_license()

    assert result == mocked_api_response_license_storage


def test_error_handling_in_license_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    with pytest.raises(ValueError):
        client.licenses.details_license()

    with pytest.raises(ValueError):
        client.licenses.storage_license()
