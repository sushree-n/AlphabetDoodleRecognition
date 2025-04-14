import torch
import torch.nn as nn
import torchvision.transforms as transforms
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
from flask_cors import CORS
import torch.nn.functional as F
from PIL import ImageOps


class ResBlock(nn.Module):
    def __init__(self, input_features, output_features):
        super(ResBlock, self).__init__()
        self.stride = 1 if input_features == output_features else 2
        
        #main convolutional path
        self.features = nn.Sequential(
            nn.Conv2d(input_features, output_features, kernel_size=3, stride=self.stride, padding=1, bias=False),
            nn.BatchNorm2d(output_features),
            nn.ReLU(inplace=True),
            nn.Conv2d(output_features, output_features, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(output_features)
        )

        #shortcut connection
        self.shortcut = nn.Identity()
        if input_features != output_features:
            self.shortcut = nn.Sequential(
                nn.Conv2d(input_features, output_features, kernel_size=1, stride=self.stride, bias=False),
                nn.BatchNorm2d(output_features)
            )

    def forward(self, x):
        residual = self.shortcut(x)
        x = self.features(x)
        x += residual
        x = F.relu(x, inplace=True)
        return x

class Resnet18(nn.Module):
    def __init__(self, num_of_classes=26):  #classes is 26 for EMNIST letters
        super(Resnet18, self).__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False), 
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),

            ResBlock(64, 64),
            ResBlock(64, 64),

            ResBlock(64, 128),
            ResBlock(128, 128),

            ResBlock(128, 256),
            ResBlock(256, 256),

            ResBlock(256, 512),
            ResBlock(512, 512),

            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.classifier = nn.Sequential(
            nn.Linear(512, num_of_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# Load model
device = "cpu"
model = Resnet18().to(device)
model.load_state_dict(torch.load("resnet_emnist_letters_cpu.pth"))
model.eval()

# Define image preprocessing
transform = transforms.Compose([transforms.Grayscale(), transforms.Resize((224, 224)), transforms.ToTensor()])

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

# Route to handle image predictions
@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"].read()
    image = Image.open(io.BytesIO(file)).convert("L")
    image = image.rotate(-90, expand=True)  # EMNIST orientation
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image = transform(image).unsqueeze(0).to(device)


      
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    class_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    prediction = class_labels[predicted.item()]

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
