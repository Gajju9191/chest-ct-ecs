
# main.py
# main.py
from cnnClassifier import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnnClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline


if __name__ == "__main__":
    # Stage 1: Data Ingestion
    try:
        logger.info(">>>>>> stage Data Ingestion Stage started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(">>>>>> stage Data Ingestion Stage completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e
    

    
    # Stage 2: Prepare Base Model
    try:
        logger.info(">>>>>> stage Prepare Base Model Stage started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(">>>>>> stage Prepare Base Model Stage completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e