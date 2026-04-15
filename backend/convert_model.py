import tensorflow as tf

print("Loading old model...")
try:
    # Try loading with different methods
    model = tf.keras.models.load_model('ml_models/plant_disease_model.h5', compile=False)
    
    print("Resaving in new Keras format...")
    model.save('ml_models/plant_disease_model.keras')
    
    print("✅ Model converted successfully!")
    print("File saved as: ml_models/plant_disease_model.keras")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nWe need to retrain the model with updated save format.")
    print("This will take 1.5 hours. Should I give you the code?")