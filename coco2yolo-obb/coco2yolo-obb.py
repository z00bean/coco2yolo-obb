import json
import os
import math
import argparse

def calculate_oriented_bounding_box(segmentation):
    x_coords = segmentation[0][::2]
    y_coords = segmentation[0][1::2]
    angle = math.atan2(y_coords[1] - y_coords[0], x_coords[1] - x_coords[0])
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    rotated_x_coords = [cos_angle * x - sin_angle * y for x, y in zip(x_coords, y_coords)]
    rotated_y_coords = [sin_angle * x + cos_angle * y for x, y in zip(x_coords, y_coords)]

    min_x = min(rotated_x_coords)
    max_x = max(rotated_x_coords)
    min_y = min(rotated_y_coords)
    max_y = max(rotated_y_coords)

    return min_x, min_y, max_x, max_y

def convert_coco_to_yolo_segmentation(json_file, output_folder="labels-obb"):
    # Load the JSON file
    with open(json_file, 'r') as file:
        coco_data = json.load(file)

    # Create an output folder to store YOLO segmentation annotations
    os.makedirs(output_folder, exist_ok=True)

    # Extract annotations from the COCO JSON data
    annotations = coco_data['annotations']
    for annotation in annotations:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        segmentation = annotation['segmentation']
        bbox = annotation['bbox']

        # Find the image filename from the COCO data
        for image in coco_data['images']:
            if image['id'] == image_id:
                image_filename = os.path.basename(image['file_name'])
                image_filename = os.path.splitext(image_filename)[0]  # Removing the extension.
                image_width = image['width']
                image_height = image['height']
                break

        # Calculate oriented bounding box
        min_x, min_y, max_x, max_y = calculate_oriented_bounding_box(segmentation)

        # Convert COCO segmentation to YOLO segmentation format for oriented bounding box
        yolo_segmentation = f"{min_x / image_width:.5f} {min_y / image_height:.5f} {max_x / image_width:.5f} {max_y / image_height:.5f}"

        # Generate the YOLO segmentation annotation line for oriented bounding box
        yolo_annotation = f"{category_id} {yolo_segmentation}"

        # Save the YOLO segmentation annotation in a file
        output_filename = os.path.join(output_folder, f"{image_filename}.txt")
        with open(output_filename, 'a+') as file:
            file.write(yolo_annotation + '\n')

    print("Conversion completed. YOLO segmentation annotations saved in '{}' folder.".format(output_folder))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO annotations to YOLO segmentation format with oriented bounding boxes.")
    parser.add_argument("--json_file", type=str, default="annotations.json", help="Path to COCO annotation JSON file")
    parser.add_argument("--output_folder", type=str, default="labels-obb", help="Path to the output folder")

    args = parser.parse_args()
    convert_coco_to_yolo_segmentation(args.json_file, args.output_folder)
