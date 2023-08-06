# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any, List, Tuple
import re
import pytest
import pandas as pd
from requests_mock import Mocker
from tim import Tim


@pytest.fixture
def authenticated_requests_mock_with_detection_endpoints(
    authenticated_requests_mock: Mocker,
    mocked_api_response_detection_job_detail: Dict[str, Any],
    mocked_api_response_detection_job_log: List[Dict[str, Any]],
    mocked_api_response_detection_job_executed: Dict[str, Any],
    mocked_api_response_detection_job_status_finished: Dict[str, Any],
    mocked_api_response_detection_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_detection_job_model: Dict[str, Any],
    mocked_api_response_detection_job_accuracies: Dict[str, Any]
) -> Mocker:
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_detection_job_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_detection_job_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_detection_job_status_finished,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/table'),
        status_code=200,
        text=mocked_api_response_detection_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/model'),
        status_code=200,
        json=mocked_api_response_detection_job_model,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/accuracies'),
        status_code=200,
        json=mocked_api_response_detection_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/rca'),
        status_code=200,
        text=mocked_api_response_detection_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/detection-jobs/results/production-table',
        status_code=200,
        text=mocked_api_response_detection_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        '/api/v5/detection-jobs/results/production-accuracies',
        status_code=200,
        json=mocked_api_response_detection_job_accuracies,
        headers={'Content-Type': 'application/json'}
    )
    return authenticated_requests_mock


def test_extended_detection_job_results(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_detail: Dict[str, Any],
    mocked_api_response_detection_job_log: List[Dict[str, Any]],
    mocked_api_response_detection_job_status_finished: Dict[str, Any],
    mocked_api_response_detection_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_detection_job_model: Dict[str, Any],
    mocked_api_response_detection_job_accuracies: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    result = client.detection_job_results(
        id=job_id,
        outputs=[
            'id',
            'details',
            'logs',
            'status',
            'table',
            'model',
            'accuracies',
            'production_table',
            'production_accuracies'
        ])

    assert result[0] == job_id
    assert result[1] == mocked_api_response_detection_job_detail
    assert result[2] == mocked_api_response_detection_job_log
    assert result[3] == mocked_api_response_detection_job_status_finished
    assert mocked_api_response_detection_results_table[0].equals(result[4])
    assert result[5] == mocked_api_response_detection_job_model
    assert result[6] == mocked_api_response_detection_job_accuracies
    assert mocked_api_response_detection_results_table[0].equals(result[7])
    assert result[8] == mocked_api_response_detection_job_accuracies


def test_extended_execute_detection_job_without_wait_to_finish(
        client: Tim,
        authenticated_requests_mock: Mocker,
        mocked_api_response_detection_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_detection_job(id=job_id, wait_to_finish=False)

    assert result == {
        'id': job_id,
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }


def test_extended_execute_detection_job_with_wait_to_finish_and_finished_job(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_detection_job_executed: Dict[str, Any],
    mocked_api_response_detection_job_status_running: Dict[str, Any],
    mocked_api_response_detection_job_status_finished: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_detection_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_detection_job(
        id=job_id,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_detection_job_status_finished,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result == {
        'id': job_id,
        'response': mocked_api_response_detection_job_executed,
        'status': mocked_api_response_detection_job_status_finished
    }


def test_extended_execute_detection_job_with_wait_to_finish_and_failed_job(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_detection_job_executed: Dict[str, Any],
    mocked_api_response_detection_job_status_running: Dict[str, Any],
    mocked_api_response_detection_job_status_failed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_detection_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    result = client.execute_detection_job(
        id=job_id,
        wait_to_finish=True,
        status_poll=lambda _: authenticated_requests_mock.request(
            'GET',
            re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
            status_code=200,
            json=mocked_api_response_detection_job_status_failed,
            headers={'Content-Type': 'application/json'}
        )
    )

    assert result == {
        'id': job_id,
        'response': mocked_api_response_detection_job_executed,
        'status': mocked_api_response_detection_job_status_failed
    }


def test_extended_execute_detection_job_with_wait_to_finish_and_timeout_reached(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_detection_job_executed: Dict[str, Any],
    mocked_api_response_detection_job_status_running: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_detection_job_status_running,
        headers={'Content-Type': 'application/json'}
    )

    with pytest.raises(ValueError):
        client.execute_detection_job(
            id=job_id,
            wait_to_finish=True,
            tries_left=2
        )


def test_extended_detection_build_kpi_model(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    configuration = {
        "name": "My first anomaly build-model job",
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "domainSpecifics": [
                {
                    "perspective": "Residual",
                    "sensitivity": 0,
                    "minSensitivity": 0,
                    "maxSensitivity": 0
                }
            ],
            "anomalousBehaviorModel": {
                "maxModelComplexity": 15,
                "detectionIntervals": [
                    {
                        "type": "Hour",
                        "value": "8-16"
                    }
                ]
            }
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            }
        }
    }

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        '/api/v5/detection-jobs/build-model/kpi-driven',
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_build_kpi_model(
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_build_kpi_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_build_kpi_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is not None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None


def test_extended_detection_build_system_model(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    configuration = {
        "name": "My first anomaly build-model job",
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "domainSpecifics": {
                "sensitivity": 0.15,
                "minSensitivity": 0,
                "maxSensitivity": 0,
                "anomalyIndicatorWindow": {
                    "baseUnit": "Hour",
                    "value": 24
                }
            }
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            }
        }
    }

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        '/api/v5/detection-jobs/build-model/system-driven',
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_build_system_model(
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_build_system_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_build_system_model(
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is not None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None


def test_extended_detection_rebuild_kpi_model(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "name": "My first anomaly rebuild-model job",
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "configuration": {
            "rebuildType": "All"
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            },
            "imputation": {
                "type": "LOCF",
                "maxGapLength": 6
            }
        }
    }

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/rebuild-model/kpi-driven'),
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_rebuild_kpi_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_rebuild_kpi_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_rebuild_kpi_model(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is not None
    assert result_finished_job[6] is not None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None


def test_extended_detection_detect(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = {
        "name": "My first anomaly detect job",
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "data": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            },
            "imputation": {
                "type": "LOCF",
                "maxGapLength": 6
            }
        }
    }

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/detect'),
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_detect(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_detect(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_detect(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is not None
    assert result_finished_job[3] is not None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None


def test_extended_detection_results_rca(
    client: Tim,
    authenticated_requests_mock: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_detail: Dict[str, Any],
    mocked_api_response_detection_job_log: List[Dict[str, Any]],
    mocked_api_response_detection_job_executed: Dict[str, Any],
    mocked_api_response_detection_job_status_finished: Dict[str, Any],
    mocked_api_response_detection_results_table: Tuple[pd.DataFrame, str],
    mocked_api_response_detection_job_model: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/rca'),
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}'),
        status_code=200,
        json=mocked_api_response_detection_job_detail,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/log'),
        status_code=200,
        json=mocked_api_response_detection_job_log,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/status'),
        status_code=200,
        json=mocked_api_response_detection_job_status_finished,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/execute'),
        status_code=202,
        json=mocked_api_response_detection_job_executed,
        headers={'Content-Type': 'application/json'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/rca'),
        status_code=200,
        text=mocked_api_response_detection_results_table[1],
        headers={'Content-Type': 'text/csv'}
    )
    authenticated_requests_mock.request(
        'GET',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/results/model'),
        status_code=200,
        json=mocked_api_response_detection_job_model,
        headers={'Content-Type': 'application/json'}
    )

    result = client.detection_results_rca(
        id=job_id
    )

    assert result[0] == job_id
    assert result[1] == mocked_api_response_detection_job_detail
    assert result[2] == mocked_api_response_detection_job_log
    assert result[3] == mocked_api_response_detection_job_status_finished
    assert mocked_api_response_detection_results_table[0].equals(result[4])


def test_extended_detection_root_cause_analysis(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/rca'),
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_root_cause_analysis(
        parent_job_id=job_id,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_root_cause_analysis(
        parent_job_id=job_id,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_root_cause_analysis(
        parent_job_id=job_id,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is None
    assert result_finished_job[3] is None
    assert result_finished_job[4] is not None


def test_extended_detection_what_if_analysis(
    client: Tim,
    authenticated_requests_mock_with_detection_endpoints: Mocker,
    mocked_api_response_detection_job_registered: Dict[str, Any],
    mocked_api_response_detection_job_executed: Dict[str, Any]
):
    job_id = '962f82ef-6b5a-4faf-8bb3-63cee630097e'
    configuration = [
        {
            "column": "Temperature",
            "data": {
                "2011-01-01 00:00:00": 12,
                "2011-01-01 01:00:00": 100
            }
        }
    ]

    authenticated_requests_mock_with_detection_endpoints.request(
        'POST',
        re.compile('/api/v5/detection-jobs/[0-9a-fA-F-]{36}/what-if'),
        status_code=200,
        json=mocked_api_response_detection_job_registered,
        headers={'Content-Type': 'application/json'}
    )

    result_not_executed_job = client.detection_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=False,
        wait_to_finish=False
    )
    result_executed_job = client.detection_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=False
    )
    result_finished_job = client.detection_what_if_analysis(
        parent_job_id=job_id,
        configuration=configuration,
        execute=True,
        wait_to_finish=True
    )

    assert result_not_executed_job == mocked_api_response_detection_job_registered
    assert result_executed_job == {
        'id': mocked_api_response_detection_job_registered['id'],
        'response': mocked_api_response_detection_job_executed,
        'status': 'Queued'
    }
    assert result_finished_job[0] == mocked_api_response_detection_job_registered['id']
    assert result_finished_job[1] is None
    assert result_finished_job[2] is None
    assert result_finished_job[3] is None
    assert result_finished_job[4] is not None
    assert result_finished_job[5] is None
    assert result_finished_job[6] is None
    assert result_finished_job[7] is None
    assert result_finished_job[8] is None
