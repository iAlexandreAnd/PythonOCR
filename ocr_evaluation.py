import csv
import json
import unicodedata
from pathlib import Path


def normalize_text(text):
    text = unicodedata.normalize("NFKC", str(text).casefold())
    return " ".join(text.split())


def _levenshtein_distance(reference, candidate):
    if len(reference) < len(candidate):
        return _levenshtein_distance(candidate, reference)

    previous = list(range(len(candidate) + 1))
    for reference_index, reference_character in enumerate(reference, 1):
        current = [reference_index]
        for candidate_index, candidate_character in enumerate(candidate, 1):
            insertion = current[-1] + 1
            deletion = previous[candidate_index] + 1
            substitution = previous[candidate_index - 1] + (
                reference_character != candidate_character
            )
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]


def calculate_cer(reference, candidate):
    reference = normalize_text(reference)
    candidate = normalize_text(candidate)
    if not reference:
        return 0.0 if not candidate else 1.0
    return _levenshtein_distance(reference, candidate) / len(reference)


def calculate_wer(reference, candidate):
    reference_words = normalize_text(reference).split()
    candidate_words = normalize_text(candidate).split()
    if not reference_words:
        return 0.0 if not candidate_words else 1.0
    return _levenshtein_distance(reference_words, candidate_words) / len(reference_words)


def load_evaluation_set(path):
    path = Path(path)
    if path.suffix.casefold() == ".json":
        with path.open("r", encoding="utf-8") as evaluation_file:
            entries = json.load(evaluation_file)
    elif path.suffix.casefold() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as evaluation_file:
            entries = list(csv.DictReader(evaluation_file))
    else:
        raise ValueError("Evaluation set must be a JSON or CSV file.")

    base_dir = path.parent
    normalized_entries = []
    for entry in entries:
        image = entry.get("image")
        ground_truth = entry.get("ground_truth")
        if not image or ground_truth is None:
            raise ValueError("Each evaluation entry requires image and ground_truth.")
        image_path = Path(image)
        if not image_path.is_absolute():
            image_path = base_dir / image_path
        normalized_entries.append(
            {"image": str(image_path), "ground_truth": ground_truth}
        )
    return normalized_entries


def evaluate_ocr(entries, recognize):
    results = []
    for entry in entries:
        detected_regions = recognize(entry["image"])
        detected_text = " ".join(
            str(region[1]) for region in detected_regions
        )
        results.append(
            {
                "image": entry["image"],
                "ground_truth": normalize_text(entry["ground_truth"]),
                "detected_text": normalize_text(detected_text),
                "cer": calculate_cer(entry["ground_truth"], detected_text),
                "wer": calculate_wer(entry["ground_truth"], detected_text),
            }
        )

    if not results:
        return {"per_image": [], "aggregate": {"cer": 0.0, "wer": 0.0}}

    return {
        "per_image": results,
        "aggregate": {
            "cer": sum(result["cer"] for result in results) / len(results),
            "wer": sum(result["wer"] for result in results) / len(results),
        },
    }
