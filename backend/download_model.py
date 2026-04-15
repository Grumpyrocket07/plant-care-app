import requests
import os

os.makedirs("ml_models", exist_ok=True)

print("=" * 50)
print("Downloading PlantVillage model...")
print("=" * 50)

# Try different source - TensorFlow Hub converted model
url = "https://github.com/MarkoArsenovic/DeepLearning_PlantDiseases/raw/master/Models/model.h5"
output_path = "ml_models/plant_disease_model.h5"

try:
    print(f"\nDownloading to: {output_path}")
    print("Please wait...\n")
    
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='')
    
    print("\n\n" + "=" * 50)
    print("✅ Model downloaded successfully!")
    print("=" * 50)
    
    # Verify file size
    file_size = os.path.getsize(output_path)
    print(f"File size: {file_size / (1024*1024):.2f} MB")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nLet's train a simple model instead - it'll take 10 minutes")