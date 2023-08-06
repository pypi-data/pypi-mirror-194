from typing import Dict, Any, List
import pytest


@pytest.fixture
def mocked_api_response_use_case_list() -> List[Dict[str, Any]]:
    return [
        {
            "businessKpi": "",
            "createdAt": "2023-01-10T09:26:57.695Z",
            "updatedBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "name": "Small sample Thailand",
            "businessValue": "",
            "id": "d88afa10-b54a-4aab-b637-fc884d5d18c6",
            "description": "",
            "businessObjective": "",
            "createdBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "workspace": {
                "name": "TestingPlace",
                "id": "960b1a67-1531-40c8-9683-1e5351b0d48d"
            },
            "isFavorite": False,
            "updatedAt": "2023-01-10T09:27:23.496Z",
            "dataset": {
                "name": "Small sample Thailand",
                "id": "d37c993f-bfca-4e76-9773-9799f1a742cf"
            },
            "userGroup": {
                "name": "Test",
                "id": "fb9f946a-1e97-41da-8b5d-b705b9f466ce"
            }
        },
        {
            "businessKpi": "",
            "createdAt": "2023-01-10T08:50:23.231Z",
            "updatedBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "name": "Testing Usecase",
            "businessValue": "",
            "id": "c74e7942-a619-4436-86d3-278759ac31b3",
            "description": "",
            "businessObjective": "",
            "createdBy": "4a52f2f1-1e4d-4a1c-820c-abdfec5df8f8",
            "workspace": {
                "name": "TestingPlace",
                "id": "960b1a67-1531-40c8-9683-1e5351b0d48d"
            },
            "isFavorite": False,
            "updatedAt": "2023-01-10T08:51:29.770Z",
            "dataset": {
                "name": "To test Relative",
                "id": "5522a4b9-ecc4-48d1-aa16-fb1563bf2a7e"
            },
            "userGroup": {
                "name": "Test",
                "id": "fb9f946a-1e97-41da-8b5d-b705b9f466ce"
            }
        }
    ]


@pytest.fixture
def mocked_api_response_use_case_detail() -> Dict[str, Any]:
    return {
        "name": "Use case 123",
        "createdBy": "21e8c780-e583-4a25-b765-9604c9611165",
        "workspace": {
            "name": "Default workspace of John",
            "id": "ef47117c-5408-4603-9d6f-735f45a74ff3"
        },
        "id": "6eb88c21-f8fb-419a-842e-0b5a48f7aeca",
        "createdAt": "2023-01-18T12:15:18.695Z"
    }


@pytest.fixture
def mocked_api_response_use_case_deleted() -> Dict[str, Any]:
    return {
        "message": "Use case XYZ successfully deleted.",
        "code": "WF17017"
    }
