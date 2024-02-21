### coco2yolo-obb
COCO Polygons to YOLO OBB converter. 

# COCO to YOLO Segmentation Converter with Oriented Bounding Boxes

This Python script simplifies the conversion of COCO segmentation annotations to YOLO segmentation format, specifically using oriented bounding boxes (OBB). The resulting YOLO OBB format is suitable for training YOLO segmentation models.

## YOLO OBB Segmentation Data Format

The YOLO OBB dataset format is structured as follows:

- One text file per image: Each image in the dataset has a corresponding text file with the same name as the image file and the ".txt" extension.
- One row per object: Each row in the text file corresponds to one object instance in the image.
- Object information per row: Each row contains the following information about the object instance:
  - Object class index: An integer representing the class of the object.
  - Oriented bounding box coordinates: Four pairs of coordinates (x1, y1, x2, y2, x3, y3, x4, y4) defining the corners of the oriented bounding box, normalized to be between 0 and 1.

The format for a single row in the YOLO OBB dataset file is as follows: 

```<class-index>, <x1>, <y1>, <x2>, <y2>, <x3>, <y3>, <x4>, <y4>```


## Usage

1. Clone the repository:
   
   ```git clone https://github.com/z00bean/coco2yolo-obb.git```

3. Navigate to the repository:
   
   ```cd coco2yolo-obb```
   
4. Run the conversion script:
   
   ```python COCO2YOLO-obb.py --json_file path/to/coco_annotations.json --output_folder path/to/output_folder```
  - Replace path/to/coco_annotations.json with the actual path to your COCO annotation JSON file.
  - Replace path/to/output_folder with the desired output folder path.

## The YOLO OBB segmentation annotations will be saved in the specified output folder

An example of an object of class 0 in YOLO OBB format:

```0, 0.780811, 0.743961, 0.782371, 0.74686, 0.777691, 0.752174, 0.776131, 0.749758```

## Contributing
If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request. Contributions are welcome!

## References

[YOLO OBB Dataset Format Documentation](https://docs.ultralytics.com/datasets/obb/)
