# 🖋️ Alphabet Doodle Recognition

An interactive deep learning web app that recognizes handwritten English alphabets drawn on a canvas. Built using a custom-trained ResNet18 model and deployed with Flask.

---
## 🌐 Hosted Web App

Check out the live app on Hugging Face Spaces:  
👉 [Alphabet Doodle Recognition on Hugging Face](https://huggingface.co/spaces/sushreen/AlphabetDoodleRecognition)

---
## 🚀 Demo

Users draw letters on a canvas. The app predicts the drawn alphabet using a trained CNN model on the EMNIST Letters dataset.

![App Screenshot](alphabet_doodle_recognition/static/demo.gif)

---

## 📦 Project Structure

```
alphabet_doodle_recognition/
│
├── static/
│   ├── favicon.ico         # Browser tab icon
│   └── script.js           # Frontend JavaScript
│
├── templates/
│   └── index.html          # Main HTML page
│
├── resnet_emnist_letters_cpu.pth   # Trained model (CPU-friendly)
├── server.py               # Flask backend and model inference
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🧠 Model Details

- Architecture: Custom ResNet18 with residual blocks
- Trained on: [EMNIST Letters Dataset](https://www.nist.gov/itl/products-and-services/emnist-dataset)
- Classes: 26 (a–z, lowercase)
- Input: 224x224 grayscale images
- Accuracy: **95.13%** on test set (EMNIST Letters)

---

## 💻 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/alphabet-doodle-recognition.git
cd alphabet_doodle_recognition
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv env
source env/bin/activate     # macOS/Linux
env\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python server.py
```

Visit `http://localhost:7860` in your browser 🎨

---

## 📌 Notes

- The canvas is black with white strokes to match the EMNIST training distribution.
- Images are rotated and flipped during preprocessing to match dataset orientation.

---

## ✨ Features

- Draw any letter with your mouse
- Live predictions via Flask API
- High accuracy with lightweight ResNet18

---

