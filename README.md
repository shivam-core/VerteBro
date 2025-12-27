# VerteBro

# VerteBro: The AI-Powered Posture Enforcer

**VerteBro** is a real-time computer vision application that actively corrects poor posture. Unlike passive notification apps, VerteBro uses an "Enforcement Mechanism" (The Fog) that renders your screen unusable until you correct your spinal alignment.

It runs locally on macOS (optimized for M1/M2/M3 Silicon) using Python 3.11, ensuring privacy and low latency.

## How It Works (The Logic)

The core engine relies on **Vector Geometry** and **Pose Estimation**.

1.  **Pose Detection:** Uses Google's **MediaPipe** framework to infer 33 3D landmarks of the human body from a 2D webcam feed.
2.  **Vector Calculation:** We isolate three critical coordinates:
    * $P_{ear}$: The coordinates of the user's ear.
    * $P_{shoulder}$: The coordinates of the user's shoulder.
    * $P_{vertical}$: A projected point on the Y-axis above the shoulder.
3.  **Angle Computation:**
    The neck inclination angle $\theta$ is calculated using the arctangent of the vector difference:
    $$\theta = | \arctan2(y_c - y_b, x_c - x_b) - \arctan2(y_a - y_b, x_a - x_b) |$$
    *Where $(a, b, c)$ correspond to the vertical point, shoulder, and ear, respectively.*
4.  **State Management:**
    * **Threshold:** If $\theta > 35^\circ$ (Slouch Threshold).
    * **Tolerance:** A 15-frame buffer (approx. 0.5s) prevents false positives from jitter.
    * **Enforcement:** If tolerance is exceeded, an OpenCV fullscreen overlay ("The Fog") is triggered, blocking the UI.

## Technical Architecture

* **Language:** Python 3.11 (Strict requirement due to MediaPipe/Protobuf compatibility on macOS ARM64).
* **Vision Engine:** OpenCV (`cv2`) for frame processing and overlay rendering.
* **Pose Estimation:** MediaPipe Solutions (BlazePose model).
* **Math:** NumPy for high-performance vector operations.
* **OS Integration:** Custom `.command` launcher shell script for macOS execution and permission handling.

## Installation & Setup

### Prerequisites
* macOS (Optimized for Apple Silicon M1/M2/M3).
* **Python 3.11** (Python 3.13 is currently incompatible with stable MediaPipe builds).

### Step 1: Clone & Environment
```bash
git clone [https://github.com/YOUR_USERNAME/VerteBro.git](https://github.com/YOUR_USERNAME/VerteBro.git)
cd VerteBro
