import torch
from torchvision import models
import time
import json
import urllib

# Multiple Decorators: Using a decorator to log the time taken to load the model
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Model loaded in {end_time - start_time:.2f} seconds.")  # Logs time
        return result
    return wrapper

# Model loading using decorator (Multiple Decorators)
@log_time
def load_model():
    # Encapsulation: The model loading logic is encapsulated within this function.
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    model.eval()  # Set the model to evaluation mode
    return model

# Load ImageNet class labels (Encapsulation)
def load_labels():
    # Encapsulation: The label loading logic is encapsulated in this function.
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    with urllib.request.urlopen(url) as f:
        labels = json.loads(f.read().decode())
    return {str(i): label for i, label in enumerate(labels)}

# Running the model and label loading
if __name__ == "__main__":
    model = load_model()  # Load the model using the decorator
    labels = load_labels()  # Load ImageNet labels