import kaggle
import os
from kaggle.api.kaggle_api_extended import KaggleApi

print("=" * 50)
print("Downloading Plant Disease Dataset...")
print("=" * 50)

# Initialize API
api = KaggleApi()
api.authenticate()

dataset = 'vipoooool/new-plant-diseases-dataset'

print(f"\nDataset: {dataset}")
print("Size: ~800MB")
print("Classes: 38 diseases")

# Create dataset folder
os.makedirs('dataset', exist_ok=True)

print("\nDownloading (this will take 5-10 minutes)...\n")

try:
    # Download with force option
    api.dataset_download_files(
        dataset,
        path='dataset',
        unzip=True,
        force=True,
        quiet=False
    )
    
    print("\n" + "=" * 50)
    print("✅ Dataset downloaded successfully!")
    print("=" * 50)
    
    # Check what was downloaded
    if os.path.exists('dataset'):
        items = os.listdir('dataset')
        print(f"\nFound {len(items)} items in dataset folder")
        print("First few items:", items[:5])
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying alternative method...")