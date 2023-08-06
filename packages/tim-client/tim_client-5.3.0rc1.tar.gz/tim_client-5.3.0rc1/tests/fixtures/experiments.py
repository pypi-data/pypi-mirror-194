from typing import Dict, Any, List
import pytest


@pytest.fixture
def mocked_api_response_experiment_list() -> List[Dict[str, Any]]:
    return [
        {
            "name": "Quick Forecast - 17/08/2022 13:53:35",
            "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
            "useCase": {
                "id": "524f8eef-e91e-4a71-b667-1579a8a93c58"
            },
            "workspace": {
                "id": "437aaea5-e1a1-472a-84c7-430a6b801fd7"
            },
            "id": "9896378d-7986-437d-ae20-135c5eecb7c6",
            "type": "Forecasting",
            "createdAt": "2022-08-17T13:53:36.864Z"
        },
        {
            "name": "Quick Forecast - 17/08/2022 13:53:32",
            "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
            "useCase": {
                "id": "d0e48403-a1f0-4973-8102-e47b4d7db5eb"
            },
            "workspace": {
                "id": "437aaea5-e1a1-472a-84c7-430a6b801fd7"
            },
            "id": "a02ef78e-be4c-456e-bb38-287e8f6606bb",
            "type": "Forecasting",
            "createdAt": "2022-08-17T13:53:33.925Z"
        }
    ]


@pytest.fixture
def mocked_api_response_experiment_detail() -> Dict[str, Any]:
    return {
        "name": "Experiment ABC 123",
        "userGroup": {
            "name": "John's personal user group",
            "id": "7e951a3c-eea8-4662-9340-3c063b0addb8"
        },
        "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
        "useCase": {
            "name": "TIM_AD_1_benchmark_1673290787",
            "id": "f74e4472-86b1-44bc-862f-5460a27ec0cf"
        },
        "workspace": {
            "name": "Default workspace of John",
            "id": "437aaea5-e1a1-472a-84c7-430a6b801fd7"
        },
        "id": "a195d044-f1cc-4219-ae06-52aea48da084",
        "description": "Some experiment description...",
        "type": "Forecasting",
        "createdAt": "2023-01-18T14:13:03.567Z"
    }


@pytest.fixture
def mocked_api_response_experiment_deleted() -> Dict[str, Any]:
    return {
        "message": "Experiment XYZ successfully deleted.",
        "code": "WF17017"
    }
