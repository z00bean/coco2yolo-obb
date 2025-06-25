# Convert COCO segmentation json to class_id, x, y, length, breadth, angle.
# Note: class_id, x, y, length, breadth, angle is not yolo OBB format.
# After converting to this format use convert_OBB.py to obtain the YOLO OBB annotation.

import json
import os
import math
import numpy as np
import cv2  # Required for calculating oriented bounding box
import argparse

def calculate_oriented_bounding_box(segmentation):
    """
    Calculate the minimum area oriented bounding box from a segmentation polygon.
    """
    # Convert segmentation to a NumPy array of shape (-1, 1, 2).
    contour = np.array(segmentation).reshape((-1, 1, 2)).astype(np.float32)

    # Calculate the minimum area oriented bounding box.
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Normalize the box points
    box_normalized = np.zeros_like(box, dtype=np.float32)
    box_normalized[:, 0] = box[:, 0] - np.min(box[:, 0])
    box_normalized[:, 1] = box[:, 1] - np.min(box[:, 1])

    return rect, box_normalized

def convert_coco_to_yolo_segmentation(json_file, output_folder="labels-obb"):
    """
    Convert COCO annotations to YOLO format with oriented bounding boxes.
    """
    # Load the JSON file
    with open(json_file, 'r') as file:
        coco_data = json.load(file)

    # Create an output folder to store YOLO segmentation annotations
    os.makedirs(output_folder, exist_ok=True)

    # Preprocess images into a dictionary for efficient lookup
    images_dict = {image['id']: image for image in coco_data['images']}

    # Extract annotations from the COCO JSON data
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        segmentation = annotation['segmentation'][0]  # Assuming the first polygon if there are multiple

        image = images_dict[image_id]
        image_filename = os.path.splitext(os.path.basename(image['file_name']))[0]  # Removing the extension
        image_width, image_height = image['width'], image['height']

        # Calculate oriented bounding box
        rect, box_normalized = calculate_oriented_bounding_box(segmentation)

        # Calculate YOLO format parameters (center_x, center_y, width, height, angle)
        center_x, center_y = rect[0]
        width, height = rect[1]
        angle = rect[2]

        yolo_format = f"{(center_x / image_width):.6f} {(center_y / image_height):.6f} {(width / image_width):.6f} {(height / image_height):.6f} {angle:.6f}"

        # Generate the YOLO segmentation annotation line for oriented bounding box
        yolo_annotation = f"{category_id} {yolo_format}"

        # Save the YOLO segmentation annotation in a file
        output_filename = os.path.join(output_folder, f"{image_filename}.txt")
        with open(output_filename, 'a') as file:
            file.write(yolo_annotation + '\n')

    print(f"Conversion completed. YOLO segmentation annotations saved in '{output_folder}' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO annotations to YOLO segmentation format with oriented bounding boxes.")
    parser.add_argument("--json_file", type=str, required=True, help="Path to COCO annotation JSON file")
    parser.add_argument("--output_folder", type=str, default="labels-obb", help="Path to the output folder")

    args = parser.parse_args()
    convert_coco_to_yolo_segmentation(args.json_file, args.output_folder)
