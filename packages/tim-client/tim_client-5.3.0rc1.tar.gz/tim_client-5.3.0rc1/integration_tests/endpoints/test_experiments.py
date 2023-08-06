# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from tim import Tim
from integration_tests.utils import create_random_string_with_timestamp


def test_experiments(client: Tim):
    new_use_case_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Use-Case")
    }
    new_use_case = client.use_cases.create_use_case(new_use_case_configuration)

    new_experiment_configuration = {
        "name": create_random_string_with_timestamp(prefix="Test-Experiment"),
        "useCase": {
            "id": new_use_case['id']
        },
        "type": "Forecasting"
    }
    updated_experiment_configuration = {
        "description": "Test Experiment Description"
    }

    new_experiment = client.experiments.create_experiment(new_experiment_configuration)
    experiment_list = client.experiments.list_experiment()
    new_experiment_detail = client.experiments.details_experiment(new_experiment['id'])
    updated_experiment = client.experiments.edit_experiment(new_experiment['id'], updated_experiment_configuration)
    client.experiments.delete_experiment(new_experiment['id'])
    client.use_cases.delete_use_case(new_use_case['id'])

    assert len(experiment_list) > 0
    assert new_experiment_detail is not None
    assert len([x for x in experiment_list if x['id'] == new_experiment_detail['id']]) > 0
    assert updated_experiment is not None
