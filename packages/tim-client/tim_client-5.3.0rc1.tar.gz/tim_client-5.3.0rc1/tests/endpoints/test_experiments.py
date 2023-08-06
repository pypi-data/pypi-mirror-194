# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List
import re
import pytest
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_list_experiment(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_experiment_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'workspaceId': 'afe4bf18-8fce-495d-884e-b8fd463f685a',
        'useCaseId': '39222e75-6d0f-430d-8a9d-11bd270b0dfe',
        'datasetId': '11c82fc4-dbcd-4cce-bc36-c5dd73842dfd',
        'sort': '-createdAd',
        'type': 'Forecasting',
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/experiments',
        status_code=200,
        json=mocked_api_response_experiment_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.experiments.list_experiment(
        offset=arguments['offset'],
        limit=arguments['limit'],
        workspace_id=arguments['workspaceId'],
        use_case_id=arguments['useCaseId'],
        dataset_id=arguments['datasetId'],
        sort=arguments['sort'],
        type=arguments['type']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_experiment_list


def test_create_experiment(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_experiment_detail: Dict[str, Any]):
    configuration = {
        "name": "Experiment ABC 123",
        "description": "Some experiment description...",
        "useCase": {
            "id": "f74e4472-86b1-44bc-862f-5460a27ec0cf"
        },
        "type": "Forecasting"
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/experiments',
        status_code=200,
        json=mocked_api_response_experiment_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.experiments.create_experiment(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_experiment_detail


def test_details_experiment(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_experiment_detail: Dict[str, Any]):
    experiment_id = '60e62008-e6be-4559-aef4-4e6b031c9a61'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/experiments/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_experiment_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.experiments.details_experiment(experiment_id)

    assert result == mocked_api_response_experiment_detail


def test_update_experiment(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_experiment_detail: Dict[str, Any]):
    experiment_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'
    configuration = {
        "name": "Experiment DEF 456",
        "description": "Other description"
    }

    authenticated_requests_mock.request(
        'PATCH',
        re.compile('/api/v5/experiments/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_experiment_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.experiments.edit_experiment(experiment_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_experiment_detail


def test_delete_experiment(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_experiment_deleted: Dict[str, Any]):
    experiment_id = '60e62008-e6be-4559-aef4-4e6b031c9a62'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/experiments/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_experiment_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.experiments.delete_experiment(experiment_id)

    assert result == mocked_api_response_experiment_deleted


def test_error_handling_in_user_group_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    experiment_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    configuration = {}

    with pytest.raises(ValueError):
        client.experiments.list_experiment()

    with pytest.raises(ValueError):
        client.experiments.create_experiment(configuration)

    with pytest.raises(ValueError):
        client.experiments.details_experiment(experiment_id)

    with pytest.raises(ValueError):
        client.experiments.edit_experiment(experiment_id, configuration)

    with pytest.raises(ValueError):
        client.experiments.delete_experiment(experiment_id)
