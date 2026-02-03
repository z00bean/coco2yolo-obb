#!/usr/bin/env python3
"""
COCO to YOLO OBB Converter

Converts COCO segmentation annotations to YOLO Oriented Bounding Box (OBB) format
in a single step. The output format uses 4 corner coordinates (x1,y1,x2,y2,x3,y3,x4,y4)
normalized to [0,1] range.

Author: Your Name
License: MIT
"""

import json
import os
import math
import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

try:
    import numpy as np
    import cv2
except ImportError as e:
    print(f"Error: Required dependency missing: {e}")
    print("Please install required packages: pip install numpy opencv-python")
    sys.exit(1)


def calculate_obb_corners(segmentation: List[float], image_width: int, image_height: int) -> List[float]:
    """
    Calculate oriented bounding box corners from segmentation polygon.
    
    Args:
        segmentation: List of polygon coordinates [x1, y1, x2, y2, ...]
        image_width: Width of the image
        image_height: Height of the image
        
    Returns:
        List of 8 normalized corner coordinates [x1, y1, x2, y2, x3, y3, x4, y4]
    """
    # Convert segmentation to numpy array
    points = np.array(segmentation).reshape(-1, 2).astype(np.float32)
    
    # Calculate minimum area rectangle
    rect = cv2.minAreaRect(points)
    box_points = cv2.boxPoints(rect)
    
    # Normalize coordinates to [0, 1] range
    normalized_corners = []
    for point in box_points:
        x_norm = point[0] / image_width
        y_norm = point[1] / image_height
        normalized_corners.extend([x_norm, y_norm])
    
    return normalized_corners


def convert_coco_to_yolo_obb(
    json_file: str, 
    output_dir: str = "labels", 
    class_mapping: Dict[int, int] = None
) -> None:
    """
    Convert COCO annotations to YOLO OBB format.
    
    Args:
        json_file: Path to COCO annotation JSON file
        output_dir: Output directory for YOLO annotation files
        class_mapping: Optional mapping from COCO category IDs to YOLO class IDs
    """
    # Load COCO annotations
    try:
        with open(json_file, 'r') as f:
            coco_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find JSON file: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {json_file}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create image lookup dictionary
    images_dict = {img['id']: img for img in coco_data['images']}
    
    # Create class mapping if not provided
    if class_mapping is None:
        categories = {cat['id']: idx for idx, cat in enumerate(coco_data['categories'])}
    else:
        categories = class_mapping
    
    # Process annotations
    annotation_count = 0
    file_count = 0
    
    # Group annotations by image
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    print(f"Processing {len(annotations_by_image)} images...")
    
    for image_id, annotations in annotations_by_image.items():
        if image_id not in images_dict:
            print(f"Warning: Image ID {image_id} not found in images list")
            continue
            
        image_info = images_dict[image_id]
        image_filename = Path(image_info['file_name']).stem
        image_width = image_info['width']
        image_height = image_info['height']
        
        # Create output file for this image
        output_file = output_path / f"{image_filename}.txt"
        
        with open(output_file, 'w') as f:
            for ann in annotations:
                # Skip annotations without segmentation
                if 'segmentation' not in ann or not ann['segmentation']:
                    continue
                
                category_id = ann['category_id']
                if category_id not in categories:
                    print(f"Warning: Category ID {category_id} not found in mapping")
                    continue
                
                class_id = categories[category_id]
                
                # Handle multiple polygons (take the first one)
                segmentation = ann['segmentation'][0] if isinstance(ann['segmentation'][0], list) else ann['segmentation']
                
                # Skip if segmentation has less than 6 points (3 vertices minimum)
                if len(segmentation) < 6:
                    continue
                
                try:
                    # Calculate OBB corners
                    corners = calculate_obb_corners(segmentation, image_width, image_height)
                    
                    # Format: class_id x1 y1 x2 y2 x3 y3 x4 y4
                    line = f"{class_id} " + " ".join(f"{coord:.6f}" for coord in corners)
                    f.write(line + "\n")
                    annotation_count += 1
                    
                except Exception as e:
                    print(f"Warning: Failed to process annotation {ann['id']}: {e}")
                    continue
        
        file_count += 1
        if file_count % 100 == 0:
            print(f"Processed {file_count} files...")
    
    print(f"\nConversion completed!")
    print(f"- Processed {file_count} images")
    print(f"- Generated {annotation_count} annotations")
    print(f"- Output saved to: {output_path.absolute()}")


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Convert COCO segmentation annotations to YOLO OBB format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s annotations.json
  %(prog)s annotations.json --output-dir yolo_labels
  %(prog)s annotations.json --output-dir labels --class-mapping 1:0 2:1 3:2
        """
    )
    
    parser.add_argument(
        'json_file',
        help='Path to COCO annotation JSON file'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='labels',
        help='Output directory for YOLO annotation files (default: labels)'
    )
    
    parser.add_argument(
        '--class-mapping',
        help='Class mapping in format "coco_id:yolo_id coco_id:yolo_id" (optional)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Parse class mapping if provided
    class_mapping = None
    if args.class_mapping:
        try:
            class_mapping = {}
            for mapping in args.class_mapping.split():
                coco_id, yolo_id = mapping.split(':')
                class_mapping[int(coco_id)] = int(yolo_id)
        except ValueError:
            print("Error: Invalid class mapping format. Use 'coco_id:yolo_id coco_id:yolo_id'")
            sys.exit(1)
    
    # Run conversion
    convert_coco_to_yolo_obb(args.json_file, args.output_dir, class_mapping)


if __name__ == "__main__":
    main()