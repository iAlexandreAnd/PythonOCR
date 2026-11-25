import argparse

import easyocr


def read_text(image_path):
    reader = easyocr.Reader(["en"], gpu=False)
    return reader.readtext(str(image_path))


def main():
    parser = argparse.ArgumentParser(description="Read text from an image.")
    parser.add_argument("image", help="Path to the image to scan")
    args = parser.parse_args()

    for _, text, confidence in read_text(args.image):
        print(f"{text} (confidence: {confidence:.2f})")


if __name__ == "__main__":
    main()