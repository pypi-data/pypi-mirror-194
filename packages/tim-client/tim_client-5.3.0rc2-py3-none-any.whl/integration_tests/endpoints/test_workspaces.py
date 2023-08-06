# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_workspaces(client: Tim):
    new_user_group_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-User-Group"),
        "users": []
    }
    new_user_group = client.user_groups.create_user_group(new_user_group_configuration)

    new_workspace_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Workspace"),
        "userGroup": {
            "id": new_user_group['id']
        }
    }
    updated_workspace_configuration = {
        "description": "Test Workspace Description"
    }

    new_workspace = client.workspaces.create_workspace(new_workspace_configuration)
    workspace_list = client.workspaces.list_workspace()
    new_workspace_detail = client.workspaces.details_workspace(new_workspace['id'])
    updated_workspace = client.workspaces.edit_workspace(new_workspace['id'], updated_workspace_configuration)
    client.workspaces.delete_workspace(new_workspace['id'])
    client.user_groups.delete_user_group(new_user_group['id'])

    assert len(workspace_list) > 0
    assert new_workspace_detail is not None
    assert len([x for x in workspace_list if x['id'] == new_workspace_detail['id']]) > 0
    assert updated_workspace is not None
