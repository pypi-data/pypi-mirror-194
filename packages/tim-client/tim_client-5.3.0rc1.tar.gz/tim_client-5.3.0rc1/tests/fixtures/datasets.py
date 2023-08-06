from typing import Dict, Any, List, Tuple
import pytest
import pandas as pd


@pytest.fixture
def mocked_api_response_dataset_uploaded() -> Dict[str, Any]:
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "version": {
            "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
        }
    }


@pytest.fixture
def mocked_api_response_dataset_updated() -> Dict[str, Any]:
    return {
        "version": {
            "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
        }
    }


@pytest.fixture
def mocked_api_response_dataset_deleted() -> Dict[str, Any]:
    return {
        "code": "DM09038",
        "message": "Dataset with ID XYZ successfully deleted."
    }


@pytest.fixture
def mocked_api_response_dataset_version_status_running() -> Dict[str, Any]:
    return {
        "status": "Running",
        "progress": 50.0,
        "createdAt": "2023-01-19T09:55:16.166Z"
    }


@pytest.fixture
def mocked_api_response_dataset_version_status_finished() -> Dict[str, Any]:
    return {
        "status": "Finished",
        "progress": 100.0,
        "createdAt": "2023-01-19T09:55:16.166Z"
    }


@pytest.fixture
def mocked_api_response_dataset_version_status_failed() -> Dict[str, Any]:
    return {
        "status": "Failed",
        "progress": 100.0,
        "createdAt": "2023-01-19T09:55:16.166Z"
    }


@pytest.fixture
def mocked_api_response_dataset_list() -> List[Dict[str, Any]]:
    return [
        {
            "estimatedSamplingPeriod": "PT15M",
            "name": "Test Tomas Dataset",
            "latestVersion": {
                "numberOfObservations": 10,
                "status": "Finished",
                "numberOfVariables": 1,
                "id": "1f4b96da-fb6c-42a5-b17c-9f111d421330",
                "firstTimestamp": "2022-11-09T05:45:00.000Z",
                "lastTimestamp": "2022-11-09T08:00:00.000Z"
            },
            "createdBy": "06575b3e-e882-4aa3-bf00-539539915fec",
            "workspace": {
                "name": "My playground",
                "id": "fbd3a918-456f-486c-a0a3-5bf2354624dd"
            },
            "userGroup": {
                "name": "Financial forecasting",
                "id": "766a1f7f-2629-48d3-a439-7e2acf94c7e8"
            },
            "isFavorite": False,
            "id": "2d6ef9a6-ebc1-43ed-ae91-ad8e2aeba124",
            "timeZoneName": "UTC",
            "createdAt": "2023-01-19T09:55:16.166Z"
        },
        {
            "timeZoneName": "Asia/Bangkok",
            "createdAt": "2023-01-10T09:25:50.224Z",
            "estimatedSamplingPeriod": "PT15M",
            "name": "Small sample Thailand",
            "id": "d37c993f-bfca-4e76-9773-9799f1a742cf",
            "description": "Arsenal London",
            "latestVersion": {
                "numberOfObservations": 10,
                "status": "Finished",
                "numberOfVariables": 1,
                "id": "2360c8f5-31aa-4991-ae1e-13cfae28f218",
                "firstTimestamp": "2022-11-09T05:45:00.000Z",
                "lastTimestamp": "2022-11-09T08:00:00.000Z"
            },
            "createdBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "workspace": {
                "name": "TestingPlace",
                "id": "960b1a67-1531-40c8-9683-1e5351b0d48d"
            },
            "isFavorite": False,
            "userGroup": {
                "name": "Test",
                "id": "fb9f946a-1e97-41da-8b5d-b705b9f466ce"
            }
        }
    ]


@pytest.fixture
def mocked_api_response_dataset_detail() -> Dict[str, Any]:
    return {
        "timeZoneName": "UTC",
        "createdAt": "2023-01-19T09:55:16.166Z",
        "estimatedSamplingPeriod": "PT15M",
        "name": "Test Tomas Dataset",
        "id": "XYZ",
        "latestVersion": {
            "numberOfObservations": 10,
            "status": "Finished",
            "numberOfVariables": 1,
            "id": "1f4b96da-fb6c-42a5-b17c-9f111d421330",
            "firstTimestamp": "2022-11-09T05:45:00.000Z",
            "lastTimestamp": "2022-11-09T08:00:00.000Z"
        },
        "createdBy": "06575b3e-e882-4aa3-bf00-539539915fec",
        "workspace": {
            "name": "My playground",
            "id": "fbd3a918-456f-486c-a0a3-5bf2354624dd"
        },
        "isFavorite": False,
        "userGroup": {
            "name": "Financial forecasting",
            "id": "766a1f7f-2629-48d3-a439-7e2acf94c7e8"
        }
    }


@pytest.fixture
def mocked_api_response_dataset_log() -> List[Dict[str, Any]]:
    return [
        {
            "message": "Successfully generated dataset_id = 2d6ef9a6-ebc1-43ed-ae91-ad8e2aeba124.",
            "messageType": "Info",
            "createdAt": "2023-01-19T09:55:16.179Z",
            "version": {
                "id": "1f4b96da-fb6c-42a5-b17c-9f111d421330"
            },
            "origin": "Upload"
        },
        {
            "message": "Successfully generated dataset_version_id = 1f4b96da-fb6c-42a5-b17c-9f111d421330.",
            "messageType": "Info",
            "createdAt": "2023-01-19T09:55:16.188Z",
            "version": {
                "id": "1f4b96da-fb6c-42a5-b17c-9f111d421330"
            },
            "origin": "Upload"
        },
        {
            "message": "Dataset downloaded from queue. Worker has started the upload...",
            "messageType": "Info",
            "createdAt": "2023-01-19T09:55:16.992Z",
            "version": {
                "id": "1f4b96da-fb6c-42a5-b17c-9f111d421330"
            },
            "origin": "Upload"
        }
    ]


@pytest.fixture
def mocked_api_response_dataset_versions_list() -> List[Dict[str, Any]]:
    return [
        {
            "firstTimestamp": "2022-11-09T05:45:00.000Z",
            "timeZoneName": "UTC",
            "createdAt": "2023-01-19T09:55:16.166Z",
            "estimatedSamplingPeriod": "PT15M",
            "variables": [
                {
                    "minimumValue": 1.22,
                    "name": "data",
                    "maximumValue": 129.1,
                    "firstTimestamp": "2022-11-09T05:45:00.000Z",
                    "lastTimestamp": "2022-11-09T08:00:00.000Z",
                    "orderInTable": 2,
                    "type": "Numerical",
                    "missingObservations": 0,
                    "averageValue": 54.754999999999995
                }
            ],
            "status": "Finished",
            "numberOfVariables": 1,
            "id": "XYZ",
            "size": 160.0,
            "lastTimestamp": "2022-11-09T08:00:00.000Z",
            "dataset": {
                "id": "2d6ef9a6-ebc1-43ed-ae91-ad8e2aeba124"
            },
            "numberOfObservations": 10
        }
    ]


@pytest.fixture
def mocked_api_response_dataset_versions_detail() -> Dict[str, Any]:
    return {
        "firstTimestamp": "2022-11-09T05:45:00.000Z",
        "timeZoneName": "UTC",
        "createdAt": "2023-01-19T09:55:16.166Z",
        "estimatedSamplingPeriod": "PT15M",
        "variables": [
            {
                "minimumValue": 1.22,
                "name": "data",
                "maximumValue": 129.1,
                "firstTimestamp": "2022-11-09T05:45:00.000Z",
                "lastTimestamp": "2022-11-09T08:00:00.000Z",
                "orderInTable": 2,
                "type": "Numerical",
                "missingObservations": 0,
                "averageValue": 54.754999999999995
            }
        ],
        "status": "Finished",
        "numberOfVariables": 1,
        "id": "XYZ",
        "lastTimestamp": "2022-11-09T08:00:00.000Z",
        "size": 160.0,
        "dataset": {
            "id": "ABC"
        },
        "numberOfObservations": 10
    }


@pytest.fixture
def mocked_api_response_dataset_slice_table() -> Tuple[pd.DataFrame, str]:
    mocked_result_df = pd.DataFrame(
        [['2020-01-01T00:00:00Z', 1, 5], ['2020-01-01T01:00:00Z', 2, 6], ['2020-01-01T02:00:00Z', 3, 7]],
        columns=['timestamp', 'col_1', 'col_2']
    )
    mocked_api_response = mocked_result_df.to_csv(index=False)
    return mocked_result_df, mocked_api_response
