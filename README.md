# VibeFlux
![Static Badge](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?color=blue)
![PyPI - Version](https://img.shields.io/pypi/v/VibeFlux?color=blue)
![PyPI - License](https://img.shields.io/pypi/l/VibeFlux?color=blue)
![PyPI - Status](https://img.shields.io/pypi/status/VibeFlux?color=blue)
![PyPI - Downloads](https://img.shields.io/pypi/dm/VibeFlux?color=blue)

**VibeFlux** is a pre-alpha Python toolkit for building **computer-vision desktop applications** with **PySide6 (Qt)**, **OpenCV**, and **Pillow**.

It bundles:
- **Media pipelines** (camera/video/image folder processing) built around Qt signals/timers
- **Reusable UI widgets** (zoomable image viewer, dialogs, toast tips)
- **Style + config loaders** (QSS + YAML)
- **Visualization utilities** for detection/classification results (boxes, masks, keypoints, skeletons, multilingual labels)
- **SQLite managers** for detection logging and user management

> Project status: **Pre-Alpha**. APIs and module layout may change quickly.

---

## Table of Contents
- [Why VibeFlux](#why-vibeflux)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Concepts](#concepts)
- [Usage Examples](#usage-examples)
  - [Example 1: Live camera feed to a Qt window](#example-1-live-camera-feed-to-a-qt-window)
  - [Example 2: Add a frame processor pipeline](#example-2-add-a-frame-processor-pipeline)
  - [Example 3: Process a single image or a folder of images](#example-3-process-a-single-image-or-a-folder-of-images)
  - [Example 4: Draw detection overlays (boxes/masks/keypoints)](#example-4-draw-detection-overlays-boxesmaskskeypoints)
  - [Example 5: Zoom & pan image viewer widget](#example-5-zoom--pan-image-viewer-widget)
  - [Example 6: Toast / tip notifications with animation](#example-6-toast--tip-notifications-with-animation)
  - [Example 7: Load QSS themes and YAML widget settings](#example-7-load-qss-themes-and-yaml-widget-settings)
  - [Example 8: Built-in Settings/Config editor dialogs](#example-8-built-in-settingsconfig-editor-dialogs)
  - [Example 9: Save detections to SQLite in the background](#example-9-save-detections-to-sqlite-in-the-background)
  - [Example 10: User registration & login](#example-10-user-registration--login)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [License](#license)
- [Credits](#credits)

---

## Why VibeFlux

When you build CV GUI apps in Python, you often end up rewriting the same glue code:
- OpenCV camera capture → Qt rendering
- Frame processing pipelines
- Overlay drawing for detections & keypoints
- QSS themes + per-widget configuration
- Toast tips, confirmation dialogs, and UI “polish”
- Simple persistence (save results, manage users)

VibeFlux is designed to be a **practical toolbox** of these building blocks so you can focus on your app logic.

---

## Features

### 1) Media handling (camera/video/images)
- **`MediaHandler`**: wraps `cv2.VideoCapture` + Qt timer (`QTimer`) and emits frames through Qt signals.
- **`ImageHandler`**: reads a single image or iterates over a folder, applies a processing pipeline, and emits frames.

Both support a simple *processor chain*:
```python
handler.addFrameProcessor(func)   # func(frame) -> frame
handler.removeFrameProcessor(func)
```

### 2) Visualization for detection/classification
- Rect boxes and **oriented boxes** (8-point polygon)
- Mask overlay (generated from boxes or provided mask maps)
- Keypoints + skeleton drawing
- Text rendering:
  - Fast OpenCV text for Latin labels
  - Automatic switch to **PIL text** when Chinese characters are detected

### 3) UI components (PySide6)
- **Zoom/pan image label** (mouse wheel zoom, click-drag pan)
- Custom message box / confirmation dialog
- Toast tip widgets with smooth fade animation
- Frameless window helpers + window control buttons

### 4) Styling & configuration
- Load QSS files into a window
- Apply widget settings from YAML:
  - enabled/show/hide
  - text
  - icon path
  - background image path
  - window icon

Also includes **GUI editors** for YAML configs:
- `SettingsDialog` (UI-focused)
- `ConfigDialog` (general YAML config editor)

### 5) Persistence (SQLite)
- `DetectionDB`: background-thread batch insertion (keeps UI responsive)
- `UserManager`: register/login, password hashing, avatar file validation

---

## Installation

### Install from PyPI
```bash
pip install VibeFlux
```

### Install from source
```bash
git clone https://github.com/HarrisonVance26/VibeFlux.git
cd VibeFlux
pip install -e .
```

---

## Requirements

- Python **3.7+** (3.7 or above is recommended)
- Core dependencies:
  - `numpy`
  - `opencv-python>=4.5.5.64`
  - `Pillow>=9.0.1`
  - `PySide6>=6.4.2`
  - `PyYAML>=6.0`
  - `ruamel.yaml>=0.18.6`
  - `captcha>=0.4`
  - `aggdraw>=1.3.19`

Optional:
- **PyTorch** (only if you use hook-based heatmaps)

---

## Concepts

### Signal-driven pipelines
VibeFlux components are designed around Qt signals. For example:
- `MediaHandler.frameReady` emits an OpenCV frame.
- Your UI connects a slot to update a `QLabel`/widget.

### BGR vs RGB
OpenCV frames are typically **BGR**. Qt expects **RGB** when constructing `QImage`.
Many helper functions in VibeFlux convert for you, but be mindful when writing custom code.

### Assets (fonts/icons)
Some modules load fonts (e.g. `GB2312.ttf`) and use Qt resource paths like `:/default_icons/...`.  
When packaging your app, make sure these assets are included and/or your Qt resources are correctly built.

---

## Usage Examples

> The examples below explain **what the code does** before showing the snippet.

### Example 1: Live camera feed to a Qt window

**What you get**
- Opens camera index `0`
- Grabs frames at ~30 FPS using a Qt timer
- Emits frames via Qt signal, displays them in a `QLabel`
- Stops camera cleanly when the window closes

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from VibeFlux.handlers import MediaHandler
from VibeFlux.base.Trans import ToQtPixmap

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VibeFlux - Camera Demo")

        self.view = QLabel("Opening camera...")
        self.view.setMinimumSize(960, 540)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        # Create handler (device=0, fps=30)
        self.media = MediaHandler(device=0, fps=30)

        # Connect signals
        self.media.frameReady.connect(self.on_frame)
        self.media.mediaFailed.connect(self.on_error)

        # Start capture
        self.media.startMedia()

    def on_error(self, msg: str):
        self.view.setText(msg)

    def on_frame(self, frame_bgr):
        # Convert BGR->RGB for Qt
        frame_rgb = frame_bgr[..., ::-1]
        pix = ToQtPixmap(frame_rgb)

        self.view.setPixmap(pix)
        self.view.setScaledContents(True)

    def closeEvent(self, event):
        if self.media.isActive():
            self.media.stopMedia()
        super().closeEvent(event)

app = QApplication(sys.argv)
w = CameraWindow()
w.show()
sys.exit(app.exec())
```

---

### Example 2: Add a frame processor pipeline

**What you get**
- Adds a processing function that runs on every frame
- Useful for filters, overlays, analytics, or model inference

```python
import time
import cv2

last_t = time.time()

def draw_fps(frame_bgr):
    global last_t
    now = time.time()
    fps = 1.0 / max(now - last_t, 1e-6)
    last_t = now
    cv2.putText(frame_bgr, f"FPS: {fps:.1f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
    return frame_bgr

media.addFrameProcessor(draw_fps)
```

> Tip: keep processors fast; heavy work should be moved to a worker thread / executor.

---

### Example 3: Process a single image or a folder of images

**What you get**
- Load a single image file or iterate through a directory of images
- Apply your processing pipeline (`addFrameProcessor`)
- Emit frames through `frameReady` so UI stays consistent with camera mode

```python
from PySide6.QtWidgets import QApplication, QLabel
from VibeFlux.handlers import ImageHandler
from VibeFlux.base.Trans import ToQtPixmap
import sys

app = QApplication(sys.argv)
label = QLabel("Waiting...")
label.resize(800, 600)
label.show()

handler = ImageHandler()

def on_frame(frame_bgr):
    frame_rgb = frame_bgr[..., ::-1]
    label.setPixmap(ToQtPixmap(frame_rgb))
    label.setScaledContents(True)

handler.frameReady.connect(on_frame)

# Choose either:
handler.setPath("demo.jpg")          # a single file
# handler.setPath("samples/")        # a folder of images

handler.startProcess()
sys.exit(app.exec())
```

---

### Example 4: Draw detection overlays (boxes/masks/keypoints)

**What you get**
- Convert model outputs (boxes/scores/class_ids) into a visual overlay on the frame
- Supports:
  - **Rect boxes** (x1,y1,x2,y2)
  - **Oriented boxes** (8 coordinates)
  - Masks
  - Keypoints + skeleton
  - Chinese labels (auto PIL rendering)

```python
import numpy as np
from VibeFlux.utils import DetectorVisual  # wrapper around IMDetectorVisual

vis = DetectorVisual()

# Example image (OpenCV BGR)
img = np.zeros((480, 640, 3), dtype=np.uint8)

# Example detections
boxes = np.array([
    [50, 60, 300, 400],                       # rect box
    [350, 100, 550, 120, 530, 260, 330, 240], # oriented box (8 coords)
])
scores = np.array([0.92, 0.88])
class_ids = np.array([0, 1])

# Optional custom labels (can include Chinese)
labels = ["person 92%", "目标 88%"]

out = vis(img, boxes=boxes, scores=scores, class_ids=class_ids, labels=labels)
```

> If your model produces keypoints, pass them as `keypoints=...` (shape typically `[N, K, 3]` for x,y,conf).

---

### Example 5: Zoom & pan image viewer widget

**What you get**
- A `QLabel`-like widget that supports:
  - mouse wheel zoom
  - click-drag pan
  - overlay text (optional)

```python
import sys
import cv2
from PySide6.QtWidgets import QApplication
from VibeFlux.frames import QImageLabel

app = QApplication(sys.argv)
viewer = QImageLabel()
viewer.resize(1000, 700)
viewer.show()

img = cv2.imread("demo.jpg")  # OpenCV BGR
viewer.dispImage(img, keepAspect=True)
viewer.dispText("Scroll to zoom, drag to move")

sys.exit(app.exec())
```

---

### Example 6: Toast / tip notifications with animation

**What you get**
- A lightweight toast notification (like “snackbar”)
- Built-in styles: `info`, `warning`, `error`, `success`
- Auto fade-in/fade-out with configurable duration and placement

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from VibeFlux.frames.TipsWidgets import MultiTipWidget

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VibeFlux - Tip Widget")

        self.tip = MultiTipWidget(self, font_family="Microsoft YaHei", font_size=18)

        btn = QPushButton("Show tip")
        btn.clicked.connect(self.show_tip)

        layout = QVBoxLayout(self)
        layout.addWidget(btn)

    def show_tip(self):
        self.tip.showTip(
            "Saved successfully!",
            duration=2000,
            position="top",
            message_type="success"
        )

app = QApplication(sys.argv)
w = Demo()
w.resize(420, 240)
w.show()
sys.exit(app.exec())
```

---

### Example 7: Load QSS themes and YAML widget settings

**What you get**
- Load a QSS theme file into your window
- Apply YAML-defined widget properties (text/icon/background/enabled)

```python
from VibeFlux.styles import loadQssStyles, loadYamlSettings

# Apply QSS theme
loadQssStyles(window=my_window, qss_file="qss/Dracula.qss", base_path=".")

# Apply per-widget YAML settings
loadYamlSettings(my_window, yaml_file="ui_settings.yaml", base_path=".")
```

**Example `ui_settings.yaml`**
```yaml
btnStart:
  enabled: True
  type: QPushButton
  text: "Start"
  icon: "assets/icons/start.png"

btnStop:
  enabled: True
  type: QPushButton
  text: "Stop"
  icon: "assets/icons/stop.png"

mainWindow:
  windowIcon: "assets/icons/app.png"

lblBackground:
  enabled: True
  type: QLabel
  background: "assets/bg/main.png"
```

> Notes:
> - `type` is used to find widgets via `findChild(type, widget_name)`.
> - Use `base_path` to make relative paths stable across different launch locations.

---

### Example 8: Built-in Settings/Config editor dialogs

**What you get**
- A ready-to-use GUI dialog to edit YAML settings/config
- Useful for building apps that allow end-users to tune UI/config without editing files manually

```python
from VibeFlux.frames.SettingsDialog import SettingsDialog, ConfigDialog
from PySide6.QtWidgets import QDialog

# UI settings editor (supports enabled/text/icon/background/windowIcon)
dlg = SettingsDialog("ui_settings.yaml", parent=my_window)
dlg.exec()

# General config editor (supports str/int/float/list)
dlg2 = ConfigDialog("app_config.yaml", parent=my_window)
if dlg2.exec() == QDialog.Accepted:
    print("Config updated. Restart app to apply changes (recommended).")
```

---

### Example 9: Save detections to SQLite in the background

**What you get**
- Log detections without blocking the UI thread
- Writes are queued and inserted in batches in a background worker thread

```python
from VibeFlux.managers import DetectionDB

db = DetectionDB("detection_results.db")

# Insert one detection
db.insert(
    class_name="person",
    class_id=0,
    confidence=0.93,
    bbox=(50, 60, 300, 400),
    image_path="frame_0001.png"
)

# Insert many detections (dict format)
db.insert_bulk([
    {"class_name": "car", "class_id": 2, "confidence": 0.88,
     "bbox": (100, 120, 320, 300), "image_path": "frame_0002.png"},
])

# IMPORTANT: close to flush queue on exit
db.close()
```

---

### Example 10: User registration & login

**What you get**
- Basic user table with:
  - username (primary key)
  - password hash (SHA-256)
  - avatar path
- Built-in validation:
  - minimum password length
  - avatar file exists and is a valid image

```python
from VibeFlux.managers import UserManager

users = UserManager("users.db")

# Register
status = users.register("alice", "secret123", "alice.png")
print("register status:", status)  # 0 ok, negative means error

# Login
print("login:", users.verify_login("alice", "secret123"))  # 0 ok

# Change password
print("change_password:", users.change_password("alice", "newpass123"))

# Change avatar (requires correct password)
print("change_avatar:", users.change_avatar("alice", "newpass123", "new_avatar.png"))

users.close()
```

---

## Troubleshooting

### 1) “Qt platform plugin” or GUI won’t start
PySide6 apps may require system Qt dependencies (varies by OS/distribution).  
Try verifying your PySide6 installation and running a minimal Qt example first.

### 2) Camera cannot be opened
- On Windows, VibeFlux uses `cv2.CAP_DSHOW` by default for stability.
- Try different device indices (`0`, `1`, `2`) or confirm the camera is not used by another app.

You can also scan available cameras:
```python
from VibeFlux.utils.CameraUtils import find_cameras
print(find_cameras(max_devices=5))
```

### 3) Missing fonts / Chinese text not rendered
Some modules load specific fonts (e.g. `GB2312.ttf`, `simkai.ttf`).  
Make sure the font files are present in your environment or package resources.

### 4) Nothing shows in QLabel
Remember:
- OpenCV is BGR; Qt expects RGB for correct color rendering.
- Use the provided converters (e.g. `ToQtPixmap`) or convert with `frame[..., ::-1]`.

---

## Roadmap

Ideas for future improvements (typical next steps for a pre-alpha toolkit):
- Clear, stable public API surface (`VibeFlux.ui`, `VibeFlux.cv`, `VibeFlux.db`, etc.)
- More examples: detection dashboard, video file player, model inference threading
- Better asset packaging and resource handling
- Optional extras (`pip install VibeFlux[torch]`, etc.)
- Automated tests & CI

---

## License

VibeFlux is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

If you distribute an application that includes VibeFlux, or deploy it as a network service, ensure you comply with AGPL obligations (including source availability requirements).

---

## Credits

Author: **Harrison Vance**  
Repository: https://github.com/HarrisonVance26/VibeFlux
