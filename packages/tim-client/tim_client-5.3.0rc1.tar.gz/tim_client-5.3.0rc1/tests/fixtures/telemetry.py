from typing import Dict, Any, List
import pytest


@pytest.fixture
def mocked_api_response_telemetry_dataset_calls() -> List[Dict[str, Any]]:
    return [
        {
            "dataset": {
                "id": "d37c993f-bfca-4e76-9773-9799f1a742cf"
            },
            "response": {
                "time": "2023-01-18T14:37:46.198Z",
                "code": 200
            },
            "TIMClientOrigin": "TIM Studio",
            "time": "2023-01-18T14:37:44.523Z",
            "id": "cdde7a19-af19-46a6-8cd1-bff5903c5db3",
            "request": {
                "method": "GET",
                "microservice": "DM",
                "target": "/datasets/d37c993f-bfca-4e76-9773-9799f1a742cf/versions"
            },
            "madeBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "imageVersion": "5.8.4"
        },
        {
            "dataset": {
                "id": "d37c993f-bfca-4e76-9773-9799f1a742cf"
            },
            "response": {
                "time": "2023-01-18T14:37:42.536Z",
                "code": 200
            },
            "TIMClientOrigin": "TIM Studio",
            "time": "2023-01-18T14:37:42.403Z",
            "id": "8e3bed54-85cb-4904-9f05-935c19905f5f",
            "request": {
                "method": "GET",
                "microservice": "DM",
                "target": "/datasets/d37c993f-bfca-4e76-9773-9799f1a742cf"
            },
            "madeBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "imageVersion": "5.8.4"
        }
    ]


@pytest.fixture
def mocked_api_response_telemetry_job_calls() -> List[Dict[str, Any]]:
    return [
        {
            "dataset": {
                "id": "d37c993f-bfca-4e76-9773-9799f1a742cf",
                "version": {
                    "id": "2360c8f5-31aa-4991-ae1e-13cfae28f218",
                    "createdAt": "2023-01-10T09:25:50.224Z",
                    "state": "Finished"
                }
            },
            "response": {
                "time": "2023-01-18T14:38:43.527Z",
                "code": 200
            },
            "TIMClientOrigin": "TIM Studio",
            "time": "2023-01-18T14:38:43.484Z",
            "job": {
                "id": "e776ed41-8cc9-42f3-aba2-3cf0ec731780",
                "createdAt": "2023-01-18T09:26:45.155Z",
                "state": "Failed"
            },
            "id": "e914d2e1-d225-49de-98c6-be0cf72a57a6",
            "experiment": {
                "id": "5b020475-b777-4cfc-a3c0-03984c4fbafc"
            },
            "request": {
                "method": "GET",
                "microservice": "JM",
                "target": "/detection-jobs?experimentId=5b020475-b777-4cfc-a3c0-03984c4fbafc&offset=0&limit=5&type=build-model,detect&approach=kpi-driven"
            },
            "madeBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "imageVersion": "5.6.4"
        },
        {
            "dataset": {
                "id": "ad3db44f-6f01-4b28-bfe7-bf887989b08c",
                "version": {
                    "id": "f6b66291-a3a0-496b-9c20-438e46374d07",
                    "createdAt": "2023-01-17T08:46:16.468Z",
                    "state": "Finished"
                }
            },
            "response": {
                "time": "2023-01-18T14:37:56.964Z",
                "code": 200
            },
            "TIMClientOrigin": "Test",
            "time": "2023-01-18T14:37:56.936Z",
            "job": {
                "id": "69fd8841-14c6-48c2-a1b4-3df5a90c6a78",
                "createdAt": "2023-01-18T14:36:14.471Z",
                "state": "Finished"
            },
            "id": "58ab5e17-1abc-473a-ad93-2590699db3ed",
            "experiment": {
                "id": "901d960a-7a49-4d14-9b66-07d264bf910d"
            },
            "request": {
                "method": "GET",
                "microservice": "JM",
                "target": "/detection-jobs/69fd8841-14c6-48c2-a1b4-3df5a90c6a78/results/model"
            },
            "madeBy": "82b407b2-a687-4b3e-a13d-5811e257605a",
            "imageVersion": "5.6.4"
        }
    ]
