# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
import pandas as pd
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_extended_datasets(client: Tim, dataset_a: pd.DataFrame, dataset_b: pd.DataFrame):
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

    new_dataset = client.upload_dataset(
        dataset=dataset_a,
        configuration=new_dataset_configuration,
        wait_to_finish=True
    )

    dataset_id = new_dataset[0]['id']

    new_dataset_version = client.update_dataset(
        dataset_id=dataset_id,
        dataset_version=dataset_b,
        wait_to_finish=True
    )

    client.datasets.delete_dataset(dataset_id)

    assert new_dataset is not None
    assert new_dataset[0] is not None
    assert new_dataset[1] is not None
    assert new_dataset[2] is not None
    assert new_dataset_version is not None
    assert new_dataset_version[0] is not None
    assert new_dataset_version[1] is not None
    assert new_dataset_version[2] is not None
