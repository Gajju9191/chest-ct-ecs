# src/cnnClassifier/components/evaluation.py
import os
import json
import mlflow
import mlflow.keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import confusion_matrix
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import save_json

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        logger.info("Evaluation component initialized")

    def _valid_generator(self):
        logger.info("Creating validation data generator...")
        
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )
        
        logger.info(f"Validation samples: {self.valid_generator.samples}")
        logger.info(f"Classes: {self.valid_generator.class_indices}")

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        logger.info(f"Loading model from: {path}")
        return tf.keras.models.load_model(path)

    def evaluation(self):
        logger.info("Starting evaluation...")
        
        # Load model
        self.model = self.load_model(self.config.model_path)
        
        # Create generator
        self._valid_generator()
        
        # Evaluate - model.evaluate() returns [loss, accuracy]
        results = self.model.evaluate(self.valid_generator)
        
        # Handle results (could be list or single value)
        if isinstance(results, list):
            self.loss = float(results[0])
            self.accuracy = float(results[1])
        else:
            self.loss = float(results)
            self.accuracy = float(results)
        
        logger.info(f"Loss: {self.loss:.4f}")
        logger.info(f"Accuracy: {self.accuracy:.4f}")
        
        # Save scores
        self.save_score()
        
        # Log to MLflow
        self.log_into_mlflow()

    def save_score(self):
        scores = {
            "loss": self.loss,
            "accuracy": self.accuracy
        }
        save_json(path=self.config.metrics_file, data=scores)
        logger.info(f"Scores saved to: {self.config.metrics_file}")

    def log_into_mlflow(self):
        logger.info("Logging to MLflow...")
        
        # Set credentials for DagsHub (ADD THESE TWO LINES)
        os.environ["MLFLOW_TRACKING_USERNAME"] = "Gajju9191"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "089e1f4ec33ad67cc8541160fe89a199ce77186d"
        
        mlflow.set_tracking_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run(run_name="Model Evaluation"):
            # Log parameters
            mlflow.log_params({
                "batch_size": self.config.params_batch_size,
                "image_size": self.config.params_image_size,
                "classes": self.config.params_classes,
                "validation_split": 0.30
            })
            
            # Log metrics
            mlflow.log_metrics({
                "loss": self.loss,
                "accuracy": self.accuracy
            })

            # Log model
            if tracking_url_type_store != "file":
                mlflow.keras.log_model(
                    self.model, 
                    "model", 
                    registered_model_name="VGG16Model"
                )
                logger.info("Model registered to MLflow Model Registry")
            else:
                mlflow.keras.log_model(self.model, "model")
                logger.info("Model logged to MLflow")
        
        logger.info("MLflow logging completed!")

    def plot_confusion_matrix(self):
        """Generate and save confusion matrix plot"""
        logger.info("Generating confusion matrix...")
        
        # Get predictions
        predictions = self.model.predict(self.valid_generator)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = self.valid_generator.classes
        class_labels = list(self.valid_generator.class_indices.keys())
        
        # Calculate confusion matrix
        cm = confusion_matrix(true_classes, predicted_classes)
        
        # Plot
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_labels,
                    yticklabels=class_labels)
        plt.title('Confusion Matrix - Chest CT Classification')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        # Save
        plt.savefig(self.config.confusion_matrix_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Confusion matrix saved to: {self.config.confusion_matrix_path}")