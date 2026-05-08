import os
import yaml
import json
import joblib
import base64
import boto3
import zipfile
from pathlib import Path
from typing import Any
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_size(path):
    """Get file size in human readable format"""
    import os
    size_bytes = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads yaml file and returns ConfigBox type"""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create list of directories"""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Save json data"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load json files data"""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save binary file"""
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary data"""
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


def decodeImage(imgstring, fileName):
    """Decode base64 image and save to file"""
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    """Encode image to base64"""
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


def download_from_s3(s3_uri: str, local_path: str) -> bool:
    """Download file from S3 bucket"""
    try:
        s3_path = s3_uri.replace('s3://', '')
        bucket, key = s3_path.split('/', 1)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket, key, local_path)
        logger.info(f"Downloaded from s3://{bucket}/{key} to {local_path}")
        return True
    except Exception as e:
        logger.error(f"S3 download failed: {e}")
        raise e


def extract_zip_file(zip_path: str, extract_to: str):
    """Extract zip file to destination directory"""
    try:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            file_count = len(zip_ref.namelist())
            logger.info(f"Extracted {file_count} files to {extract_to}")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise e
