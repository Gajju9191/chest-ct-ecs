# app.py
from flask import Flask, request, jsonify, render_template
import os
import sys
from flask_cors import CORS, cross_origin
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path.cwd() / "src"))

from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.prediction import PredictionPipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    # Run DVC pipeline to retrain model
    os.system("dvc repro")
    # Reload model after training
    clApp.classifier.load_model()
    return "Training done successfully! Model reloaded."


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        # Get image from request (supports both JSON and form-data)
        if request.is_json:
            image = request.json['image']
            decodeImage(image, clApp.filename)
        else:
            # Handle file upload
            file = request.files['image']
            file.save(clApp.filename)
        
        # Make prediction
        result = clApp.classifier.predict()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_batch", methods=['POST'])
@cross_origin()
def predictBatchRoute():
    try:
        # Check if multiple files are uploaded
        if 'images' not in request.files:
            return jsonify({"error": "No images provided"}), 400
        
        files = request.files.getlist('images')
        
        if len(files) == 0:
            return jsonify({"error": "No files selected"}), 400
        
        results = []
        
        for file in files:
            if file.filename == '':
                continue
                
            # Save file temporarily
            file.save(clApp.filename)
            
            # Make prediction
            result = clApp.classifier.predict()
            
            # Add filename to result
            result["filename"] = file.filename
            
            results.append(result)
        
        # Clean up
        if os.path.exists(clApp.filename):
            os.remove(clApp.filename)
        
        return jsonify({
            "total": len(results),
            "results": results
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=['GET'])
@cross_origin()
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": clApp.classifier.model is not None
    })


if __name__ == "__main__":
    clApp = ClientApp()
    # Load model on startup
    clApp.classifier.load_model()
    print(f"Model loaded: {clApp.classifier.model is not None}")
    app.run(host='0.0.0.0', port=8080, debug=False)