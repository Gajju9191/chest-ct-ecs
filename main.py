# main.py
from cnnClassifier import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnnClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from cnnClassifier.pipeline.stage_03_model_trainer import ModelTrainingPipeline
from cnnClassifier.pipeline.stage_04_model_evaluation import EvaluationPipeline

STAGE_1 = "Data Ingestion Stage"
STAGE_2 = "Prepare Base Model Stage"
STAGE_3 = "Training Stage"
STAGE_4 = "Evaluation Stage"

if __name__ == "__main__":
    
    # Stage 1: Data Ingestion
    try:
        logger.info(f">>>>>> stage {STAGE_1} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_1} completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e
    
    # Stage 2: Prepare Base Model
    try:
        logger.info(f">>>>>> stage {STAGE_2} started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_2} completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e
    
    # Stage 3: Training
    try:
        logger.info(f">>>>>> stage {STAGE_3} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_3} completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e
    
    # Stage 4: Evaluation
    try:
        logger.info(f">>>>>> stage {STAGE_4} started <<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_4} completed <<<<<<\n\n==========x==========")
    except Exception as e:
        logger.exception(e)
        raise e
    
    logger.info("="*50)
    logger.info("ALL STAGES COMPLETED SUCCESSFULLY!")
    logger.info("="*50)