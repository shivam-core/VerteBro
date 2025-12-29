# VerteBro

**VerteBro** is a local computer vision agent that enforces posture by locking the operating system UI when spinal inclination exceeds a defined threshold. It functions as a background daemon, monitoring user biometrics in real-time without transmitting data externally.

## System Architecture

The application operates on a linear inference pipeline:

**Input (Webcam) $\rightarrow$ Inference (MediaPipe) $\rightarrow$ Vector Math $\rightarrow$ State Machine $\rightarrow$ UI Enforcement**

### 1. Pose Estimation Pipeline
The core logic utilizes **Google MediaPipe (BlazePose)** to infer a 33-point skeletal topology from a 2D video frame.
* **Model Complexity:** 1 (Lite) or 2 (Full) for balance between latency and accuracy.
* **Keypoints Used:**
    * **Nose (0)**
    * **Left/Right Shoulder (11, 12)**
    * **Left/Right Ear (7, 8)**

### 2. Vector Geometry & Mathematics
To determine the "slouch state," the system calculates the inclination angle $\theta$ of the neck relative to the vertical axis.

We define three vectors in 2D space:
* $P_{shoulder}$: The geometric center of the shoulder marker.
* $P_{ear}$: The geometric center of the ear marker.
* $P_{vertical}$: A projected reference point $(x_{shoulder}, y_{shoulder} - k)$ on the Y-axis.

The inclination angle $\theta$ is derived using the arctangent of the vector difference:

$$\theta = | \arctan2(y_{ear} - y_{shoulder}, x_{ear} - x_{shoulder}) - \arctan2(y_{vert} - y_{shoulder}, x_{vert} - x_{shoulder}) |$$

### 3. State Management (Hysteresis)
To prevent UI flickering due to sensor noise or micro-movements, a buffer system is implemented:
* **Threshold:** $\theta > 35^\circ$ triggers a potential violation.
* **Buffer Window:** A 15-frame buffer (approx. 500ms at 30FPS) must be saturated before the enforcement state is active.
* **Reset:** Physical correction immediately clears the buffer.

## Tech Stack

* **Runtime:** Python 3.11 (Required for MediaPipe protobuf compatibility).
* **Computer Vision:** OpenCV (`cv2`) for frame capture and overlay rendering.
* **ML Framework:** MediaPipe Solutions.
* **Math:** NumPy for vector calculations.
* **OS Integration:**
    * **macOS:** Custom `.command` launcher prevents "App Nap" from suspending the background process.
    * **Windows:** Compatible via standard Python execution.

## Installation & Usage

### Prerequisites
* **Python 3.11** is strictly required. (Newer versions like 3.13 may cause dependency conflicts with stable MediaPipe builds).
* Webcam availability.

### 1. Clone the Repository
```bash
git clone [https://github.com/shivam-core/VerteBro.git](https://github.com/shivam-core/VerteBro.git)
cd VerteBro

```

### 2. Install Dependencies

Create a virtual environment (recommended) and install requirements:

```bash
pip install -r requirements.txt

```

### 3. Run the Agent

#### On macOS (Apple Silicon M1/M2/M3 & Intel)

To ensure the process runs with high priority and isn't throttled by macOS power saving:

1. Navigate to the folder in Finder.
2. Double-click **`vertebro.command`**.
3. Grant Camera and Accessibility permissions if prompted.

*Alternatively, via terminal:*

```bash
./vertebro.command

```

#### On Windows

Windows does not require the `.command` wrapper. Run the script directly:

```bash
python vertebro.py

```

## Configuration

You can modify `vertebro.py` to adjust sensitivity:

* `SLOUCH_THRESHOLD`: Adjust the angle (Default: 35 degrees).
* `BUFFER_SIZE`: Adjust how quickly the screen locks (Default: 15 frames).

## License

MIT License. See `LICENSE` for details.
