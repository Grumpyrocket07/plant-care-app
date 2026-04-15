import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import pathlib

print("=" * 50)
print("PLANT DISEASE MODEL TRAINING")
print("=" * 50)

# Configuration
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 10  # Change to 20-30 for better accuracy (takes longer)

# Dataset path
data_dir = pathlib.Path("dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)")

# If folder structure is different, try:
# data_dir = pathlib.Path("dataset/train")

print(f"\nDataset location: {data_dir}")

# Check if dataset exists
if not data_dir.exists():
    print("❌ Dataset folder not found!")
    print("\nLooking for dataset...")
    # Try to find it
    for root, dirs, files in os.walk("dataset"):
        if "train" in dirs:
            data_dir = pathlib.Path(root) / "train"
            print(f"✅ Found dataset at: {data_dir}")
            break

# Count images and classes
train_dir = data_dir / "train" if (data_dir / "train").exists() else data_dir
image_count = len(list(train_dir.glob('*/*.jpg'))) + len(list(train_dir.glob('*/*.JPG')))

print(f"\nTotal training images: {image_count}")

# Create training dataset
print("\nLoading training data...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

# Create validation dataset
print("Loading validation data...")
val_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)

print(f"\n✅ Found {num_classes} classes:")
for i, name in enumerate(class_names[:10]):  # Show first 10
    print(f"  {i+1}. {name}")
if num_classes > 10:
    print(f"  ... and {num_classes - 10} more")

# Optimize performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Build model using MobileNetV2 (lightweight, good for phones)
print("\n" + "=" * 50)
print("Building model (MobileNetV2)...")
print("=" * 50)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Freeze base model

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\n✅ Model built successfully!")
model.summary()

# Train
print("\n" + "=" * 50)
print(f"STARTING TRAINING ({EPOCHS} epochs)")
print("This will take 30-60 minutes...")
print("=" * 50)
print("\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    verbose=1
)

# Save model
print("\n" + "=" * 50)
print("Saving model...")
print("=" * 50)

os.makedirs("ml_models", exist_ok=True)
model.save("ml_models/plant_disease_model.h5")

# Save class names
import json
with open("ml_models/class_names.json", "w") as f:
    json.dump(class_names, f, indent=2)

print("\n✅ Model saved to: ml_models/plant_disease_model.h5")
print("✅ Classes saved to: ml_models/class_names.json")

# Show final accuracy
final_accuracy = history.history['accuracy'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]

print("\n" + "=" * 50)
print("TRAINING COMPLETE!")
print("=" * 50)
print(f"Training Accuracy: {final_accuracy*100:.2f}%")
print(f"Validation Accuracy: {final_val_accuracy*100:.2f}%")