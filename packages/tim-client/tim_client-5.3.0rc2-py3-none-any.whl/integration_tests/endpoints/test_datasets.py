# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from time import sleep
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_datasets(client: Tim, dataset_a: pd.DataFrame, dataset_b: pd.DataFrame):
    new_dataset_configuration = {
        "timestampFormat": "yyyy-mm-dd HH:MM:SS",
        "timestampColumn": "Date",
        "decimalSeparator": ".",
        "timeZone": "Z",
        "name": create_random_string_with_timestamp(prefix="Test-Dataset"),
        "samplingPeriod": {
            "baseUnit": "Hour",
            "value": 1
        }
    }

    updated_dataset_configuration = {
        "description": "Test Dataset Description"
    }

    new_dataset = client.datasets.upload_dataset(dataset_a, configuration=new_dataset_configuration)
    sleep(5)
    i = 0
    while True:
        new_dataset_status = client.datasets.status_dataset_version(
            new_dataset['id'],
            new_dataset['version']['id']
        )
        status = new_dataset_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Dataset upload failed')
        if i > 90:
            raise ValueError('Dataset upload took too long')
        i += 1
        sleep(2)

    dataset_list = client.datasets.list_dataset(
        offset=0,
        limit=10,
        sort='-createdAt'
    )
    new_dataset_detail = client.datasets.details_dataset(new_dataset['id'])

    new_dataset_version = client.datasets.update_dataset(new_dataset['id'], dataset_b)
    sleep(5)
    i = 0
    while True:
        new_dataset_status = client.datasets.status_dataset_version(
            new_dataset['id'],
            new_dataset_version['version']['id']
        )
        status = new_dataset_status.get('status')
        if status.startswith('Finished'):
            break
        if status.startswith('Failed'):
            raise ValueError('Dataset update failed')
        if i > 90:
            raise ValueError('Dataset update took too long')
        i += 1
        sleep(2)

    dataset_versions_list = client.datasets.list_dataset_versions(new_dataset['id'])
    updated_dataset = client.datasets.edit_dataset_details(new_dataset['id'], updated_dataset_configuration)

    new_dataset_slice = client.datasets.slice_dataset_version(new_dataset['id'], new_dataset['version']['id'])

    client.datasets.delete_dataset(new_dataset['id'])

    assert len(dataset_list) > 0
    assert new_dataset is not None
    assert new_dataset_detail is not None
    assert new_dataset_version is not None
    assert dataset_versions_list is not None
    assert len(dataset_versions_list) == 2
    assert updated_dataset is not None
    assert new_dataset_slice is not None
