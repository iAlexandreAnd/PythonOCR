import argparse
import json

from ocr_evaluation import evaluate_ocr, load_evaluation_set


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate EasyOCR against a labeled image set."
    )
    parser.add_argument(
        "evaluation_set",
        nargs="?",
        default="evaluation/evaluation_set.json",
        help="JSON or CSV evaluation set",
    )
    args = parser.parse_args()

    entries = load_evaluation_set(args.evaluation_set)
    if entries:
        from ocr_basic import read_text
        recognize = read_text
    else:
        recognize = lambda _image_path: []

    report = evaluate_ocr(entries, recognize)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
