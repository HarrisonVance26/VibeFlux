# IMcore

import os
import yaml
import random
from typing import List, Dict, Any

# Define the path to the colors.yaml file
CONF_YAML_PATH = os.path.join(os.path.dirname(__file__), 'VisualSet.yaml')


def load_predefined_colors() -> List[List[int]]:
    """
    Load predefined colors from the colors.yaml file.

    This function reads the colors.yaml file, which contains a list of RGB color values, and returns them as a list of lists.

    Returns:
        List[List[int]]: A list of colors, where each color is represented as a list of three integers [R, G, B]
        corresponding to the red, green, and blue color channels.
    """
    with open(CONF_YAML_PATH, 'r', encoding='utf-8') as file:
        colors_data = yaml.safe_load(file)
    return colors_data.get('DefColors', [])


# Predefined_Colors is a module-level variable that holds the list of predefined colors
DefColors: List[List[int]] = load_predefined_colors()


def generate_random_color() -> List[int]:
    """
    Generate a random RGB color.

    This function generates a random color represented as a list of three integers [R, G, B].

    Returns:
        List[int]: A list of three integers representing a random RGB color.
    """
    return [random.randint(0, 255) for _ in range(3)]


def get_predefined_colors(class_names: List[str] = None) -> List[List[int]]:
    """
    Get the list of predefined colors, extended if necessary to match the number of class names.

    This function returns the list of predefined colors loaded from the colors.yaml file. If the number of predefined colors
    is less than the number of class names, additional colors are generated and appended to the list.

    Args:
        class_names (List[str]): A list of class names for which colors are required.

    Returns:
        List[List[int]]: A list of colors, each represented as a list of three integers [R, G, B].
    """
    if class_names is None:
        return DefColors

    num_classes = len(class_names)
    num_colors = len(DefColors)

    if num_colors < num_classes:
        # Generate additional colors to match the number of class names
        additional_colors = [generate_random_color() for _ in range(num_classes - num_colors)]
        return DefColors + additional_colors

    return DefColors[:num_classes]


def load_names() -> Dict[str, str]:
    """
    Load initial category names from the coco.yaml file.

    This function reads the coco.yaml file, which contains a dictionary of English category names
    mapped to their corresponding names.

    Returns:
        Dict[str, str]: A dictionary where keys are English category names and values are names.
    """
    with open(CONF_YAML_PATH, 'r', encoding='utf-8') as file:
        coco_data = yaml.safe_load(file)
    return coco_data.get('names', {})


# Names is a module-level variable that holds the dictionary of category names
Names: Dict[str, str] = load_names()


def get_names() -> Dict[str, str]:
    """
    Get the dictionary of initial category names.

    This function returns the dictionary of category names loaded from the coco.yaml file.

    Returns:
        Dict[str, str]: A dictionary where keys are English category names and values are names.
    """
    return Names
