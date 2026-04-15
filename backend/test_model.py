import tensorflow as tf
import json

print("Loading model...")
model = tf.keras.models.load_model('ml_models/plant_disease_model.h5')

print("\n" + "="*50)
print("MODEL INFO")
print("="*50)

print(f"\nInput shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")
print(f"\nNumber of classes: {model.output_shape[-1]}")

model.summary()