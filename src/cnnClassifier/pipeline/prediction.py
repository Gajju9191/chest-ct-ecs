# src/cnnClassifier/pipeline/prediction.py
import numpy as np
from keras.models import load_model  # type: ignore
from keras.preprocessing import image  # type: ignore
import os
from pathlib import Path
from cnnClassifier import logger

class PredictionPipeline:
    def __init__(self, filename=None):
        self.filename = filename
        self.model = None
        self.class_labels = {0: "Adenocarcinoma Cancer", 1: "Normal"}
    
    def load_model(self):
        """Load the trained model"""
        try:
            possible_paths = [
                "model.h5",
                os.path.join("artifacts", "training", "model.h5"),
                os.path.join("model", "model.h5"),
                "artifacts/training/model.h5",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.model = load_model(path)
                    logger.info(f"Model loaded from: {path}")
                    return self.model
            
            raise FileNotFoundError("Model not found in any expected location")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        test_image = image.load_img(image_path, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        test_image = test_image / 255.0
        return test_image
    
    def predict(self):
        """Make prediction on the image"""
        if self.model is None:
            self.load_model()
        
        if self.model is None:  # Add this check for type checker
            raise ValueError("Model failed to load")
        
        if self.filename is None:
            raise ValueError("No filename provided")
        
        try:
            processed_image = self.preprocess_image(self.filename)
            predictions = self.model.predict(processed_image)
            result_idx = int(np.argmax(predictions[0]))  # Convert to int
            confidence = float(predictions[0][result_idx])
            
            logger.info(f"Prediction: {self.class_labels[result_idx]} with confidence: {confidence:.4f}")
            
            return {
                "prediction": self.class_labels[result_idx],
                "confidence": confidence,
                "class_index": result_idx
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise e
    
    def predict_batch(self, image_paths):
        """Make predictions on multiple images"""
        results = []
        for path in image_paths:
            self.filename = path
            result = self.predict()
            results.append(result)
        return results

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path.cwd() / "src"))
    print("✅ PredictionPipeline class defined successfully")