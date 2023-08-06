from typing import Dict, Any
import pytest


@pytest.fixture
def mocked_api_response_user_detail() -> Dict[str, Any]:
    return {
        "isActive": True,
        "isAdmin": True,
        "additionalUserData": None,
        "lastLogin": "2023-02-13T13:15:40.602Z",
        "id": "21e8c780-e583-4a25-b765-9604c9611165",
        "lastName": "Doe",
        "firstName": "John",
        "license": {
            "licenseKey": "grew-w48e-e4gw-gwe9"
        },
        "email": "john.doe@tangent.works",
        "personalUserGroup": {
            "id": "7e951a3c-eea8-4662-9340-3c063b0addb8"
        }
    }
