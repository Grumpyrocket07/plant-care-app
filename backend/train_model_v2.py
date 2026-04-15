import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import pathlib

print("=" * 50)
print("PLANT DISEASE MODEL TRAINING (v2 - New Format)")
print("=" * 50)

# Configuration
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 15  # Slightly more epochs for better accuracy

# Dataset path
data_dir = pathlib.Path("dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train")

print(f"\nDataset location: {data_dir}")

# Count images
image_count = len(list(data_dir.glob('*/*.jpg'))) + len(list(data_dir.glob('*/*.JPG')))
print(f"Total training images: {image_count}")

# Create datasets
print("\nLoading training data...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

print("Loading validation data...")
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)

print(f"\n✅ Found {num_classes} classes")

# Optimize
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Build model
print("\n" + "=" * 50)
print("Building MobileNetV2 model...")
print("=" * 50)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

# Use functional API for better compatibility
inputs = keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = keras.Model(inputs, outputs)

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\n✅ Model built!")
model.summary()

# Train
print("\n" + "=" * 50)
print(f"STARTING TRAINING ({EPOCHS} epochs)")
print("This will take ~1.5 hours...")
print("=" * 50)
print("\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    verbose=1
)

# Save in NEW Keras format
print("\n" + "=" * 50)
print("Saving model in new Keras format...")
print("=" * 50)

os.makedirs("ml_models", exist_ok=True)

# Save as .keras (new format)
model.save("ml_models/plant_disease_model.keras")

# Also save class names
import json
with open("ml_models/class_names.json", "w") as f:
    json.dump(class_names, f, indent=2)

print("\n✅ Model saved to: ml_models/plant_disease_model.keras")
print("✅ Classes saved to: ml_models/class_names.json")

# Results
final_accuracy = history.history['accuracy'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]

print("\n" + "=" * 50)
print("TRAINING COMPLETE!")
print("=" * 50)
print(f"Training Accuracy: {final_accuracy*100:.2f}%")
print(f"Validation Accuracy: {final_val_accuracy*100:.2f}%")
print("\n🎉 Ready to use!")