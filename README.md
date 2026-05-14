# VibeFlux

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/VibeFlux/)
[![PyPI](https://img.shields.io/pypi/v/VibeFlux?color=blue)](https://pypi.org/project/VibeFlux/)
[![License](https://img.shields.io/pypi/l/VibeFlux?color=blue)](LICENSE)
[![Status](https://img.shields.io/pypi/status/VibeFlux?color=blue)](https://pypi.org/project/VibeFlux/)

**Language / 语言： [中文](#中文文档) | [English](#english-documentation)**

---

<a id="中文文档"></a>

# VibeFlux 中文文档

[English](#english-documentation) | [完整中文 API 参考](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.zh-CN.md) | [English API Reference](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.en.md)

**VibeFlux** 是一个面向计算机视觉桌面应用的 Python 工具包，围绕 **PySide6 / Qt**、**OpenCV**、**Pillow**、可复用 UI 控件、检测可视化、SQLite 管理器，以及 OpenAI-compatible LLM 调用能力组织。它适合用来快速搭建 YOLO / 深度学习视觉应用、检测结果展示工具、训练结果分析工具、带登录和配置面板的桌面软件，以及结合大模型进行图像理解或文本总结的视觉工作流。

> 当前状态：Pre-Alpha。接口已经可用，但仍可能在后续版本中调整。生产项目建议固定版本，例如 `VibeFlux==0.8.0`。

## 中文目录

- [0.8.0 更新重点](#080-更新重点)
- [安装](#安装)
- [依赖](#依赖)
- [功能总览](#功能总览)
- [包结构](#包结构)
- [快速开始](#快速开始)
- [媒体处理接口](#媒体处理接口)
- [图像与检测可视化](#图像与检测可视化)
- [PySide6 控件与窗口](#pyside6-控件与窗口)
- [QSS 与 YAML 配置](#qss-与-yaml-配置)
- [SQLite 数据管理](#sqlite-数据管理)
- [LLM 大模型调用](#llm-大模型调用)
- [模型抽象与热力图](#模型抽象与热力图)
- [路径、文件、摄像头与系统工具](#路径文件摄像头与系统工具)
- [公共 API 摘要](#公共-api-摘要)
- [常见问题](#常见问题)
- [许可证](#许可证)

## 0.8.0 更新重点

`0.8.0` 是从 `0.7.1` 升级而来的功能版本。相比上一版，核心变化是新增 LLM 统一调用层，并补齐兼容导入路径、资源文件访问和双语 API 文档。

新增能力：

- 新增 `VibeFlux.llms` 包。
- 新增 `LLMClient`，支持 OpenAI-compatible Chat Completions API。
- 新增 `APIKeyManager`，用于管理本地 `api_keys.json` 和环境变量 fallback。
- 新增 `ModelRegistry`、`ProviderInfo`、`ModelInfo`，用于预设和自定义模型管理。
- 新增 DeepSeek、Qwen / Alibaba Cloud Bailian、Doubao / Volcengine Ark、ZhipuAI / GLM、自定义 endpoint 预设。
- 新增单轮对话、多轮对话、流式输出、图片理解、文件辅助分析、图片生成 endpoint 包装。
- 新增 JSON 输出模板，适合检测、分割、图片理解、文本提取、文件总结和结构化报告。
- 新增 `LLMWorker`、`LLMQtRunner`，便于 PySide6 GUI 非阻塞调用大模型。
- 新增 `VibeFlux.frames` 与 `VibeFlux.managers` 兼容命名空间。
- 改进包内资源组织，安装后可以直接访问 README、QSS、YAML、UI、QRC、JSON 和图标资源。
- 默认关闭导入 banner；需要时设置 `VIBEFLUX_VERBOSE=1`。

依赖说明：LLM 功能本身使用 Python 标准库 `urllib`，没有强制新增 `openai`、`httpx`、`requests`。PDF 解析通过可选依赖 `VibeFlux[pdf]` 启用。

## 安装

从 PyPI 安装：

```bash
pip install VibeFlux
```

安装指定版本：

```bash
pip install VibeFlux==0.8.0
```

启用 PDF 文件分析：

```bash
pip install "VibeFlux[pdf]"
```

启用 PyTorch 热力图相关能力：

```bash
pip install "VibeFlux[torch]"
```

从源码安装：

```bash
git clone https://github.com/HarrisonVance26/VibeFlux.git
cd VibeFlux
pip install -e .
```

## 依赖

核心依赖：

- Python `>=3.7`
- `numpy`
- `opencv-python>=4.5.5.64`
- `Pillow>=9.0.1`
- `PySide6>=6.4.2`
- `PyYAML>=6.0`
- `captcha>=0.4`
- `aggdraw>=1.3.19`
- `ruamel.yaml>=0.18.6`

可选依赖：

- `pypdf>=4.0.0`：用于 PDF 文本提取。
- `torch`：用于 hook-based heatmap 相关功能。

## 功能总览

VibeFlux 按功能可以分为以下几类：

| 功能域 | 主要模块 | 说明 |
| --- | --- | --- |
| 媒体处理 | `VibeFlux.handlers` | 相机、视频、图片、图片文件夹处理，支持处理器链和 Qt signals。 |
| 图像转换 | `VibeFlux.base.Trans`, `VibeFlux.utils.Pixmap` | OpenCV 图像与 Qt `QPixmap` 之间转换。 |
| 检测可视化 | `VibeFlux.utils.DetVisual`, `VibeFlux.base.Visual`, `VibeFlux.utils.ImageUtils` | 绘制检测框、旋转框、mask、关键点、骨架、分类标签。 |
| UI 控件 | `VibeFlux.widgets`, `VibeFlux.frames` | 图像显示控件、窗口控制、消息框、提示气泡、登录框、设置按钮。 |
| 样式配置 | `VibeFlux.styles`, `VibeFlux.base.Sets` | 加载 QSS 主题，按 YAML 设置控件文本、图标、背景、启用状态。 |
| 数据库 | `VibeFlux.manager`, `VibeFlux.managers` | 检测日志 SQLite 管理、用户注册登录管理。 |
| LLM | `VibeFlux.llms` | 大模型 provider、model、key、消息、模板、同步/流式/Qt worker 调用。 |
| 模型抽象 | `VibeFlux.models` | Detector 抽象类、heatmap 生成器。 |
| 文件路径 | `VibeFlux.path` | 路径拼接、复制、移动、删除、文本替换、文件枚举。 |
| 摄像头工具 | `VibeFlux.utils.CameraUtils` | 摄像头扫描、分辨率和属性获取。 |
| 运行信息 | `VibeFlux.utils.Sysinfo` | 系统信息、运行环境、banner。 |

## 包结构

```text
VibeFlux/
  base/          底层 UI、转换、绘图、配置和工具函数
  config/        全局配置、可视化配置、api_keys.example.json
  default_icons/ 内置 PNG/SVG 图标资源
  examples/      示例脚本
  frames/        widgets 的兼容导入路径
  handlers/      MediaHandler 和 ImageHandler
  llms/          LLM client、配置、消息、模板、注册表、Qt worker
  manager/       DetectionDB 和 UserManager
  managers/      manager 的兼容导入路径
  models/        Detector 抽象类和 HeatmapGenerator
  path/          路径与文件管理工具
  qss/           内置 QSS 主题
  styles/        QSS / YAML 样式加载器
  utils/         图像、检测、摄像头、系统信息工具
  widgets/       PySide6 控件、窗口、对话框和提示组件
```

## 快速开始

检查版本：

```python
import VibeFlux

print(VibeFlux.__version__)
```

默认导入不输出 banner。如果需要显示运行信息：

```bash
set VIBEFLUX_VERBOSE=1
```

Linux / macOS：

```bash
export VIBEFLUX_VERBOSE=1
```

## 媒体处理接口

### `MediaHandler`

`MediaHandler` 用于处理摄像头或视频流。它使用 `cv2.VideoCapture` 读取帧，使用 Qt timer 定时触发，并通过 signal 输出帧。

常用方法：

- `setDevice(device)`：设置摄像头编号或视频文件路径。
- `setFps(fps)`：设置读取帧率。
- `startMedia()`：启动媒体读取。
- `stopMedia()`：停止并释放资源。
- `isActive()`：判断是否正在运行。
- `getMediaInfo()`：获取宽高、fps、总帧数等信息。
- `addFrameProcessor(func)`：添加帧处理函数。
- `removeFrameProcessor(func)`：移除帧处理函数。

示例：

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from VibeFlux.handlers import MediaHandler
from VibeFlux.base.Trans import ToQtPixmap


class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QLabel("Opening camera...")
        self.view.setMinimumSize(960, 540)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self.media = MediaHandler(device=0, fps=30)
        self.media.frameReady.connect(self.on_frame)
        self.media.mediaFailed.connect(self.view.setText)
        self.media.startMedia()

    def on_frame(self, frame_bgr):
        frame_rgb = frame_bgr[..., ::-1]
        self.view.setPixmap(ToQtPixmap(frame_rgb))
        self.view.setScaledContents(True)

    def closeEvent(self, event):
        if self.media.isActive():
            self.media.stopMedia()
        super().closeEvent(event)


app = QApplication(sys.argv)
window = CameraWindow()
window.show()
sys.exit(app.exec())
```

### `ImageHandler`

`ImageHandler` 用于处理单张图片或图片文件夹。

常用方法：

- `setPath(path)`：设置图片路径或图片文件夹。
- `startProcess()`：开始处理。
- `stopProcess()`：停止处理。
- `isActive()`：判断是否正在处理。
- `getFileName()`：获取当前文件名。
- `addFrameProcessor(func)` / `removeFrameProcessor(func)`：处理器链。

示例：

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel
from VibeFlux.handlers import ImageHandler
from VibeFlux.base.Trans import ToQtPixmap

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
handler.setPath("demo.jpg")
# handler.setPath("sample_images/")
handler.startProcess()

sys.exit(app.exec())
```

### 处理器链

处理器函数格式通常是 `func(frame) -> frame`。

```python
import time
import cv2

last_time = time.time()


def draw_fps(frame_bgr):
    global last_time
    now = time.time()
    fps = 1.0 / max(now - last_time, 1e-6)
    last_time = now
    cv2.putText(frame_bgr, f"FPS: {fps:.1f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    return frame_bgr


media.addFrameProcessor(draw_fps)
```

## 图像与检测可视化

### `DetectorVisual`

`DetectorVisual` 是推荐的检测可视化入口。它支持：

- 矩形框：`[x1, y1, x2, y2]`
- 旋转框 / OBB：8 个坐标点
- instance mask 或基于 bbox 的 mask 填充
- keypoints
- skeleton
- 分类结果
- 自定义 label
- 中文 / 多语言文字渲染 fallback

示例：

```python
import numpy as np
from VibeFlux.utils import DetectorVisual

visualizer = DetectorVisual()
image = np.zeros((480, 640, 3), dtype=np.uint8)

boxes = np.array([
    [50, 60, 300, 400],
    [350, 100, 550, 120, 530, 260, 330, 240],
])
scores = np.array([0.92, 0.88])
class_ids = np.array([0, 1])
labels = ["person 92%", "目标 88%"]

output = visualizer.draw_detections(
    image=image,
    boxes=boxes,
    scores=scores,
    class_ids=class_ids,
    labels=labels,
)
```

分类结果绘制：

```python
output = visualizer.draw_classification(
    image=image,
    prob=0.97,
    class_name="normal",
    custom_label="normal 97%",
)
```

### 绘图函数

常用函数：

- `drawRectBox(image, rect, ...)`
- `drawRectEdge(image, rect, ...)`
- `drawOrientedBox(image, box, ...)`
- `horizontal_bar(...)`
- `vertical_bar(...)`
- `verticalBar(...)`
- `cv_imread(file_path)`：支持 Unicode 路径读取。

```python
from VibeFlux.utils.ImageUtils import cv_imread, drawRectBox

image = cv_imread("测试图片.jpg")
image = drawRectBox(image, [20, 30, 200, 180], addText="object")
```

## PySide6 控件与窗口

主要入口：

```python
from VibeFlux.widgets import QMainWindow, QLoginDialog, QImageLabel, QWindowCtrls, QMessageBox
# 兼容路径：
from VibeFlux.frames import QImageLabel
```

### `QImageLabel`

图像显示控件，支持：

- OpenCV 图像显示
- 保持比例缩放
- 鼠标滚轮缩放
- 鼠标拖拽平移
- 覆盖文本

```python
import sys
import cv2
from PySide6.QtWidgets import QApplication
from VibeFlux.frames import QImageLabel

app = QApplication(sys.argv)
viewer = QImageLabel()
viewer.resize(1000, 700)
viewer.show()

image = cv2.imread("demo.jpg")
viewer.dispImage(image, keepAspect=True)
viewer.dispText("Scroll to zoom, drag to move")

sys.exit(app.exec())
```

### `MultiTipWidget`

多类型提示组件，支持 `info`、`warning`、`error`、`success`。

```python
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from VibeFlux.frames.TipsWidgets import MultiTipWidget


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.tip = MultiTipWidget(self, font_family="Microsoft YaHei", font_size=18)
        button = QPushButton("Show tip")
        button.clicked.connect(self.show_tip)
        layout = QVBoxLayout(self)
        layout.addWidget(button)

    def show_tip(self):
        self.tip.showTip("Saved successfully!", duration=2000, position="top", message_type="success")


app = QApplication(sys.argv)
window = Demo()
window.show()
sys.exit(app.exec())
```

### 设置和配置对话框

```python
from VibeFlux.frames.SettingsDialog import SettingsDialog, ConfigDialog

settings_dialog = SettingsDialog("ui_settings.yaml", parent=my_window)
settings_dialog.exec()

config_dialog = ConfigDialog("app_config.yaml", parent=my_window)
config_dialog.exec()
```

## QSS 与 YAML 配置

加载 QSS：

```python
from VibeFlux.styles import loadQssStyles

loadQssStyles(window=my_window, qss_file="qss/DarkDracula.qss", base_path=".")
```

加载 YAML 控件设置：

```python
from VibeFlux.styles import loadYamlSettings

loadYamlSettings(my_window, yaml_file="ui_settings.yaml", base_path=".")
```

YAML 示例：

```yaml
btnStart:
  enabled: true
  type: QPushButton
  text: Start
  icon: assets/icons/start.png

btnStop:
  enabled: true
  type: QPushButton
  text: Stop
  icon: assets/icons/stop.png

mainWindow:
  windowIcon: assets/icons/app.png
```

## SQLite 数据管理

### `DetectionDB`

用于检测结果写入 SQLite，内部使用队列和后台线程，适合视频帧连续写入。

```python
from VibeFlux.managers import DetectionDB

db = DetectionDB("detection_results.db")

db.insert(
    class_name="person",
    class_id=0,
    confidence=0.93,
    bbox=(50, 60, 300, 400),
    image_path="frame_0001.png",
)

db.insert_bulk([
    {
        "class_name": "car",
        "class_id": 2,
        "confidence": 0.88,
        "bbox": (100, 120, 320, 300),
        "image_path": "frame_0002.png",
    }
])

db.close()
```

### `UserManager`

用于简单用户系统：注册、登录校验、密码修改、头像修改、删除用户。

```python
from VibeFlux.managers import UserManager

users = UserManager("users.db")

status = users.register("alice", "secret123", "alice.png")
print("register:", status)
print("login:", users.verify_login("alice", "secret123"))
print("avatar:", users.get_avatar("alice"))

users.close()
```

## LLM 大模型调用

### 支持的 provider

| Provider key | 服务 | 默认环境变量 |
| --- | --- | --- |
| `deepseek` | DeepSeek | `DEEPSEEK_API_KEY` |
| `qwen` | Qwen / Alibaba Cloud Bailian | `DASHSCOPE_API_KEY` |
| `doubao` | Doubao / Volcengine Ark | `ARK_API_KEY` |
| `zhipu` | ZhipuAI / GLM | `ZAI_API_KEY` |
| `custom` | 任意 OpenAI-compatible endpoint | 用户自定义 |

### API Key 管理

```python
from VibeFlux.llms import APIKeyManager

keys = APIKeyManager("api_keys.json")
keys.set_api_key("qwen", "YOUR_API_KEY")
keys.set_active(provider="qwen", model="qwen-plus")
```

也可以使用环境变量：

```bash
set DASHSCOPE_API_KEY=your-api-key
```

Linux / macOS：

```bash
export DASHSCOPE_API_KEY=your-api-key
```

查看包内示例配置路径：

```python
from VibeFlux.llms import package_example_config_path

print(package_example_config_path())
```

### 单轮对话

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")
reply = client.single_chat("用三句话介绍 VibeFlux。")
print(reply.content)
```

### 多轮对话

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")
client.reset_history(system="你是一个严谨的桌面视觉应用助手。")

print(client.send("请记住：我的应用使用 PySide6。").content)
print(client.send("我上一句提到的 GUI 框架是什么？").content)
```

### 图片理解和 JSON 输出

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")

result = client.ask_image(
    image="sample.jpg",
    prompt="识别图中的主要目标、位置和异常。",
    task="image_detection",
    response_format="json",
)

print(result.content)
```

### 文件辅助分析

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")
summary = client.analyze_file("notes.md", task="file_summary", response_format="json")
print(summary.content)
```

PDF 需要：

```bash
pip install "VibeFlux[pdf]"
```

### 流式输出

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")

for chunk in client.single_chat("请总结这批检测结果中的主要异常。", stream=True):
    print(chunk, end="", flush=True)
```

### 自定义模型

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")

client.add_custom_model(
    provider="custom",
    name="local-chat-model",
    api_model="local-chat-model",
    capabilities=["text", "stream", "json"],
)

client.configure(
    provider="custom",
    model="local-chat-model",
    base_url="http://127.0.0.1:8000/v1",
)
```

### PySide6 后台调用

```python
from VibeFlux.llms import LLMQtRunner

runner = LLMQtRunner(config_path="api_keys.json")
runner.responseReady.connect(lambda response: print(response.content))
runner.chunkReady.connect(lambda text: print(text, end=""))
runner.failed.connect(print)

runner.ask("总结当前检测结果。", stream=True)
```

### 输出模板

```python
from VibeFlux.llms import template_names, render_template_prompt

print(template_names())
print(render_template_prompt("image_detection", user_input="分析这张图片"))
```

常用模板包括：

- `image_detection`
- `image_segmentation`
- `image_understanding`
- `text_extraction`
- `file_summary`
- `structured_report`

## 模型抽象与热力图

### `Detector`

`Detector` 是抽象检测器接口，用于约束自定义模型类。

需要实现：

- `load_model(model_path)`
- `preprocess(img)`
- `predict(img)`
- `postprocess(prediction)`

```python
from VibeFlux.models import Detector


class MyDetector(Detector):
    def load_model(self, model_path):
        self.model = ...

    def preprocess(self, img):
        return img

    def predict(self, img):
        return self.model(img)

    def postprocess(self, prediction):
        return prediction
```

### `HeatmapGenerator`

用于从模型指定层提取 feature map 并生成热力图。该功能通常需要 PyTorch。

```python
from VibeFlux.models import HeatmapGenerator

generator = HeatmapGenerator(model, target_layer)
heatmap = generator.get_heatmap(img)
```

## 路径文件摄像头与系统工具

路径：

```python
from VibeFlux.path import abs_path, join_paths, create_dir, list_files

path = abs_path("assets/icon.png")
folder = join_paths("runs", "detect")
create_dir(folder)
print(list_files(folder))
```

文件管理：

```python
from VibeFlux.path import copy_file_folder, get_subfiles, modify_content

copy_file_folder("src", "dst", overwrite=True)
files, names = get_subfiles("dst")
modify_content("config.yaml", "old", "new")
```

摄像头：

```python
from VibeFlux.utils.CameraUtils import find_cameras, get_cam_properties

print(find_cameras(max_devices=5))
print(get_cam_properties(0))
```

系统信息：

```python
from VibeFlux.utils.Sysinfo import get_runtime_info

print(get_runtime_info())
```

## 公共 API 摘要

完整逐项 API 参考见：[中文 API 参考](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.zh-CN.md)。下面是主要入口摘要。

| 模块 | 重要 API |
| --- | --- |
| `VibeFlux.handlers` | `MediaHandler`, `ImageHandler` |
| `VibeFlux.widgets` / `VibeFlux.frames` | `QMainWindow`, `QLoginDialog`, `QImageLabel`, `QWindowCtrls`, `QMessageBox`, `SettingsDialog`, `ConfigDialog`, `MultiTipWidget` |
| `VibeFlux.styles` | `loadQssStyles`, `loadYamlSettings`, `BaseStyle` |
| `VibeFlux.utils` | `DetectorVisual`, `DetectorVisualPIL`, `cv_imread`, `drawRectBox`, `drawRectEdge`, `drawOrientedBox`, `find_cameras` |
| `VibeFlux.manager` / `VibeFlux.managers` | `DetectionDB`, `UserManager` |
| `VibeFlux.llms` | `LLMClient`, `LLMResponse`, `LLMAPIError`, `APIKeyManager`, `ModelRegistry`, `ProviderInfo`, `ModelInfo`, `OutputTemplate`, `LLMQtRunner`, `LLMWorker` |
| `VibeFlux.models` | `Detector`, `HeatmapGenerator` |
| `VibeFlux.path` | `abs_path`, `get_abs_path`, `join_paths`, `list_files`, `copy_file_folder`, `delete_file`, `modify_content` |
| `VibeFlux.base` | `ToQtPixmap`, `scalePixmap`, `imRandCode`, `BaseDB`, `IMDetectorVisual`, `IMTipWidget` |

## 常见问题

### Qt platform plugin 报错

先确认 PySide6 可正常启动最小窗口，再导入 VibeFlux。不同系统可能需要额外 Qt runtime 组件。

### 摄像头打不开

确认摄像头没有被其他程序占用，尝试 `0`、`1`、`2` 等设备编号，并使用 `find_cameras()` 扫描。

### OpenCV 图像颜色不对

OpenCV 默认是 BGR，Qt 常用 RGB：

```python
frame_rgb = frame_bgr[..., ::-1]
```

### LLM 报 API key 为空

设置 `api_keys.json` 或环境变量。真实 key 不要提交到版本库。

### PDF 文件无法提取文本

安装：

```bash
pip install "VibeFlux[pdf]"
```

## 许可证

VibeFlux 使用 **GNU Affero General Public License v3.0 or later**。

如果你分发包含 VibeFlux 的应用，或将其部署为网络服务，请确认理解并遵守 AGPL 义务。

---

<a id="english-documentation"></a>

# VibeFlux English Documentation

[中文](#中文文档) | [Full English API Reference](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.en.md) | [中文 API 参考](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.zh-CN.md)

**VibeFlux** is a Python toolkit for building computer-vision desktop applications around **PySide6 / Qt**, **OpenCV**, **Pillow**, reusable UI widgets, detection visualization utilities, SQLite managers, and an OpenAI-compatible LLM client layer. It is useful for YOLO / deep-learning visual applications, result inspection tools, training dashboards, desktop apps with login/config panels, and workflows that combine computer vision with LLM-powered image or file understanding.

> Status: Pre-Alpha. The APIs are usable, but the package may still evolve. Pin a version such as `VibeFlux==0.8.0` for production projects.

## English Table of Contents

- [What's New in 0.8.0](#whats-new-in-080)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Feature Overview](#feature-overview)
- [Package Layout](#package-layout)
- [Quick Start](#quick-start)
- [Media Handling](#media-handling)
- [Image and Detection Visualization](#image-and-detection-visualization)
- [PySide6 Widgets and Windows](#pyside6-widgets-and-windows)
- [QSS and YAML Configuration](#qss-and-yaml-configuration)
- [SQLite Data Managers](#sqlite-data-managers)
- [LLM Integration](#llm-integration)
- [Model Interfaces and Heatmaps](#model-interfaces-and-heatmaps)
- [Path File Camera and System Utilities](#path-file-camera-and-system-utilities)
- [Public API Summary](#public-api-summary)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## What's New in 0.8.0

Version `0.8.0` upgrades VibeFlux from `0.7.1` with a new LLM layer, compatibility import paths, resource access improvements, and bilingual API documentation.

Highlights:

- Added `VibeFlux.llms`.
- Added `LLMClient` for OpenAI-compatible Chat Completions APIs.
- Added `APIKeyManager` for local `api_keys.json` and environment-variable fallback.
- Added `ModelRegistry`, `ProviderInfo`, and `ModelInfo` for preset and custom models.
- Added presets for DeepSeek, Qwen / Alibaba Cloud Bailian, Doubao / Volcengine Ark, ZhipuAI / GLM, and custom endpoints.
- Added single-turn chat, multi-turn chat, streaming output, image understanding, file-assisted analysis, and image-generation endpoint wrapping.
- Added JSON output templates for detection, segmentation, image understanding, text extraction, file summaries, and structured reports.
- Added `LLMWorker` and `LLMQtRunner` for non-blocking PySide6 integration.
- Added compatibility namespaces `VibeFlux.frames` and `VibeFlux.managers`.
- Improved in-package resource organization for README, QSS, YAML, UI, QRC, JSON, and icon assets.
- Imports are silent by default; set `VIBEFLUX_VERBOSE=1` to print the runtime banner.

The LLM layer uses Python's standard-library `urllib`; it does not require `openai`, `httpx`, or `requests` as mandatory dependencies. PDF extraction is available through the optional `VibeFlux[pdf]` extra.

## Installation

```bash
pip install VibeFlux
```

Install a pinned version:

```bash
pip install VibeFlux==0.8.0
```

Install optional PDF support:

```bash
pip install "VibeFlux[pdf]"
```

Install optional PyTorch support:

```bash
pip install "VibeFlux[torch]"
```

Install from source:

```bash
git clone https://github.com/HarrisonVance26/VibeFlux.git
cd VibeFlux
pip install -e .
```

## Dependencies

Core dependencies:

- Python `>=3.7`
- `numpy`
- `opencv-python>=4.5.5.64`
- `Pillow>=9.0.1`
- `PySide6>=6.4.2`
- `PyYAML>=6.0`
- `captcha>=0.4`
- `aggdraw>=1.3.19`
- `ruamel.yaml>=0.18.6`

Optional dependencies:

- `pypdf>=4.0.0` for PDF text extraction.
- `torch` for hook-based heatmap workflows.

## Feature Overview

| Area | Main modules | Description |
| --- | --- | --- |
| Media handling | `VibeFlux.handlers` | Camera, video, image, and image-folder processing with processor chains and Qt signals. |
| Image conversion | `VibeFlux.base.Trans`, `VibeFlux.utils.Pixmap` | Convert OpenCV images to Qt `QPixmap`. |
| Detection visualization | `VibeFlux.utils.DetVisual`, `VibeFlux.base.Visual`, `VibeFlux.utils.ImageUtils` | Draw boxes, oriented boxes, masks, keypoints, skeletons, classification labels, and multilingual text. |
| UI widgets | `VibeFlux.widgets`, `VibeFlux.frames` | Image viewers, window controls, message boxes, toast tips, login dialogs, settings buttons. |
| Styling | `VibeFlux.styles`, `VibeFlux.base.Sets` | Load QSS themes and apply YAML-driven widget settings. |
| Database | `VibeFlux.manager`, `VibeFlux.managers` | Detection logging and user management on SQLite. |
| LLM | `VibeFlux.llms` | Provider/model/key management, messages, templates, sync/streaming/Qt-worker calls. |
| Models | `VibeFlux.models` | Abstract detector interface and heatmap generation. |
| File paths | `VibeFlux.path` | Path joining, copying, moving, deleting, text replacement, file enumeration. |
| Camera tools | `VibeFlux.utils.CameraUtils` | Camera scanning, resolution, and property helpers. |
| Diagnostics | `VibeFlux.utils.Sysinfo` | Runtime system information and banner output. |

## Package Layout

```text
VibeFlux/
  base/          Core UI, conversion, drawing, config, and utility primitives
  config/        Global config, visualization config, api_keys.example.json
  default_icons/ Built-in PNG/SVG resources
  examples/      Example scripts
  frames/        Compatibility import path for widgets
  handlers/      MediaHandler and ImageHandler
  llms/          LLM client, config, messages, templates, registry, Qt workers
  manager/       DetectionDB and UserManager
  managers/      Compatibility import path for manager
  models/        Detector abstract base and HeatmapGenerator
  path/          Path and file management tools
  qss/           Built-in QSS themes
  styles/        QSS / YAML style loaders
  utils/         Image, detection, camera, and system helpers
  widgets/       PySide6 widgets, windows, dialogs, and tips
```

## Quick Start

```python
import VibeFlux

print(VibeFlux.__version__)
```

Imports are silent by default. To print a runtime banner:

```bash
set VIBEFLUX_VERBOSE=1
```

Linux / macOS:

```bash
export VIBEFLUX_VERBOSE=1
```

## Media Handling

### `MediaHandler`

`MediaHandler` reads a camera or video source through `cv2.VideoCapture`, schedules frame reads through a Qt timer, and emits frames through signals.

Common methods:

- `setDevice(device)`
- `setFps(fps)`
- `startMedia()`
- `stopMedia()`
- `isActive()`
- `getMediaInfo()`
- `addFrameProcessor(func)`
- `removeFrameProcessor(func)`

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from VibeFlux.handlers import MediaHandler
from VibeFlux.base.Trans import ToQtPixmap


class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QLabel("Opening camera...")
        self.view.setMinimumSize(960, 540)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self.media = MediaHandler(device=0, fps=30)
        self.media.frameReady.connect(self.on_frame)
        self.media.mediaFailed.connect(self.view.setText)
        self.media.startMedia()

    def on_frame(self, frame_bgr):
        frame_rgb = frame_bgr[..., ::-1]
        self.view.setPixmap(ToQtPixmap(frame_rgb))
        self.view.setScaledContents(True)

    def closeEvent(self, event):
        if self.media.isActive():
            self.media.stopMedia()
        super().closeEvent(event)


app = QApplication(sys.argv)
window = CameraWindow()
window.show()
sys.exit(app.exec())
```

### `ImageHandler`

`ImageHandler` processes one image or an image folder.

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel
from VibeFlux.handlers import ImageHandler
from VibeFlux.base.Trans import ToQtPixmap

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
handler.setPath("demo.jpg")
handler.startProcess()

sys.exit(app.exec())
```

Processor functions usually follow `func(frame) -> frame`:

```python
import time
import cv2

last_time = time.time()


def draw_fps(frame_bgr):
    global last_time
    now = time.time()
    fps = 1.0 / max(now - last_time, 1e-6)
    last_time = now
    cv2.putText(frame_bgr, f"FPS: {fps:.1f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    return frame_bgr


media.addFrameProcessor(draw_fps)
```

## Image and Detection Visualization

`DetectorVisual` is the recommended high-level visualization class. It supports rectangular boxes, oriented boxes, masks, keypoints, skeletons, classification results, custom labels, and multilingual text rendering.

```python
import numpy as np
from VibeFlux.utils import DetectorVisual

visualizer = DetectorVisual()
image = np.zeros((480, 640, 3), dtype=np.uint8)

boxes = np.array([
    [50, 60, 300, 400],
    [350, 100, 550, 120, 530, 260, 330, 240],
])
scores = np.array([0.92, 0.88])
class_ids = np.array([0, 1])
labels = ["person 92%", "target 88%"]

output = visualizer.draw_detections(
    image=image,
    boxes=boxes,
    scores=scores,
    class_ids=class_ids,
    labels=labels,
)
```

Classification drawing:

```python
output = visualizer.draw_classification(
    image=image,
    prob=0.97,
    class_name="normal",
    custom_label="normal 97%",
)
```

Drawing helpers:

- `drawRectBox(image, rect, ...)`
- `drawRectEdge(image, rect, ...)`
- `drawOrientedBox(image, box, ...)`
- `horizontal_bar(...)`
- `vertical_bar(...)`
- `verticalBar(...)`
- `cv_imread(file_path)` for Unicode paths.

## PySide6 Widgets and Windows

```python
from VibeFlux.widgets import QMainWindow, QLoginDialog, QImageLabel, QWindowCtrls, QMessageBox
from VibeFlux.frames import QImageLabel  # compatibility path
```

### `QImageLabel`

A zoomable and pannable image display widget.

```python
import sys
import cv2
from PySide6.QtWidgets import QApplication
from VibeFlux.frames import QImageLabel

app = QApplication(sys.argv)
viewer = QImageLabel()
viewer.resize(1000, 700)
viewer.show()

image = cv2.imread("demo.jpg")
viewer.dispImage(image, keepAspect=True)
viewer.dispText("Scroll to zoom, drag to move")

sys.exit(app.exec())
```

### `MultiTipWidget`

```python
from VibeFlux.frames.TipsWidgets import MultiTipWidget

self.tip = MultiTipWidget(self)
self.tip.showTip("Saved successfully!", duration=2000, position="top", message_type="success")
```

### Settings dialogs

```python
from VibeFlux.frames.SettingsDialog import SettingsDialog, ConfigDialog

SettingsDialog("ui_settings.yaml", parent=my_window).exec()
ConfigDialog("app_config.yaml", parent=my_window).exec()
```

## QSS and YAML Configuration

```python
from VibeFlux.styles import loadQssStyles, loadYamlSettings

loadQssStyles(window=my_window, qss_file="qss/DarkDracula.qss", base_path=".")
loadYamlSettings(my_window, yaml_file="ui_settings.yaml", base_path=".")
```

Example YAML:

```yaml
btnStart:
  enabled: true
  type: QPushButton
  text: Start
  icon: assets/icons/start.png

mainWindow:
  windowIcon: assets/icons/app.png
```

## SQLite Data Managers

### `DetectionDB`

```python
from VibeFlux.managers import DetectionDB

db = DetectionDB("detection_results.db")
db.insert("person", 0, 0.93, (50, 60, 300, 400), "frame_0001.png")
db.insert_bulk([
    {"class_name": "car", "class_id": 2, "confidence": 0.88, "bbox": (100, 120, 320, 300), "image_path": "frame_0002.png"}
])
db.close()
```

### `UserManager`

```python
from VibeFlux.managers import UserManager

users = UserManager("users.db")
users.register("alice", "secret123", "alice.png")
print(users.verify_login("alice", "secret123"))
users.close()
```

## LLM Integration

### Providers

| Provider key | Service | Default environment variable |
| --- | --- | --- |
| `deepseek` | DeepSeek | `DEEPSEEK_API_KEY` |
| `qwen` | Qwen / Alibaba Cloud Bailian | `DASHSCOPE_API_KEY` |
| `doubao` | Doubao / Volcengine Ark | `ARK_API_KEY` |
| `zhipu` | ZhipuAI / GLM | `ZAI_API_KEY` |
| `custom` | Any OpenAI-compatible endpoint | user-defined |

### API key management

```python
from VibeFlux.llms import APIKeyManager

keys = APIKeyManager("api_keys.json")
keys.set_api_key("qwen", "YOUR_API_KEY")
keys.set_active(provider="qwen", model="qwen-plus")
```

Environment variable example:

```bash
set DASHSCOPE_API_KEY=your-api-key
```

### Single-turn chat

```python
from VibeFlux.llms import LLMClient

client = LLMClient(config_path="api_keys.json")
reply = client.single_chat("Explain VibeFlux in three concise sentences.")
print(reply.content)
```

### Multi-turn chat

```python
client.reset_history(system="You are a careful desktop CV application assistant.")
print(client.send("Remember that my app uses PySide6.").content)
print(client.send("Which GUI framework did I mention?").content)
```

### Image understanding

```python
result = client.ask_image(
    image="sample.jpg",
    prompt="Identify the main objects, positions, and anomalies.",
    task="image_detection",
    response_format="json",
)
print(result.content)
```

### File-assisted analysis

```python
summary = client.analyze_file("notes.md", task="file_summary", response_format="json")
print(summary.content)
```

PDF files require:

```bash
pip install "VibeFlux[pdf]"
```

### Streaming

```python
for chunk in client.single_chat("Summarize the main anomalies in these detection results.", stream=True):
    print(chunk, end="", flush=True)
```

### Custom model

```python
client.add_custom_model(
    provider="custom",
    name="local-chat-model",
    api_model="local-chat-model",
    capabilities=["text", "stream", "json"],
)
client.configure(provider="custom", model="local-chat-model", base_url="http://127.0.0.1:8000/v1")
```

### PySide6 worker

```python
from VibeFlux.llms import LLMQtRunner

runner = LLMQtRunner(config_path="api_keys.json")
runner.responseReady.connect(lambda response: print(response.content))
runner.chunkReady.connect(lambda text: print(text, end=""))
runner.failed.connect(print)
runner.ask("Summarize the current detection result.", stream=True)
```

## Model Interfaces and Heatmaps

```python
from VibeFlux.models import Detector


class MyDetector(Detector):
    def load_model(self, model_path):
        self.model = ...

    def preprocess(self, img):
        return img

    def predict(self, img):
        return self.model(img)

    def postprocess(self, prediction):
        return prediction
```

```python
from VibeFlux.models import HeatmapGenerator

generator = HeatmapGenerator(model, target_layer)
heatmap = generator.get_heatmap(img)
```

## Path File Camera and System Utilities

```python
from VibeFlux.path import abs_path, join_paths, create_dir, list_files

path = abs_path("assets/icon.png")
folder = join_paths("runs", "detect")
create_dir(folder)
print(list_files(folder))
```

```python
from VibeFlux.utils.CameraUtils import find_cameras, get_cam_properties

print(find_cameras(max_devices=5))
print(get_cam_properties(0))
```

```python
from VibeFlux.utils.Sysinfo import get_runtime_info

print(get_runtime_info())
```

## Public API Summary

See the full generated reference: [English API Reference](https://github.com/HarrisonVance26/VibeFlux/blob/main/docs/API.en.md). Key entry points:

| Module | Important APIs |
| --- | --- |
| `VibeFlux.handlers` | `MediaHandler`, `ImageHandler` |
| `VibeFlux.widgets` / `VibeFlux.frames` | `QMainWindow`, `QLoginDialog`, `QImageLabel`, `QWindowCtrls`, `QMessageBox`, `SettingsDialog`, `ConfigDialog`, `MultiTipWidget` |
| `VibeFlux.styles` | `loadQssStyles`, `loadYamlSettings`, `BaseStyle` |
| `VibeFlux.utils` | `DetectorVisual`, `DetectorVisualPIL`, `cv_imread`, `drawRectBox`, `drawRectEdge`, `drawOrientedBox`, `find_cameras` |
| `VibeFlux.manager` / `VibeFlux.managers` | `DetectionDB`, `UserManager` |
| `VibeFlux.llms` | `LLMClient`, `LLMResponse`, `LLMAPIError`, `APIKeyManager`, `ModelRegistry`, `ProviderInfo`, `ModelInfo`, `OutputTemplate`, `LLMQtRunner`, `LLMWorker` |
| `VibeFlux.models` | `Detector`, `HeatmapGenerator` |
| `VibeFlux.path` | `abs_path`, `get_abs_path`, `join_paths`, `list_files`, `copy_file_folder`, `delete_file`, `modify_content` |
| `VibeFlux.base` | `ToQtPixmap`, `scalePixmap`, `imRandCode`, `BaseDB`, `IMDetectorVisual`, `IMTipWidget` |

## Troubleshooting

### Qt platform plugin errors

Verify that a minimal PySide6 window can start in your environment before importing VibeFlux UI modules.

### Camera cannot be opened

Check whether another app is using the camera, try device indices `0`, `1`, `2`, and use `find_cameras()`.

### Wrong image colors

OpenCV uses BGR while Qt usually expects RGB:

```python
frame_rgb = frame_bgr[..., ::-1]
```

### Empty LLM API key

Set `api_keys.json` or the provider environment variable. Do not commit real keys.

### PDF text extraction fails

```bash
pip install "VibeFlux[pdf]"
```

## License

VibeFlux is licensed under the **GNU Affero General Public License v3.0 or later**.

If you distribute an application that includes VibeFlux, or deploy it as a network service, make sure you understand and comply with AGPL obligations.
