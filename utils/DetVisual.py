# VibeFlux, AGPL-3.0 license

from typing import Tuple, List, Optional, Union

import cv2
import numpy as np
from aggdraw import Draw, Pen
from PIL import Image, ImageDraw, ImageFont

from ..base.Visual import IMDetectorVisual, IMDetectorVisualPIL
from ..config.VisualConf import get_names, get_predefined_colors

# Initialize predefined colors and class names
default_class_names = list(get_names().values())


class DetectorVisual(IMDetectorVisual):
    def __init__(self,
                 cls_names: Optional[List[str]] = None,
                 colors: Optional[List[Tuple[int, int, int]]] = None,
                 keypoint_color: Tuple[int, int, int] = (127, 0, 255),
                 skeleton_color: Tuple[int, int, int] = (175, 114, 63),
                 skeleton: Optional[List[Tuple[int, int]]] = None):
        """
        Initialize the visualizer with class names, corresponding colors, and skeleton settings.

        Args:
            cls_names (Optional[List[str]]): List of class names corresponding to the class IDs.
                                             If None, default class names are used.
            colors (Optional[List[Tuple[int, int, int]]]): List of BGR colors corresponding to the class IDs.
                                                           If None, default colors are used.
            keypoint_color (Tuple[int, int, int]): BGR Color for drawing keypoints. Default is pink (127, 0, 255).
            skeleton_color (Tuple[int, int, int]): BGR Color for drawing skeletons. Default is (175, 114, 63).
            skeleton (Optional[List[Tuple[int, int]]]): Skeleton connections as a list of keypoint index pairs.
                                                        If None, default COCO skeleton is used.

        Example:
            visualizer = DetectorVisual()
        """
        super().__init__(cls_names=cls_names,
                         colors=colors,
                         keypoint_color=keypoint_color,
                         skeleton_color=skeleton_color,
                         skeleton=skeleton)

    def set_params(self, cls_names: Optional[List[str]] = None,
                   colors: Optional[List[Tuple[int, int, int]]] = None):
        """
        Set class names and corresponding colors for visualization.

        Args:
            cls_names (Optional[List[str]]): List of class names. If None, defaults will be used.
            colors (Optional[List[Tuple[int, int, int]]]): List of colors. If None, defaults will be used.
        """
        return super().set_params(cls_names, colors)

    def get_cached_font(self, font_size: int):
        """
        Get cached font for the specified size.

        Args:
            font_size (int): The requested font size.

        Returns:
            PIL.ImageFont.FreeTypeFont: A font object of the requested size.

        Example:
            font = self.get_cached_font(40)
        """
        if font_size not in self.font_cache:
            self.font_cache[font_size] = self.chinese_font_base.font_variant(size=font_size)
        return self.font_cache[font_size]

    def __call__(self,
                 image: np.ndarray,
                 boxes: Optional[Union[np.ndarray, List]] = None,
                 scores: Optional[Union[np.ndarray, List[float]]] = None,
                 class_ids: Optional[Union[np.ndarray, List[int]]] = None,
                 keypoints: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                 mask_alpha: float = 0.3,
                 mask_maps: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                 labels: Optional[List[str]] = None,
                 cls_prob: Optional[float] = None,
                 cls_class_id: Optional[int] = None,
                 cls_class_name: Optional[str] = None,
                 cls_label: Optional[str] = None,
                 bg_alpha: float = 0.5) -> np.ndarray:
        """
        Draw detections (boxes, masks, keypoints), classification results, and skeletons on the image.

        Args:
            image (np.ndarray): Input image (BGR) on which to draw.
            boxes (Optional[Union[np.ndarray, List]]): Detected boxes.
                                                      Each box can be:
                                                      [x1, y1, x2, y2] or
                                                      [x1, y1, x2, y2, x3, y3, x4, y4] for rotated boxes.
            scores (Optional[Union[np.ndarray, List[float]]]): Confidence scores for each detection.
            class_ids (Optional[Union[np.ndarray, List[int]]]): Class IDs for each detection.
            keypoints (Optional[Union[np.ndarray, List[np.ndarray]]]): Keypoints for each detection.
            mask_alpha (float): Transparency for mask overlay. Default is 0.3.
            mask_maps (Optional[Union[np.ndarray, List[np.ndarray]]]): Instance segmentation masks for detected objects.
            labels (Optional[List[str]]): Custom labels for each detection. If None, defaults to "classname score%".
            cls_prob (Optional[float]): Probability for classification result to draw.
            cls_class_id (Optional[int]): Class ID for the classification result.
            cls_class_name (Optional[str]): Class name for the classification result.
            cls_label (Optional[str]): Custom label for classification result. If None, defaults to 'classname: score%'.
            bg_alpha (float): Alpha transparency for the classification background rectangle. Range [0,1].
                              Default is 0.5. 0 fully transparent, 1 fully opaque.

        Returns:
            np.ndarray: The annotated image (BGR).

        Example:
            # Detections
            image = cv2.imread("image.jpg")
            boxes = [[100,100,200,200]]
            scores = [0.9]
            class_ids = [0]
            visualizer = DetectorVisual()
            out_image = visualizer(image, boxes, scores, class_ids)

            # Classification
            out_image = visualizer(image, cls_prob=0.95, cls_class_name="cat", bg_alpha=0.4)
        """

        # If boxes, scores, class_ids are provided, draw detections
        if boxes is not None and scores is not None and class_ids is not None:
            image = self.draw_detections(image, boxes, scores, class_ids, keypoints, mask_maps, mask_alpha, labels)

        # If classification details are provided, draw classification result
        if cls_prob is not None and (cls_class_id is not None or cls_class_name is not None):
            image = self.draw_classification(image, cls_prob, cls_class_id, cls_class_name, cls_label, bg_alpha)

        return image

    @staticmethod
    def contains_chinese(text: str) -> bool:
        """
        Check if the text contains Chinese characters.

        Args:
            text (str): Input text.

        Returns:
            bool: True if Chinese characters are present, else False.

        Example:
            has_chinese = DetectorVisual.contains_chinese("测试")
        """
        return any('\u4e00' <= ch <= '\u9fff' for ch in text)

    def draw_detections(self,
                        image: np.ndarray,
                        boxes: Union[np.ndarray, List],
                        scores: Union[np.ndarray, List[float]],
                        class_ids: Union[np.ndarray, List[int]],
                        keypoints: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                        mask_maps: Optional[np.ndarray] = None,
                        mask_alpha: float = 0.3,
                        labels: Optional[List[str]] = None) -> np.ndarray:
        """
        Draw detections, including boxes, masks, keypoints, and skeletons.

        Args:
            image (np.ndarray): Input image (BGR).
            boxes (Union[np.ndarray, List]): Detected boxes.
            scores (Union[np.ndarray, List[float]]): Confidence scores for each detection.
            class_ids (Union[np.ndarray, List[int]]): Class IDs for each detection.
            keypoints (Optional[Union[np.ndarray, List[np.ndarray]]]): Keypoints for each detection.
            mask_maps (Optional[np.ndarray]): Instance masks.
            mask_alpha (float): Transparency for mask overlay. Default 0.3.
            labels (Optional[List[str]]): Custom labels for each detection.

        Returns:
            np.ndarray: The image with detections drawn.

        Example:
            image = cv2.imread("image.jpg")
            boxes = [[100,100,200,200]]
            scores = [0.9]
            class_ids = [0]
            out_image = self.draw_detections(image, boxes, scores, class_ids)
        """
        return super().draw_detections(image, boxes, scores, class_ids, keypoints, mask_maps, mask_alpha, labels)

    @staticmethod
    def draw_all_boxes(image: np.ndarray,
                       rect_boxes: List[Union[np.ndarray, List[float]]],
                       rect_colors: List[Tuple[int, int, int]],
                       rotated_boxes: List[Union[np.ndarray, List[float]]],
                       rotated_colors: List[Tuple[int, int, int]],
                       thickness: int = 2):
        """
        Draw all bounding boxes on the image.

        Args:
            image (np.ndarray): The image to draw on.
            rect_boxes (List): List of rectangular boxes [x1,y1,x2,y2].
            rect_colors (List): Colors for each rectangular box.
            rotated_boxes (List): List of rotated boxes [x1,y1,x2,y2,x3,y3,x4,y4].
            rotated_colors (List): Colors for each rotated box.
            thickness (int): Line thickness.

        Example:
            self.draw_all_boxes(image, [[100,100,200,200]], [(0,255,0)], [], [])
        """
        return IMDetectorVisual.draw_all_boxes(image, rect_boxes, rect_colors, rotated_boxes, rotated_colors, thickness)

    def draw_all_texts_pil(self,
                           image: np.ndarray,
                           text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int],
                           float, int, str]]) -> np.ndarray:
        """
        Draw all text annotations using PIL for better character (e.g., Chinese) support.

        Args:
            image (np.ndarray): The image to draw text on.
            text_annotations (List[Tuple]): Each item: (text, box, color, font_size, text_thickness, box_type).

        Returns:
            np.ndarray: Image with text drawn.

        Example:
            annotations = [("Label", [100,100,200,200], (0,255,0), 1, 1, 'rect')]
            out_image = self.draw_all_texts_pil(image, annotations)
        """
        return super().draw_all_texts_pil(image, text_annotations)

    def draw_all_texts_cv2(self,
                           image: np.ndarray,
                           text_annotations: List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int],
                           float, int, str]]):
        """
        Draw all text annotations using OpenCV. Suitable for non-Chinese text.

        Args:
            image (np.ndarray): The image to draw text on.
            text_annotations (List[Tuple]): (text, box, color, font_size, text_thickness, box_type).

        Example:
            annotations = [("Label", [100,100,200,200], (0,255,0), 1, 1, 'rect')]
            self.draw_all_texts_cv2(image, annotations)
        """
        return super().draw_all_texts_cv2(image, text_annotations)

    @staticmethod
    def compute_text_position(box: Union[List[float], np.ndarray], box_type: str) -> Tuple[int, int]:
        """
        Compute the text start position for both rectangular and rotated boxes.
        For rotated boxes, find the top edge midpoint.

        Args:
            box (Union[List[float], np.ndarray]): The box coordinates.
            box_type (str): 'rect' or 'rotated'.

        Returns:
            Tuple[int, int]: (x0, y0) coordinates for text placement.

        Example:
            x0, y0 = self.compute_text_position([100,100,200,200], 'rect')
        """
        return IMDetectorVisual.compute_text_position(box, box_type)

    def draw_masks(self,
                   image: np.ndarray,
                   boxes: Union[np.ndarray, List],
                   classes: np.ndarray,
                   mask_alpha: float = 0.3,
                   mask_maps: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Draw masks on the image. If mask_maps is provided, apply instance segmentation masks.
        Otherwise, draw filled boxes.

        Args:
            image (np.ndarray): The original image.
            boxes (Union[np.ndarray, List]): Detected boxes.
            classes (np.ndarray): Class IDs for each detection.
            mask_alpha (float): Transparency for mask overlay.
            mask_maps (Optional[np.ndarray]): Instance segmentation masks.

        Returns:
            np.ndarray: Image with masks drawn.

        Example:
            masked_img = self.draw_masks(image, boxes, class_ids, 0.3, mask_maps)
        """
        return super().draw_masks(image, boxes, classes, mask_alpha, mask_maps)

    def draw_keypoints(self,
                       image: np.ndarray,
                       keypoints: np.ndarray,
                       conf_threshold: float = 0.0,
                       circle_radius: int = 3):
        """
        Draw keypoints on the image.

        Args:
            image (np.ndarray): The image to draw on.
            keypoints (np.ndarray): Keypoints, shape (num_keypoints, 3) with (x,y,confidence).
            conf_threshold (float): Minimum confidence to draw the keypoint.
            circle_radius (int): Radius of the circle for keypoints.

        Example:
            self.draw_keypoints(image, keypoints)
        """
        return super().draw_keypoints(image, keypoints, conf_threshold, circle_radius)

    def draw_skeleton(self,
                      image: np.ndarray,
                      keypoints: np.ndarray,
                      conf_threshold: float = 0.0,
                      line_thickness: int = 2):
        """
        Draw skeleton on the image, connecting keypoints based on predefined skeleton structure.

        Args:
            image (np.ndarray): The image to draw on.
            keypoints (np.ndarray): Keypoints, shape (num_keypoints, 3) with (x,y,confidence).
            conf_threshold (float): Minimum confidence to draw a connection.
            line_thickness (int): Thickness of the skeleton lines.

        Example:
            self.draw_skeleton(image, keypoints)
        """
        return super().draw_skeleton(image, keypoints, conf_threshold, line_thickness)

    def draw_classification(self,
                            image: np.ndarray,
                            prob: float,
                            class_id: Optional[int] = None,
                            class_name: Optional[str] = None,
                            custom_label: Optional[str] = None,
                            bg_alpha: float = 0.5) -> np.ndarray:
        """
        Draw classification results on the image with a transparent background.

        Args:
            image (np.ndarray): The original image.
            prob (float): Classification probability score.
            class_id (Optional[int]): Class ID of the predicted class. If None, class_name must be provided.
            class_name (Optional[str]): Class name. If None, class_id must be provided.
            custom_label (Optional[str]): Custom label for the classification result.
                                          If None, defaults to 'classname: score%'.
            bg_alpha (float): Alpha transparency for the background rectangle. Range [0,1],
                              where 0 is fully transparent and 1 is fully opaque.

        Returns:
            np.ndarray: Image with classification result drawn.
        """
        return super().draw_classification(image, prob, class_id, class_name, custom_label, bg_alpha)


class DetectorVisualPIL(IMDetectorVisualPIL):
    def __init__(self,
                 cls_names: Optional[List[str]] = None,
                 colors: Optional[List[Tuple[int, int, int]]] = None,
                 keypoint_color: Tuple[int, int, int] = (127, 0, 255),
                 skeleton_color: Tuple[int, int, int] = (175, 114, 63),
                 skeleton: Optional[List[Tuple[int, int]]] = None):
        """
        Initializes a visualization class for object detection, with support for bounding boxes,
        keypoints, skeletons, and masks. Used to annotate images with detection or classification results.

        Args:
            cls_names (Optional[List[str]]): Class names for detected objects; defaults to a predefined list.
            colors (Optional[List[Tuple[int, int, int]]]): RGB colors corresponding to each class;
                                                           defaults to predefined colors.
            keypoint_color (Tuple[int, int, int]): RGB color for keypoints. Default is (127, 0, 255).
            skeleton_color (Tuple[int, int, int]): RGB color for skeleton connections. Default is (175, 114, 63).
            skeleton (Optional[List[Tuple[int, int]]]): Joint pairs defining the skeleton structure for visualization;
                                                        defaults to COCO keypoint order.

        Attributes:
            cls_names (List[str]): Class names used for generating detection labels.
            colors (List[Tuple[int, int, int]]): List of RGB colors for each class.
            skeleton (List[Tuple[int, int]]): List representing keypoint connections (e.g., joint pairs).
            font_cache (dict): Font cache for efficiently reusing font objects.
            keypoint_color (Tuple[int, int, int]): Visualization color for keypoints.
            skeleton_color (Tuple[int, int, int]): Visualization color for skeletons.
            chinese_font_base (ImageFont): Default font for Chinese character display; fallback to default font if unavailable.

        Example:
            >>> # Initialize DetectorVisual with default settings
            >>> visualizer = DetectorVisualPIL()
            >>>
            >>> # Define a blank image (500x500 pixels, black background)
            >>> import numpy as np
            >>> blank_image = np.zeros((500, 500, 3), dtype=np.uint8)
            >>>
            >>> # Use the visualizer to process and annotate the image (no detection input shown here)
            >>> result_image = visualizer(blank_image)
            >>>
            >>> # Save or preview the result image
            >>> from PIL import Image
            >>> Image.fromarray(result_image).save("annotated_image.png")
        """
        super().__init__(cls_names=cls_names,
                         colors=colors,
                         keypoint_color=keypoint_color,
                         skeleton_color=skeleton_color,
                         skeleton=skeleton)

    def set_params(self, cls_names: Optional[List[str]] = None,
                   colors: Optional[List[Tuple[int, int, int]]] = None):
        """
        Set class names and corresponding colors for visualization.

        Args:
            cls_names (Optional[List[str]]): List of class names. If None, defaults will be used.
            colors (Optional[List[Tuple[int, int, int]]]): List of colors. If None, defaults will be used.
        """
        return super().set_params(cls_names, colors)

    def get_cached_font(self, font_size: int):
        """
        Retrieves or generates a font object of a given size, using a cache for performance optimization.

        Args:
            font_size (int): The size (in points) for the desired font.

        Returns:
            ImageFont: A PIL font object for rendering text.

        Example:
            >>> # Initialize the DetectorVisual object
            >>> visualizer = DetectorVisualPIL()
            >>>
            >>> # Get a cached or new font object
            >>> my_font = visualizer.get_cached_font(25)  # Request font of size 25
            >>>
            >>> # Use the font for text rendering
            >>> from PIL import Image, ImageDraw
            >>> img = Image.new("RGB", (200, 100), color=(255, 255, 255))  # Create blank white image
            >>> draw = ImageDraw.Draw(img)
            >>> draw.text((10, 10), "Hello World", font=my_font, fill=(0, 0, 0))  # Render text on image
            >>> img.show()
        """
        if font_size not in self.font_cache:
            # Create a new font object and cache it for future use
            self.font_cache[font_size] = self.chinese_font_base.font_variant(size=font_size)
        return self.font_cache[font_size]

    def __call__(self,
                 image: np.ndarray,
                 boxes: Optional[Union[np.ndarray, List]] = None,
                 scores: Optional[Union[np.ndarray, List[float]]] = None,
                 class_ids: Optional[Union[np.ndarray, List[int]]] = None,
                 keypoints: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                 mask_alpha: float = 0.3,
                 mask_maps: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                 labels: Optional[List[str]] = None,
                 cls_prob: Optional[float] = None,
                 cls_class_id: Optional[int] = None,
                 cls_class_name: Optional[str] = None,
                 cls_label: Optional[str] = None,
                 bg_alpha: float = 0.5) -> np.ndarray:
        """
            Visualizes and annotates an image with detection results (bounding boxes, masks, keypoints, skeletons,
            classification info, etc.) by overlaying visual elements on the input image.

            Args:
                image (np.ndarray): The input image in BGR format as a NumPy array.
                boxes (Optional[Union[np.ndarray, List]]): Detected bounding boxes, shape (N, 4) for rectangular boxes
                                                          or (N, 8) for rotated boxes.
                scores (Optional[Union[np.ndarray, List[float]]]): List or array of confidence scores for each box.
                class_ids (Optional[Union[np.ndarray, List[int]]]): List or array of class IDs corresponding to detected objects.
                keypoints (Optional[Union[np.ndarray, List[np.ndarray]]]): List or array of keypoint locations with confidence values
                                                                           (shape [N, K, 3], where K is the number of keypoints).
                mask_alpha (float): Transparency level of masks (0.0 = fully transparent, 1.0 = opaque). Default: 0.3.
                mask_maps (Optional[Union[np.ndarray, List[np.ndarray]]]): Binary or probability maps for instance masks with shape [H, W, N].
                labels (Optional[List[str]]): List of custom labels for detected objects, overrides class name if provided.
                cls_prob (Optional[float]): Probability score for global image classification (e.g., logo/motif detection).
                cls_class_id (Optional[int]): Class ID for global image classification result.
                cls_class_name (Optional[str]): Class name for global image classification.
                cls_label (Optional[str]): Custom label for the global classification result.
                bg_alpha (float): Transparency level for the classification text's background. Default: 0.5.

            Returns:
                np.ndarray: The annotated image in BGR format as a NumPy array.

            Notes:
                - The image is converted from BGR to RGB at the beginning for PIL processing and converted back to BGR afterwards.
                - Both detection and classification results, if provided, are overlayed on the image.

            Example:
                >>> import numpy as np
                >>> from PIL import Image
                >>>
                >>> # Initialize the visualizer
                >>> visualizer = DetectorVisualPIL()
                >>>
                >>> # Create a dummy input image (500x500, black background)
                >>> input_image = np.zeros((500, 500, 3), dtype=np.uint8)
                >>>
                >>> # Dummy inputs for visualization
                >>> boxes = [[50, 50, 200, 200]]  # One bounding box
                >>> scores = [0.9]  # Confidence score for the box
                >>> class_ids = [1]  # Class ID of the detected object
                >>> keypoints = [[[100, 100, 1.0], [150, 150, 0.8]]]  # One set of keypoints
                >>>
                >>> # Visualize the detection results
                >>> output_image = visualizer(
                >>>     image=input_image,
                >>>     boxes=boxes,
                >>>     scores=scores,
                >>>     class_ids=class_ids,
                >>>     keypoints=keypoints
                >>> )
                >>>
                >>> # Convert output to a PIL image and save or display
                >>> Image.fromarray(output_image).save("annotated_output.png")
            """
        return super().__call__(
            image=image,
            boxes=boxes,
            scores=scores,
            class_ids=class_ids,
            keypoints=keypoints,
            mask_alpha=mask_alpha,
            mask_maps=mask_maps,
            labels=labels,
            cls_prob=cls_prob,
            cls_class_id=cls_class_id,
            cls_class_name=cls_class_name,
            cls_label=cls_label,
            bg_alpha=bg_alpha
        )

    @staticmethod
    def contains_chinese(text: str) -> bool:
        """
            Checks if a given string contains any Chinese characters.

            Args:
                text (str): The input string to check.

            Returns:
                bool: True if the string contains Chinese characters, False otherwise.

            Example:
                >>> DetectorVisualPIL.contains_chinese("Hello World")  # False
                >>> DetectorVisualPIL.contains_chinese("你好世界")      # True
            """
        # Check each character to see if it falls in the Unicode range for Chinese characters
        return any('\u4e00' <= ch <= '\u9fff' for ch in text)

    def draw_detections(self,
                        pil_img: Image.Image,
                        boxes: Union[np.ndarray, List],
                        scores: Union[np.ndarray, List[float]],
                        class_ids: Union[np.ndarray, List[int]],
                        keypoints: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
                        mask_maps: Optional[np.ndarray] = None,
                        mask_alpha: float = 0.3,
                        labels: Optional[List[str]] = None) -> Image.Image:
        """
            Draw detection annotations on the image, including bounding boxes, masks, keypoints, and skeletons.

            Args:
                pil_img (Image.Image): The input image (PIL format) to be annotated.
                boxes (Union[np.ndarray, List]): List or array of bounding boxes with coordinates.
                                                 Format: [N, 4] for rectangular boxes or [N, 8] for rotated boxes.
                scores (Union[np.ndarray, List[float]]): List or array of confidence scores for each detection.
                class_ids (Union[np.ndarray, List[int]]): List or array of class IDs for each detection.
                keypoints (Optional[Union[np.ndarray, List[np.ndarray]]]): Keypoint annotations, optional. Should be in
                                                                           the format [N, K, 3], where
                                                                           K is the number of keypoints for each detection.
                mask_maps (Optional[np.ndarray]): Binary or probability maps for instance masks. Shape: [H, W, N].
                                                   If None, no masks are drawn. Default: None.
                mask_alpha (float): Transparency (0 to 1, 0 = fully transparent) of the drawn masks. Default: 0.3.
                labels (Optional[List[str]]): Custom text labels for each detection. Overrides class name. Default: None.

            Returns:
                Image.Image: The annotated image in PIL format.

            Example:
                >>> from PIL import Image
                >>> import numpy as np
                >>>
                >>> # Create a dummy image
                >>> pil_img = Image.new("RGB", (500, 500), color=(255, 255, 255))
                >>>
                >>> # Dummy boxes, scores, classes, keypoints, and masks
                >>> boxes = [[50, 50, 200, 200], [100, 100, 300, 300]]  # Two rectangular bounding boxes
                >>> scores = [0.9, 0.8]  # Confidence scores
                >>> class_ids = [0, 1]  # Class IDs
                >>> keypoints = [
                >>>     [[60, 60, 1], [190, 190, 1]],  # Keypoints for the first object
                >>>     [[110, 110, 0.8], [280, 280, 1]]  # Keypoints for the second object
                >>> ]
                >>> mask_alpha = 0.3
                >>>
                >>> # Initialize a visualizer with available class names and colors
                >>> visualizer = DetectorVisualPIL(
                >>>     cls_names=["Class_A", "Class_B"],
                >>>     colors=[(255, 0, 0), (0, 255, 0)]  # Red for Class_A, Green for Class_B
                >>> )
                >>>
                >>> # Annotate the image
                >>> ann_img = visualizer.draw_detections(
                >>>     pil_img=pil_img,
                >>>     boxes=boxes,
                >>>     scores=scores,
                >>>     class_ids=class_ids,
                >>>     keypoints=keypoints,
                >>>     mask_alpha=mask_alpha
                >>> )
                >>>
                >>> # Save or display the annotated image
                >>> ann_img.save("annotated_detections.png")

            Notes:
                - This function is highly customizable and supports multiple types of detection annotations.
                - Keypoints, skeletons, and masks are optional and rendered if provided.
                - Supports both rectangular and rotated bounding boxes.
            """
        return super().draw_detections(
            pil_img=pil_img,
            boxes=boxes,
            scores=scores,
            class_ids=class_ids,
            keypoints=keypoints,
            mask_maps=mask_maps,
            mask_alpha=mask_alpha,
            labels=labels
        )

    def draw_all_boxes(self,
                       pil_img: Image.Image,
                       rect_boxes: List[Union[np.ndarray, List[float]]],
                       rect_colors: List[Tuple[int, int, int]],
                       rotated_boxes: List[Union[np.ndarray, List[float]]],
                       rotated_colors: List[Tuple[int, int, int]],
                       thickness: int = 2) -> Image.Image:
        """
            Draws all detection boxes, including both rectangular and rotated bounding boxes.

            Args:
                pil_img (Image.Image): The input PIL image to draw bounding boxes on.
                rect_boxes (List[Union[np.ndarray, List[float]]]): List of rectangular box coordinates [(x1, y1, x2, y2)].
                rect_colors (List[Tuple[int, int, int]]): List of RGB colors for each rectangular box (e.g., [(255, 0, 0)]).
                rotated_boxes (List[Union[np.ndarray, List[float]]]): List of rotated box coordinates, represented as
                                                                     [x1, y1, x2, y2, ..., x4, y4] for 4 corners.
                rotated_colors (List[Tuple[int, int, int]]): List of RGB colors for each rotated box.
                thickness (int): Thickness of the bounding box lines. Default: 2.

            Returns:
                Image.Image: The image with bounding boxes drawn.

            Example:
                >>> from PIL import Image
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))  # Blank white image
                >>>
                >>> # Define rectangular and rotated boxes
                >>> rect_boxes = [[50, 50, 150, 150]]
                >>> rotated_boxes = [[200, 200, 300, 200, 300, 300, 200, 300]]
                >>> rect_colors = [(255, 0, 0)]  # Red for rectangular boxes
                >>> rotated_colors = [(0, 255, 0)]  # Green for rotated boxes
                >>>
                >>> # Draw boxes
                >>> visualizer = DetectorVisualPIL()
                >>> img_with_boxes = visualizer.draw_all_boxes(
                >>>     img,
                >>>     rect_boxes=rect_boxes,
                >>>     rect_colors=rect_colors,
                >>>     rotated_boxes=rotated_boxes,
                >>>     rotated_colors=rotated_colors
                >>> )
                >>> img_with_boxes.show()
            """
        return super().draw_all_boxes(
            pil_img=pil_img,
            rect_boxes=rect_boxes,
            rect_colors=rect_colors,
            rotated_boxes=rotated_boxes,
            rotated_colors=rotated_colors,
            thickness=thickness
        )

    def draw_all_texts_pil(self,
                           pil_img: Image.Image,
                           text_annotations: List[
                               Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int], float, int, str]]
                           ) -> Image.Image:
        """
            Draws text annotations using PIL, supporting multilingual text, including Chinese.

            Args:
                pil_img (Image.Image): The input image (PIL format) to add text annotations to.
                text_annotations (List[Tuple[str, Union[np.ndarray, List[float]], Tuple[int, int, int],
                                  float, int, str]]): A list of text annotation info, where each tuple contains:
                    - Text (str): The text to be displayed.
                    - Box (Union[np.ndarray, List[float]]): Bounding box coordinates associated with the text.
                    - Color (Tuple[int, int, int]): Background color (RGB) for the text.
                    - Font size (float): Font size for the text.
                    - Text thickness (int): Thickness of the text outline.
                    - Box type (str): Type of bounding box ("rect" or "rotated").

            Returns:
                Image.Image: The updated image with text annotations.

            Example:
                >>> from PIL import Image
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))
                >>> annotations = [
                >>>     ("Class A", [50, 50, 100, 100], (255, 0, 0), 15, 1, 'rect')
                >>> ]
                >>> visualizer = DetectorVisualPIL()
                >>> annotated_img = visualizer.draw_all_texts_pil(img, annotations)
                >>> annotated_img.show()
            """
        return super().draw_all_texts_pil(pil_img, text_annotations)


    @staticmethod
    def compute_text_position(box: Union[List[float], np.ndarray], box_type: str) -> Tuple[int, int]:
        """
            Computes the starting position for text annotation based on the given bounding box.

            Args:
                box (Union[List[float], np.ndarray]): The bounding box coordinates.
                    - For rectangular boxes ('rect'), format is [x1, y1, x2, y2].
                    - For rotated boxes, format is [x0, y0, x1, y1, ..., xN, yN] representing the polygon vertices.
                box_type (str): The type of the bounding box. Accepts:
                    - 'rect': Indicates a rectangular bounding box.
                    - Other values are assumed to be for rotated bounding boxes.

            Returns:
                Tuple[int, int]: The (x, y) coordinates for starting the text annotation:
                    - For 'rect', returns the top-left corner (x1, y1).
                    - For rotated boxes, returns the geometric midpoint of the top two vertices.

            Raises:
                ValueError: If the `box_type` is not recognized.

            Example:
                >>> # Example with a rectangular box
                >>> box = [100, 50, 200, 150]
                >>> compute_text_position(box, box_type='rect')
                (100, 50)

                >>> # Example with a rotated box
                >>> rotated_box = [50, 50, 150, 50, 150, 100, 50, 100]
                >>> compute_text_position(rotated_box, box_type='rotated')
                (100, 50)

            """
        return IMDetectorVisualPIL.compute_text_position(box, box_type)


    def draw_masks(self,
                   pil_img: Image.Image,
                   boxes: Union[np.ndarray, List],
                   classes: np.ndarray,
                   mask_alpha: float = 0.3,
                   mask_maps: Optional[np.ndarray] = None) -> Image.Image:
        """
            Draws instance masks on the image. If mask maps are not provided, fills the bounding box area instead.

            Args:
                pil_img (Image.Image): The input image (PIL format) to add masks to.
                boxes (Union[np.ndarray, List]): List or array of bounding boxes (or polygons for rotated boxes).
                classes (np.ndarray): Array of class IDs corresponding to the bounding boxes.
                mask_alpha (float): Blend transparency for the masks (0.0 = fully transparent, 1.0 = fully opaque).
                                    Default: 0.3.
                mask_maps (Optional[np.ndarray]): Instance binary or probability map for masks. If None, bounding box regions
                                                  are filled instead.

            Returns:
                Image.Image: The updated image with masks overlayed.

            Example:
                >>> from PIL import Image
                >>> import numpy as np
                >>>
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))  # Blank white image
                >>> boxes = [[50, 50, 100, 100]]
                >>> classes = np.array([0])
                >>> mask_alpha = 0.5
                >>>
                >>> visualizer = DetectorVisualPIL()
                >>> img_with_masks = visualizer.draw_masks(img, boxes, classes, mask_alpha)
                >>> img_with_masks.show()
            """
        return super().draw_masks(
            pil_img=pil_img,
            boxes=boxes,
            classes=classes,
            mask_alpha=mask_alpha,
            mask_maps=mask_maps
        )

    def draw_keypoints(self,
                       pil_img: Image.Image,
                       keypoints: np.ndarray,
                       conf_threshold: float = 0.5,
                       circle_radius: int = 3) -> Image.Image:
        """
            Draws keypoints on the image, represented as small circles.

            Args:
                pil_img (Image.Image): The input image in PIL format.
                keypoints (np.ndarray): Array of keypoints with format [N, 3], where (x, y, conf).
                conf_threshold (float): Threshold for the confidence score above which the keypoints are drawn.
                                        Default: 0.5.
                circle_radius (int): Radius of the circle representing the keypoint. Default: 3.

            Returns:
                Image.Image: The image with keypoints drawn.

            Example:
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))
                >>> keypoints = np.array([[100, 100, 0.9], [200, 200, 0.7], [300, 300, 0.4]])
                >>> visualizer = DetectorVisualPIL()
                >>> img_with_keypoints = visualizer.draw_keypoints(img, keypoints, conf_threshold=0.5, circle_radius=5)
                >>> img_with_keypoints.show()
            """
        return super().draw_keypoints(
            pil_img=pil_img,
            keypoints=keypoints,
            conf_threshold=conf_threshold,
            circle_radius=circle_radius
        )

    def draw_skeleton(self,
                      pil_img: Image.Image,
                      keypoints: np.ndarray,
                      conf_threshold: float = 0.5,
                      line_thickness: int = 2) -> Image.Image:
        """
            Draws the skeleton by connecting keypoints with lines, based on the specified skeleton structure.

            Args:
                pil_img (Image.Image): The input image in PIL format.
                keypoints (np.ndarray): Array of keypoints with format [N, 3], where (x, y, conf).
                conf_threshold (float): Threshold for the confidence score above which the keypoints are used.
                                        Default: 0.5.
                line_thickness (int): Thickness of the line used to draw the skeleton. Default: 2.

            Returns:
                Image.Image: The image with the skeleton drawn.

            Example:
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))
                >>> keypoints = np.array([[100, 100, 0.9], [200, 200, 0.7], [300, 300, 0.8]])
                >>> visualizer = DetectorVisualPIL(skeleton=[[0, 1], [1, 2]])
                >>> img_with_skeleton = visualizer.draw_skeleton(img, keypoints, conf_threshold=0.5, line_thickness=3)
                >>> img_with_skeleton.show()
            """
        return super().draw_skeleton(
            pil_img=pil_img,
            keypoints=keypoints,
            conf_threshold=conf_threshold,
            line_thickness=line_thickness
        )

    def draw_classification(self,
                            pil_img: Union[Image.Image, np.ndarray],
                            prob: float,
                            class_id: Optional[int] = None,
                            class_name: Optional[str] = None,
                            custom_label: Optional[str] = None,
                            bg_alpha: float = 0.5) -> np.ndarray:
        """
            Annotates the image with a classification result. Draws a semi-transparent text box with the class name,
            confidence score, or a custom label.

            Args:
                pil_img (Union[Image.Image, np.ndarray]): The input image in PIL or NumPy format.
                prob (float): Confidence score of the classification result (0 to 1).
                class_id (Optional[int]): Index of the predicted class. Required if `class_name` is not provided.
                class_name (Optional[str]): Name of the predicted class. Overrides `class_id`.
                custom_label (Optional[str]): Custom text label for the annotation. Overrides the default label.
                bg_alpha (float): Transparency of the background box (0 = fully transparent, 1 = fully opaque).
                                  Default: 0.5.

            Returns:
                np.ndarray: The annotated image, returned as a NumPy array in BGR format.

            Example:
                >>> import numpy as np
                >>> from PIL import Image
                >>> img = Image.new("RGB", (500, 500), color=(255, 255, 255))
                >>> visualizer = DetectorVisualPIL(cls_names=["Cat", "Dog"], colors=[(255, 0, 0), (0, 255, 0)])
                >>> annotated_img = visualizer.draw_classification(
                >>>     pil_img=img,
                >>>     prob=0.95,
                >>>     class_id=1
                >>> )
                >>> Image.fromarray(annotated_img[..., ::-1]).show()
            """
        return super().draw_classification(
            pil_img=pil_img,
            prob=prob,
            class_id=class_id,
            class_name=class_name,
            custom_label=custom_label,
            bg_alpha=bg_alpha
        )
