# Rock Paper Scissors — CNN Image Classifier

## Overview

Real-time hand gesture recognition system powered by a Convolutional Neural Network trained from scratch with TensorFlow/Keras, deployed as an interactive game using Streamlit.

The model detects Rock, Paper, and Scissors gestures through a live webcam feed and plays against the user in real time.

---

## Project Structure

```
├── spr_project_CNN_final.ipynb   # Model training & evaluation
├── streamlit_app_clean.py        # Interactive web application
├── CNN_model1.keras              # Trained model weights
└── README.md
```

---

## Model Architecture

Built from scratch — no pretrained weights or transfer learning.

| Block | Layers |
|-------|--------|
| Block 1 | Conv2D(32) → BatchNorm → MaxPooling |
| Block 2 | Conv2D(64) → BatchNorm → MaxPooling |
| Block 3 | Conv2D(128) → BatchNorm → MaxPooling → Dropout(0.25) |
| Block 4 | Conv2D(256) → BatchNorm → MaxPooling → Dropout(0.25) |
| Head | GlobalAveragePooling → Dense → Softmax (3 classes) |

- **Input:** 128×128 RGB
- **Classes:** Paper, Rock, Scissors
- **Optimizer:** Adam + ReduceLROnPlateau
- **Loss:** Categorical Crossentropy

---

## Training Pipeline

**Data Augmentation**
- Random horizontal flip, rotation (±15°), zoom (±15%), translation
- Random brightness & contrast adjustments

**Callbacks**
- `EarlyStopping` — patience 25, monitors val_loss
- `ModelCheckpoint` — saves best model by val_accuracy
- `ReduceLROnPlateau` — reduces LR on plateau

**Evaluation**
- Confusion Matrix & Classification Report (Precision, Recall, F1)
- t-SNE feature space visualization
- CNN activation maps per layer

---

## Streamlit App

**Game Modes**
- Endless Mode — unlimited rounds
- Best of 3 — first to 2 wins
- Best of 5 — first to 3 wins

**Features**
- Live webcam capture & real-time prediction
- Confidence bars for all 3 classes
- Scoreboard: wins, losses, ties, win rate, best streak
- Last 5 matches history
- AI messages that react to each round result

---

## How to Run

```bash
# Install dependencies
pip install tensorflow streamlit opencv-python pillow numpy

# Launch app
streamlit run streamlit_app_clean.py
```

> Make sure `CNN_model1.keras` is in the same directory.

---

## Tech Stack

Python, TensorFlow, Keras, OpenCV, Streamlit, Scikit-Learn, NumPy

---