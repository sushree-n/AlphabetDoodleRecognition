# Alphabet Doodle App

This folder contains the core files for the alphabet doodle recognition web app.

## Contents

- `server.py` — Flask backend with ResNet18 model
- `templates/index.html` — Web UI for drawing letters
- `static/` — Favicon and optional scripts/styles
- `resnet_emnist_letters_cpu.pth` — Trained model weights (EMNIST Letters)

## Run Locally

```bash
python server.py
```

App will be available at [http://localhost:7860](http://localhost:7860)