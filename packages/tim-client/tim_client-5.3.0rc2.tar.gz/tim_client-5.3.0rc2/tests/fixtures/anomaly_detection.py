from typing import Dict, Any, List, Tuple
import pytest
import pandas as pd


@pytest.fixture
def mocked_api_response_detection_job_registered() -> Dict[str, Any]:
    return {
        "id": "9ac3c670-a39c-11ec-17e1-917d3c34fc3f"
    }


@pytest.fixture
def mocked_api_response_detection_job_executed() -> Dict[str, Any]:
    return {
        "code": "JM09020",
        "message": "Detection job XYZ has been posted to queue."
    }


@pytest.fixture
def mocked_api_response_detection_job_status_running() -> Dict[str, Any]:
    return {
        "createdAt": "2020-01-01T00:00:00.000Z",
        "status": "Running",
        "progress": 75.0,
        "memory": 92,
        "CPU": 92
    }


@pytest.fixture
def mocked_api_response_detection_job_status_finished() -> Dict[str, Any]:
    return {
        "createdAt": "2020-01-01T00:00:00.000Z",
        "status": "Finished",
        "progress": 100.0,
        "memory": 92,
        "CPU": 92
    }


@pytest.fixture
def mocked_api_response_detection_job_status_failed() -> Dict[str, Any]:
    return {
        "createdAt": "2020-01-01T00:00:00.000Z",
        "status": "Failed",
        "progress": 100.0,
        "memory": 92,
        "CPU": 92
    }


@pytest.fixture
def mocked_api_response_detection_job_status_collect() -> List[Dict[str, Any]]:
    return [
        {
            "createdAt": "2020-01-01T00:00:00.000Z",
            "status": "Running",
            "progress": 75.0,
            "memory": 92,
            "CPU": 92
        }
    ]


@pytest.fixture
def mocked_api_response_detection_job_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "My first anomaly detection job",
            "type": "build-model",
            "approach": "kpi-driven",
            "status": "Running",
            "parentJob": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            },
            "useCase": {
                "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
            },
            "dataset": {
                "version": {
                    "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
                }
            },
            "createdAt": "2020-01-13T00:00:00.000Z",
            "executedAt": "2020-01-14T00:00:00.000Z",
            "completedAt": "2020-01-14T00:00:10.000Z",
            "experiment": {
                "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
            },
            "workerVersion": "v5.0.1",
            "jobLoad": "Heavy",
            "calculationTime": "PT45.2S",
            "errorMeasures": {
                "AUC": 0.9375,
                "confusionMatrix": {
                    "truePositive": 4,
                    "trueNegative": 95,
                    "falsePositive": 0,
                    "falseNegative": 1
                }
            }
        }
    ]


@pytest.fixture
def mocked_api_response_detection_job_detail() -> Dict[str, Any]:
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "My first anomaly detection job",
        "type": "build-model",
        "approach": "kpi-driven",
        "status": "Running",
        "parentJob": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "useCase": {
            "id": "47c21df1-f5e5-4310-924c-5ea4c9adcbb2"
        },
        "dataset": {
            "version": {
                "id": "a74ae716-a86e-47f0-8a50-d8b21d6d7dd6"
            }
        },
        "createdAt": "2020-01-13T00:00:00.000Z",
        "executedAt": "2020-01-14T00:00:00.000Z",
        "completedAt": "2020-01-14T00:00:10.000Z",
        "experiment": {
            "id": "f2d3d8ee-3c05-4df7-abcf-b13f44073f42"
        },
        "workerVersion": "v5.0.1",
        "jobLoad": "Heavy",
        "calculationTime": "PT45.2S",
        "errorMeasures": {
            "AUC": 0.9375,
            "confusionMatrix": {
                "truePositive": 4,
                "trueNegative": 95,
                "falsePositive": 0,
                "falseNegative": 1
            }
        }
    }


@pytest.fixture
def mocked_api_response_detection_job_deleted() -> Dict[str, Any]:
    return {
        "message": "Detection job XYZ successfully stopped and deleted.",
        "code": "JM07027"
    }


@pytest.fixture
def mocked_api_response_detection_job_log() -> List[Dict[str, Any]]:
    return [
        {
            "createdAt": "2020-01-01T00:00:00.000Z",
            "origin": "Registration",
            "messageType": "Info",
            "message": "License is valid"
        }
    ]


@pytest.fixture
def mocked_api_response_detection_results_table() -> Tuple[pd.DataFrame, str]:
    mocked_result_df = pd.DataFrame(
        [['2020-01-01T00:00:00Z', 1], ['2020-01-01T01:00:00Z', 2], ['2020-01-01T02:00:00Z', 3]],
        columns=['timestamp', 'value']
    )
    mocked_api_response = mocked_result_df.to_csv(index=False)
    return mocked_result_df, mocked_api_response


@pytest.fixture
def mocked_api_response_detection_job_model() -> Dict[str, Any]:
    return {
        "modelVersion": "5.4",
        "model": {
            "modelZoo": {
                "samplingPeriod": "P1Y",
                "averageTrainingLength": 20,
                "models": [
                    {
                        "index": 1,
                        "terms": [
                            {
                                "importance": 100,
                                "parts": [
                                    {
                                        "type": "TimeLags",
                                        "predictor": "target",
                                        "offset": -1
                                    },
                                    {
                                        "type": "β",
                                        "value": 1.0987697211304948
                                    }
                                ]
                            }
                        ],
                        "dayTime": None,
                        "variableOffsets": [
                            {
                                "name": "Irradiation",
                                "dataFrom": -2,
                                "dataTo": -2
                            }
                        ],
                        "samplesAhead": [
                            1
                        ],
                        "modelQuality": 4,
                        "predictionIntervals": [
                            -157.42918064610092,
                            120.70451046551489
                        ],
                        "lastTargetTimestamp": "1994-01-01 00:00:00.0",
                        "RInv": [
                            0.0010011905696512698
                        ],
                        "g": [
                            1097.4631148525632
                        ],
                        "mx": [
                            2631.2636363636366
                        ],
                        "cases": [
                            {
                                "dayTime": "00:00:00.0",
                                "variableOffsets": [
                                    {
                                        "name": "Gascons",
                                        "dataTo": -1
                                    },
                                    {
                                        "name": "Irradiation",
                                        "dataTo": -2
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "difficulty": 0.6993536799963264,
                "targetName": "target",
                "holidayName": "",
                "groupKeys": [],
                "upperBoundary": 11209.8475,
                "lowerBoundary": 0,
                "dailyCycle": False,
                "confidenceLevel": 90,
                "variableProperties": [
                    {
                        "name": "target",
                        "min": 940.66,
                        "max": 9156.01,
                        "dataFrom": -1,
                        "importance": 100,
                        "aggregation": "Mean"
                    }
                ]
            }
        },
        "signature": "d65ad4bfabd23130c3f32b49472e0d92ae0ec"
    }


@pytest.fixture
def mocked_api_response_detection_job_accuracies() -> Dict[str, Any]:
    return {
        "AUC": 0.9375,
        "confusionMatrix": {
            "truePositive": 4,
            "trueNegative": 95,
            "falsePositive": 0,
            "falseNegative": 1
        }
    }
