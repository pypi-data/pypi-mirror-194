# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_user_groups(client: Tim):
    new_user_group_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-User-Group"),
        "users": []
    }
    updated_user_group_configuration = {
        "name": new_user_group_configuration['name'],
        "description": "Test User Group Description",
        "users": new_user_group_configuration['users']
    }

    new_user_group = client.user_groups.create_user_group(new_user_group_configuration)
    user_group_list = client.user_groups.list_user_group()
    new_user_group_detail = client.user_groups.details_user_group(new_user_group['id'])
    updated_user_group = client.user_groups.update_user_group(new_user_group['id'], updated_user_group_configuration)
    client.user_groups.delete_user_group(new_user_group['id'])

    assert len(user_group_list) > 1
    assert new_user_group_detail is not None
    assert len([x for x in user_group_list if x['id'] == new_user_group_detail['id']]) > 0
    assert updated_user_group is not None
