# src/cnnClassifier/components/data_ingestion.py
import os
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size, download_from_s3
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config):
        self.config = config
    
    def download_file(self):
        try:
            dataset_url = self.config['source_URL']
            zip_download_dir = self.config['local_data_file']
            
            os.makedirs(os.path.dirname(zip_download_dir), exist_ok=True)
            
            logger.info(f"Downloading data from {dataset_url}")
            logger.info(f"Saving to: {zip_download_dir}")
            
            download_from_s3(dataset_url, zip_download_dir)
            
            file_size = get_size(zip_download_dir)
            logger.info(f"Downloaded successfully! File size: {file_size}")
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise e
    
    def extract_zip_file(self):
        try:
            unzip_path = self.config['unzip_dir']
            os.makedirs(unzip_path, exist_ok=True)
            
            with zipfile.ZipFile(self.config['local_data_file'], 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
                file_count = len(zip_ref.namelist())
            
            logger.info(f"Extracted {file_count} files to {unzip_path}")
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise e