import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
import os

class PlantDiseasePredictor:
    def __init__(self):
        self.model = None
        self.class_names = []
        self.load_model()
    
    def load_model(self):
        """Load the trained model and class names"""
        try:
            print("Loading plant disease model...")
            model_path = "ml_models/plant_disease_model.keras"  # Changed to .keras
            class_names_path = "ml_models/class_names.json"
            
            if not os.path.exists(model_path):
                print("❌ Model file not found!")
                return
            
            self.model = tf.keras.models.load_model(model_path)
            
            with open(class_names_path, 'r') as f:
                self.class_names = json.load(f)
            
            print(f"✅ Model loaded! ({len(self.class_names)} classes)")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Model will not be available for predictions.")
    
    def preprocess_image(self, image_bytes):
        """Preprocess image for prediction"""
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((224, 224))
        image = image.convert('RGB')
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    
    def predict(self, image_bytes):
        """Predict disease from image"""
        if self.model is None:
            return {
                "error": "Model not loaded",
                "disease": "Unknown",
                "confidence": 0.0
            }
        
        try:
            # Preprocess
            processed_image = self.preprocess_image(image_bytes)
            
            # Predict
            predictions = self.model.predict(processed_image, verbose=0)
            predicted_idx = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            
            disease_name = self.class_names[predicted_idx]
            
            # Get top 3 predictions
            top_3_idx = np.argsort(predictions[0])[-3:][::-1]
            top_3 = [
                {
                    "disease": self.class_names[idx],
                    "confidence": round(float(predictions[0][idx]) * 100, 2)
                }
                for idx in top_3_idx
            ]
            
            return {
                "disease": disease_name,
                "confidence": round(confidence * 100, 2),
                "top_3": top_3
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "disease": "Error",
                "confidence": 0.0
            }

# Global predictor instance
predictor = PlantDiseasePredictor()