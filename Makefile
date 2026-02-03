.PHONY: help install test clean example build upload

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run example usage"
	@echo "  clean      - Clean up generated files"
	@echo "  example    - Run example conversion"
	@echo "  build      - Build package for PyPI"
	@echo "  upload     - Upload to PyPI (requires credentials)"

install:
	pip install -r requirements.txt

test: install
	python example_usage.py

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf example_output_basic custom_labels_dir mapped_labels
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

example: install
	python example_usage.py

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

# Development helpers
lint:
	python -m flake8 coco2yolo_obb.py --max-line-length=100

format:
	python -m black coco2yolo_obb.py example_usage.py