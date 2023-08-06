from typing import Optional, Union
from tim.core.types import (
    UploadDatasetConfiguration,
    UpdateDatasetConfiguration
)


def is_valid_csv_configuration(
    configuration: Optional[Union[UploadDatasetConfiguration, UpdateDatasetConfiguration]]
) -> bool:
    if configuration is None:
        return True
    if "csvSeparator" in configuration:
        return False
    return True
