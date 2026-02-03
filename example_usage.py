#!/usr/bin/env python3
"""
Example usage of the coco2yolo_obb converter.

This script demonstrates how to use the converter programmatically
and shows different usage patterns.
"""

import json
import tempfile
import os
from pathlib import Path

# Import the converter (assuming it's in the same directory)
try:
    from coco2yolo_obb import convert_coco_to_yolo_obb
except ImportError:
    print("Please ensure coco2yolo_obb.py is in the same directory")
    exit(1)


def create_sample_coco_data():
    """Create a sample COCO annotation file for testing."""
    sample_data = {
        "images": [
            {
                "id": 1,
                "file_name": "image1.jpg",
                "width": 640,
                "height": 480
            },
            {
                "id": 2,
                "file_name": "image2.jpg", 
                "width": 800,
                "height": 600
            }
        ],
        "categories": [
            {"id": 1, "name": "person"},
            {"id": 2, "name": "car"},
            {"id": 3, "name": "bicycle"}
        ],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "segmentation": [[100, 100, 200, 100, 200, 200, 100, 200]]
            },
            {
                "id": 2,
                "image_id": 1,
                "category_id": 2,
                "segmentation": [[300, 150, 400, 150, 400, 250, 300, 250]]
            },
            {
                "id": 3,
                "image_id": 2,
                "category_id": 3,
                "segmentation": [[50, 50, 150, 50, 150, 150, 50, 150]]
            }
        ]
    }
    return sample_data


def example_basic_usage():
    """Example 1: Basic usage with default settings."""
    print("Example 1: Basic usage")
    print("-" * 40)
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(create_sample_coco_data(), f)
        json_file = f.name
    
    try:
        # Convert with default settings
        convert_coco_to_yolo_obb(json_file, "example_output_basic")
        print("✅ Basic conversion completed\n")
    finally:
        os.unlink(json_file)


def example_custom_output_dir():
    """Example 2: Custom output directory."""
    print("Example 2: Custom output directory")
    print("-" * 40)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(create_sample_coco_data(), f)
        json_file = f.name
    
    try:
        # Convert with custom output directory
        convert_coco_to_yolo_obb(json_file, "custom_labels_dir")
        print("✅ Custom output directory conversion completed\n")
    finally:
        os.unlink(json_file)


def example_class_mapping():
    """Example 3: Using class mapping."""
    print("Example 3: Class mapping")
    print("-" * 40)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(create_sample_coco_data(), f)
        json_file = f.name
    
    try:
        # Convert with class mapping: COCO ID -> YOLO ID
        class_mapping = {1: 0, 2: 1, 3: 2}  # person->0, car->1, bicycle->2
        convert_coco_to_yolo_obb(json_file, "mapped_labels", class_mapping)
        print("✅ Class mapping conversion completed\n")
    finally:
        os.unlink(json_file)


def show_output_files():
    """Show the generated output files."""
    print("Generated output files:")
    print("-" * 40)
    
    output_dirs = ["example_output_basic", "custom_labels_dir", "mapped_labels"]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            print(f"\n📁 {output_dir}/")
            for file in sorted(os.listdir(output_dir)):
                if file.endswith('.txt'):
                    file_path = os.path.join(output_dir, file)
                    print(f"  📄 {file}")
                    with open(file_path, 'r') as f:
                        content = f.read().strip()
                        for line in content.split('\n'):
                            if line:
                                print(f"    {line}")


if __name__ == "__main__":
    print("COCO to YOLO OBB Converter - Usage Examples")
    print("=" * 50)
    print()
    
    try:
        example_basic_usage()
        example_custom_output_dir()
        example_class_mapping()
        show_output_files()
        
        print("\n🎉 All examples completed successfully!")
        print("\nTo clean up generated files, run:")
        print("rm -rf example_output_basic custom_labels_dir mapped_labels")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Make sure you have numpy and opencv-python installed:")
        print("pip install numpy opencv-python")