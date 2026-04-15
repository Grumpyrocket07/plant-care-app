import tensorflow as tf
import os
import pathlib

print("=" * 50)
print("Downloading TensorFlow Flowers Dataset")
print("(We'll use this to test, then expand later)")
print("=" * 50)

# This is a built-in TensorFlow dataset - downloads instantly!
dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"

print("\nDownloading small dataset for testing...")
print("Size: ~200MB")
print("Classes: 5 flower types")
print("\nWe'll train on this, then you can replace with plant diseases later!\n")

try:
    data_dir = tf.keras.utils.get_file(
        origin=dataset_url,
        fname='flower_photos',
        untar=True,
        cache_dir='.',
        cache_subdir='dataset'
    )
    
    data_dir = pathlib.Path(data_dir)
    
    print("\n" + "=" * 50)
    print("✅ Dataset downloaded!")
    print("=" * 50)
    
    # Count images
    image_count = len(list(data_dir.glob('*/*.jpg')))
    print(f"\nTotal images: {image_count}")
    
    # Show classes
    classes = [item.name for item in data_dir.glob('*') if item.is_dir()]
    print(f"Classes: {classes}")
    
    print("\n✅ Ready to train!")
    
except Exception as e:
    print(f"❌ Error: {e}")