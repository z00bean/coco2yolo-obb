# COCO to YOLO OBB Converter

A Python tool that converts COCO segmentation annotations to YOLO Oriented Bounding Box (OBB) format in a single step. This tool simplifies the conversion process and produces annotations suitable for training YOLO models with oriented bounding boxes.

## Features

- ✅ **Single-step conversion** - No more two-step process
- ✅ **Command-line interface** - Easy to use with argparse
- ✅ **Robust error handling** - Graceful handling of edge cases
- ✅ **Class mapping support** - Flexible class ID remapping
- ✅ **Progress tracking** - Real-time conversion progress
- ✅ **Batch processing** - Handles multiple images efficiently

## Installation

### Prerequisites

```bash
pip install numpy opencv-python
```

### Clone the repository

```bash
git clone https://github.com/z00bean/coco2yolo-obb.git
cd coco2yolo-obb
```

## Usage

### Basic Usage

Convert COCO annotations to YOLO OBB format:

```bash
python coco2yolo_obb.py annotations.json
```

### Advanced Usage

Specify custom output directory:

```bash
python coco2yolo_obb.py annotations.json --output-dir yolo_labels
```

Use custom class mapping:

```bash
python coco2yolo_obb.py annotations.json --class-mapping "1:0 2:1 3:2"
```

### Command Line Options

```
positional arguments:
  json_file             Path to COCO annotation JSON file

optional arguments:
  -h, --help            Show help message and exit
  --output-dir, -o      Output directory for YOLO annotation files (default: labels)
  --class-mapping       Class mapping in format "coco_id:yolo_id coco_id:yolo_id"
  --version             Show program's version number and exit
```

## YOLO OBB Format

The YOLO OBB format uses oriented bounding boxes defined by 4 corner coordinates:

```
<class-index> <x1> <y1> <x2> <y2> <x3> <y3> <x4> <y4>
```

Where:
- `class-index`: Integer representing the object class
- `x1, y1, x2, y2, x3, y3, x4, y4`: Four corner coordinates of the oriented bounding box, normalized to [0, 1]

### Example Output

```
0 0.780811 0.743961 0.782371 0.746860 0.777691 0.752174 0.776131 0.749758
1 0.234567 0.345678 0.345678 0.456789 0.456789 0.567890 0.567890 0.678901
```

## File Structure

```
coco2yolo-obb/
├── coco2yolo_obb.py          # Main conversion script
├── coco2yolo-obb/            # Legacy scripts (deprecated)
│   ├── 1.coco2yolo-obb.py
│   └── 2.convert_OBB.py
├── README.md
├── LICENSE
└── .gitignore
```

## Migration from Legacy Scripts

If you were using the old two-step process:

**Old way:**
```bash
python 1.coco2yolo-obb.py --json_file annotations.json --output_folder labels-obb
python 2.convert_OBB.py  # (required manual editing of paths)
```

**New way:**
```bash
python coco2yolo_obb.py annotations.json --output-dir labels
```

## Error Handling

The tool includes robust error handling for common issues:

- Missing or invalid JSON files
- Missing required dependencies
- Invalid segmentation data
- Missing image information
- Class mapping errors

## Future Plans

- 📦 **PyPI Package** - Install via `pip install coco2yolo-obb`
- 🔧 **Additional formats** - Support for more annotation formats
- 🚀 **Performance optimization** - Faster processing for large datasets
- 📊 **Validation tools** - Verify conversion accuracy

## Contributing

Contributions are welcome! Please feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [YOLO OBB Dataset Format Documentation](https://docs.ultralytics.com/datasets/obb/)
- [COCO Dataset Format](https://cocodataset.org/#format-data)
