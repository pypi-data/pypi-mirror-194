from enum import Enum
from typing import List, Union, Optional, NamedTuple
from typing_extensions import TypedDict
from pandas import DataFrame

# ------------------------------------ General ------------------------------------


class Id(TypedDict):
    id: str


class ExtendedId(TypedDict):
    id: str
    name: str


class SortDirection(Enum):
    CREATED_AT_DESC = '-createdAt'
    CREATED_AT_ASC = '+createdAt'
    UPDATED_AT_DESC = '-updatedAt'
    UPDATED_AT_ASC = '+updatedAt'
    TITLE_DESC = '-title'
    TITLE_ASC = '+title'


class BaseUnit(Enum):
    DAY = 'Day'
    HOUR = 'Hour'
    MINUTE = 'Minute'
    SECOND = 'Second'
    MONTH = 'Month'
    SAMPLE = 'Sample'


class BaseUnitRange(TypedDict):
    baseUnit: BaseUnit
    value: int


class RangeType(Enum):
    FIRST = 'First'
    LAST = 'Last'


class RelativeRange(TypedDict):
    type: RangeType
    baseUnit: BaseUnit
    value: int


Range = TypedDict('Range', {'from': str, 'to': str})


class Status(Enum):
    REGISTERED = 'Registered'
    RUNNING = 'Running'
    FINISHED = 'Finished'
    FINISHED_WITH_WARNING = 'FinishedWithWarning'
    FAILED = 'Failed'
    QUEUED = 'Queued'
# ------------------------------------ Telemetry ------------------------------------


class JobState(Enum):
    EXISTING = 'Existing'
    DELETED = 'Deleted'


class TelemetryCallState(Enum):
    DELETED = 'Deleted'
    REGISTERED = 'Registered'
    RUNNING = 'Running'
    FINISHED = 'Finished'
    FINISHED_WITH_WARNING = 'FinishedWithWarning'
    FAILED = 'Failed'
    QUEUED = 'Queued'


class BlockWithIdStateAndCreatedAt(TypedDict):
    id: str
    state: TelemetryCallState
    createdAt: Optional[str]


class TelemetryDataset(TypedDict):
    id: Optional[str]
    version: Optional[BlockWithIdStateAndCreatedAt]


class TelemetryResponse(TypedDict):
    time: Optional[str]
    code: Optional[int]
    APIResponseCode: Optional[str]


class TelemetryRequest(TypedDict):
    method: str
    target: str
    microservice: str


class DatasetCall(TypedDict):
    id: str
    time: str
    TIMClientOrigin: str
    imageVersion: str
    madeBy: Optional[str]
    dataset: Optional[TelemetryDataset]
    response: Optional[TelemetryResponse]
    request: Optional[TelemetryRequest]


class TelemetryJob(TypedDict):
    id: str
    parentJob: Optional[Id]
    state: TelemetryCallState
    createdAt: Optional[str]


class JobCall(TypedDict):
    id: str
    time: str
    TIMClientOrigin: str
    imageVersion: str
    madeBy: Optional[str]
    dataset: Optional[TelemetryDataset]
    response: Optional[TelemetryResponse]
    request: Optional[TelemetryRequest]
    job: Optional[TelemetryJob]
    experiment: Optional[Id]

# ------------------------------------ Licenses ------------------------------------


class LicensePlan(Enum):
    TRIAL = 'Trial'
    BASIC = 'Basic'
    PROFESSIONAL = 'Professional'
    ENTERPISE = 'Enterprise'
    GENERAL = 'General'
    PARTNER = 'Partner'


class License(TypedDict):
    licenseKey: str
    name: str
    organizationName: str
    expiration: str
    plan: LicensePlan
    storageLimit: float
    datasetRowsLimit: int
    datasetColumnsLimit: int
    additionalLicenseData: Optional[TypedDict]


class LicenseStorage(TypedDict):
    usedMb: float
    limitMb: float
    hasFreeSpace: bool
    datasetRowsLimit: int
    datasetColumnsLimit: int

# ------------------------------------ User Groups ------------------------------------


class UserGroup(TypedDict, total=False):
    id: str
    name: str
    description: Optional[str]
    createdAt: str
    createdBy: str
    updatedAt: Optional[str]
    updatedBy: Optional[str]


class UserGroupUser(TypedDict):
    id: str
    isOwner: bool


class UserGroupPost(TypedDict):
    name: str
    description: Optional[str]
    users: List[UserGroupUser]

# ------------------------------------ Authentication ------------------------------------


class Role(Enum):
    ADMINISTRATOR = 'administrator'
    STANDARD = 'standard'


class TokenPayload(TypedDict):
    email: str
    firstName: str
    lastName: str
    userId: str
    licenseKey: str
    role: Role
    loggedInAt: str
    expiresIn: int
    expiresAt: str
    tokenId: str


class LicenseKey(TypedDict):
    licenseKey: str


class User(TypedDict):
    id: str
    email: str
    firstName: str
    lastName: str
    license: LicenseKey
    isActive: bool
    isAdmin: bool
    additionalUserData: Optional[TypedDict]
    personalUserGroup: Id
    lastLogin: Optional[str]


class AuthResponse(TypedDict):
    token: str
    loggedInAt: str
    expiresIn: int
    tokenPayload: TokenPayload
    license: License
    user: User
    personalUserGroup: UserGroup

# ------------------------------------ Workspaces ------------------------------------


class Workspace(TypedDict):
    id: str
    name: str
    description: Optional[str]
    userGroup: Id
    isFavorite: bool
    createdAt: str
    createdBy: str
    updatedAt: Optional[str]
    updatedBy: Optional[str]


class WorkspacePost(TypedDict):
    name: str
    description: Optional[str]
    userGroup: Id
    isFavorite: Optional[bool]


class WorkspacePut(TypedDict):
    name: Optional[str]
    description: Optional[str]
    isFavorite: Optional[bool]

# ------------------------------------ Use Cases ------------------------------------


class UseCase(TypedDict):
    id: str
    name: str
    description: Optional[str]
    input: Optional[str]
    output: Optional[str]
    businessValue: Optional[str]
    businessObjective: Optional[str]
    businessKpi: Optional[str]
    accuracyImpact: Optional[int]
    workspace: Id
    dataset: Optional[Id]
    isFavorite: bool
    defaultFExperiment: Optional[Id]
    defaultADExperiment: Optional[Id]
    createdAt: str
    createdBy: str
    updatedAt: Optional[str]
    updatedBy: Optional[str]


class UseCasePost(TypedDict):
    name: str
    description: Optional[str]
    input: Optional[str]
    output: Optional[str]
    businessValue: Optional[str]
    businessObjective: Optional[str]
    businessKpi: Optional[str]
    accuracyImpact: Optional[int]
    workspace: Optional[Id]
    dataset: Optional[Id]
    isFavorite: Optional[bool]


class UseCasePut(TypedDict):
    name: Optional[str]
    description: Optional[str]
    input: Optional[str]
    output: Optional[str]
    businessValue: Optional[str]
    businessObjective: Optional[str]
    businessKpi: Optional[str]
    accuracyImpact: Optional[int]
    dataset: Optional[Id]
    isFavorite: Optional[bool]
    defaultFExperiment: Optional[Id]
    defaultADExperiment: Optional[Id]
# # ------------------------------------ Experiments ------------------------------------


class JobType(Enum):
    FORECASTING = 'Forecasting'
    ANOMALYDETECTION = 'AnomalyDetection'


class Experiment(TypedDict):
    id: str
    name: str
    description: Optional[str]
    useCase: Id
    workspace: Id
    userGroup: Id
    type: JobType
    createdAt: str
    createdBy: str
    updatedAt: Optional[str]
    updatedBy: Optional[str]


class ExperimentPost(TypedDict):
    name: str
    description: Optional[str]
    useCase: Id
    type: JobType


class ExperimentPut(TypedDict):
    name: Optional[str]
    description: Optional[str]

# # ------------------------------------ Datasets ------------------------------------


class DecimalSeparator(Enum):
    COMMA = ','
    DOT = '.'


class CSVSeparator(Enum):
    SEMICOLON = ';'
    TAB = ' '
    COMMA = ','


class UploadDatasetConfiguration(TypedDict, total=False):
    timestampFormat: Optional[str]
    timestampColumn: Optional[Union[str, int]]
    decimalSeparator: Optional[DecimalSeparator]
    csvSeparator: Optional[str]
    timeZone: Optional[str]
    timeZoneName: Optional[str]
    groupKeys: Optional[List[Union[str, int]]]
    name: Optional[str]
    description: Optional[str]
    samplingPeriod: Optional[BaseUnitRange]
    workspace: Optional[Id]


class DatasetCreated(TypedDict):
    id: str
    version: Id


class UpdateDatasetConfiguration(TypedDict, total=False):
    timestampFormat: Optional[str]
    timestampColumn: Optional[Union[str, int]]
    decimalSeparator: Optional[DecimalSeparator]
    csvSeparator: Optional[str]


class DatasetVersion(TypedDict):
    version: Id


class DatasetStatusResponse(TypedDict):
    createdAt: str
    status: Status
    progress: int


class LatestVersion(TypedDict):
    id: str
    status: Status
    numberOfVariables: int
    numberOfObservations: int
    firstTimestamp: str
    lastTimestamp: str


class DatasetDetails(TypedDict):
    id: str
    latestVersion: LatestVersion
    createdAt: str
    createdBy: str
    updatedAt: Optional[str]
    updatedBy: Optional[str]
    description: Optional[str]
    isFavorite: bool
    estimatedSamplingPeriod: str
    groupKeys: Optional[List[Union[str, int]]]
    timeZoneName: Optional[str]
    workspace: ExtendedId
    name: str


class Variables(TypedDict):
    name: str
    type: str
    firstTimestamp: str
    lastTimestamp: str
    minimumValue: float
    maximumValue: float
    averageValue: float
    missingObservations: int


class DatasetVersionDetails(TypedDict):
    id: str
    dataset: Id
    estimatedSamplingPeriod: str
    size: int
    numberOfObservations: int
    numberOfVariables: int
    firstTimestamp: str
    lastTimestamp: str
    variables: List[Variables]
    createdAt: str
    status: Status
    groupKeys: Optional[List[Union[str, int]]]
    timeZoneName: Optional[str]


class DatasetOrigin(Enum):
    UPLOAD = 'Upload'
    UPDATE = 'Update'


class MessageType(Enum):
    INFO = 'Info'
    WARNING = 'Warning'
    ERROR = 'Error'


class DatasetLog(TypedDict):
    createdAt: str
    origin: DatasetOrigin
    messageType: MessageType
    message: str
    version: Id


class DatasetVersionLog(TypedDict):
    createdAt: str
    origin: DatasetOrigin
    messageType: MessageType
    message: str


class DatasetPut(TypedDict):
    name: Optional[str]
    description: Optional[str]


class UploadDatasetResponse(NamedTuple):
    response: DatasetVersion
    details: Optional[DatasetDetails]
    logs: List[DatasetLog]


class DatasetOutputs(Enum):
    RESPONSE = 'response'
    LOGS = 'logs'
    METADATA = 'metadata'

# ------------------------------------ Forecasting ------------------------------------


class ModelQuality(Enum):
    COMBINED = 'Combined'
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    VERYHIGH = 'VeryHigh'
    ULTRAHIGH = 'UltraHigh'


class Features(Enum):
    EXPONENTIAL_MOVING_AVERAGE = 'ExponentialMovingAverage'
    REST_OF_WEEK = 'RestOfWeek'
    PERIODIC = 'Periodic'
    INTERCEPT = 'Intercept'
    PIECEWISE_LINEAR = 'PiecewiseLinear'
    TIME_OFFSETS = 'TimeOffsets'
    POLYNOMIAL = 'Polynomial'
    IDENTITY = 'Identity'
    SIMPLE_MOVING_AVERAGE = 'SimpleMovingAverage'
    MONTH = 'Month'
    TREND = 'Trend'
    DAY_OF_WEEK = 'DayOfWeek'
    FOURIER = 'Fourier'
    PUBLIC_HOLIDAYS = 'PublicHolidays'
    COS = 'Cos'
    SIN = 'Sin'


class OffsetLimitType(Enum):
    EXPLICIT = 'Explicit'


class OffsetLimit(TypedDict):
    type: OffsetLimitType
    value: int


class PredictionBoundariesType(Enum):
    EXPLICIT = 'Explicit'
    NONE = 'None'


class PredictionBoundaries(TypedDict):
    type: PredictionBoundariesType
    maxValue: float
    minValue: float


class Backtest(Enum):
    ALL = 'All'
    PRODUCTION = 'Production'
    OUT_OF_SAMPLE = 'OutOfSample'


class ImputationType(Enum):
    LINEAR = 'Linear'
    LOCF = 'LOCF'
    NONE = 'None'


class Imputation(TypedDict):
    type: ImputationType
    maxGapLength: int


class Aggregation(Enum):
    MEAN = 'Mean'
    SUM = 'Sum'
    MINIMUM = 'Minumum'
    MAXIMUM = 'Maximum'


class DataUntil(TypedDict):
    column: Union[str, int]
    baseUnit: BaseUnit
    offset: int


class DataAlignement(TypedDict):
    lastTargetTimestamp: str
    dataUntil: List[DataUntil]


class PreprocessorType(Enum):
    CATEGORYFILTER = 'CategoryFilter'


class CategoryFilterSimple(TypedDict):
    column: str
    categories: List[str]


class Preprocessors(TypedDict):
    type: PreprocessorType
    value: Union[CategoryFilterSimple, List[CategoryFilterSimple]]


class ForecastingBuildModelConfiguration(TypedDict):
    predictionTo: Optional[BaseUnitRange]
    predictionFrom: Optional[BaseUnitRange]
    modelQuality: Optional[ModelQuality]
    normalization: Optional[bool]
    maxModelComplexity: Optional[int]
    features: Optional[List[Features]]
    dailyCycle: Optional[bool]
    allowOffsets: Optional[bool]
    offsetLimit: Optional[OffsetLimit]
    memoryLimitCheck: Optional[bool]
    predictionIntervals: Optional[float]
    predictionBoundaries: Optional[PredictionBoundaries]
    rollingWindow: Optional[BaseUnitRange]
    backtest: Optional[Backtest]


class ForecastingBuildModelData(TypedDict):
    version: Optional[Id]
    inSampleRows: Optional[Union[RelativeRange, List[Range]]]
    outOfSampleRows: Optional[Union[RelativeRange, List[Range]]]
    imputation: Optional[Imputation]
    columns: Optional[List[Union[str, int]]]
    targetColumn: Optional[Union[str, int]]
    holidayColumn: Optional[Union[str, int]]
    timeScale: Optional[BaseUnitRange]
    aggregation: Optional[Aggregation]
    alignment: Optional[DataAlignement]
    preprocessors: Optional[List[Preprocessors]]


class ForecastingBuildModel(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[ForecastingBuildModelConfiguration]
    data: Optional[ForecastingBuildModelData]


class RebuildingPolicyType(Enum):
    NEWSITUATIONS = 'NewSituations'
    ALL = 'All'
    OLDERTHAN = 'OlderThan'


class RebuildingPolicy(TypedDict):
    type: RebuildingPolicyType
    time: BaseUnitRange


class ForecastingRebuildModelConfiguration(TypedDict):
    predictionTo: Optional[BaseUnitRange]
    predictionFrom: Optional[BaseUnitRange]
    modelQuality: Optional[ModelQuality]
    normalization: Optional[bool]
    maxModelComplexity: Optional[int]
    features: Optional[List[Features]]
    allowOffsets: Optional[bool]
    offsetLimit: Optional[OffsetLimit]
    memoryLimitCheck: Optional[bool]
    rebuildingPolicy: Optional[RebuildingPolicy]
    predictionIntervals: Optional[float]
    predictionBoundaries: Optional[PredictionBoundaries]
    rollingWindow: Optional[BaseUnitRange]
    backtest: Optional[Backtest]


class ForecastingRebuildModelData(TypedDict):
    version: Optional[Id]
    inSampleRows: Optional[Union[RelativeRange, List[Range]]]
    outOfSampleRows: Optional[Union[RelativeRange, List[Range]]]
    imputation: Optional[Imputation]
    columns: Optional[List[Union[str, int]]]
    alignment: Optional[DataAlignement]
    preprocessors: Optional[List[Preprocessors]]


class ForecastingRebuildModel(TypedDict):
    name: Optional[str]
    experiment: Optional[Id]
    configuration: Optional[ForecastingRebuildModelConfiguration]
    data: Optional[ForecastingRebuildModelData]


class ForecastingRetrainModelConfiguration(TypedDict):
    predictionTo: Optional[BaseUnitRange]
    predictionFrom: Optional[BaseUnitRange]
    normalization: Optional[bool]
    memoryLimitCheck: Optional[bool]
    predictionBoundaries: Optional[PredictionBoundaries]
    rollingWindow: Optional[BaseUnitRange]
    backtest: Optional[Backtest]


class ForecastingRetrainModelData(TypedDict):
    version: Optional[Id]
    inSampleRows: Optional[Union[RelativeRange, List[Range]]]
    outOfSampleRows: Optional[Union[RelativeRange, List[Range]]]
    imputation: Optional[Imputation]
    alignment: Optional[DataAlignement]
    preprocessors: Optional[List[Preprocessors]]


class ForecastingRetrainModel(TypedDict):
    name: Optional[str]
    experiment: Optional[Id]
    configuration: Optional[ForecastingRetrainModelConfiguration]
    data: Optional[ForecastingRetrainModelData]


class ForecastingPredictConfiguration(TypedDict):
    predictionTo: Optional[BaseUnitRange]
    predictionFrom: Optional[BaseUnitRange]
    predictionBoundaries: Optional[PredictionBoundaries]
    rollingWindow: Optional[BaseUnitRange]


class ForecastingPredictData(TypedDict):
    version: Optional[Id]
    outOfSampleRows: Optional[Union[RelativeRange, List[Range]]]
    imputation: Optional[Imputation]
    alignment: Optional[DataAlignement]
    preprocessors: Optional[List[Preprocessors]]


class ForecastingPredict(TypedDict):
    name: Optional[str]
    experiment: Optional[Id]
    configuration: Optional[ForecastingPredictConfiguration]
    data: Optional[ForecastingPredictData]


class JobResponse(TypedDict):
    id: str
    expectedResultsTableSize: float


class ForecastingJobType(Enum):
    BUILD_MODEL = 'build-model'
    UPLOAD_MODEL = 'upload-model'
    REBUILD_MODEL = 'rebuild-model'
    RETRAIN_MODEL = 'retrain-model'
    PREDICT = 'predict'
    RCA = 'rca'
    WHAT_IF = 'what-if'


class AccuraciesRegression(TypedDict):
    mae: float
    mape: float
    rmse: float


class ConfusionMatrix(TypedDict):
    truePositive: int
    trueNegative: int
    falsePositive: int
    falseNegative: int


class AccuraciesClassification(TypedDict):
    accuracy: float
    AUC: float
    confusionMatrix: ConfusionMatrix


class AccuraciesForecasting(TypedDict):
    name: str
    outOfSample: Union[AccuraciesRegression, AccuraciesClassification]
    inSample: Union[AccuraciesRegression, AccuraciesClassification]


class ErrorMeasures(TypedDict):
    all: AccuraciesForecasting
    bin: List[AccuraciesForecasting]
    samplesAhead: List[AccuraciesForecasting]


class ExecuteResponse(TypedDict):
    message: str
    code: str


class StatusResponse(TypedDict):
    createdAt: str
    status: Status
    progress: float
    memory: int
    CPU: int


class JobExecuteResponse(TypedDict):
    id: str
    response: ExecuteResponse
    status: Union[str, StatusResponse]


class ForecastLogPayload(TypedDict, total=False):
    id: str
    offset: int
    limit: int
    sort: SortDirection


class ForecastTableRequestPayload(TypedDict):
    forecastType: Optional[str]
    modelIndex: Optional[int]


class JobOrigin(Enum):
    REGISTRATION = 'Registration'
    EXECUTION = 'Executed'
    VALIDATION = 'Validation'


class JobLogs(TypedDict):
    createdAt: str
    origin: JobOrigin
    messageType: MessageType
    message: str


class VariableProperties(TypedDict, total=False):
    name: str
    min: float
    max: float
    dataFrom: int
    importance: float
    aggregation: str


class VariableOffsets(TypedDict, total=False):
    name: str
    dataFrom: int
    dataTo: int


class Cases(TypedDict):
    dayTime: str
    variableOffsets: VariableOffsets


class Part(TypedDict):
    type: str
    predictor: str
    offset: int
    value: float
    window: int
    knot: float
    subtype: int
    period: float
    cosOrders: List[float]
    sinOrder: List[float]
    cosβ: List[float]
    sinβ: List[float]
    unit: str
    day: int
    month: int


class Term(TypedDict):
    importance: int
    parts: List[Part]


class ModelZooModel(TypedDict):
    index: int
    terms: List[Term]
    dayTime: str
    variableOffsets: List[VariableOffsets]
    samplesAhead: List[int]
    modelQuality: int
    predictionIntervals: List[int]
    lastTargetTimestamp: str
    RInv: List[float]
    g: List[float]
    mx: List[float]
    cases: List[Cases]


class ModelZoo(TypedDict):
    samplingPeriod: str
    averageTrainingLength: int
    models: List[ModelZooModel]
    difficulty: int
    targetName: str
    holidayName: str
    groupKeys: List[str]
    upperBoundary: int
    lowerBoundary: int
    dailyCycle: bool
    confidenceLevel: int
    variableProperties: List[VariableProperties]
    inSampleRows: List[Range]
    outofSampleRows: List[Range]


class Model(TypedDict):
    modelZoo: ModelZoo


class ForecastModelResult(TypedDict):
    modelVersion: str
    model: Model
    signature: str


class WhatIf(TypedDict):
    column: str
    data: TypedDict


class WhatIfPanel(TypedDict):
    column: str
    groupKeysValues: List[Union[str, int]]
    data: TypedDict


class CopyExperiment(TypedDict):
    experiment: Id


class ProductionAccuraciesForecasting(TypedDict):
    name: str
    production: Union[AccuraciesRegression, AccuraciesClassification]


class ResultsProductionAccuraciesForecasting(TypedDict):
    all: ProductionAccuraciesForecasting
    bin: List[ProductionAccuraciesForecasting]
    samplesAhead: List[ProductionAccuraciesForecasting]


class ModelFromJob(TypedDict):
    job: Id


class ForecastingUploadModel(TypedDict):
    name: str
    useCase: Id
    experiment: Id
    model: Union[ModelFromJob, ForecastModelResult]


class ForecastingResultsOptions(Enum):
    ID = 'id'
    DETAILS = 'details'
    LOGS = 'logs'
    TABLE = 'table'
    STATUS = 'status'
    PRODUCTION_FORECAST = 'production_forecast'
    MODEL = 'model'
    ACCURACIES = 'accuracies'
    PRODUCTION_TABLE = 'production_table'
    PRODUCTION_ACCURACIES = 'production_accuracies'


class ForecastingJobMetaData(TypedDict):
    registrationBody: Union[
        ForecastingBuildModel,
        ForecastingRebuildModel,
        ForecastingRetrainModel,
        ForecastingPredict,
        ForecastingUploadModel,
        WhatIf,
        WhatIfPanel
    ]
    errorMeasures: ErrorMeasures
    id: str
    name: Optional[str]
    type: ForecastingJobType
    status: Optional[Status]
    parentJob: Id
    sequenceId: Optional[str]
    useCase: Id
    experiment: Id
    dataset: DatasetVersion
    createdAt: str
    executedAt: Optional[str]
    completedAt: Optional[str]
    workerVersion: Optional[str]
    jobLoad: Optional[str]
    calculationTime: Optional[str]


class ForecastingResultsOutputs(NamedTuple):
    id: Optional[str]
    details: Optional[ForecastingJobMetaData]
    logs: Optional[List[JobLogs]]
    status: Optional[StatusResponse]
    table: Optional[DataFrame]
    production_forecast: Optional[DataFrame]
    model: Optional[ForecastModelResult]
    accuracies: Optional[ErrorMeasures]
    production_table: Optional[DataFrame]
    production_accuracies: Optional[ResultsProductionAccuraciesForecasting]


class RCAResults(TypedDict):
    indexOfModel: int
    results: DataFrame


class ForecastingResultsRCAOptions(Enum):
    ID = 'id'
    DETAILS = 'details'
    LOGS = 'logs'
    STATUS = 'status'
    RESULTS = 'results'


class ForecastingRCAOutput(NamedTuple):
    id: Optional[str]
    details: Optional[ForecastingJobMetaData]
    logs: Optional[List[JobLogs]]
    status: Optional[StatusResponse]
    results: RCAResults


class QuickForecast(NamedTuple):
    upload_response: Union[DatasetCreated, UploadDatasetResponse]
    forecast_response: Union[JobResponse, JobExecuteResponse, ForecastingResultsOutputs]
    delete_response: ExecuteResponse

# # ------------------------------------ Detection ------------------------------------


class Perspective(Enum):
    RESIDUAL = 'Residual'
    RESIDUAL_CHANGE = 'ResidualChange'
    FLUCTUATION = 'Fluctuation'
    FLUCTUATION_CHANGE = 'FluctuationChange'
    IMBALANCE = 'Imbalance'
    IMBALANCE_CHANGE = 'ImbalanceChange'


class DomainSpecificsKPI(TypedDict):
    perspective: Perspective
    sensitivity: float
    minSensitivity: float
    maxSensitivity: float


class NormalBehaviorModel(TypedDict):
    useNormalBehaviorModel: bool
    normalization: bool
    maxModelComplexity: int
    features: List[Features]
    dailyCycle: bool
    useKPIoffsets: bool
    allowOffsets: bool
    offsetLimit: OffsetLimit


class DetectionIntervalsType(Enum):
    DAY = 'Day'
    HOUR = 'Hour'
    MINUTE = 'Minute'
    SECOND = 'Second'


class DetectionIntervals(TypedDict):
    type: DetectionIntervalsType
    value: str


class AnomalousBehaviorModel(TypedDict):
    maxModelComplexity: int
    detectionIntervals: List[DetectionIntervals]


class UpdateTime(TypedDict):
    type: DetectionIntervalsType
    value: str


class UpdateUntilBaseUnit(Enum):
    DAY = 'Day'
    HOUR = 'Hour'
    SAMPLE = 'Sample'


class UpdateUntil(TypedDict):
    baseUnit: UpdateUntilBaseUnit
    offset: int


class Updates(TypedDict):
    column: Union[str, int]
    updateTime: List[UpdateTime]
    updateUntil: UpdateUntil


class DetectionBuildKPIModelConfiguration(TypedDict):
    domainSpecifics: Optional[List[DomainSpecificsKPI]]
    normalBehaviorModel: Optional[NormalBehaviorModel]
    anomalousBehaviorModel: Optional[AnomalousBehaviorModel]


class DetectionBuildKPIModelData(TypedDict):
    version: Optional[Id]
    rows: Optional[Union[RelativeRange, List[Range]]]
    columns: Optional[List[Union[str, int]]]
    KPIColumn: Optional[Union[str, int]]
    holidayColumn: Optional[Union[str, int]]
    labelColumn: Optional[Union[str, int]]
    imputation: Optional[Imputation]
    timeScale: Optional[BaseUnitRange]
    aggregation: Optional[Aggregation]
    updates: Optional[List[Updates]]


class DetectionBuildKPIModel(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[DetectionBuildKPIModelConfiguration]
    data: Optional[DetectionBuildKPIModelData]


class DetectionBuildDriftModelKolmogorovSmirnovConfiguration(TypedDict):
    pValue: Optional[float]


class DetectionBuildDriftModelKolmogorovSmirnovData(TypedDict):
    version: Optional[Id]
    referenceRows: Optional[Union[RelativeRange, List[Range]]]
    testRows: Union[RelativeRange, List[Range]]
    columns: Optional[List[Union[str, int]]]
    timeScale: Optional[BaseUnitRange]


class DetectionBuildDriftModelKolmogorovSmirnov(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[DetectionBuildDriftModelKolmogorovSmirnovConfiguration]
    data: DetectionBuildDriftModelKolmogorovSmirnovData


class DetectionBuildDriftModelJensenShannonConfiguration(TypedDict):
    threshold: Optional[float]


class DetectionBuildDriftModelJensenShannonData(TypedDict):
    version: Optional[Id]
    referenceRows: Optional[Union[RelativeRange, List[Range]]]
    testRows: Union[RelativeRange, List[Range]]
    columns: Optional[List[Union[str, int]]]
    timeScale: Optional[BaseUnitRange]


class DetectionBuildDriftModelJensenShannon(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[DetectionBuildDriftModelJensenShannonConfiguration]
    data: DetectionBuildDriftModelJensenShannonData


class DomainSpecificsSystem(TypedDict):
    sensitivity: float
    minSensitivity: float
    maxSensitivity: float
    anomalyIndicatorWindow: BaseUnitRange


class SystemModelConfiguration(TypedDict):
    numberOfTrees: int
    subSampleSize: int
    maxTreeDepth: int
    extensionLevel: int
    normalization: bool


class DetectionBuildSystemModelConfiguration(TypedDict):
    domainSpecifics: Optional[DomainSpecificsSystem]
    model: Optional[SystemModelConfiguration]


class DetectionBuildSystemModelData(TypedDict):
    version: Id
    rows: Union[RelativeRange, List[Range]]
    columns: List[Union[str, int]]
    labelColumn: Union[str, int]
    imputation: Imputation
    timeScale: BaseUnitRange


class DetectionBuildSystemModel(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[DetectionBuildSystemModelConfiguration]
    data: Optional[DetectionBuildSystemModelData]


class DetectionBuildOutlierModelConfiguration(TypedDict):
    maxModelComplexity: Optional[int]
    sensitivity: Optional[int]


class DetectionBuildOutlierModelData(TypedDict):
    version: Optional[Id]
    rows: Optional[Union[RelativeRange, List[Range]]]
    columns: Optional[List[Union[str, int]]]
    timeScale: Optional[BaseUnitRange]


class DetectionBuildOutlierModel(TypedDict):
    name: Optional[str]
    useCase: Id
    experiment: Optional[Id]
    configuration: Optional[DetectionBuildOutlierModelConfiguration]
    data: Optional[DetectionBuildOutlierModelData]


class RebuildType(Enum):
    DOMAIN_SPECIFICS = 'DomainSpecifics'
    ANOMALOUS_BEHAVIOR_MODEL = 'AnomalousBehaviorModel'
    ALL = 'All'


class DetectionRebuildKPIModelConfiguration(TypedDict):
    domainSpecifics: Optional[List[DomainSpecificsKPI]]
    rebuildType: Optional[RebuildType]


class DetectionRebuildKPIModelData(TypedDict):
    version: Optional[Id]
    rows: Optional[Union[RelativeRange, List[Range]]]
    imputation: Optional[Imputation]


class DetectionRebuildKPIModel(TypedDict):
    name: Optional[str]
    experiment: Optional[Id]
    configuration: Optional[DetectionRebuildKPIModelConfiguration]
    data: Optional[DetectionRebuildKPIModelData]


class DetectionDetect(TypedDict):
    name: Optional[str]
    experiment: Optional[Id]
    data: Optional[DetectionRebuildKPIModelData]


class DetectionErrorMeasures(TypedDict):
    AUC: float
    confusionMatrix: ConfusionMatrix


class AnomalyDetectionType(Enum):
    BUILD_MODEL = 'build-model'
    UPLOAD_MODEL = 'upload-model'
    REBUILD_MODEL = 'rebuild-model'
    DETECT = 'detect'
    RCA = 'rca'


class Approach(Enum):
    KPI_DRIVEN = 'kpi-driven'
    SYSTEM_DRIVEN = 'system-driven'


class DetectionPeriods(TypedDict):
    seconds: List[int]
    minutes: List[int]
    hours: List[int]
    DoW: List[int]


class anomalousBehaviorSettings(TypedDict):
    maxModelComplexity: int
    detectionPeriods: DetectionPeriods


class SettingsUpdatesUntil(TypedDict):
    increment: str
    offset: int


class SettingsUpdatesTimes(TypedDict):
    when: DetectionPeriods
    until: SettingsUpdatesUntil


class SettingsUpdates(TypedDict):
    predictorName: str
    update: SettingsUpdatesTimes


class ModelKpiDrivenSettingsData(TypedDict):
    rows: List[Range]
    columns: List[str]
    KPIColumn: str
    holidayColumn: str
    labelColumn: str
    imputation: Imputation
    timeScale: BaseUnitRange
    updates: List[SettingsUpdates]


class ProbabilityDistribution(TypedDict):
    n: int
    d: int
    w: List[float]


class ModelKpiDrivenNormalBehaviorModelModels(TypedDict):
    index: int
    terms: List[Term]
    dayTime: str
    variableOffsets: List[VariableOffsets]


class Submodel(TypedDict):
    perspective: Perspective
    probabilityDistribution: ProbabilityDistribution
    detectedSensitivity: float
    threshold: float
    translation: float
    cut: int


class ModelKpiDrivenSettings(TypedDict):
    data: ModelKpiDrivenSettingsData
    domainSpecifics: List[DomainSpecificsKPI]
    normalBehavior: NormalBehaviorModel
    anomalousBehavior: anomalousBehaviorSettings


class ModelKpiDrivenNormalBehaviorModel(TypedDict):
    samplingPeriod: str
    timeZone: str
    models: List[ModelKpiDrivenNormalBehaviorModelModels]
    VariableProperties: List[VariableProperties]


class ModelKpiDrivenAnomalousBehaviorModel(TypedDict):
    submodels: List[Submodel]


class ModelSystemSettingsData(TypedDict):
    rows: List[Range]
    columns: List[str]
    labelColumn: str
    imputation: Imputation
    timeScale: BaseUnitRange


class ModelSystemSettingsDomainSpecifics(TypedDict):
    sensitivity: float
    anomalyIndicatorWindow: BaseUnitRange


class ModelSystemSettingsModel(TypedDict):
    numberOfTrees: int
    subSampleSize: int
    maxTreeDepth: Union[str, int]
    extensionLevel: Union[str, int]
    normalization: bool


class Hyperplane(TypedDict):
    normal: List[float]
    intercept: List[float]


class InternalNode(TypedDict):
    type: str
    leftNode: TypedDict
    rightNode: TypedDict
    hyperplane: Hyperplane
    numOfRecords: int
    depth: int


class LeafNode(TypedDict):
    type: str
    numOfRecords: int
    depth: int


class rootNode(TypedDict):
    type: str
    leftNode: Union[InternalNode, LeafNode]
    rightNode: Union[InternalNode, LeafNode]
    hyperplane: Hyperplane
    numOfRecords: int
    depth: int


class TreeNodes(TypedDict):
    rootNode: rootNode
    numOfNodes: int


class TreeSettings(TypedDict):
    numOfTrees: int
    subSampleSize: int
    maxTreeDepth: int
    extensionLevel: int


class ModelSystemParametersAnomalyIndicator(TypedDict):
    detectedSensitivity: float
    threshold: float
    translation: float
    windowLength: int


class ModelSystemParametersNormalization(TypedDict):
    variableNames: List[str]
    mu: List[float]
    sigma: List[float]


class ModelSystemSettings(TypedDict):
    data: ModelSystemSettingsData
    domainSpecifics: ModelSystemSettingsDomainSpecifics
    model: ModelSystemSettingsModel


class ModelSystemModel(TypedDict):
    trees: List[TreeNodes]
    settings: TreeSettings


class ModelSystemParameters(TypedDict):
    anomalyIndicator: ModelSystemParametersAnomalyIndicator
    normalization: ModelSystemParametersNormalization
    samplingPeriod: str
    timeZone: str


class ModelKpiDriven(TypedDict):
    settings: ModelKpiDrivenSettings
    normalBehaviorModel: ModelKpiDrivenNormalBehaviorModel
    anomalousBehaviorModel: ModelKpiDrivenAnomalousBehaviorModel


class ModelSystemDriven(TypedDict):
    settings: ModelSystemSettings
    model: ModelSystemModel
    parameters: ModelSystemParameters


class DetectionModelResult(TypedDict):
    modelVersion: str
    approach: str
    model: Union[ModelKpiDriven, ModelSystemDriven]
    signature: str


class DetectionUploadModel(TypedDict):
    name: str
    useCase: Id
    experiment: Id
    model: Union[ModelFromJob, DetectionModelResult]


class DetectionResultsOptions(Enum):
    ID = 'id'
    DETAILS = 'details'
    LOGS = 'logs'
    TABLE = 'table'
    STATUS = 'status'
    MODEL = 'model'
    ACCURACIES = 'accuracies'
    PRODUCTION_TABLE = 'production_table'
    PRODUCTION_ACCURACIES = 'production_accuracies'


class DetectionJobDetails(TypedDict):
    id: str
    name: str
    type: AnomalyDetectionType
    approach: Approach
    status: Status
    parentJob: Id
    sequenceId: Optional[str]
    useCase: Id
    dataset: DatasetVersion
    createdAt: str
    executedAt: Optional[str]
    completedAt: Optional[str]
    experiment: Id
    workerVersion: Optional[str]
    jobLoad: Optional[str]
    calculationTime: Optional[str]
    registrationBody: Union[
        DetectionBuildKPIModel,
        DetectionBuildSystemModel,
        DetectionRebuildKPIModel,
        DetectionDetect,
        DetectionUploadModel,
        WhatIf,
        WhatIfPanel
    ]
    errorMeasures: Optional[DetectionErrorMeasures]


class DetectionResultsOutputs(NamedTuple):
    id: Optional[str]
    details: Optional[DetectionJobDetails]
    logs: Optional[List[JobLogs]]
    status: Optional[StatusResponse]
    table: Optional[DataFrame]
    model: Optional[ForecastModelResult]
    accuracies: Optional[ErrorMeasures]
    production_table: Optional[DataFrame]
    production_accuracies: Optional[DetectionErrorMeasures]


class DetectionResultsRCAOptions(Enum):
    ID = 'id'
    DETAILS = 'details'
    LOGS = 'logs'
    STATUS = 'status'
    RESULTS = 'results'


class DetectionRCAOutput(NamedTuple):
    id: Optional[str]
    details: Optional[DetectionJobDetails]
    logs: Optional[List[JobLogs]]
    status: Optional[StatusResponse]
    results: RCAResults


# # ------------------------------------ Datasets 2 ----------------------------------

class DatasetSliceConfiguration(TypedDict, total=False):
    outputFormat: Optional[str]
    rows: Optional[List[Range]]
    columns: Optional[List[Union[str, int]]]
    targetColumn: Optional[Union[str, int]]
    imputation: Optional[Imputation]
    timeScale: Optional[Union[str, BaseUnitRange]]
    aggregation: Optional[Aggregation]
    preprocessors: Optional[List[Preprocessors]]
    plotlyFriendly: Optional[bool]
    includeWasImputed: Optional[bool]
