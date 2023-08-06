# type: ignore
# pylint: disable=missing-docstring, redefined-outer-name, unused-argument
from typing import Dict, Any
from tim import Tim


def test_properties(client: Tim, mocked_api_response_forecasting_job_model: Dict[str, Any]):
    expected_csv_string = 'name;min;max;dataFrom;importance;aggregation;rel_importance\ntarget;940.66;9156.01;-1;100;Mean;0.5\ntarget2;900.0;1000.0;-1;100;Mean;0.5\n'

    result = client.post_process.properties(mocked_api_response_forecasting_job_model)

    assert result.to_csv(sep=';', index=False) == expected_csv_string


def test_features(client: Tim, mocked_api_response_forecasting_job_model: Dict[str, Any]):
    expected_csv_string = 'Model;Term;Feature;importance;beta\n1;0;_test_;100;1.0987697211304948\n1;1;Intercept(1);0;75.74809714282492\n'

    result = client.post_process.features(mocked_api_response_forecasting_job_model)

    assert result.to_csv(sep=';', index=False) == expected_csv_string


def test_forecast_accuracy_table(client: Tim, mocked_api_response_forecasting_job_accuracies: Dict[str, Any]):
    expected_csv_string = 'KPI;name;accuracy_type;variable;value\nmae;all;all;outOfSample;2582.226415047165\nmape;all;all;outOfSample;5.073956161084446\nrmse;all;all;outOfSample;3348.002586596367\naccuracy;all;all;outOfSample;\nmae;1;samplesAhead;outOfSample;1457.9453762721573\nmape;1;samplesAhead;outOfSample;4.207242500336746\nrmse;1;samplesAhead;outOfSample;1908.051212051961\naccuracy;1;samplesAhead;outOfSample;\nmae;2;samplesAhead;outOfSample;1934.7433073553798\nmape;2;samplesAhead;outOfSample;5.9141594571897835\nrmse;2;samplesAhead;outOfSample;2673.0627076742135\naccuracy;2;samplesAhead;outOfSample;\nmae;S+1:S+2;bin;outOfSample;2582.226415047165\nmape;S+1:S+2;bin;outOfSample;5.073956161084446\nrmse;S+1:S+2;bin;outOfSample;3348.002586596367\naccuracy;S+1:S+2;bin;outOfSample;\nmae;all;all;inSample;2001.3693249439452\nmape;all;all;inSample;2.9330755325805624\nrmse;all;all;inSample;2586.7610856724464\naccuracy;all;all;inSample;\nmae;1;samplesAhead;inSample;1551.0465446016906\nmape;1;samplesAhead;inSample;3.1213518585471154\nrmse;1;samplesAhead;inSample;1860.5871856162785\naccuracy;1;samplesAhead;inSample;\nmae;2;samplesAhead;inSample;1274.326920891542\nmape;2;samplesAhead;inSample;2.6398151561182694\nrmse;2;samplesAhead;inSample;1615.911282512909\naccuracy;2;samplesAhead;inSample;\nmae;S+1:S+2;bin;inSample;2001.3693249439452\nmape;S+1:S+2;bin;inSample;2.9330755325805624\nrmse;S+1:S+2;bin;inSample;2586.7610856724464\naccuracy;S+1:S+2;bin;inSample;\n'

    result = client.post_process.forecast_accuracy_table(mocked_api_response_forecasting_job_accuracies)

    assert result.to_csv(sep=';', index=False) == expected_csv_string
