from typing import Dict, Any, List
import pytest


@pytest.fixture
def mocked_api_response_workspace_list() -> List[Dict[str, Any]]:
    return [
        {
            "name": "Test_Workspace",
            "userGroup": {
                "name": "Test Team",
                "id": "a09909f3-e8c6-44ff-9350-e7c5da2fb745"
            },
            "createdBy": "f7ebf0d6-9880-4df5-aa98-206e6d51636a",
            "isFavorite": True,
            "id": "bb9585e9-b5a2-48de-9dcc-3f4459bc7556",
            "createdAt": "2022-03-07T15:21:43.565Z",
            "description": ""
        },
        {
            "name": "Default workspace of John",
            "userGroup": {
                "name": "John's personal user group",
                "id": "7e951a3c-eea8-4662-9340-3c063b0addb8"
            },
            "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
            "isFavorite": True,
            "id": "437aaea5-e1a1-472a-84c7-430a6b801fd7",
            "createdAt": "2021-05-22T20:51:32.232Z",
            "description": ""
        }
    ]


@pytest.fixture
def mocked_api_response_workspace_detail() -> Dict[str, Any]:
    return {
        "name": "Test workspace 123",
        "userGroup": {
            "name": "ABC'DEF",
            "id": "9a7e960b-5071-4eb5-a372-913f7d426a2c"
        },
        "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
        "id": "edad6c90-d63d-4d9b-a561-d16f161c54bc",
        "description": "Some interesting description",
        "createdAt": "2023-01-18T10:02:34.623Z"
    }


@pytest.fixture
def mocked_api_response_workspace_deleted() -> Dict[str, Any]:
    return {
        "message": "Workspace XYZ successfully deleted.",
        "code": "WF17017"
    }
