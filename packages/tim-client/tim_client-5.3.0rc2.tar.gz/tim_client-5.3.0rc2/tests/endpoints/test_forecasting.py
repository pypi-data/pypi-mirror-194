# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List, Tuple
import re
import pytest
import pandas as pd
from requests_mock import Mocker
from tim import Tim
from tests.utils import validate_mocked_request_body, validate_mocked_request_query_params


def test_build_model(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    configuration = {
        "name": "My first forecast job",
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "targetOffsets": "Combined",
            "predictorOffsets": "Common",
            "allowOffsets": True,
            "offsetLimit": {
                "type": "Explicit",
                "value": 0
            }
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            },
            "imputation": {
                "type": "Linear",
                "maxGapLength": 6
            }
        }
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/forecast-jobs/build-model',
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.build_model(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_upload_model(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    configuration = {
        "name": "My first forecast job",
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        }
    }

    authenticated_requests_mock.request(
        'POST',
        '/api/v5/forecast-jobs/upload-model',
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.upload_model(configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_rebuild_model(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "name": "My first forecast job",
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        }
    }

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/rebuild-model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.rebuild_model(job_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_retrain_model(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "name": "My first forecast job",
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "predictionTo": {
                "baseUnit": "Sample",
                "value": 1
            },
            "predictionFrom": {
                "baseUnit": "Sample",
                "value": 1
            },
            "normalization": True,
            "memoryLimitCheck": True
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            },
            "imputation": {
                "type": "Linear",
                "maxGapLength": 6
            }
        }
    }

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/retrain-model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.retrain_model(job_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_predict(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "name": "My first forecast job",
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "predictionTo": {
                "baseUnit": "Sample",
                "value": 1
            },
            "predictionFrom": {
                "baseUnit": "Sample",
                "value": 1
            }
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            }
        }
    }

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/predict'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.predict(job_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_rca(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/rca'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.rca(job_id)

    assert result == mocked_api_response_forecasting_job_registered


def test_what_if(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = [
        {
            "column": "Temperature",
            "groupKeysValues": [
                1,
                "London"
            ],
            "data": {
                "2011-01-01 00:00:00": 12,
                "2011-01-01 01:00:00": 100
            }
        }
    ]

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/what-if'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.what_if(job_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_job_list(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_list: List[Dict[str, Any]]):
    arguments = {
        'offset': 10,
        'limit': 20,
        'experimentId': '51c207a9-2b49-45e1-afe8-80afb785e930',
        'useCaseId': '6fc29481-f349-481b-82d4-ce0671b82341',
        'type': 'build-model,upload-model,rebuild-model',
        'status': 'Registered,Queued',
        'parentId': '78eb729f-14b7-4678-8c7b-fed633eab317',
        'from': '2021-01-01 00:00:00Z',
        'to': '2021-01-31 00:00:00Z',
        'sort': '-createdAt',
        'sequenceJobId': 'e2b996ad-3909-4086-ac04-cc3e760666c9'
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/forecast-jobs',
        status_code=200,
        json=mocked_api_response_forecasting_job_list,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.job_list(
        offset=arguments['offset'],
        limit=arguments['limit'],
        experiment_id=arguments['experimentId'],
        use_case_id=arguments['useCaseId'],
        type=arguments['type'],
        status=arguments['status'],
        parent_id=arguments['parentId'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to'],
        sort=arguments['sort'],
        sequence_job_id=arguments['sequenceJobId']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_forecasting_job_list


def test_delete_job_list(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_deleted: Dict[str, Any]):
    arguments = {
        'experimentId': '51c207a9-2b49-45e1-afe8-80afb785e930',
        'useCaseId': '6fc29481-f349-481b-82d4-ce0671b82341',
        'type': 'build-model,upload-model,rebuild-model',
        'status': 'Registered,Queued',
        'parentId': '78eb729f-14b7-4678-8c7b-fed633eab317',
        'from': '2021-01-01 00:00:00Z',
        'to': '2021-01-31 00:00:00Z'
    }

    authenticated_requests_mock.request(
        'DELETE',
        '/api/v5/forecast-jobs',
        status_code=200,
        json=mocked_api_response_forecasting_job_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.delete_job_list(
        experiment_id=arguments['experimentId'],
        use_case_id=arguments['useCaseId'],
        type=arguments['type'],
        status=arguments['status'],
        parent_id=arguments['parentId'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_forecasting_job_deleted


def test_job_details(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_detail: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_forecasting_job_detail,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.job_details(job_id)

    assert result == mocked_api_response_forecasting_job_detail


def test_delete_job(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_deleted: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'DELETE',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_forecasting_job_deleted,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.delete_job(job_id)

    assert result == mocked_api_response_forecasting_job_deleted


def test_copy_job(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_registered: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        }
    }

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/copy'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.copy_job(job_id, configuration)

    validate_mocked_request_body(authenticated_requests_mock, configuration)
    assert result == mocked_api_response_forecasting_job_registered


def test_execute(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_executed: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.execute(job_id)

    assert result == mocked_api_response_forecasting_job_executed


def test_job_logs(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_log: List[Dict[str, Any]]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    arguments = {
        'offset': 10,
        'limit': 20,
        'sort': '-createdAt'
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_forecasting_job_log,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.job_logs(
        job_id,
        offset=arguments['offset'],
        limit=arguments['limit'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_forecasting_job_log


def test_status(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_status_running: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.status(job_id)

    assert result == mocked_api_response_forecasting_job_status_running


def test_status_collect(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_status_collect: List[Dict[str, Any]]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    arguments = {
        'offset': 10,
        'limit': 20,
        'sort': '-createdAt'
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status/collect'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_collect,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.status_collect(
        job_id,
        offset=arguments['offset'],
        limit=arguments['limit'],
        sort=arguments['sort']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_forecasting_job_status_collect


def test_results_table(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    arguments = {
        'forecastType': 'OutOfSample',
        'modelIndex': 5
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/table'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )

    result = client.forecasting.results_table(
        job_id,
        forecast_type=arguments['forecastType'],
        model_index=arguments['modelIndex']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert mocked_api_response_forecasting_results_table[0].equals(result)


def test_results_production_forecast(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/production-forecast'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )

    result = client.forecasting.results_production_forecast(job_id)

    assert mocked_api_response_forecasting_results_table[0].equals(result)


def test_results_model(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_model: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_model,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.results_model(job_id)

    assert result == mocked_api_response_forecasting_job_model


def test_results_accuracies(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_accuracies: Dict[str, Any]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/accuracies'),
        status_code=200,
        json=mocked_api_response_forecasting_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.results_accuracies(job_id)

    assert result == mocked_api_response_forecasting_job_accuracies


def test_results_rca(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str]):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    arguments = {
        'indexOfModel': 6,
        'timestamp': '2020-01-01T06:00:00Z',
        'radius': 10
    }

    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/rca'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )

    result = client.forecasting.results_rca(
        job_id,
        index_of_model=arguments['indexOfModel'],
        timestamp=arguments['timestamp'],
        radius=arguments['radius']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert mocked_api_response_forecasting_results_table[0].equals(result)


def test_results_production_table(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str]):
    arguments = {
        'sequenceJobId': '962f82ef-6b5a-4faf-8bb3-63cee630097e',
        'datasetVersionId': 'ca1f3059-158e-4ea2-bc67-a32f62d21ee2',
        'type': 'build-model,upload-model',
        'from': '2020-01-01T00:00:00Z',
        'to': '2020-01-02T00:00:00Z',
        'allowOverlapping': True,
        'colocatedJobs': False
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/forecast-jobs/results/production-table',
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )

    result = client.forecasting.results_production_table(
        sequence_job_id=arguments['sequenceJobId'],
        dataset_version_id=arguments['datasetVersionId'],
        type=arguments['type'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to'],
        allow_overlapping=arguments['allowOverlapping'],
        colocated_jobs=arguments['colocatedJobs']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert mocked_api_response_forecasting_results_table[0].equals(result)


def test_results_production_accuracies(client: Tim, authenticated_requests_mock: Mocker, mocked_api_response_forecasting_job_accuracies: Dict[str, Any]):
    arguments = {
        'sequenceJobId': 'cf1cf911-027c-4ad6-8065-ef6ac16b2c04',
        'datasetVersionId': '3d9af24e-372b-41b9-bbc7-21f8af89b65a',
        'type': 'build-model,upload-model',
        'from': '2020-01-01T00:00:00.000Z',
        'to': '2020-01-31T00:00:00.000Z',
        'allowOverlapping': True,
        'colocatedJobs': False,
        'individualAccuracies': True
    }

    authenticated_requests_mock.request(
        'GET',
        '/api/v5/forecast-jobs/results/production-accuracies',
        status_code=200,
        json=mocked_api_response_forecasting_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting.results_production_accuracies(
        sequence_job_id=arguments['sequenceJobId'],
        dataset_version_id=arguments['datasetVersionId'],
        type=arguments['type'],
        from_datetime=arguments['from'],
        to_datetime=arguments['to'],
        allow_overlapping=arguments['allowOverlapping'],
        colocated_jobs=arguments['colocatedJobs'],
        individual_accuracies=arguments['individualAccuracies']
    )

    validate_mocked_request_query_params(authenticated_requests_mock, arguments)
    assert result == mocked_api_response_forecasting_job_accuracies


def test_error_handling_in_forecasting_functions(client: Tim, requests_mock_with_erroring_endpoints: Mocker):
    job_id = 'bb9585e9-b5a2-48de-9dcc-3f4459bc7556'
    configuration = {}
    index_of_model = 1

    with pytest.raises(ValueError):
        client.forecasting.build_model(configuration)

    with pytest.raises(ValueError):
        client.forecasting.upload_model(configuration)

    with pytest.raises(ValueError):
        client.forecasting.rebuild_model(job_id, configuration)

    with pytest.raises(ValueError):
        client.forecasting.retrain_model(job_id, configuration)

    with pytest.raises(ValueError):
        client.forecasting.predict(job_id, configuration)

    with pytest.raises(ValueError):
        client.forecasting.rca(job_id)

    with pytest.raises(ValueError):
        client.forecasting.what_if(job_id, configuration)

    with pytest.raises(ValueError):
        client.forecasting.job_list()

    with pytest.raises(ValueError):
        client.forecasting.delete_job_list()

    with pytest.raises(ValueError):
        client.forecasting.job_details(job_id)

    with pytest.raises(ValueError):
        client.forecasting.delete_job(job_id)

    with pytest.raises(ValueError):
        client.forecasting.copy_job(job_id, configuration)

    with pytest.raises(ValueError):
        client.forecasting.execute(job_id)

    with pytest.raises(ValueError):
        client.forecasting.job_logs(job_id)

    with pytest.raises(ValueError):
        client.forecasting.status(job_id)

    with pytest.raises(ValueError):
        client.forecasting.status_collect(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_table(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_production_forecast(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_model(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_accuracies(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_rca(job_id, index_of_model)

    with pytest.raises(ValueError):
        client.forecasting.results_production_table(job_id)

    with pytest.raises(ValueError):
        client.forecasting.results_production_accuracies(job_id)
