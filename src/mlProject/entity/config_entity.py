from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict
    cleaned_file_path: str

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    read_data_path: Path
    eda_report_path: Path
    fe_file_path: str
    transformed_train_data: str
    transformed_test_data: str
