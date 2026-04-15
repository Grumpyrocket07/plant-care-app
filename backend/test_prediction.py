import tensorflow as tf
import numpy as np
from PIL import Image
import json

print("=" * 50)
print("Testing Plant Disease Model")
print("=" * 50)

# Load model
print("\nLoading model...")
model = tf.keras.models.load_model('ml_models/plant_disease_model.h5')

# Load class names
with open('ml_models/class_names.json', 'r') as f:
    class_names = json.load(f)

print(f"✅ Model loaded! ({len(class_names)} classes)")

# Test with a sample image from dataset
import os
import random

# Find a random test image
dataset_path = "dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"
classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
random_class = random.choice(classes)
class_path = os.path.join(dataset_path, random_class)
images = [f for f in os.listdir(class_path) if f.endswith('.JPG') or f.endswith('.jpg')]
random_image = random.choice(images)
image_path = os.path.join(class_path, random_image)

print(f"\nTesting with: {random_class}/{random_image}")

# Load and preprocess image
img = Image.open(image_path).resize((224, 224))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
print("\nPredicting...")
predictions = model.predict(img_array, verbose=0)
predicted_class = class_names[np.argmax(predictions[0])]
confidence = np.max(predictions[0]) * 100

print("\n" + "=" * 50)
print("RESULT")
print("=" * 50)
print(f"Actual:     {random_class}")
print(f"Predicted:  {predicted_class}")
print(f"Confidence: {confidence:.2f}%")
print("\nTop 3 predictions:")
top_3 = np.argsort(predictions[0])[-3:][::-1]
for i, idx in enumerate(top_3, 1):
    print(f"  {i}. {class_names[idx]}: {predictions[0][idx]*100:.2f}%")