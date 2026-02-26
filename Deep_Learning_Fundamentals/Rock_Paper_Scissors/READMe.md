<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:C96B9E,50:E8907C,100:F0B060&height=180&section=header&text=Rock%20Paper%20Scissors%20AI&fontSize=45&fontColor=fff&animation=twinkling&fontAlignY=38&desc=CNN%20Image%20Classifier%20%2B%20Interactive%20Game&descAlignY=58&descSize=18&descColor=ffffff"/>

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

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:C96B9E,50:E8907C,100:F0B060&height=100&section=footer&animation=twinkling"/>