# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List, Tuple
import re
import pytest
import pandas as pd
from requests_mock import Mocker
from tim import Tim


@pytest.fixture
def authenticated_requests_mock_with_forecasting_endpoints(
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_detail: Dict[str, Any],
    mocked_api_response_forecasting_job_log: List[Dict[str, Any]],
    mocked_api_response_forecasting_job_executed: Dict[str, Any],
    mocked_api_response_forecasting_job_status_finished: Dict[str, Any],
    mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_forecasting_job_model: Dict[str, Any],
    mocked_api_response_forecasting_job_accuracies: Dict[str, Any]
) -> Mocker:
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_forecasting_job_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_forecasting_job_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_finished,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/table'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/production-forecast'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_model,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/accuracies'),
        status_code=200,
        json=mocked_api_response_forecasting_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/rca'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/forecast-jobs/results/production-table',
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/forecast-jobs/results/production-accuracies',
        status_code=200,
        json=mocked_api_response_forecasting_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )
    return authenticated_requests_mock


def test_extended_forecasting_job_results(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_detail: Dict[str, Any],
    mocked_api_response_forecasting_job_log: List[Dict[str, Any]],
    mocked_api_response_forecasting_job_status_finished: Dict[str, Any],
    mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_forecasting_job_model: Dict[str, Any],
    mocked_api_response_forecasting_job_accuracies: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    result = client.forecasting_job_results(
        id=job_id,
        outputs=[
            'details',
            'logs',
            'status',
            'table',
            'production_forecast',
            'model',
            'accuracies',
            'production_table',
            'production_accuracies'
        ]
    )

    assert result[0] == job_id
    assert result[1] == mocked_api_response_forecasting_job_detail
    assert result[2] == mocked_api_response_forecasting_job_log
    assert result[3] == mocked_api_response_forecasting_job_status_finished
    assert mocked_api_response_forecasting_results_table[0].equals(result[4])
    assert mocked_api_response_forecasting_results_table[0].equals(result[5])
    assert result[6] == mocked_api_response_forecasting_job_model
    assert result[7] == mocked_api_response_forecasting_job_accuracies
    assert mocked_api_response_forecasting_results_table[0].equals(result[8])
    assert result[9] == mocked_api_response_forecasting_job_accuracies


def test_extended_execute_forecast_job_without_wait_to_finish(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_forecast_job(id=job_id, wait_to_finish=False)

    assert result == {
        'id': job_id,
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }


def test_extended_execute_forecast_job_with_wait_to_finish_and_finished_job(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_executed: Dict[str, Any],
    mocked_api_response_forecasting_job_status_running: Dict[str, Any],
    mocked_api_response_forecasting_job_status_finished: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_forecast_job(
        id=job_id,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_forecasting_job_status_finished,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result == {
        'id': job_id,
        'response': mocked_api_response_forecasting_job_executed,
        'status': mocked_api_response_forecasting_job_status_finished
    }


def test_extended_execute_forecast_job_with_wait_to_finish_and_failed_job(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_executed: Dict[str, Any],
    mocked_api_response_forecasting_job_status_running: Dict[str, Any],
    mocked_api_response_forecasting_job_status_failed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_forecast_job(
        id=job_id,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_forecasting_job_status_failed,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result == {
        'id': job_id,
        'response': mocked_api_response_forecasting_job_executed,
        'status': mocked_api_response_forecasting_job_status_failed
    }


def test_extended_execute_forecast_job_with_wait_to_finish_and_timeout_reached(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_executed: Dict[str, Any],
    mocked_api_response_forecasting_job_status_running: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    with pytest.raises(ValueError):
        client.execute_forecast_job(
            id=job_id,
            wait_to_finish=True,
            tries_left=2
        )


def test_extended_forecasting_build_model(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
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

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        '/api/v5/forecast-jobs/build-model',
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_build_model(
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_build_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_build_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is not None
    assert result_finished_job[8] is None
    assert result_finished_job[9] is None


def test_extended_forecasting_predict(
        client: Tim,
        authenticated_requests_mock_with_forecasting_endpoints: Mocker,
        mocked_api_response_forecasting_job_registered: Dict[str, Any],
        mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
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

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/predict'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_predict(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_predict(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_predict(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None
    assert result_finished_job[9] is None


def test_extended_forecasting_rebuild_model(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
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

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/rebuild-model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_rebuild_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_rebuild_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_rebuild_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is not None
    assert result_finished_job[8] is None
    assert result_finished_job[9] is None


def test_extended_forecasting_retrain_model(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
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

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/retrain-model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_retrain_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_retrain_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_retrain_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is not None
    assert result_finished_job[8] is None
    assert result_finished_job[9] is None


def test_extended_forecasting_results_rca(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_detail: Dict[str, Any],
    mocked_api_response_forecasting_job_log: List[Dict[str, Any]],
    mocked_api_response_forecasting_job_executed: Dict[str, Any],
    mocked_api_response_forecasting_job_status_finished: Dict[str, Any],
    mocked_api_response_forecasting_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_forecasting_job_model: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/rca'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_forecasting_job_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_forecasting_job_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_forecasting_job_status_finished,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/rca'),
        status_code=200,
        text=mocked_api_response_forecasting_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/results/model'),
        status_code=200,
        json=mocked_api_response_forecasting_job_model,
        headers={'Content-Type': 'application/json'}
    )

    result = client.forecasting_results_rca(
        id=job_id
    )

    assert result[0] == job_id
    assert result[1] == mocked_api_response_forecasting_job_detail
    assert result[2] == mocked_api_response_forecasting_job_log
    assert result[3] is None
    assert len(result[4]) == 1


def test_extended_forecasting_root_cause_analysis(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/rca'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_root_cause_analysis(
        parent_job_id=job_id,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_root_cause_analysis(
        parent_job_id=job_id,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_root_cause_analysis(
        parent_job_id=job_id,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is None
    assert result_finished_job[3] is None
    assert result_finished_job[4] is not None


def test_extended_forecasting_what_if_analysis(
    client: Tim,
    authenticated_requests_mock_with_forecasting_endpoints: Mocker,
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
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

    authenticated_requests_mock_with_forecasting_endpoints.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/what-if'),
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.forecasting_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.forecasting_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.forecasting_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_forecasting_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_forecasting_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is None
    assert result_finished_job[3] is None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None
    assert result_finished_job[9] is None


def test_extended_quick_forecast(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_dataset_uploaded: Dict[str, Any],
    mocked_api_response_dataset_version_status_finished: Dict[str, Any],
    mocked_api_response_dataset_detail: Dict[str, Any],
    mocked_api_response_forecasting_job_registered: Dict[str, Any],
    mocked_api_response_forecasting_job_executed: Dict[str, Any]
):
    workspace_id = 'a4f23f1a-9017-4983-8967-3de98300b9cb'
    mocked_dataset_df = pd.DataFrame(
        [['2020-01-01T00:00:00Z', 1], ['2020-01-01T01:00:00Z', 2], ['2020-01-01T02:00:00Z', 3]],
        columns=['timestamp', 'value']
    )
    dataset_configuration = {
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
    job_configuration = {
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
        re.compile('/api/v5/datasets/[0-9a-fA-F-]{36}/versions/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_dataset_version_status_finished,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        '/api/v5/forecast-jobs/build-model',
        status_code=200,
        json=mocked_api_response_forecasting_job_registered,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/forecast-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_forecasting_job_executed,
        headers={'Content-Type': 'application/json'}
    )

    result = client.quick_forecast(
        dataset=mocked_dataset_df,
        job_configuration=job_configuration,
        workspace_id=workspace_id,
        dataset_configuration=dataset_configuration,
        execute=True,
        wait_to_finish=False,
        delete_items=False
    )

    assert result[0] == mocked_api_response_dataset_uploaded
    assert result[1] == {
        'id': mocked_api_response_forecasting_job_registered['id'],
        'response': mocked_api_response_forecasting_job_executed,
        'status': 'Queued'
    }
    assert result[2] is None
