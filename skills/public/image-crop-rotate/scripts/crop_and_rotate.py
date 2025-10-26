#!/usr/bin/env python3
"""
Crop and rotate images.

This script crops an image to 50% of its size from the center
and rotates it 90 degrees clockwise.
"""

import sys
from pathlib import Path
from PIL import Image


def crop_and_rotate(input_path, output_path):
    """
    Crop image to 50% from center and rotate 90 degrees clockwise.

    Args:
        input_path: Path to input image file
        output_path: Path to save the processed image
    """
    print(f"Opening image: {input_path}")

    # Open the image
    img = Image.open(input_path)
    original_size = img.size
    print(f"Original image size: {original_size}")

    # Crop to 50% from center
    width, height = img.size
    new_width = width // 2
    new_height = height // 2

    # Calculate crop box (left, top, right, bottom)
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped image size: {cropped.size}")

    # Rotate 90 degrees clockwise (using ROTATE_270 which is equivalent to 90° clockwise)
    rotated = cropped.transpose(Image.ROTATE_270)
    print(f"Final image size after rotation: {rotated.size}")

    # Save the result
    rotated.save(output_path)
    print(f"Processed image saved to: {output_path}")

    # Print summary
    print(f"\n✓ Successfully processed image")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Original size: {original_size}")
    print(f"  Cropped size: {cropped.size}")
    print(f"  Final size: {rotated.size}")

    # Cleanup
    img.close()
    cropped.close()
    rotated.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python crop_and_rotate.py <input_image> <output_image>")
        print("\nExample:")
        print("  python crop_and_rotate.py input.jpg output.jpg")
        sys.exit(1)

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    # Validate input file exists
    if not Path(input_image).exists():
        print(f"ERROR: Input file does not exist: {input_image}")
        sys.exit(1)

    # Validate output directory exists
    output_dir = Path(output_image).parent
    if not output_dir.exists():
        print(f"ERROR: Output directory does not exist: {output_dir}")
        sys.exit(1)

    try:
        crop_and_rotate(input_image, output_image)
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
