# VibeFlux API 参考（中文）

[English API](API.en.md) | [返回 README](../README.md#中文文档)

本文档由源码中的公开类、函数和方法扫描整理而来，覆盖 `VibeFlux` 包当前公开 API。带下划线开头的内部对象未列入。

## 模块索引

- [`VibeFlux._runtime`](#vibefluxruntime) - 运行时依赖检查工具。
- [`VibeFlux.base.Encode`](#vibefluxbaseencode) - 验证码图片生成。
- [`VibeFlux.base.Extension`](#vibefluxbaseextension) - 底层扩展控件。
- [`VibeFlux.base.Manager`](#vibefluxbasemanager) - SQLite 基础连接管理。
- [`VibeFlux.base.Plots`](#vibefluxbaseplots) - 图表、矩形框、旋转框绘图函数。
- [`VibeFlux.base.Processor`](#vibefluxbaseprocessor) - 媒体和图片处理信号基类。
- [`VibeFlux.base.Sets`](#vibefluxbasesets) - QSS 与 YAML 设置加载。
- [`VibeFlux.base.Tips`](#vibefluxbasetips) - 提示气泡和淡入淡出动画。
- [`VibeFlux.base.Trans`](#vibefluxbasetrans) - OpenCV / Qt 图像转换。
- [`VibeFlux.base.Utils`](#vibefluxbaseutils) - 基础路径工具。
- [`VibeFlux.base.Visual`](#vibefluxbasevisual) - 检测、分割、关键点、分类可视化核心。
- [`VibeFlux.base.VisualConf`](#vibefluxbasevisualconf) - 类别名称和颜色配置读取。
- [`VibeFlux.base.Widget`](#vibefluxbasewidget) - 底层窗口、对话框和设置编辑器基类。
- [`VibeFlux.config.QfConfig`](#vibefluxconfigqfconfig) - 全局运行配置。
- [`VibeFlux.config.VisualConf`](#vibefluxconfigvisualconf) - 可视化配置读取。
- [`VibeFlux.examples.llm_usage`](#vibefluxexamplesllmusage) - 公开模块。
- [`VibeFlux.handlers.Handler`](#vibefluxhandlershandler) - 相机、视频、图片和图片文件夹处理器。
- [`VibeFlux.llms.Client`](#vibefluxllmsclient) - OpenAI-compatible LLM 客户端。
- [`VibeFlux.llms.Config`](#vibefluxllmsconfig) - API Key 和 LLM 配置管理。
- [`VibeFlux.llms.Message`](#vibefluxllmsmessage) - 文本、图片、文件消息构造工具。
- [`VibeFlux.llms.QtBridge`](#vibefluxllmsqtbridge) - PySide6 后台线程 LLM 调用。
- [`VibeFlux.llms.Registry`](#vibefluxllmsregistry) - Provider 和 Model 注册表。
- [`VibeFlux.llms.Templates`](#vibefluxllmstemplates) - 结构化输出模板。
- [`VibeFlux.llms.Updater`](#vibefluxllmsupdater) - 从 provider /models 接口刷新模型列表。
- [`VibeFlux.manager.DetManager`](#vibefluxmanagerdetmanager) - 检测结果 SQLite 管理。
- [`VibeFlux.manager.UserManager`](#vibefluxmanagerusermanager) - 用户注册、登录和头像管理。
- [`VibeFlux.models.AbstractModel`](#vibefluxmodelsabstractmodel) - 检测模型抽象接口。
- [`VibeFlux.models.Heatmap`](#vibefluxmodelsheatmap) - 基于 PyTorch hook 的热力图生成。
- [`VibeFlux.path.FManager`](#vibefluxpathfmanager) - 文件复制、删除、查找、文本替换工具。
- [`VibeFlux.path.Path`](#vibefluxpathpath) - 路径拼接、列举、移动、复制工具。
- [`VibeFlux.RecSystem`](#vibefluxrecsystem) - Qt 资源系统入口，通常由包内部导入。
- [`VibeFlux.styles.Formers`](#vibefluxstylesformers) - YAML UI 设置应用函数。
- [`VibeFlux.styles.Styles`](#vibefluxstylesstyles) - QSS 主题和样式应用。
- [`VibeFlux.utils.CameraUtils`](#vibefluxutilscamerautils) - 摄像头扫描、分辨率和属性工具。
- [`VibeFlux.utils.DetVisual`](#vibefluxutilsdetvisual) - 检测可视化公开包装类。
- [`VibeFlux.utils.FileUtils`](#vibefluxutilsfileutils) - QSS 读取和 YAML 配置访问。
- [`VibeFlux.utils.ImageUtils`](#vibefluxutilsimageutils) - 图像读取、图表、检测框绘制工具。
- [`VibeFlux.utils.Pixmap`](#vibefluxutilspixmap) - OpenCV 图像到 QPixmap 的转换。
- [`VibeFlux.utils.Sysinfo`](#vibefluxutilssysinfo) - 系统和运行环境信息。
- [`VibeFlux.widgets.BaseFrame`](#vibefluxwidgetsbaseframe) - 窗口基类、登录框、动画、表格和图像显示工具。
- [`VibeFlux.widgets.ExtWidgets`](#vibefluxwidgetsextwidgets) - 图像标签、窗口控制、消息框扩展控件。
- [`VibeFlux.widgets.SettingsDialog`](#vibefluxwidgetssettingsdialog) - YAML 设置和通用配置编辑对话框。
- [`VibeFlux.widgets.TipsWidgets`](#vibefluxwidgetstipswidgets) - 多类型提示气泡。
- [`VibeFlux.widgets.Widgets`](#vibefluxwidgetswidgets) - 面向用户的 Qt 控件包装。

<a id="vibefluxruntime"></a>
## `VibeFlux._runtime`

运行时依赖检查工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `check_dependencies` | `check_dependencies()` | - |

<a id="vibefluxbaseencode"></a>
## `VibeFlux.base.Encode`

验证码图片生成。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `imRandCode` | `imRandCode(width=170, height=80, length=4, characters=None)` | Generates a random verification code and returns an image of the code and the code itself as a string. :param width: The width of the image. Defaults to 170. |

<a id="vibefluxbaseextension"></a>
## `VibeFlux.base.Extension`

底层扩展控件。

### 类

#### `IMageLabel`

A QLabel extension that provides additional functionality for displaying images. This class extends QLabel, providing the ability to display images and text. It allows for interactive

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setAspectMode` | `setAspectMode(self, keepAspect: bool)` | Sets the aspect ratio mode for the label. |
| `dispText` | `dispText(self, text)` | Displays text in the label. |
| `dispImage` | `dispImage(self, image, keepAspect=True)` | Displays an image read by OpenCV in the label. |
| `paintEvent` | `paintEvent(self, e)` | Handles paint events. |
| `wheelEvent` | `wheelEvent(self, event)` | Handles mouse wheel events. This will allow to zoom the image in or out. |
| `mouseMoveEvent` | `mouseMoveEvent(self, e)` | Handles mouse move events. This will allow to pan the image when the mouse is moved. |
| `mousePressEvent` | `mousePressEvent(self, e)` | Handles mouse press events. This will start the panning operation. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, e)` | Handles mouse release events. This will end the panning operation. |
| `normButton` | `normButton(self)` | Resets the image size to the original size. |
| `bigButton` | `bigButton(self)` | Increases the size of the image by 10%. |
| `smallButton` | `smallButton(self)` | Decreases the size of the image by 10%. |

#### `IMessageBox`

This class represents a custom message box that inherits from QDialog. The message box includes a title, a message, and Yes/No buttons.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_icon` | `set_icon(self, icon_path)` | Sets the window icon. |
| `layoutMessage` | `layoutMessage(self, message='', yes_text='Yes', no_text='No')` | - |

#### `IMExtWindow`

FBaseWindow is a class derived from QMainWindow to provide custom methods and properties for handling graphical user interface (GUI) related operations in the application.

<a id="vibefluxbasemanager"></a>
## `VibeFlux.base.Manager`

SQLite 基础连接管理。

### 类

#### `BaseDB`

A base class that provides fundamental database connection management.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `connect` | `connect(self, check_same_thread: bool=True)` | Establishes a connection to the SQLite database. |
| `close` | `close(self)` | Closes the database connection. |

<a id="vibefluxbaseplots"></a>
## `VibeFlux.base.Plots`

图表、矩形框、旋转框绘图函数。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `imHBar` | `imHBar(label_name, value, colors, width, height, value_name=None, color_text='#000000', alpha=0.8, margin=20, fontB=None)` | Creates a horizontal bar chart image. Args: |
| `imVBar` | `imVBar(label_name, value, colors, width, height, value_name=None, color_text='#000000', alpha=0.7, margin=20, fontB=None)` | Creates a vertical bar chart image. Args: |
| `imVBarPer` | `imVBarPer(label_name, value, colors, width, height, value_name=None, color_text='#000000', alpha=0.7, margin=20, fontB=None)` | Generate a vertical bar chart as a QPixmap. Args: |
| `imRectBox` | `imRectBox(img, rect, color=None, alpha=0.25, addText=None, line_thickness=None, fontC=None)` | Draws a rectangular bounding box on an image. Args: |
| `imRectEdge` | `imRectEdge(img, rect, color=None, alpha=0.2, addText=None, line_thickness=None, fontC=None)` | Draw a rectangle with annotated edges on an image. Args: |
| `draw_oriented_box` | `draw_oriented_box(image, box, color=None, alpha=0.25, addText=None, line_thickness=None, fontC=None)` | Draws an oriented bounding box (OBB) on an image. Args: |

<a id="vibefluxbaseprocessor"></a>
## `VibeFlux.base.Processor`

媒体和图片处理信号基类。

### 类

#### `IMediaSignals`

The MediaSignals class encapsulates signals related to media operations. Attributes:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `addFrameProcessor` | `addFrameProcessor(self, func)` | Adds a frame processing function to the list. This function will be applied to each frame of the media. |
| `removeFrameProcessor` | `removeFrameProcessor(self, func)` | Removes a frame processing function from the list. |
| `setDevice` | `setDevice(self, device)` | Sets the media source device. |
| `isActive` | `isActive(self)` | Checks if the media feed is currently active (playing). |

#### `ImageSignals`

ImageHandler is responsible for managing and processing image files. It provides functionalities to process images individually or in batches if provided with a directory path. The class supports custom image processing functionalities, where each image can be processed using user-defined functions. Signals are emitted to indicate

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `addFrameProcessor` | `addFrameProcessor(self, func)` | Adds a function to the list of image processors. Each processor is applied sequentially to the images. |
| `removeFrameProcessor` | `removeFrameProcessor(self, func)` | Removes a function from the list of processors that are applied to each image. |
| `setPath` | `setPath(self, path)` | Sets the path of the image or directory to be processed. |
| `stopProcess` | `stopProcess(self)` | Stops the ongoing image processing tasks. Emits an 'imageClosed' signal after processing is stopped. |
| `isActive` | `isActive(self)` | Checks if the ImageHandler is currently processing an image. |
| `getFileName` | `getFileName(self)` | Gets the name of the current file being processed. |

<a id="vibefluxbasesets"></a>
## `VibeFlux.base.Sets`

QSS 与 YAML 设置加载。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `loadSettings` | `loadSettings(window, widget, widget_name, settings, base_path='./')` | Load settings for a QWidget from a YAML file and apply them to the specified window. Args: |
| `loadStyles` | `loadStyles(window, qss_file, base_path='./')` | Load QSS styles for a QMainWindow. :param window: QMainWindow instance to apply the styles to. |
| `readQssFile` | `readQssFile(qss_file_path)` | Read and return the content of a QSS file. Args: |
| `tryImportOriStyle` | `tryImportOriStyle(window, qss_file)` | - |

<a id="vibefluxbasetips"></a>
## `VibeFlux.base.Tips`

提示气泡和淡入淡出动画。

### 类

#### `IMTipWidget`

A custom widget for displaying tooltip messages with fade-in and fade-out animations. This widget is designed to overlay on its parent widget and provide a non-intrusive notification message.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setOpacity` | `setOpacity(self, opacity: float)` | Set the opacity of the tooltip. |
| `getOpacity` | `getOpacity(self)` | Retrieve the current opacity value of the tooltip. |
| `showTip` | `showTip(self, text: str, duration: int=3000, position: str | tuple[int, int] | QPoint='center')` | Display the tooltip with the specified text, duration, and position. |
| `setPosition` | `setPosition(self, position: str | tuple[int, int] | QPoint)` | Set the position of the tooltip relative to its parent widget. |
| `fadeIn` | `fadeIn(self)` | Start the fade-in animation to make the tooltip visible (opacity: 0.0 to 1.0). |
| `fadeOut` | `fadeOut(self)` | Start the fade-out animation to hide the tooltip (opacity: 1.0 to 0.0). |
| `closeEvent` | `closeEvent(self, event)` | Handle the close event by stopping the timer and performing cleanup. |

<a id="vibefluxbasetrans"></a>
## `VibeFlux.base.Trans`

OpenCV / Qt 图像转换。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `ToQtPixmap` | `ToQtPixmap(cv_image_rgb)` | Converts an RGB OpenCV image to a QPixmap. Args: |
| `scalePixmap` | `scalePixmap(pixmap, size, keepAspect)` | Scales a QPixmap to a specified size. :param pixmap: The QPixmap to be scaled. |
| `setPixmap` | `setPixmap(label, pixmap)` | Set a QPixmap to a specified QLabel. :param label: The QLabel name. :param pixmap: The QPixmap to be scaled. |

<a id="vibefluxbaseutils"></a>
## `VibeFlux.base.Utils`

基础路径工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `pathExists` | `pathExists(path: str)` | Checks if the specified path exists. Args: |
| `catchPath` | `catchPath(relative_path: str, base_path: Optional[str]=None, path_type: Optional[str]='current')` | Appends an absolute path prefix to a single relative path. Args: |

<a id="vibefluxbasevisual"></a>
## `VibeFlux.base.Visual`

检测、分割、关键点、分类可视化核心。

### 类

#### `IMDetectorVisual`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_params` | `set_params(self, cls_names: Optional[List[str]]=None, colors: Optional[List[Tuple[int, int, int]]]=None)` | Set class names and corresponding colors for visualization. |
| `get_cached_font` | `get_cached_font(self, font_size: int)` | Get cached font for the specified size. |
| `contains_chinese` | `contains_chinese(text: str)` | Check if the text contains Chinese characters. |
| `draw_detections` | `draw_detections(self, image: np.ndarray, boxes: Union[np.ndarray, List], scores: Union[np.ndarray, List[float]], class_ids: Union[np.ndarray, List[int]], keypoints: Optional[Union[np.ndarray, List[np.ndarray]]]=None, mask_maps: Optional[np.ndarray]=None, mask_alpha: float=0.3, labels: Optional[List[str]]=None)` | Draw detections, including boxes, masks, keypoints, and skeletons. |
| `draw_all_boxes` | `draw_all_boxes(image: np.ndarray, rect_boxes: List[Union[np.ndarray, List[float]]], rect_colors: List[Tuple[int, int, int]], rotated_boxes: List[Union[np.ndarray, List[float]]], rotated_colors: List[Tuple[int, int, int]], thickness: int=2)` | Draw all bounding boxes on the image. |
| `draw_all_texts_pil` | `draw_all_texts_pil(self, image: np.ndarray, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draw all text annotations using PIL for better character (e.g., Chinese) support. |
| `draw_all_texts_cv2` | `draw_all_texts_cv2(self, image: np.ndarray, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draw all text annotations using OpenCV. Suitable for non-Chinese text. |
| `compute_text_position` | `compute_text_position(box: Union[List[float], np.ndarray], box_type: str)` | Compute the text start position for both rectangular and rotated boxes. For rotated boxes, find the top edge midpoint. |
| `draw_masks` | `draw_masks(self, image: np.ndarray, boxes: Union[np.ndarray, List], classes: np.ndarray, mask_alpha: float=0.3, mask_maps: Optional[np.ndarray]=None)` | Draw masks on the image. If mask_maps is provided, apply instance segmentation masks. Otherwise, draw filled boxes. |
| `draw_keypoints` | `draw_keypoints(self, image: np.ndarray, keypoints: np.ndarray, conf_threshold: float=0.0, circle_radius: int=3)` | Draw keypoints on the image. |
| `draw_skeleton` | `draw_skeleton(self, image: np.ndarray, keypoints: np.ndarray, conf_threshold: float=0.0, line_thickness: int=2)` | Draw skeleton on the image, connecting keypoints based on predefined skeleton structure. |
| `draw_classification` | `draw_classification(self, image: np.ndarray, prob: float, class_id: Optional[int]=None, class_name: Optional[str]=None, custom_label: Optional[str]=None, bg_alpha: float=0.5)` | Draw classification results on the image with a transparent background. |

#### `IMDetectorVisualPIL`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_params` | `set_params(self, cls_names: Optional[List[str]]=None, colors: Optional[List[Tuple[int, int, int]]]=None)` | Set class names and corresponding colors for visualization. |
| `get_cached_font` | `get_cached_font(self, font_size: int)` | Retrieves or generates a font object of a given size, using a cache for performance optimization. |
| `contains_chinese` | `contains_chinese(text: str)` | Checks if a given string contains any Chinese characters. |
| `draw_detections` | `draw_detections(self, pil_img: Image.Image, boxes: Union[np.ndarray, List], scores: Union[np.ndarray, List[float]], class_ids: Union[np.ndarray, List[int]], keypoints: Optional[Union[np.ndarray, List[np.ndarray]]]=None, mask_maps: Optional[np.ndarray]=None, mask_alpha: float=0.3, labels: Optional[List[str]]=None)` | Draw detection annotations on the image, including bounding boxes, masks, keypoints, and skeletons. |
| `draw_all_boxes` | `draw_all_boxes(self, pil_img: Image.Image, rect_boxes: List[Union[np.ndarray, List[float]]], rect_colors: List[Tuple[int, int, int]], rotated_boxes: List[Union[np.ndarray, List[float]]], rotated_colors: List[Tuple[int, int, int]], thickness: int=2)` | Draws all detection boxes, including both rectangular and rotated bounding boxes. |
| `draw_all_texts_pil` | `draw_all_texts_pil(self, pil_img: Image.Image, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draws text annotations using PIL, supporting multilingual text, including Chinese. |
| `compute_text_position` | `compute_text_position(box: Union[List[float], np.ndarray], box_type: str)` | Computes the starting position for text annotation based on the given bounding box. |
| `draw_masks` | `draw_masks(self, pil_img: Image.Image, boxes: Union[np.ndarray, List], classes: np.ndarray, mask_alpha: float=0.3, mask_maps: Optional[np.ndarray]=None)` | Draws instance masks on the image. If mask maps are not provided, fills the bounding box area instead. |
| `draw_keypoints` | `draw_keypoints(self, pil_img: Image.Image, keypoints: np.ndarray, conf_threshold: float=0.5, circle_radius: int=3)` | Draws keypoints on the image, represented as small circles. |
| `draw_skeleton` | `draw_skeleton(self, pil_img: Image.Image, keypoints: np.ndarray, conf_threshold: float=0.5, line_thickness: int=2)` | Draws the skeleton by connecting keypoints with lines, based on the specified skeleton structure. |
| `draw_classification` | `draw_classification(self, pil_img: Union[Image.Image, np.ndarray], prob: float, class_id: Optional[int]=None, class_name: Optional[str]=None, custom_label: Optional[str]=None, bg_alpha: float=0.5)` | Annotates the image with a classification result. Draws a semi-transparent text box with the class name, confidence score, or a custom label. |

<a id="vibefluxbasevisualconf"></a>
## `VibeFlux.base.VisualConf`

类别名称和颜色配置读取。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `load_predefined_colors` | `load_predefined_colors()` | Load predefined colors from the colors.yaml file. This function reads the colors.yaml file, which contains a list of RGB color values, and returns them as a list of lists. |
| `generate_random_color` | `generate_random_color()` | Generate a random RGB color. This function generates a random color represented as a list of three integers [R, G, B]. |
| `get_predefined_colors` | `get_predefined_colors(class_names: List[str]=None)` | Get the list of predefined colors, extended if necessary to match the number of class names. This function returns the list of predefined colors loaded from the colors.yaml file. If the number of predefined colors |
| `load_names` | `load_names()` | Load initial category names from the coco.yaml file. This function reads the coco.yaml file, which contains a dictionary of English category names |
| `get_names` | `get_names()` | Get the dictionary of initial category names. This function returns the dictionary of category names loaded from the coco.yaml file. |

<a id="vibefluxbasewidget"></a>
## `VibeFlux.base.Widget`

底层窗口、对话框和设置编辑器基类。

### 类

#### `IMainWindow`

FBaseWindow is a class derived from QMainWindow to provide custom methods and properties for handling graphical user interface (GUI) related operations in the application.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setUiStyle` | `setUiStyle(self, windowFlag=False, transBackFlag=False)` | Sets UI styles and widget states based on the provided flags. |
| `styleSheet` | `styleSheet(self, user=None)` | - |
| `moveToCenter` | `moveToCenter(self)` | Moves the current window to the center of the screen. |
| `mousePressEvent` | `mousePressEvent(self, event)` | Event handler for mouse press event. |
| `mouseMoveEvent` | `mouseMoveEvent(self, QMouseEvent)` | Event handler for mouse move event. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, QMouseEvent)` | Event handler for mouse release event. |

#### `IMDialog`

A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setSlots` | `setSlots(self)` | Method to define slots for the Login dialog. The actual implementation needs to be provided. |
| `set_tab_order` | `set_tab_order(self, *widgets)` | Sets the tab order for the given widgets. |
| `setUiStyle` | `setUiStyle(self, windowFlag=False, transBackFlag=False)` | Sets the user interface style and widget states of the dialog. |
| `mousePressEvent` | `mousePressEvent(self, event)` | Overriding the mousePressEvent for custom behavior. |
| `mouseMoveEvent` | `mouseMoveEvent(self, QMouseEvent)` | Overriding the mouseMoveEvent for custom behavior. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, QMouseEvent)` | Overriding the mouseReleaseEvent for custom behavior. |
| `styleSheet` | `styleSheet(self, user=None)` | - |

#### `IMSettingsDialog`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load_yaml` | `load_yaml(self, yaml_path: str)` | Load YAML file using ruamel.yaml while preserving comments, order, and case. |
| `create_control_group` | `create_control_group(self, control_name: str, control_info: Dict[str, Any])` | Create a QGroupBox for each control based on YAML configuration, dynamically generating "info" display (read-only), "enabled" checkbox, |
| `on_browse_file` | `on_browse_file(self)` | Unified slot function: Finds the corresponding lineEdit based on sender() and updates its text with the selected file path. Validates that the selected |
| `save_and_close` | `save_and_close(self)` | Write the edited information back to the YAML file (preserving comments, order, and uppercase True/False), then close the dialog. |

#### `IMConfigDialog`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load_yaml` | `load_yaml(self)` | Load the YAML configuration file. |
| `init_ui` | `init_ui(self)` | Initialize the user interface by creating widgets based on YAML content. |
| `create_widget` | `create_widget(self, section: str, key: str, value: Any)` | Create appropriate widget based on the value type and key. |
| `browse_file_or_dir` | `browse_file_or_dir(self)` | Open a file or directory dialog based on the button's associated key. |
| `save_config` | `save_config(self)` | Save the modified configuration back to the YAML file. |

<a id="vibefluxconfigqfconfig"></a>
## `VibeFlux.config.QfConfig`

全局运行配置。

### 类

#### `QF_Config`

Configuration Manager for VibeFlux. This class provides methods to manage the configuration settings for the VibeFlux application. It allows

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_verbose` | `set_verbose(cls, mode=True)` | Set the verbosity of the VibeFlux package. |
| `is_verbose` | `is_verbose(cls)` | Check if the VibeFlux package is in verbose mode. |
| `save_config` | `save_config(cls, file_path)` | Save the current configuration to a file. |
| `load_config` | `load_config(cls, file_path)` | Load configuration from a file. |
| `reset_config` | `reset_config(cls)` | Reset configuration to default values. |

<a id="vibefluxconfigvisualconf"></a>
## `VibeFlux.config.VisualConf`

可视化配置读取。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `load_predefined_colors` | `load_predefined_colors()` | Load predefined colors from the colors.yaml file. This function reads the colors.yaml file, which contains a list of RGB color values, and returns them as a list of lists. |
| `generate_random_color` | `generate_random_color()` | Generate a random RGB color. This function generates a random color represented as a list of three integers [R, G, B]. |
| `get_predefined_colors` | `get_predefined_colors(class_names: List[str]=None)` | Get the list of predefined colors, extended if necessary to match the number of class names. This function returns the list of predefined colors loaded from the colors.yaml file. If the number of predefined colors |
| `load_names` | `load_names()` | Load initial category names from the coco.yaml file. This function reads the coco.yaml file, which contains a dictionary of English category names |
| `get_names` | `get_names()` | Get the dictionary of initial category names. This function returns the dictionary of category names loaded from the coco.yaml file. |

<a id="vibefluxexamplesllmusage"></a>
## `VibeFlux.examples.llm_usage`

公开模块。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `main` | `main()` | Run text, multi-turn, image, and file-assisted examples. |

<a id="vibefluxhandlershandler"></a>
## `VibeFlux.handlers.Handler`

相机、视频、图片和图片文件夹处理器。

### 类

#### `MediaHandler`

The MediaHandler class is responsible for handling media feeds, such as video files or live camera streams. It inherits from IMediaSignals and thus has access to a range of signals for different media states and events. The class supports frame processing, where each frame captured from the media can be processed using

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `addFrameProcessor` | `addFrameProcessor(self, func)` | Adds a frame processing function to the list. This function will be applied to each frame of the media. |
| `removeFrameProcessor` | `removeFrameProcessor(self, func)` | Removes a frame processing function from the list. |
| `getMediaInfo` | `getMediaInfo(self)` | Returns information about the current media feed, such as resolution, fps, and total frames. |
| `setFps` | `setFps(self, fps)` | Sets the frames per second for the media feed. Adjusts the timer interval accordingly. |
| `isActive` | `isActive(self)` | Checks if the media feed is currently active (playing). |
| `startMedia` | `startMedia(self)` | Starts the media feed. Opens the media source and begins reading frames. Emits signals on status changes. |
| `stopMedia` | `stopMedia(self)` | Stops the media feed. Releases the media source and stops reading frames. Emits a signal indicating closure. |
| `setDevice` | `setDevice(self, device)` | Sets the media source device. |

#### `ImageHandler`

ImageHandler is responsible for managing and processing image files. It provides functionalities to process images individually or in batches if provided with a directory path. The class supports custom image processing functionalities, where each image can be processed using user-defined functions. Signals are emitted to indicate

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `addFrameProcessor` | `addFrameProcessor(self, func)` | Adds a function to the list of image processors. Each processor is applied sequentially to the images. |
| `removeFrameProcessor` | `removeFrameProcessor(self, func)` | Removes a function from the list of processors that are applied to each image. |
| `setPath` | `setPath(self, path)` | Sets the path of the image or directory to be processed. |
| `startProcess` | `startProcess(self)` | Starts the image processing tasks. If the path is a file, a single image will be processed. If the path is a directory, all the images in the directory will be processed. Emits the 'stopOtherActivities' signal before |
| `stopProcess` | `stopProcess(self)` | Stops the ongoing image processing tasks. Emits an 'imageClosed' signal after processing is stopped. |
| `isActive` | `isActive(self)` | Checks if the ImageHandler is currently processing an image. |
| `getFileName` | `getFileName(self)` | Gets the name of the current file being processed. |

<a id="vibefluxllmsclient"></a>
## `VibeFlux.llms.Client`

OpenAI-compatible LLM 客户端。

### 类

#### `LLMResponse`

Normalized LLM response object. Args:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `to_dict` | `to_dict(self)` | Convert the response to a dictionary. |

#### `LLMAPIError`

Error raised when a provider API call fails.

#### `LLMClient`

Unified LLM client for text, vision, file-assisted chat, streaming, and image generation.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `configure` | `configure(self, provider: Optional[str]=None, model: Optional[str]=None, api_key: Optional[str]=None, base_url: Optional[str]=None, save: bool=True)` | Update active provider, model, API key, or base URL. |
| `set_api_key` | `set_api_key(self, api_key: str, provider: Optional[str]=None, save: bool=True)` | Set an API key for the current or given provider. |
| `add_custom_model` | `add_custom_model(self, provider: str, name: str, api_model: Optional[str]=None, capabilities: Optional[Iterable[str]]=None, model_type: str='chat', description: str='Custom model', save: bool=True)` | Add a custom model to both runtime registry and api_keys.json. |
| `list_models` | `list_models(self, provider: Optional[str]=None, capability: Optional[str]=None, model_type: Optional[str]=None)` | List registered models with optional filters. |
| `list_providers` | `list_providers(self)` | List registered providers. |
| `refresh_models` | `refresh_models(self, provider: Optional[str]=None, api_key: Optional[str]=None, base_url: Optional[str]=None, endpoint: str='/models', save: bool=True, overwrite: bool=False)` | Refresh provider model entries through the OpenAI-compatible model list API. |
| `resolve_model` | `resolve_model(self, model: Optional[str]=None, provider: Optional[str]=None)` | Resolve a model. Unknown model names are treated as custom names under the selected provider. |
| `resolve_provider` | `resolve_provider(self, provider: Optional[str]=None, model_info: Optional[ModelInfo]=None)` | Resolve a provider using explicit provider, model provider, or active provider. |
| `chat` | `chat(self, messages: Optional[Union[str, Dict[str, Any], Sequence[Dict[str, Any]]]]=None, prompt: Optional[str]=None, system: Optional[str]=None, template: Optional[str]=None, extra_context: Optional[str]=None, images: Optional[Union[str, Sequence[str]]]=None, image_urls: Optional[Union[str, Sequence[str]]]=None, files: Optional[Union[str, Sequence[str]]]=None, provider: Optional[str]=None, model: Optional[str]=None, stream: bool=False, temperature: Optional[float]=None, max_tokens: Optional[int]=None, response_format: Optional[Union[str, Dict[str, Any]]]=None, thinking: Optional[Union[bool, str, Dict[str, Any]]]=None, return_reasoning: bool=True, reasoning_effort: Optional[str]=None, binary_files_as_base64: bool=False, extra_body: Optional[Dict[str, Any]]=None, **kwargs: Any)` | Call a chat completion model. |
| `single_chat` | `single_chat(self, prompt: str, **kwargs: Any)` | Convenience method for a single-turn chat call. |
| `reset_history` | `reset_history(self, system: Optional[str]=None)` | Clear conversation history and optionally keep a system prompt. |
| `get_history` | `get_history(self)` | Return a copy of the current conversation history. |
| `set_history` | `set_history(self, messages: Sequence[Dict[str, Any]])` | Replace the current conversation history. |
| `send` | `send(self, prompt: str, images: Optional[Union[str, Sequence[str]]]=None, image_urls: Optional[Union[str, Sequence[str]]]=None, files: Optional[Union[str, Sequence[str]]]=None, keep_history: bool=True, stream: bool=False, **kwargs: Any)` | Send one user turn in a multi-round conversation. |
| `ask_image` | `ask_image(self, image: Union[str, Sequence[str]], prompt: str='Please analyze this image.', task: str='image_understanding', **kwargs: Any)` | Analyze one or more images with a vision-capable model. |
| `analyze_file` | `analyze_file(self, file_path: Union[str, Sequence[str]], prompt: str='Please analyze this file.', task: str='file_summary', **kwargs: Any)` | Analyze one or more files by inserting extracted text into the message. |
| `generate_image` | `generate_image(self, prompt: str, images: Optional[Union[str, Sequence[str]]]=None, image_urls: Optional[Union[str, Sequence[str]]]=None, provider: Optional[str]=None, model: Optional[str]=None, size: Optional[str]=None, n: int=1, extra_body: Optional[Dict[str, Any]]=None, **kwargs: Any)` | Call an OpenAI-compatible image generation endpoint. |

<a id="vibefluxllmsconfig"></a>
## `VibeFlux.llms.Config`

API Key 和 LLM 配置管理。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `default_config_path` | `default_config_path(filename: str='api_keys.json')` | Return the default runtime configuration path in the current working directory. |
| `package_example_config_path` | `package_example_config_path()` | Return the path of the packaged api_keys example file. |

### 类

#### `APIKeyManager`

Manage the api_keys.json file used by LLM clients.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load` | `load(self)` | Load api_keys.json and merge it with default values. |
| `save` | `save(self)` | Save api_keys.json to disk. |
| `ensure_provider` | `ensure_provider(self, provider: str)` | Ensure a provider block exists in api_keys.json. |
| `set_api_key` | `set_api_key(self, provider: str, api_key: str, save: bool=True)` | Store an API key for a provider. |
| `get_api_key` | `get_api_key(self, provider: str, env_fallback: bool=True)` | Get the API key for a provider, optionally falling back to environment variables. |
| `set_base_url` | `set_base_url(self, provider: str, base_url: str, save: bool=True)` | Store the base URL for a provider. |
| `get_base_url` | `get_base_url(self, provider: str)` | Get a provider base URL from api_keys.json or presets. |
| `set_active` | `set_active(self, provider: Optional[str]=None, model: Optional[str]=None, save: bool=True)` | Set the active provider and model. |
| `get_active_provider` | `get_active_provider(self)` | Return the active provider key. |
| `get_active_model` | `get_active_model(self)` | Return the active model name. |
| `get_runtime` | `get_runtime(self, key: Optional[str]=None, default: Any=None)` | Get runtime options from the configuration. |
| `set_runtime` | `set_runtime(self, key: str, value: Any, save: bool=True)` | Store a runtime option such as timeout or temperature. |
| `add_custom_model` | `add_custom_model(self, provider: str, name: str, api_model: Optional[str]=None, capabilities: Optional[Iterable[str]]=None, model_type: str='chat', description: str='Custom model', save: bool=True)` | Add a custom model definition to api_keys.json. |
| `upsert_custom_models` | `upsert_custom_models(self, models: Iterable[Dict[str, Any]], save: bool=True)` | Add or replace custom model definitions in api_keys.json. |
| `get_custom_models` | `get_custom_models(self)` | Return custom model definitions from api_keys.json. |
| `load_custom_models_to_registry` | `load_custom_models_to_registry(self, registry: Optional[ModelRegistry]=None)` | Load custom models from api_keys.json into a registry. |
| `mask_api_key` | `mask_api_key(self, api_key: str)` | Return a masked API key suitable for display. |
| `to_safe_dict` | `to_safe_dict(self)` | Export configuration with masked API keys. |
| `create_example_file` | `create_example_file(self, output_path: Optional[str]=None)` | Create an example API key file and return its path. |

<a id="vibefluxllmsmessage"></a>
## `VibeFlux.llms.Message`

文本、图片、文件消息构造工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `guess_mime_type` | `guess_mime_type(path_or_url: str, default: str='application/octet-stream')` | Guess the MIME type of a local file path or URL. |
| `is_image_file` | `is_image_file(path_or_url: str)` | Check whether a file path or URL looks like an image. |
| `file_to_base64` | `file_to_base64(path: str)` | Read a local file and return its base64 string. |
| `file_to_data_url` | `file_to_data_url(path: str, mime_type: Optional[str]=None)` | Convert a local file to a data URL. |
| `image_to_part` | `image_to_part(path_or_url: str)` | Convert a local image path or remote image URL to an OpenAI-compatible image_url part. |
| `read_text_file` | `read_text_file(path: str, max_chars: int=20000, encodings: Optional[Iterable[str]]=None)` | Read a text file with several common encodings. |
| `read_pdf_text` | `read_pdf_text(path: str, max_chars: int=20000)` | Extract text from a PDF file if pypdf is installed. |
| `file_to_text_part` | `file_to_text_part(path: str, max_chars: int=20000, binary_files_as_base64: bool=False, max_binary_bytes: int=1024 * 256)` | Convert a local file into a text message part. |
| `build_user_content` | `build_user_content(text: Optional[str]=None, images: Optional[Union[str, Sequence[str]]]=None, image_urls: Optional[Union[str, Sequence[str]]]=None, files: Optional[Union[str, Sequence[str]]]=None, max_file_chars: int=20000, binary_files_as_base64: bool=False)` | Build a user message content value from text, images, URLs, and files. |
| `build_message` | `build_message(role: str, text: Optional[str]=None, images: Optional[Union[str, Sequence[str]]]=None, image_urls: Optional[Union[str, Sequence[str]]]=None, files: Optional[Union[str, Sequence[str]]]=None, max_file_chars: int=20000, binary_files_as_base64: bool=False)` | Build one OpenAI-compatible message dictionary. |
| `normalize_messages` | `normalize_messages(messages: Optional[Union[str, Dict[str, Any], Sequence[Dict[str, Any]]]])` | Normalize strings, dictionaries, or message lists into a message list. |
| `append_system_message` | `append_system_message(messages: List[Dict[str, Any]], system: Optional[str])` | Prepend a system message if one is provided. |

<a id="vibefluxllmsqtbridge"></a>
## `VibeFlux.llms.QtBridge`

PySide6 后台线程 LLM 调用。

### 类

#### `LLMWorker`

Worker object for one LLM request.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `run` | `run(self)` | Execute the request and emit Qt signals. |

#### `LLMQtRunner`

Convenience QObject that starts LLM calls in a managed QThread.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `configure` | `configure(self, **kwargs: Any)` | Forward configuration to the underlying LLMClient. |
| `run_request` | `run_request(self, request_kwargs: Dict[str, Any])` | Run a chat request in a new QThread. |
| `ask` | `ask(self, prompt: str, stream: bool=False, **kwargs: Any)` | Run a prompt request in a new QThread. |

<a id="vibefluxllmsregistry"></a>
## `VibeFlux.llms.Registry`

Provider 和 Model 注册表。

### 类

#### `ProviderInfo`

Describes one LLM provider. Args:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `to_dict` | `to_dict(self)` | Convert the provider object to a dictionary. |

#### `ModelInfo`

Describes one model entry. Args:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `supports` | `supports(self, capability: str)` | Check whether the model supports a capability. |
| `to_dict` | `to_dict(self)` | Convert the model object to a JSON-serializable dictionary. |
| `from_dict` | `from_dict(cls, data: Dict[str, Any])` | Build a ModelInfo from a dictionary loaded from JSON. |

#### `ModelRegistry`

Registry that stores built-in and custom provider/model definitions.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `get_provider` | `get_provider(self, provider: str)` | Return a provider by key. |
| `add_provider` | `add_provider(self, provider: ProviderInfo)` | Add or replace a provider. |
| `list_providers` | `list_providers(self)` | Return all registered providers. |
| `get_model` | `get_model(self, model: str)` | Return a model by name, API model ID, or alias. |
| `add_model` | `add_model(self, model: ModelInfo)` | Add or replace a model entry. |
| `add_custom_model` | `add_custom_model(self, provider: str, name: str, api_model: Optional[str]=None, capabilities: Optional[Iterable[str]]=None, model_type: str='chat', description: str='Custom model', aliases: Optional[Iterable[str]]=None, extra: Optional[Dict[str, Any]]=None)` | Add a custom model to the registry. |
| `remove_model` | `remove_model(self, model: str)` | Remove a model from the registry. |
| `list_models` | `list_models(self, provider: Optional[str]=None, capability: Optional[str]=None, model_type: Optional[str]=None)` | List models with optional filters. |
| `load_custom_models` | `load_custom_models(self, models: Iterable[Dict[str, Any]])` | Load custom model definitions from a list of dictionaries. |
| `export_custom_models` | `export_custom_models(self, preset_names: Optional[Iterable[str]]=None)` | Export model entries that are not part of the preset registry. |
| `to_dict` | `to_dict(self)` | Export the registry to a dictionary. |

<a id="vibefluxllmstemplates"></a>
## `VibeFlux.llms.Templates`

结构化输出模板。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `get_template` | `get_template(name: str)` | Return a preset task template by name. |
| `list_templates` | `list_templates()` | Return all preset templates. |
| `template_names` | `template_names()` | Return all preset template names. |
| `render_template_prompt` | `render_template_prompt(name: str, user_input: Optional[str]=None, extra_context: Optional[str]=None)` | Render the user prompt of a preset template. |

### 类

#### `OutputTemplate`

Standard task template for LLM output formatting. Args:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `to_dict` | `to_dict(self)` | Convert the template to a dictionary. |
| `render_user_prompt` | `render_user_prompt(self, user_input: Optional[str]=None, extra_context: Optional[str]=None)` | Render a user prompt with the schema and optional context. |

<a id="vibefluxllmsupdater"></a>
## `VibeFlux.llms.Updater`

从 provider /models 接口刷新模型列表。

### 类

#### `ModelPresetUpdateResult`

Result returned after refreshing model presets from a provider endpoint.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `added_names` | `added_names(self)` | Return names of models added to the registry. |

#### `ModelPresetUpdater`

Refresh provider model entries from OpenAI-compatible model list APIs.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `refresh_provider` | `refresh_provider(self, provider: Optional[str]=None, api_key: Optional[str]=None, base_url: Optional[str]=None, endpoint: str='/models', save: bool=True, overwrite: bool=False)` | Fetch and merge model entries for one provider. |
| `refresh_all` | `refresh_all(self, providers: Optional[Iterable[str]]=None, save: bool=True, overwrite: bool=False)` | Refresh all configured providers. Providers without an API key return an error result. |
| `fetch_provider_models` | `fetch_provider_models(self, provider: Optional[str]=None, api_key: Optional[str]=None, base_url: Optional[str]=None, endpoint: str='/models')` | Call a provider model list API and return normalized ModelInfo entries. |
| `parse_provider_models` | `parse_provider_models(self, provider: str, payload: Any)` | Parse a provider model list response into ModelInfo entries. |

<a id="vibefluxmanagerdetmanager"></a>
## `VibeFlux.manager.DetManager`

检测结果 SQLite 管理。

### 类

#### `DetectionDB`

SQLite database manager for storing object detection results. Supports asynchronous insertion operations to accommodate high-frame-rate video streams.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `create_table` | `create_table(self)` | Creates the table for storing detection results if it does not already exist. |
| `insert` | `insert(self, class_name: str, class_id: int, confidence: float, bbox: tuple[int, int, int, int], image_path: str)` | Adds a single detection result to the insertion queue. |
| `insert_bulk` | `insert_bulk(self, detections: list[dict] | list[tuple])` | Adds multiple detection results to the insertion queue in bulk. |
| `close` | `close(self)` | Stops the background thread and closes the database connection. |

<a id="vibefluxmanagerusermanager"></a>
## `VibeFlux.manager.UserManager`

用户注册、登录和头像管理。

### 类

#### `UserManager`

A class for managing a database of users. This class provides methods for registering users, getting user data,

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `hash_password` | `hash_password(password: str)` | Hashes a password using SHA-256. |
| `verify_avatar` | `verify_avatar(avatar_path)` | Check if an avatar file is valid. |
| `register` | `register(self, username, password, avatar)` | Registers a new user. |
| `get_user` | `get_user(self, username)` | Retrieves data for a user. |
| `change_password` | `change_password(self, username, new_password)` | Changes a user's password. |
| `change_avatar` | `change_avatar(self, username, password, new_avatar)` | Changes a user's avatar. |
| `verify_login` | `verify_login(self, username, password)` | Verify a user's login credentials. |
| `get_avatar` | `get_avatar(self, username)` | Get the avatar of a user. |
| `delete_user` | `delete_user(self, username, password)` | Delete a user account. |

<a id="vibefluxmodelsabstractmodel"></a>
## `VibeFlux.models.AbstractModel`

检测模型抽象接口。

### 类

#### `Detector`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load_model` | `load_model(self, model_path)` | Abstract method to load a model. |
| `preprocess` | `preprocess(self, img)` | Abstract method for image preprocessing. |
| `predict` | `predict(self, img)` | Abstract method to make a prediction on the input image. |
| `postprocess` | `postprocess(self, prediction)` | Abstract method for postprocessing the prediction result. |

<a id="vibefluxmodelsheatmap"></a>
## `VibeFlux.models.Heatmap`

基于 PyTorch hook 的热力图生成。

### 类

#### `HeatmapGenerator`

Class for generating heatmaps from a specific layer of a model. Attributes:

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `register_hook` | `register_hook(self, reg_layer)` | Registers a forward hook on the specified layer of the model. |
| `get_heatmap` | `get_heatmap(self, img)` | Generates a heatmap. |

<a id="vibefluxpathfmanager"></a>
## `VibeFlux.path.FManager`

文件复制、删除、查找、文本替换工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `log` | `log(message)` | - |
| `copy_file_folder` | `copy_file_folder(src, dst, create_dst_dir=True, overwrite=False)` | Copies a file or folder to a specified path. Args: |
| `delete_file` | `delete_file(file_path)` | Deletes a file at a specified path. Args: |
| `delete_files_pattern` | `delete_files_pattern(directory, pattern)` | Deletes all files in a specified directory that match a given regular expression pattern and logs the names of deleted files. Args: |
| `get_subfolders` | `get_subfolders(directory)` | Gets the absolute paths and names of all subfolders within a given directory. Args: |
| `get_subfiles` | `get_subfiles(directory)` | Gets the absolute paths and names of all subfiles within a specified directory. Args: |
| `count_images` | `count_images(folder, img_extensions=None)` | Counts the number of image files in a specified folder. Args: |
| `modify_content` | `modify_content(file_path, old_string, new_string)` | Modifies specific strings within a given file. Args: |
| `modify_multi_contents` | `modify_multi_contents(file_path, old_strings, new_strings)` | Modifies multiple specific strings within a given file and logs the details of replacements. Args: |
| `modify_multi_patterns` | `modify_multi_patterns(file_path, old_patterns, new_strings)` | Modifies multiple specific patterns within a given file, supporting multi-line patterns, and logs the details of replacements. Args: |
| `extract_text_pattern` | `extract_text_pattern(file_path, pattern)` | Extracts text matching a specific pattern using regular expressions from a file. Args: |
| `contains_text` | `contains_text(file_path, pattern)` | Checks if the file contains text that matches a specific regular expression pattern. Args: |
| `copy_subfiles_filter` | `copy_subfiles_filter(src_folder, dst_folder, exclude_files=None, include_files=None)` | Copies files within a folder to another folder, with options to exclude or include only specific files. Args: |
| `copy_subfolders_filter` | `copy_subfolders_filter(src_folder, dst_folder, exclude_folders=None, include_folders=None)` | Copies subfolders within a parent folder to another folder, with options to exclude or include only specific subfolders. Args: |

<a id="vibefluxpathpath"></a>
## `VibeFlux.path.Path`

路径拼接、列举、移动、复制工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `get_abs_path` | `get_abs_path(base_path: Optional[str]=None, *relative_paths: str)` | Appends an absolute path prefix to a set of relative paths. Args: |
| `abs_path` | `abs_path(relative_path: str, base_path: Optional[str]=None, path_type: Optional[str]='current')` | Appends an absolute path prefix to a single relative path. Args: |
| `get_files` | `get_files(prefix: str, paths: List[str])` | Get all files using a specified prefix and list of paths. Args: |
| `list_all_files` | `list_all_files(paths: List[str])` | List all files from multiple directories. Args: |
| `list_files` | `list_files(path: str)` | List all files in a specified directory. Args: |
| `path_exists` | `path_exists(path: str)` | Checks if the specified path exists. Args: |
| `create_dir` | `create_dir(path: str, exist_ok: bool=True)` | Creates a new directory at the specified path. Args: |
| `list_dir` | `list_dir(path: str)` | Lists files and directories in the given path. Args: |
| `get_extension` | `get_extension(filename: str)` | Returns the file extension of the specified file. Args: |
| `join_paths` | `join_paths(*paths: str)` | Joins multiple paths into a single path, normalizes it, and ensures it is compatible with the operating system. Args: |
| `to_abs_path` | `to_abs_path(relative_path: str)` | Converts a relative path to an absolute path. Args: |
| `get_script_dir` | `get_script_dir()` | Get the directory of the current executing script. Returns: |
| `get_script_path` | `get_script_path()` | Get the absolute path of the current executing script. Returns: |
| `get_filename` | `get_filename(path: str)` | Returns the filename without its extension from the given path. Args: |
| `get_size` | `get_size(path: str)` | Returns the size of the file or directory at the specified path. Args: |
| `copy_file` | `copy_file(src: str, dest: str)` | Copies a file from the source to the destination. Args: |
| `move_or_rename` | `move_or_rename(src: str, dest: str)` | Moves or renames a file or directory. Args: |

<a id="vibefluxrecsystem"></a>
## `VibeFlux.RecSystem`

Qt 资源系统入口，通常由包内部导入。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `qInitResources` | `qInitResources()` | - |
| `qCleanupResources` | `qCleanupResources()` | - |

<a id="vibefluxstylesformers"></a>
## `VibeFlux.styles.Formers`

YAML UI 设置应用函数。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `applyText` | `applyText(widget, text)` | Apply text settings to a widget. Args: |
| `applyIcon` | `applyIcon(widget, icon_path)` | Apply icon settings to a widget. Args: |
| `applyBackground` | `applyBackground(widget, background_path)` | Apply background settings to a widget. Args: |
| `loadYamlSettings` | `loadYamlSettings(window, yaml_file, base_path='./')` | Load settings for a QWidget from a YAML file and apply them to the specified window. Args: |
| `apply_WindowIcon` | `apply_WindowIcon(window, settings, base_path)` | Apply window icon setting to the main window. Args: |
| `applyWindowIcon` | `applyWindowIcon(window, icon_path)` | Apply window icon settings to a window. Args: |
| `applyQssStyles` | `applyQssStyles(window, qss_data)` | Apply QSS styles to a QMainWindow. Args: |
| `applyWidgetSettings` | `applyWidgetSettings(widget, widget_name, settings, base_path)` | Apply individual settings to a widget. Args: |

<a id="vibefluxstylesstyles"></a>
## `VibeFlux.styles.Styles`

QSS 主题和样式应用。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `loadQssStyles` | `loadQssStyles(window, qss_file, base_path='./')` | Load QSS styles for a QMainWindow. :param window: QMainWindow instance to apply the styles to. |

### 类

#### `BaseStyle`

This class serves as a style decorator to apply custom styles to Qt widgets. It supports using either predefined style names or custom QSS files.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_named_style` | `set_named_style(self, widget, style_name, encoding='utf-8')` | Apply a predefined style to a given widget. |
| `set_style_text` | `set_style_text(self, widget, style_text)` | Apply a given style text to a widget. |

<a id="vibefluxutilscamerautils"></a>
## `VibeFlux.utils.CameraUtils`

摄像头扫描、分辨率和属性工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `find_cameras` | `find_cameras(max_devices: int=3)` | Detects and returns a list of available camera device indices. Args: |
| `get_cam_resolutions` | `get_cam_resolutions(index: int)` | Retrieves a list of resolutions supported by the specified camera. Args: |
| `set_cam_resolution` | `set_cam_resolution(index: int, width: int, height: int)` | Sets the resolution of the specified camera. Args: |
| `is_cam_available` | `is_cam_available(index: int)` | Checks if a specific camera is available. Args: |
| `show_cam_feed` | `show_cam_feed(index: int)` | Displays the real-time feed of the specified camera. Args: |
| `get_cam_properties` | `get_cam_properties(index: int)` | Retrieves various properties of the specified camera. Args: |

<a id="vibefluxutilsdetvisual"></a>
## `VibeFlux.utils.DetVisual`

检测可视化公开包装类。

### 类

#### `DetectorVisual`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_params` | `set_params(self, cls_names: Optional[List[str]]=None, colors: Optional[List[Tuple[int, int, int]]]=None)` | Set class names and corresponding colors for visualization. |
| `get_cached_font` | `get_cached_font(self, font_size: int)` | Get cached font for the specified size. |
| `contains_chinese` | `contains_chinese(text: str)` | Check if the text contains Chinese characters. |
| `draw_detections` | `draw_detections(self, image: np.ndarray, boxes: Union[np.ndarray, List], scores: Union[np.ndarray, List[float]], class_ids: Union[np.ndarray, List[int]], keypoints: Optional[Union[np.ndarray, List[np.ndarray]]]=None, mask_maps: Optional[np.ndarray]=None, mask_alpha: float=0.3, labels: Optional[List[str]]=None)` | Draw detections, including boxes, masks, keypoints, and skeletons. |
| `draw_all_boxes` | `draw_all_boxes(image: np.ndarray, rect_boxes: List[Union[np.ndarray, List[float]]], rect_colors: List[Tuple[int, int, int]], rotated_boxes: List[Union[np.ndarray, List[float]]], rotated_colors: List[Tuple[int, int, int]], thickness: int=2)` | Draw all bounding boxes on the image. |
| `draw_all_texts_pil` | `draw_all_texts_pil(self, image: np.ndarray, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draw all text annotations using PIL for better character (e.g., Chinese) support. |
| `draw_all_texts_cv2` | `draw_all_texts_cv2(self, image: np.ndarray, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draw all text annotations using OpenCV. Suitable for non-Chinese text. |
| `compute_text_position` | `compute_text_position(box: Union[List[float], np.ndarray], box_type: str)` | Compute the text start position for both rectangular and rotated boxes. For rotated boxes, find the top edge midpoint. |
| `draw_masks` | `draw_masks(self, image: np.ndarray, boxes: Union[np.ndarray, List], classes: np.ndarray, mask_alpha: float=0.3, mask_maps: Optional[np.ndarray]=None)` | Draw masks on the image. If mask_maps is provided, apply instance segmentation masks. Otherwise, draw filled boxes. |
| `draw_keypoints` | `draw_keypoints(self, image: np.ndarray, keypoints: np.ndarray, conf_threshold: float=0.0, circle_radius: int=3)` | Draw keypoints on the image. |
| `draw_skeleton` | `draw_skeleton(self, image: np.ndarray, keypoints: np.ndarray, conf_threshold: float=0.0, line_thickness: int=2)` | Draw skeleton on the image, connecting keypoints based on predefined skeleton structure. |
| `draw_classification` | `draw_classification(self, image: np.ndarray, prob: float, class_id: Optional[int]=None, class_name: Optional[str]=None, custom_label: Optional[str]=None, bg_alpha: float=0.5)` | Draw classification results on the image with a transparent background. |

#### `DetectorVisualPIL`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_params` | `set_params(self, cls_names: Optional[List[str]]=None, colors: Optional[List[Tuple[int, int, int]]]=None)` | Set class names and corresponding colors for visualization. |
| `get_cached_font` | `get_cached_font(self, font_size: int)` | Retrieves or generates a font object of a given size, using a cache for performance optimization. |
| `contains_chinese` | `contains_chinese(text: str)` | Checks if a given string contains any Chinese characters. |
| `draw_detections` | `draw_detections(self, pil_img: Image.Image, boxes: Union[np.ndarray, List], scores: Union[np.ndarray, List[float]], class_ids: Union[np.ndarray, List[int]], keypoints: Optional[Union[np.ndarray, List[np.ndarray]]]=None, mask_maps: Optional[np.ndarray]=None, mask_alpha: float=0.3, labels: Optional[List[str]]=None)` | Draw detection annotations on the image, including bounding boxes, masks, keypoints, and skeletons. |
| `draw_all_boxes` | `draw_all_boxes(self, pil_img: Image.Image, rect_boxes: List[Union[np.ndarray, List[float]]], rect_colors: List[Tuple[int, int, int]], rotated_boxes: List[Union[np.ndarray, List[float]]], rotated_colors: List[Tuple[int, int, int]], thickness: int=2)` | Draws all detection boxes, including both rectangular and rotated bounding boxes. |
| `draw_all_texts_pil` | `draw_all_texts_pil(self, pil_img: Image.Image, text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]])` | Draws text annotations using PIL, supporting multilingual text, including Chinese. |
| `compute_text_position` | `compute_text_position(box: Union[List[float], np.ndarray], box_type: str)` | Computes the starting position for text annotation based on the given bounding box. |
| `draw_masks` | `draw_masks(self, pil_img: Image.Image, boxes: Union[np.ndarray, List], classes: np.ndarray, mask_alpha: float=0.3, mask_maps: Optional[np.ndarray]=None)` | Draws instance masks on the image. If mask maps are not provided, fills the bounding box area instead. |
| `draw_keypoints` | `draw_keypoints(self, pil_img: Image.Image, keypoints: np.ndarray, conf_threshold: float=0.5, circle_radius: int=3)` | Draws keypoints on the image, represented as small circles. |
| `draw_skeleton` | `draw_skeleton(self, pil_img: Image.Image, keypoints: np.ndarray, conf_threshold: float=0.5, line_thickness: int=2)` | Draws the skeleton by connecting keypoints with lines, based on the specified skeleton structure. |
| `draw_classification` | `draw_classification(self, pil_img: Union[Image.Image, np.ndarray], prob: float, class_id: Optional[int]=None, class_name: Optional[str]=None, custom_label: Optional[str]=None, bg_alpha: float=0.5)` | Annotates the image with a classification result. Draws a semi-transparent text box with the class name, confidence score, or a custom label. |

<a id="vibefluxutilsfileutils"></a>
## `VibeFlux.utils.FileUtils`

QSS 读取和 YAML 配置访问。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `readQssFile` | `readQssFile(qss_file_path, encoding='utf-8')` | Read and return the content of a QSS file using the specified encoding. Args: |

### 类

#### `QConfig`

A class for loading a YAML configuration file and extracting only the final (leaf) keys for direct access.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `get` | `get(self, key: str, default: Any=None)` | Returns the value for the specified key, or a default if key is not found. |
| `keys` | `keys(self)` | Lists the keys that have been extracted from the YAML file. |
| `as_dict` | `as_dict(self)` | Returns a shallow copy of the internal dictionary for direct manipulation. |

<a id="vibefluxutilsimageutils"></a>
## `VibeFlux.utils.ImageUtils`

图像读取、图表、检测框绘制工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `get_cls_color` | `get_cls_color(cls_name)` | Returns a list of color codes based on the class name. :param cls_name: Class name string. |
| `horizontal_bar` | `horizontal_bar(label_name, value, colors, width, height, color_text='#000000', alpha=0.8, margin=20)` | Creates a horizontal bar chart as an image. Args: |
| `vertical_bar` | `vertical_bar(label_name, value, colors, width, height, color_text='#000000', alpha=0.7, margin=20)` | Create a vertical bar chart as an image. :param label_name: The labels for each bar. |
| `verticalBar` | `verticalBar(label_name, value, colors, width, height, color_text='#000000', alpha=0.7, margin=20)` | Generate a vertical bar chart as a QPixmap. :param label_name: List of bar labels. |
| `cv_imread` | `cv_imread(file_path)` | Read an image file using cv2 in a way that also supports Unicode paths. :param file_path: The path to the image file. |
| `drawRectEdge` | `drawRectEdge(image, rect, color=None, alpha=0.2, addText=None, line_thickness=None)` | Draw a rectangle with annotated edges on an image. :param image: The image to draw on, as a numpy array. |
| `drawRectBox` | `drawRectBox(image, rect, color=None, alpha=0.25, addText=None, line_thickness=None)` | Draws a rectangular bounding box on an image. :param image: A numpy array representing the image to draw on. |
| `drawOrientedBox` | `drawOrientedBox(image, box, color=None, alpha=0.25, addText=None, line_thickness=None)` | Draws an oriented bounding box (OBB) on an image with optimized performance. Args: |

<a id="vibefluxutilspixmap"></a>
## `VibeFlux.utils.Pixmap`

OpenCV 图像到 QPixmap 的转换。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `cvImageToQtPixmap` | `cvImageToQtPixmap(cv_image)` | Converts an OpenCV image to a QPixmap. :param cv_image: The OpenCV image to be converted. |
| `scalePixmap` | `scalePixmap(pixmap, size, keepAspect)` | Scales a QPixmap to a specified size. :param pixmap: The QPixmap to be scaled. |

<a id="vibefluxutilssysinfo"></a>
## `VibeFlux.utils.Sysinfo`

系统和运行环境信息。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `get_os_pretty` | `get_os_pretty()` | Return a human-friendly operating system string. On Windows, this function tries to read OS marketing name and version |
| `get_runtime_info` | `get_runtime_info()` | Collect runtime environment information for logging/diagnostics. This function returns a dictionary with basic system information and |
| `print_banner` | `print_banner(pkg_name: str, version: str, verbose: bool=True)` | Print a standardized one-time banner for VibeFlux. The banner format is: |

<a id="vibefluxwidgetsbaseframe"></a>
## `VibeFlux.widgets.BaseFrame`

窗口基类、登录框、动画、表格和图像显示工具。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `verbose_class` | `verbose_class(cls)` | Class decorator for VibeFlux to optionally print a single runtime banner. This decorator is intended to be applied to classes inside the VibeFlux package. |
| `findContainLayout` | `findContainLayout(widget, layout=None)` | Find the layout containing the given widget. :param widget: The widget for which the containing layout is to be found. |
| `replaceWidget` | `replaceWidget(original, DerivedClass, properties=['minimumSize', 'maximumSize', 'objectName', 'styleSheet'])` | Replace a widget with an instance of a derived class, preserving certain properties. :param original: The original QWidget instance to be replaced. |
| `moveCenter` | `moveCenter(main_window, msg_box)` | Move a message box to the center of the main window. :param main_window: The main window of the application. |
| `addTableItem` | `addTableItem(tableWidget, row, column, text, alignment=Qt.AlignCenter)` | Add a new item to a QTableWidget. :param tableWidget: The QTableWidget to which the new item is to be added. |
| `updateTable` | `updateTable(table_widget, row_number, *row_data)` | Update a specific row in a QTableWidget with new data. :param table_widget: The QTableWidget to be updated. |
| `getFramePath` | `getFramePath(file_path: str, cur_frames: int, imageHandler: ImageHandler=None, snapshots_dir: str='./snapshots')` | Generates or returns a unified file path for the current frame based on the file path and frame index. Args: |
| `fadeIn` | `fadeIn(widget, duration, reverse=False)` | Create a fade-in effect on a QWidget. :param widget: The QWidget to apply the fade-in effect to. |
| `zoomIn` | `zoomIn(widget, duration, startSize, endSize, reverse=False)` | Create a zoom-in effect on a QWidget. :param widget: The QWidget to apply the zoom-in effect to. |
| `dispImage` | `dispImage(label, image, keepAspect=True)` | Displays an image in a QLabel. :param label: The QLabel name. :param image: The image to be displayed. |

### 类

#### `FBaseWindow`

FBaseWindow is a class derived from QMainWindow to provide custom methods and properties for handling graphical user interface (GUI) related operations in the application.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `init_login_info` | `init_login_info(self, *args, **kwargs)` | - |
| `init_reg_info` | `init_reg_info(self, *args, **kwargs)` | - |
| `get_cls_color` | `get_cls_color(self, cls_name)` | Returns a list of color codes based on the class name. |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |
| `set_buttons_enabled` | `set_buttons_enabled(self, enabled)` | Enable or disable all QToolButtons in the current window. |
| `loadYamlSettings` | `loadYamlSettings(self, yaml_file, base_path='./')` | Load settings for a QWidget from a YAML file and apply them to the specified window. |
| `showTime` | `showTime(self)` | Method to show the window. The actual implementation needs to be provided. |
| `showEvent` | `showEvent(self, event)` | Event handler for when the window is shown. |
| `setUiStyle` | `setUiStyle(self, windowFlag=False, transBackFlag=False)` | Sets UI styles and widget states based on the provided flags. |
| `clearUI` | `clearUI(self)` | Clears the UI and reloads settings from a YAML file. |
| `setConfig` | `setConfig(self)` | Method to set the configuration of the application. The actual implementation needs to be provided. |
| `dispImage` | `dispImage(label_display, image, keepAspect=False)` | Displays an image in a QLabel. |
| `setupWidget` | `setupWidget(widget, properties)` | Set up a QWidget with given properties. |
| `moveToCenter` | `moveToCenter(self)` | Moves the current window to the center of the screen. |
| `mousePressEvent` | `mousePressEvent(self, event)` | Event handler for mouse press event. |
| `mouseMoveEvent` | `mouseMoveEvent(self, QMouseEvent)` | Event handler for mouse move event. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, QMouseEvent)` | Event handler for mouse release event. |
| `plot_vertical_bar` | `plot_vertical_bar(label, label_name, value, colors=None, color_text='#FFFFFF', alpha=0.7, width=None, height=None, margin=20)` | Plots a vertical bar on a QLabel. |
| `plot_horizontal_bar` | `plot_horizontal_bar(label, label_name, value, colors=None, color_text='#FFFFFF', alpha=0.8, width=None, height=None, margin=20)` | Plots a horizontal bar on a QLabel. |
| `plot_verticalBar` | `plot_verticalBar(label, label_name, value, colors=None, color_text='#FFFFFF', alpha=0.7, width=None, height=None, margin=20)` | Plots a vertical bar on a QLabel. Seems similar to the 'plot_vertical_bar' method. |

#### `FLoginDialog`

A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setSlots` | `setSlots(self)` | Method to define slots for the Login dialog. The actual implementation needs to be provided. |
| `setUiStyle` | `setUiStyle(self, windowFlag=False, transBackFlag=False)` | Sets the user interface style and widget states of the dialog. |
| `generate_random_code` | `generate_random_code(self, widget=None, width=170, height=80, length=4, characters=None)` | Generates a random verification code and returns an image of the code and the code itself as a string. |
| `set_tab_order` | `set_tab_order(self, *widgets)` | Sets the tab order for the given widgets. |
| `show_dialog` | `show_dialog(self)` | Displays the dialog. |
| `minButton` | `minButton(self)` | Minimizes the dialog window. |
| `mousePressEvent` | `mousePressEvent(self, event)` | Overriding the mousePressEvent for custom behavior. |
| `mouseMoveEvent` | `mouseMoveEvent(self, QMouseEvent)` | Overriding the mouseMoveEvent for custom behavior. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, QMouseEvent)` | Overriding the mouseReleaseEvent for custom behavior. |

<a id="vibefluxwidgetsextwidgets"></a>
## `VibeFlux.widgets.ExtWidgets`

图像标签、窗口控制、消息框扩展控件。

### 类

#### `FImageLabel`

A QLabel extension that provides additional functionality for displaying images. This class extends QLabel, providing the ability to display images and text. It allows for interactive

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `setAspectMode` | `setAspectMode(self, keepAspect: bool)` | Sets the aspect ratio mode for the label. |
| `init_ui` | `init_ui(self)` | Initializes the user interface (UI) of the label. |
| `dispImage` | `dispImage(self, image, keepAspect=True)` | Displays an image read by OpenCV in the label. |
| `dispText` | `dispText(self, text)` | Displays text in the label. |
| `paintEvent` | `paintEvent(self, e)` | Handles paint events. |
| `wheelEvent` | `wheelEvent(self, event)` | Handles mouse wheel events. This will allow to zoom the image in or out. |
| `mouseMoveEvent` | `mouseMoveEvent(self, e)` | Handles mouse move events. This will allow to pan the image when the mouse is moved. |
| `mousePressEvent` | `mousePressEvent(self, e)` | Handles mouse press events. This will start the panning operation. |
| `mouseReleaseEvent` | `mouseReleaseEvent(self, e)` | Handles mouse release events. This will end the panning operation. |
| `boxToolButton` | `boxToolButton(self, button_size=25)` | Sets up the buttons for the tool bar. |
| `normButton` | `normButton(self)` | Resets the image size to the original size. |
| `bigButton` | `bigButton(self)` | Increases the size of the image by 10%. |
| `smallButton` | `smallButton(self)` | Decreases the size of the image by 10%. |

#### `FWindowCtrls`

This class represents a main window with custom controls, including close, minimize, and hint buttons. Inherits from QMainWindow.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `closeQButton` | `closeQButton(self)` | Method to create a QMessageBox on closing the application. |
| `setMessageBox` | `setMessageBox(self, title='Message Box', message='Are you sure you want to quit?', yes_text='Yes', no_text='No', hint_flag=False, icon=HOME)` | Method to set a custom message box. |
| `closeButton` | `closeButton(self)` | Method to handle the close button event. |
| `minButton` | `minButton(self)` | Method to minimize the main window. |
| `maxButton` | `maxButton(self)` | Method to maximize, fullscreen, or restore the main window. |
| `hintButton` | `hintButton(self)` | Method to handle the hint button event. |
| `eventFilter` | `eventFilter(self, watched, event)` | Keeps icon colors in sync with title bar button hover and press states. |
| `setupWindowControls` | `setupWindowControls(self)` | Method to set up window controls like buttons. |

#### `FMessageBox`

This class represents a custom message box that inherits from QDialog. The message box includes a title, a message, and Yes/No buttons.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `set_message` | `set_message(self, message)` | Sets the message in the message box. |
| `set_icon` | `set_icon(self, icon_path)` | Sets the window icon. |
| `result` | `result(self)` | Executes the QDialog and returns the result. |
| `set_stylesheet` | `set_stylesheet(self, stylesheet=None)` | Sets the QSS stylesheet. |

<a id="vibefluxwidgetssettingsdialog"></a>
## `VibeFlux.widgets.SettingsDialog`

YAML 设置和通用配置编辑对话框。

### 类

#### `SettingsDialog`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load_yaml` | `load_yaml(self, yaml_path: str)` | Load YAML file using ruamel.yaml while preserving comments, order, and case. |
| `create_control_group` | `create_control_group(self, control_name: str, control_info: Dict[str, Any])` | Create a QGroupBox for each control based on YAML configuration, dynamically generating "info" display (read-only), "enabled" checkbox, |
| `on_browse_file` | `on_browse_file(self)` | Unified slot function: Finds the corresponding lineEdit based on sender() and updates its text with the selected file path. Validates that the selected |
| `save_and_close` | `save_and_close(self)` | Write the edited information back to the YAML file (preserving comments, order, and uppercase True/False), then close the dialog. |

#### `ConfigDialog`

-

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `load_yaml` | `load_yaml(self)` | Load the YAML configuration file using the parent class's method. |
| `init_ui` | `init_ui(self)` | Initialize the user interface by creating widgets based on YAML content. Utilizes the parent class's method. |
| `create_widget` | `create_widget(self, section: str, key: str, value: Any)` | Create appropriate widget based on the value type and key. Utilizes the parent class's method. |
| `browse_file_or_dir` | `browse_file_or_dir(self)` | Open a file or directory dialog based on the button's associated key. Utilizes the parent class's method. |
| `save_config` | `save_config(self)` | Save the modified configuration back to the YAML file. Utilizes the parent class's method. |

<a id="vibefluxwidgetstipswidgets"></a>
## `VibeFlux.widgets.TipsWidgets`

多类型提示气泡。

### 类

#### `MultiTipWidget`

An extended tooltip widget with multiple message types. Supports the following types: info, warning, error, success.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `showTip` | `showTip(self, text: str, duration: int=3000, position='center', message_type='info')` | Display the tooltip with the specified text, duration, position, and message type. |

<a id="vibefluxwidgetswidgets"></a>
## `VibeFlux.widgets.Widgets`

面向用户的 Qt 控件包装。

### 函数

| 名称 | 签名 | 说明 |
| --- | --- | --- |
| `QSkinCtrls` | `QSkinCtrls(parent: Optional[QWidget]=None, yaml_path: str='', geometry: Optional[Tuple[int, int, int, int]]=None, text: str='', icon_path: str='', hidden: bool=False, style_qss: Optional[str]=None)` | Create a modern "skin" button with a background image, transparent background, and dynamic border/padding effects on hover and click. When clicked, it will pop up SettingsDialog internally. |
| `QConfigCtrls` | `QConfigCtrls(parent: Optional[QWidget]=None, yaml_path: str='', geometry: Optional[Tuple[int, int, int, int]]=None, text: str='', icon_path: str='', hidden: bool=False, style_qss: Optional[str]=None)` | Create a button that opens the ConfigDialog when clicked. Args: |

### 类

#### `QMainWindow`

QMainWindow is a class derived from QMainWindow to provide custom methods and properties for handling graphical user interface (GUI) related operations in the application.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `clearUI` | `clearUI(self)` | Clears the UI and reloads settings from a YAML file. |
| `setConfig` | `setConfig(self)` | Method to set the configuration of the application. The actual implementation needs to be provided. |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |
| `closeEvent` | `closeEvent(self, event: QCloseEvent)` | Handles the close event of the main window. |
| `setNamedStyle` | `setNamedStyle(self, style_name='STYLE_TRANS')` | Apply a predefined style to the widget. |
| `setStyleText` | `setStyleText(self, style_text)` | Apply a given style text to a widget. |
| `loadYamlSettings` | `loadYamlSettings(self, yaml_file, base_path='./')` | Load settings for a QWidget from a YAML file and apply them to the specified window. |

#### `QLoginDialog`

A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |
| `loadYamlSettings` | `loadYamlSettings(self, yaml_file, base_path='./')` | Load settings for a QWidget from a YAML file and apply them to the specified window. |
| `setNamedStyle` | `setNamedStyle(self, style_name='STYLE_TRANS')` | Apply a predefined style to the widget. |
| `setStyleText` | `setStyleText(self, style_text)` | Apply a given style text to a widget. |

#### `QImageLabel`

A QLabel extension that provides additional functionality for displaying images. This class extends QLabel, providing the ability to display images and text. It allows for interactive

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |

#### `QWindowCtrls`

This class represents a main window with custom controls, including close, minimize, and hint buttons. Inherits from QMainWindow.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |

#### `QMessageBox`

This class represents a custom message box that inherits from QDialog. The message box includes a title, a message, and Yes/No buttons.

| 方法 | 签名 | 说明 |
| --- | --- | --- |
| `loadStyleSheet` | `loadStyleSheet(self, qssFilePath, base_path='./')` | Loads a QSS style sheet for the application from a given file path. |
| `setNamedStyle` | `setNamedStyle(self, style_name='STYLE_TRANS')` | Apply a predefined style to the widget. |
| `setStyleText` | `setStyleText(self, style_text)` | Apply a given style text to a widget. |

