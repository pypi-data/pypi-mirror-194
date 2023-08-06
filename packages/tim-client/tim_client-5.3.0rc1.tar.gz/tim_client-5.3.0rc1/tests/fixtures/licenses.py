from typing import Dict, Any
import pytest


@pytest.fixture
def mocked_api_response_license_detail() -> Dict[str, Any]:
    return {
        "name": "Tangent Works  - General License",
        "organizationName": "Tangent Works",
        "expiration": "2042-11-07T00:00:00.000Z",
        "datasetRowsLimit": 1000000,
        "additionalLicenseData": {
            "license_origin": "User",
            "administrator": "philip.wauters@tangent.works",
            "trial_license_case_description": "Regular license for Tangent Works",
            "telemetry_level": 2,
            "fqdn": "https://timws.tangent.works"
        },
        "licenseKey": "grew-w48e-e4gw-gwe9",
        "storageLimit": 204800.0,
        "datasetColumnsLimit": 6000,
        "plan": "General"
    }


@pytest.fixture
def mocked_api_response_license_storage() -> Dict[str, Any]:
    return {
        "datasetRowsLimit": 1000000,
        "limitMb": 204800.0,
        "hasFreeSpace": True,
        "datasetColumnsLimit": 6000,
        "usedMb": 26968.436608314514
    }
