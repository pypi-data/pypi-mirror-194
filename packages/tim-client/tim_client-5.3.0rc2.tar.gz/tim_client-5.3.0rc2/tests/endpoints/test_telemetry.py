# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List
import pytest
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_query_params


def test_dataset_calls_telemetry(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_telemetry_dataset_calls: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'datasetId': 'b08c20fc-7188-4a04-aac8-60fb7146339c',
        'experimentId': '9245703e-080f-468f-9a48-69f344b540ab',
        'userId': '44662620-e6b6-40d6-8a7c-82c63537778d',
        'datasetState': 'Existing',
        'datasetVersionState': 'Deleted',
        'endpointId': 'abc,def',
        'from': '2020-01-01T01:02:03.123Z',
        'to': '2021-02-02T02:03:04.345Z',
        'sort': '-time'
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/ops/dataset-calls',
        status_code=200,
        json=mocked_api_response_telemetry_dataset_calls,
        headers={'Content-Type': 'application/json'}
    )

    result = client.telemetry.dataset_calls(
        offset=arguments['offset'],
        limit=arguments['limit'],
        dataset_id=arguments['datasetId'],
        experiment_id=arguments['experimentId'],
        user_id=arguments['userId'],
        dataset_state=arguments['datasetState'],
        dataset_version_state=arguments['datasetVersionState'],
        endpoint_id=arguments['endpointId'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_telemetry_dataset_calls


def test_job_calls_telemetry(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_telemetry_job_calls: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'datasetId': 'b08c20fc-7188-4a04-aac8-60fb7146339c',
        'datasetVersionId': 'b7b79d0e-4711-4868-a4fe-d5bd61e2958d',
        'experimentId': '9245703e-080f-468f-9a48-69f344b540ab',
        'jobId': '88b54cd7-be29-4fec-bf2e-59b3b82f763e',
        'parentJobId': '6f0c21a5-870a-4af0-812f-587d01ada0a6',
        'userId': '44662620-e6b6-40d6-8a7c-82c63537778d',
        'type': 'Forecasting',
        'jobState': 'Existing',
        'endpointId': 'abc,def',
        'from': '2020-01-01T01:02:03.123Z',
        'to': '2021-02-02T02:03:04.345Z',
        'fromCalculationTime': 'PT1S',
        'toCalculationTime': 'PT20S',
        'sort': '-time'
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/ops/job-calls',
        status_code=200,
        json=mocked_api_response_telemetry_job_calls,
        headers={'Content-Type': 'application/json'}
    )

    result = client.telemetry.job_calls(
        offset=arguments['offset'],
        limit=arguments['limit'],
        dataset_id=arguments['datasetId'],
        dataset_version_id=arguments['datasetVersionId'],
        experiment_id=arguments['experimentId'],
        job_id=arguments['jobId'],
        parent_job_id=arguments['parentJobId'],
        user_id=arguments['userId'],
        type=arguments['type'],
        job_state=arguments['jobState'],
        endpoint_id=arguments['endpointId'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to'],
        from_calculation_time=arguments['fromCalculationTime'],
        to_calculation_time=arguments['toCalculationTime'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_telemetry_job_calls


def test_error_handling_in_telemetry_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    with pytest.raises(ValueError):
        client.telemetry.dataset_calls()

    with pytest.raises(ValueError):
        client.telemetry.job_calls()
