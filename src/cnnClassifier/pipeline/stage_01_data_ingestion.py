# src/cnnClassifier/pipeline/stage_01_data_ingestion.py
from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logger.info(f"Starting {STAGE_NAME}")
            
            # Get configuration
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            
            # Run data ingestion
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
            
            logger.info(f"{STAGE_NAME} completed successfully!")
            
        except Exception as e:
            logger.error(f"{STAGE_NAME} failed: {e}")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e