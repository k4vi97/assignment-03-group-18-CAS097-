import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from torchvision import transforms
 
# Import the model and labels from part1.py
from part1 import load_model, load_labels
 
# Base class: Encapsulation of common Tkinter functionality
class BaseApp(tk.Tk):
    def __init__(self, model, labels):
        super().__init__()
        self.model = model  # Encapsulation: Model is stored inside the class
        self.labels = labels  # Encapsulation: Labels are stored inside the class
        self.setup_ui()  # Setup the user interface
 
    def setup_ui(self):
        self.title("Image Classification App")
        self.geometry("400x400")
        self.label = tk.Label(self, text="Upload an image")
        self.label.pack(pady=10)
 
        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)
 
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)
 
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)
 
    # Method Overriding: The upload_image method is customized to handle image upload and classification
    def upload_image(self):
        # Method to open an image file and display it
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((200, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img
            self.classify_image(file_path)  # Classify the uploaded image
 
    # Encapsulation: Image classification logic is encapsulated within this method
    def classify_image(self, image_path):
        image = Image.open(image_path)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)
 
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            self.model.to('cuda')
 
        with torch.no_grad():
            output = self.model(input_batch)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        category = torch.argmax(probabilities).item()
        self.display_result(category)
 
    # Polymorphism and Method Overriding: Overriding this method to customize result display
    def display_result(self, category):
        result = self.labels.get(str(category), "Unknown")  # Map category index to label
        self.result_label.config(text=f"Predicted: {result}")  # Display result
 
# Running the part 2 application
if __name__ == "__main__":
    model = load_model()  # Load the model from part1
    labels = load_labels()  # Load the labels from part1
    app = BaseApp(model, labels)  # Instantiate the application
    app.mainloop()  # Start the Tkinter event loop