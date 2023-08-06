# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_use_cases(client: Tim):
    new_use_case_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Use-Case")
    }
    updated_use_case_configuration = {
        "description": "Test Use Case Description"
    }

    new_use_case = client.use_cases.create_use_case(new_use_case_configuration)
    use_case_list = client.use_cases.list_use_case()
    new_use_case_detail = client.use_cases.details_use_case(new_use_case['id'])
    updated_use_case = client.use_cases.edit_use_case(new_use_case['id'], updated_use_case_configuration)
    client.use_cases.delete_use_case(new_use_case['id'])

    assert len(use_case_list) > 0
    assert new_use_case_detail is not None
    assert len([x for x in use_case_list if x['id'] == new_use_case_detail['id']]) > 0
    assert updated_use_case is not None
