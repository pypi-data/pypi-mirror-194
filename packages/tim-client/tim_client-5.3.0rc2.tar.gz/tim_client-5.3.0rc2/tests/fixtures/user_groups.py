from typing import Dict, Any, List
import pytest


@pytest.fixture
def mocked_api_response_user_group_list() -> List[Dict[str, Any]]:
    return [
        {
            "name": "Test user group 1",
            "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
            "id": "60e62008-e6be-4559-aef4-4e6b031c9a61",
            "createdAt": "2021-10-22T11:26:34.315Z",
            "description": "ABC123"
        },
        {
            "name": "Test user group 2",
            "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
            "id": "78abaca2-2802-43e1-82ea-0e1a43078c25",
            "createdAt": "2021-10-22T11:25:12.648Z",
            "description": "DEF456"
        }
    ]


@pytest.fixture
def mocked_api_response_user_group_detail() -> Dict[str, Any]:
    return {
        "name": "ABC DEF",
        "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
        "id": "9e2aa4c5-f9a0-4f3a-8e38-8315865e1768",
        "createdAt": "2023-01-18T08:36:25.316Z"
    }


@pytest.fixture
def mocked_api_response_user_group_deleted() -> Dict[str, Any]:
    return {
        "message": "User group XYZ successfully deleted.",
        "code": "WF17017"
    }
