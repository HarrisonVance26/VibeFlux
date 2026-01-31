# IMcore

from typing import Tuple, List, Optional, Union
import cv2
import numpy as np
from aggdraw import Draw, Pen
from PIL import Image, ImageDraw, ImageFont
from .VisualConf import get_names, get_predefined_colors

# Initialize predefined colors and class names
default_class_names = list(get_names().values())


class IMDetectorVisual:
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
            visualizer = IMDetectorVisual()
        """
        self.cls_names = cls_names if cls_names is not None else default_class_names
        self.colors = colors if colors is not None else get_predefined_colors(class_names=self.cls_names)

        # Default skeleton (COCO format)
        self.skeleton = skeleton if skeleton is not None else [
            (15, 13), (13, 11), (16, 14), (14, 12),
            (11, 12), (5, 11), (6, 12), (5, 6),
            (5, 7), (6, 8), (7, 9), (8, 10),
            (1, 2), (0, 1), (0, 2), (1, 3), (2, 4),
            (3, 5), (4, 6)
        ]

        # Font cache
        self.font_cache = {}

        self.keypoint_color = keypoint_color
        self.skeleton_color = skeleton_color

        # Load font for Chinese characters
        from PIL import ImageFont
        import os

        font_path = "C:/Windows/Fonts/simkai.ttf"  # Update path if needed
        if not os.path.exists(font_path):
            font_path = "simkai.ttf"
        try:
            self.chinese_font_base = ImageFont.truetype(font_path, 20)
        except IOError:
            print("Font file not found. Using default font.")
            self.chinese_font_base = ImageFont.load_default()

    def set_params(self, cls_names: Optional[List[str]] = None,
                   colors: Optional[List[Tuple[int, int, int]]] = None):
        """
        Set class names and corresponding colors for visualization.

        Args:
            cls_names (Optional[List[str]]): List of class names. If None, defaults will be used.
            colors (Optional[List[Tuple[int, int, int]]]): List of colors. If None, defaults will be used.
        """
        self.cls_names = cls_names if cls_names is not None else default_class_names
        self.colors = colors if colors is not None else get_predefined_colors(class_names=self.cls_names)

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
            visualizer = IMDetectorVisual()
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
            has_chinese = IMDetectorVisual.contains_chinese("测试")
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
        if isinstance(boxes, list):
            boxes = np.array(boxes)
        if isinstance(scores, list):
            scores = np.array(scores)
        if isinstance(class_ids, list):
            class_ids = np.array(class_ids)

        img_height, img_width = image.shape[:2]
        box_line_thickness = max(round(min(img_height, img_width) * 0.0015), 2)
        font_size = max(int(round(min(img_height, img_width) * 0.0010)), 1)
        text_thickness = max(round(min(img_height, img_width) * 0.0015), 1)
        keypoint_radius = max(round(min(img_height, img_width) * 0.0035), 3)
        skeleton_line_thickness = max(round(min(img_height, img_width) * 0.0015), 2)

        # Draw masks
        image = self.draw_masks(image, boxes, class_ids, mask_alpha, mask_maps)

        if keypoints is not None:
            if isinstance(keypoints, list):
                keypoints = np.array(keypoints)
        else:
            keypoints = np.array([None] * len(boxes))

        processed_boxes = []
        for box in boxes:
            if len(box) == 4:
                processed_boxes.append(('rect', box))
            elif len(box) == 8:
                processed_boxes.append(('rotated', box))
            else:
                raise ValueError("Box format not recognized. Must have 4 or 8 coordinates.")

        text_annotations = []
        rect_boxes = []
        rotated_boxes = []
        rect_colors = []
        rotated_colors = []
        keypoints_list = []
        need_pil = False

        for i, (class_id, (box_type, box), score, kp) in enumerate(
                zip(class_ids, processed_boxes, scores, keypoints)):
            color = self.colors[class_id]
            label = self.cls_names[class_id]
            caption = labels[i] if (labels is not None and len(labels) > i) else f'{label} {int(score * 100)}%'

            if self.contains_chinese(caption):
                need_pil = True

            text_annotations.append((caption, box, color, font_size, text_thickness, box_type))
            if box_type == 'rect':
                rect_boxes.append(box)
                rect_colors.append(color)
            else:
                rotated_boxes.append(box)
                rotated_colors.append(color)

            if kp is not None:
                keypoints_list.append((kp, color))

        # Draw boxes
        self.draw_all_boxes(image, rect_boxes, rect_colors, rotated_boxes, rotated_colors, box_line_thickness)

        # Draw keypoints and skeletons
        for kp, color in keypoints_list:
            self.draw_skeleton(image, kp, line_thickness=skeleton_line_thickness)
            self.draw_keypoints(image, kp, circle_radius=keypoint_radius)

        # Draw texts
        if need_pil:
            image = self.draw_all_texts_pil(image, text_annotations)
        else:
            self.draw_all_texts_cv2(image, text_annotations)

        return image

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
        # Draw regular boxes
        for box, color in zip(rect_boxes, rect_colors):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

        # Draw rotated boxes
        for box, color in zip(rotated_boxes, rotated_colors):
            pts = np.array(box, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [pts], isClosed=True, color=color, thickness=thickness)

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
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image_rgb)
        draw = ImageDraw.Draw(pil_img)

        for text, box, color, font_size, text_thickness, box_type in text_annotations:
            x0, y0 = self.compute_text_position(box, box_type)
            font_size_pil = max(int(font_size * 40), 12)
            font = self.get_cached_font(font_size_pil)
            text_size = draw.textsize(text, font=font)
            y0 = max(y0 - text_size[1], 0)

            # Draw background
            draw.rectangle([x0, y0, x0 + text_size[0], y0 + text_size[1]], fill=tuple(color[::-1]))
            # Draw text
            draw.text((x0, y0), text, font=font, fill=(255, 255, 255))

        image_with_text = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return image_with_text

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
        for text, box, color, font_size, text_thickness, box_type in text_annotations:
            x0, y0 = self.compute_text_position(box, box_type)
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, text_thickness)
            y0 = max(y0 - text_height - 5, 0)

            cv2.rectangle(image, (x0, y0), (x0 + text_width, y0 + text_height + 5), color, -1)
            cv2.putText(image, text, (x0, y0 + text_height), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                        (255, 255, 255), text_thickness, cv2.LINE_AA)

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
        if box_type == 'rect':
            x1, y1, x2, y2 = map(int, box)
            return x1, y1
        else:
            pts = np.array(box, dtype=np.int32).reshape((-1, 2))
            pts_sorted = pts[np.lexsort((pts[:, 0], pts[:, 1]))]
            top_two = pts_sorted[:2]
            top_mid_x = int((top_two[0][0] + top_two[1][0]) / 2)
            top_mid_y = int((top_two[0][1] + top_two[1][1]) / 2)
            return top_mid_x, top_mid_y

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
        combined_mask = np.zeros_like(image, dtype=np.uint8)

        for i, (box, class_id) in enumerate(zip(boxes, classes)):
            color = self.colors[class_id]
            if mask_maps is None:
                # No mask, just fill bounding box area
                if len(box) == 4:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(combined_mask, (x1, y1), (x2, y2), color, -1)
                elif len(box) == 8:
                    pts = np.array(box, dtype=np.int32).reshape((-1, 1, 2))
                    cv2.fillPoly(combined_mask, [pts], color)
            else:
                # With mask maps
                if len(box) == 4:
                    x1, y1, x2, y2 = map(int, box)
                elif len(box) == 8:
                    pts = np.array(box, dtype=np.int32).reshape((-1, 2))
                    x1, y1 = np.min(pts[:, 0]), np.min(pts[:, 1])
                    x2, y2 = np.max(pts[:, 0]), np.max(pts[:, 1])
                else:
                    raise ValueError("Box format not recognized.")

                crop_mask = mask_maps[i][y1:y2, x1:x2, np.newaxis]
                crop_mask_img = combined_mask[y1:y2, x1:x2]
                crop_mask_img = crop_mask_img * (1 - crop_mask) + crop_mask * color
                combined_mask[y1:y2, x1:x2] = crop_mask_img

        image = cv2.addWeighted(combined_mask, mask_alpha, image, 1 - mask_alpha, 0)
        return image

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
        for idx, (x, y, conf) in enumerate(keypoints):
            if conf > conf_threshold:
                cv2.circle(image, (int(x), int(y)), circle_radius, self.keypoint_color, -1, lineType=cv2.LINE_AA)

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
        for joint in self.skeleton:
            idx1, idx2 = joint
            if keypoints[idx1][2] > conf_threshold and keypoints[idx2][2] > conf_threshold:
                x1_kp, y1_kp = int(keypoints[idx1][0]), int(keypoints[idx1][1])
                x2_kp, y2_kp = int(keypoints[idx2][0]), int(keypoints[idx2][1])
                # cv2.line(image, (x1_kp, y1_kp), (x2_kp, y2_kp), self.skeleton_color, line_thickness)
                cv2.line(image, (x1_kp, y1_kp), (x2_kp, y2_kp), self.skeleton_color, line_thickness,
                         lineType=cv2.LINE_AA)

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
        if class_name is not None:
            label = class_name
            if class_name in self.cls_names:
                idx = self.cls_names.index(class_name)
                color = self.colors[idx]
            else:
                color = (0, 255, 0)
        elif class_id is not None:
            label = self.cls_names[class_id]
            color = self.colors[class_id]
        else:
            raise ValueError("Either class_name or class_id must be provided.")

        # If custom_label is provided, use it. Otherwise use default text.
        text = custom_label if custom_label is not None else f"{label}: {prob * 100:.2f}%"

        img = image.copy()
        height, width, _ = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = max(0.5, min(1.5, width / 600))
        thickness = max(1, int(width / 500))

        # If text contains Chinese, use PIL
        if self.contains_chinese(text):
            # For Chinese text, we can still do transparency by blending background first
            # Create overlay for the rectangle
            overlay = img.copy()
            (text_width, text_height), _ = cv2.getTextSize("Placeholder", font, font_scale, thickness)
            # Estimate text size with PIL instead of this placeholder if needed

            # Since we are using PIL for text, let's do a rough estimate or draw the background slightly larger
            # We'll finalize text size with PIL after blending
            # For simplicity, let's first do a rectangle at the top center
            estimated_text_w, estimated_text_h = int(width * 0.3), int(height * 0.05)
            text_x = (width - estimated_text_w) // 2
            text_y = estimated_text_h + 20

            cv2.rectangle(overlay,
                          (text_x - 10, text_y - estimated_text_h - 10),
                          (text_x + estimated_text_w + 10, text_y + 10),
                          color, -1)

            # Blend the overlay
            cv2.addWeighted(overlay, bg_alpha, img, 1 - bg_alpha, 0, img)

            # Now draw the text with PIL after blending
            text_annotations = [(text, (0, 0, width, height), color, font_scale, thickness, 'rect')]
            img = self.draw_all_texts_pil(img, text_annotations)

        else:
            # Non-Chinese text version
            (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
            text_height = int(text_height * 1.2)
            text_x = (width - text_width) // 2
            text_y = text_height + 20

            # Create overlay
            overlay = img.copy()
            cv2.rectangle(overlay, (text_x - 5, text_y - text_height - 5),
                          (text_x + text_width + 5, text_y + 5),
                          color, -1)
            # Blend overlay into img
            cv2.addWeighted(overlay, bg_alpha, img, 1 - bg_alpha, 0, img)

            # Draw text (without blending) on the final image
            cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

        return img


class IMDetectorVisualPIL:
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
            >>> # Initialize IMDetectorVisual with default settings
            >>> visualizer = IMDetectorVisualPIL()
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
        self.cls_names = cls_names if cls_names is not None else default_class_names
        self.colors = colors if colors is not None else get_predefined_colors(class_names=self.cls_names)

        # Default skeleton structure (COCO keypoints order)
        self.skeleton = skeleton if skeleton is not None else [
            (15, 13), (13, 11), (16, 14), (14, 12),
            (11, 12), (5, 11), (6, 12), (5, 6),
            (5, 7), (6, 8), (7, 9), (8, 10),
            (1, 2), (0, 1), (0, 2), (1, 3), (2, 4),
            (3, 5), (4, 6)
        ]

        # Font cache for text rendering
        self.font_cache = {}

        self.keypoint_color = keypoint_color
        self.skeleton_color = skeleton_color

        # Attempt to load a font for Chinese characters
        import os
        font_path = "C:/Windows/Fonts/simkai.ttf"  # SimKai font path
        if not os.path.exists(font_path):
            font_path = "simkai.ttf"
        try:
            self.chinese_font_base = ImageFont.truetype(font_path, 20)  # Default font size 20
        except IOError:
            print("Font file not found. Using default font.")
            self.chinese_font_base = ImageFont.load_default()

    def set_params(self, cls_names: Optional[List[str]] = None,
                   colors: Optional[List[Tuple[int, int, int]]] = None):
        """
        Set class names and corresponding colors for visualization.

        Args:
            cls_names (Optional[List[str]]): List of class names. If None, defaults will be used.
            colors (Optional[List[Tuple[int, int, int]]]): List of colors. If None, defaults will be used.
        """
        self.cls_names = cls_names if cls_names is not None else default_class_names
        self.colors = colors if colors is not None else get_predefined_colors(class_names=self.cls_names)

    def get_cached_font(self, font_size: int):
        """
        Retrieves or generates a font object of a given size, using a cache for performance optimization.

        Args:
            font_size (int): The size (in points) for the desired font.

        Returns:
            ImageFont: A PIL font object for rendering text.

        Example:
            >>> # Initialize the IMDetectorVisual object
            >>> visualizer = IMDetectorVisualPIL()
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
                >>> visualizer = IMDetectorVisualPIL()
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
        # Convert input image from BGR to RGB
        image_rgb = image[..., ::-1]  # Flip color channels from BGR to RGB
        pil_img = Image.fromarray(image_rgb)

        # If detection results are provided, draw detections (boxes, masks, keypoints)
        if boxes is not None and scores is not None and class_ids is not None:
            pil_img = self.draw_detections(
                pil_img, boxes, scores, class_ids, keypoints, mask_maps, mask_alpha, labels
            )

        # If classification results are provided, draw classification information
        if cls_prob is not None and (cls_class_id is not None or cls_class_name is not None):
            pil_img = self.draw_classification(
                pil_img, cls_prob, cls_class_id, cls_class_name, cls_label, bg_alpha
            )

        # Convert the image back to BGR format and return
        out_image = np.array(pil_img)[..., ::-1]  # Flip RGB to BGR
        return out_image

    @staticmethod
    def contains_chinese(text: str) -> bool:
        """
            Checks if a given string contains any Chinese characters.

            Args:
                text (str): The input string to check.

            Returns:
                bool: True if the string contains Chinese characters, False otherwise.

            Example:
                >>> IMDetectorVisualPIL.contains_chinese("Hello World")  # False
                >>> IMDetectorVisualPIL.contains_chinese("你好世界")      # True
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
                >>> visualizer = IMDetectorVisualPIL(
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
        # Convert input lists to numpy arrays if necessary for unified processing
        if isinstance(boxes, list):
            boxes = np.array(boxes)
        if isinstance(scores, list):
            scores = np.array(scores)
        if isinstance(class_ids, list):
            class_ids = np.array(class_ids)

        # Extract image dimensions
        img_width, img_height = pil_img.size

        # Calculate visual element sizes based on image dimensions
        box_line_thickness = max(round(min(img_height, img_width) * 0.0015), 2)  # Thickness of bounding box lines
        font_size = max(int(round(min(img_height, img_width) * 0.0010)), 1)  # Font size for text annotations
        text_thickness = max(round(min(img_height, img_width) * 0.0015), 1)  # Text outline thickness
        keypoint_radius = max(round(min(img_height, img_width) * 0.0035), 3)  # Keypoint radius for circles
        skeleton_line_thickness = max(round(min(img_height, img_width) * 0.0015), 2)  # Line thickness for skeletons

        # Draw instance masks if provided
        pil_img = self.draw_masks(pil_img, boxes, class_ids, mask_alpha, mask_maps)

        # Process keypoints for skeleton and keypoint rendering
        if keypoints is not None:
            if isinstance(keypoints, list):
                keypoints = np.array(keypoints)
        else:
            keypoints = np.array([None] * len(boxes))  # Placeholder if no keypoints provided

        # Process bounding boxes into labeled and categorized formats
        processed_boxes = []
        for box in boxes:
            if len(box) == 4:
                processed_boxes.append(('rect', box))  # Rectangular box
            elif len(box) == 8:
                processed_boxes.append(('rotated', box))  # Rotated box
            else:
                raise ValueError("Box format not recognized. Must have 4 or 8 coordinates.")

        # Prepare to aggregate annotations (bounding boxes, labels, keypoints, etc.)
        text_annotations = []
        rect_boxes = []  # Rectangular boxes
        rotated_boxes = []  # Rotated boxes
        rect_colors = []  # Colors for rectangular boxes
        rotated_colors = []  # Colors for rotated boxes
        keypoints_list = []  # Keypoints and associated colors
        need_pil = False  # Placeholder for extended font rendering

        # Aggregate detection results
        for i, (class_id, (box_type, box), score, kp) in enumerate(
                zip(class_ids, processed_boxes, scores, keypoints)):
            color = self.colors[class_id]  # Get color for the class ID
            label = self.cls_names[class_id]  # Get class name for the class ID
            caption = labels[i] if (
                    labels is not None and len(labels) > i) else f'{label} {int(score * 100)}%'  # Label text

            # Check if label contains Chinese characters (affects text rendering)
            if self.contains_chinese(caption):
                need_pil = True

            # Append relevant annotation details
            text_annotations.append((caption, box, color, font_size, text_thickness, box_type))

            # Separate bounding boxes by type (rectangular vs rotated)
            if box_type == 'rect':
                rect_boxes.append(box)
                rect_colors.append(color)
            else:
                rotated_boxes.append(box)
                rotated_colors.append(color)

            # If keypoints provided, store them with corresponding color
            if kp is not None:
                keypoints_list.append((kp, color))

        # Draw bounding boxes (both rectangular and rotated)
        pil_img = self.draw_all_boxes(pil_img, rect_boxes, rect_colors, rotated_boxes, rotated_colors,
                                      thickness=box_line_thickness)

        # Draw keypoints and skeletons if provided
        for kp, _ in keypoints_list:
            pil_img = self.draw_skeleton(pil_img, kp, line_thickness=skeleton_line_thickness)  # Skeleton
            pil_img = self.draw_keypoints(pil_img, kp, circle_radius=keypoint_radius)  # Keypoints

        # Draw text annotations using PIL (supports both English and Chinese characters)
        pil_img = self.draw_all_texts_pil(pil_img, text_annotations)

        return pil_img

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
                >>> visualizer = IMDetectorVisualPIL()
                >>> img_with_boxes = visualizer.draw_all_boxes(
                >>>     img,
                >>>     rect_boxes=rect_boxes,
                >>>     rect_colors=rect_colors,
                >>>     rotated_boxes=rotated_boxes,
                >>>     rotated_colors=rotated_colors
                >>> )
                >>> img_with_boxes.show()
            """
        draw = ImageDraw.Draw(pil_img)

        # Draw rectangular boxes
        for box, color in zip(rect_boxes, rect_colors):
            x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers for consistency
            draw.rectangle([x1, y1, x2, y2], outline=(color[2], color[1], color[0]), width=thickness)

        # Draw rotated boxes
        for box, color in zip(rotated_boxes, rotated_colors):
            pts = list(map(int, box))  # Convert coordinates to integers
            polygon = [(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)]  # Convert flat list to polygon points
            draw.polygon(polygon, outline=(color[2], color[1], color[0]))

        return pil_img

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
                >>> visualizer = IMDetectorVisualPIL()
                >>> annotated_img = visualizer.draw_all_texts_pil(img, annotations)
                >>> annotated_img.show()
            """
        draw = ImageDraw.Draw(pil_img)

        for text, box, color, font_size, text_thickness, box_type in text_annotations:
            # Compute the starting position for the text
            x0, y0 = self.compute_text_position(box, box_type)

            # Adjust font size and load cached font for text rendering
            font_size_pil = max(int(font_size * 40), 12)  # Scale font size for larger displays
            font = self.get_cached_font(font_size_pil)
            text_size = draw.textsize(text, font=font)
            y0 = max(y0 - text_size[1], 0)  # Adjust y-coordinate to prevent overflow

            # Draw a background rectangle for the text
            draw.rectangle([x0, y0, x0 + text_size[0], y0 + text_size[1]], fill=(color[2], color[1], color[0]))

            # Draw the text (in white)
            draw.text((x0, y0), text, font=font, fill=(255, 255, 255))

        return pil_img

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
        if box_type == 'rect':
            x1, y1, x2, y2 = map(int, box)
            return x1, y1
        else:
            pts = np.array(box, dtype=np.int32).reshape((-1, 2))  # Reshape to Nx2 format
            pts_sorted = pts[np.lexsort((pts[:, 0], pts[:, 1]))]  # Sort by y (primary) and x (secondary)
            top_two = pts_sorted[:2]  # Extract the top two points
            top_mid_x = int((top_two[0][0] + top_two[1][0]) / 2)  # Compute midpoint x
            top_mid_y = int((top_two[0][1] + top_two[1][1]) / 2)  # Compute midpoint y
            return top_mid_x, top_mid_y

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
                >>> visualizer = IMDetectorVisualPIL()
                >>> img_with_masks = visualizer.draw_masks(img, boxes, classes, mask_alpha)
                >>> img_with_masks.show()
            """
        img_width, img_height = pil_img.size

        # Create an empty RGB layer to draw the masks
        mask_layer = Image.new("RGB", (img_width, img_height), (0, 0, 0))
        mask_draw = ImageDraw.Draw(mask_layer)

        for i, (box, class_id) in enumerate(zip(boxes, classes)):
            color = self.colors[class_id]
            fill_color = (color[2], color[1], color[0])

            if mask_maps is None:
                # Fill the bounding box area directly if no mask is provided
                if len(box) == 4:  # Rectangular box
                    x1, y1, x2, y2 = map(int, box)
                    mask_draw.rectangle([x1, y1, x2, y2], fill=fill_color)
                elif len(box) == 8:  # Rotated box
                    pts = list(map(int, box))
                    polygon = [(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)]
                    mask_draw.polygon(polygon, fill=fill_color)
            else:
                # Use provided mask maps to draw the mask
                # Extract the relevant region of the mask
                if len(box) == 4:
                    x1, y1, x2, y2 = map(int, box)
                elif len(box) == 8:
                    pts = np.array(box, dtype=np.int32).reshape((-1, 2))
                    x1, y1 = np.min(pts[:, 0]), np.min(pts[:, 1])
                    x2, y2 = np.max(pts[:, 0]), np.max(pts[:, 1])
                else:
                    raise ValueError("Box format not recognized.")

                crop_mask = mask_maps[i][y1:y2, x1:x2]
                crop_array = np.array(mask_layer)
                crop_region = crop_array[y1:y2, x1:x2].copy()
                crop_region[crop_mask > 0.5] = [color[2], color[1], color[0]]
                crop_array[y1:y2, x1:x2] = crop_region
                mask_layer = Image.fromarray(crop_array)

        # Blend the original image with the mask layer
        pil_img = Image.blend(pil_img, mask_layer, mask_alpha)
        return pil_img

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
                >>> visualizer = IMDetectorVisualPIL()
                >>> img_with_keypoints = visualizer.draw_keypoints(img, keypoints, conf_threshold=0.5, circle_radius=5)
                >>> img_with_keypoints.show()
            """
        draw = ImageDraw.Draw(pil_img)

        for x, y, conf in keypoints:
            if conf > conf_threshold:  # Draw only if confidence exceeds threshold
                # Define the circle boundary
                left_up = (int(x) - circle_radius, int(y) - circle_radius)
                right_down = (int(x) + circle_radius, int(y) + circle_radius)

                # Draw the circle
                draw.ellipse([left_up, right_down],
                             fill=(self.keypoint_color[2], self.keypoint_color[1], self.keypoint_color[0]))

        return pil_img

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
                >>> visualizer = IMDetectorVisualPIL(skeleton=[[0, 1], [1, 2]])
                >>> img_with_skeleton = visualizer.draw_skeleton(img, keypoints, conf_threshold=0.5, line_thickness=3)
                >>> img_with_skeleton.show()
            """
        # Create an anti-aliased drawing context
        draw = Draw(pil_img)

        # Define the skeleton color in RGB order
        line_color = self.skeleton_color[::-1]

        for joint in self.skeleton:
            idx1, idx2 = joint
            if keypoints[idx1][2] > conf_threshold and keypoints[idx2][2] > conf_threshold:
                x1, y1 = int(keypoints[idx1][0]), int(keypoints[idx1][1])
                x2, y2 = int(keypoints[idx2][0]), int(keypoints[idx2][1])

                # Draw a line connecting the two keypoints
                pen = Pen(line_color, line_thickness)
                draw.line((x1, y1, x2, y2), pen)

        draw.flush()  # Apply drawing operations
        return pil_img

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
                >>> visualizer = IMDetectorVisualPIL(cls_names=["Cat", "Dog"], colors=[(255, 0, 0), (0, 255, 0)])
                >>> annotated_img = visualizer.draw_classification(
                >>>     pil_img=img,
                >>>     prob=0.95,
                >>>     class_id=1
                >>> )
                >>> Image.fromarray(annotated_img[..., ::-1]).show()
            """
        # Convert input NumPy array format to PIL if needed
        if isinstance(pil_img, np.ndarray):
            if pil_img.ndim == 3 and pil_img.shape[2] == 3:
                pil_img = Image.fromarray(pil_img[..., ::-1])  # Convert BGR to RGB
            else:
                pil_img = Image.fromarray(pil_img)

        img_width, img_height = pil_img.size

        # Get class name, color, and label text
        if class_name is not None:
            label = class_name
            if class_name in self.cls_names:
                idx = self.cls_names.index(class_name)
                color = self.colors[idx]
            else:
                color = (0, 255, 0)  # Default color if class name is unknown
        elif class_id is not None:
            label = self.cls_names[class_id]
            color = self.colors[class_id]
        else:
            raise ValueError("Either class_name or class_id must be provided.")

        text = custom_label if custom_label is not None else f"{label}: {prob * 100:.2f}%"

        # Calculate text box parameters
        font_scale = max(0.5, min(1.5, img_width / 600))  # Dynamic font scaling based on image width
        font_size_pil = max(int(font_scale * 40), 12)
        font = self.get_cached_font(font_size_pil)

        text_width, text_height = font.getsize(text)  # Calculate text box size
        text_x = (img_width - text_width) // 2  # Center the text horizontally
        text_y = 20  # Fixed top padding for the text
        padding_x = 5  # Horizontal padding for text background
        padding_y = 2  # Vertical padding for text background

        # Create an overlay for the background box
        overlay = pil_img.copy()
        draw_overlay = ImageDraw.Draw(overlay)
        draw_overlay.rectangle((text_x - padding_x, text_y - padding_y,
                                text_x + text_width + padding_x, text_y + text_height + padding_y),
                               fill=(color[2], color[1], color[0]))  # Background box color

        # Blend the image with the background box
        pil_img = Image.blend(pil_img, overlay, bg_alpha)

        # Draw the classification label text
        draw = ImageDraw.Draw(pil_img)
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))  # White text color

        # Convert the result back to a NumPy array and return
        return np.array(pil_img)[..., ::-1]  # Convert from RGB to BGR
