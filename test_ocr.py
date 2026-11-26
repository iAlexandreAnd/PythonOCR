import os
import unittest

from ocr_evaluation import (
    calculate_cer,
    calculate_wer,
    evaluate_ocr,
    normalize_text,
)

IMAGE_PATH = os.environ.get("OCR_TEST_IMAGE")
EXPECTED_TEXT = os.environ.get("OCR_EXPECTED_TEXT")


@unittest.skipUnless(IMAGE_PATH, "Set OCR_TEST_IMAGE to run the image OCR test.")
class OCRImageTest(unittest.TestCase):
    def test_image_text_is_detected(self):
        from ocr_basic import read_text

        results = read_text(IMAGE_PATH)
        detected_text = " ".join(text for _, text, _ in results).casefold()
        self.assertTrue(detected_text.strip(), "No text was detected in the image.")

        if EXPECTED_TEXT:
            expected = " ".join(EXPECTED_TEXT.split()).casefold()
            normalized_detected = " ".join(detected_text.split())
            self.assertIn(
                expected,
                normalized_detected,
                "The expected phrase was not recognized.",
            )


class OCRMetricsTest(unittest.TestCase):
    def test_normalize_text_removes_case_and_whitespace_variation(self):
        self.assertEqual(normalize_text("  HELLO\n  world  "), "hello world")

    def test_cer_measures_imperfect_transcription(self):
        self.assertGreater(calculate_cer("hello", "hallo"), 0)
        self.assertEqual(calculate_cer("hello", "hello"), 0)

    def test_wer_measures_imperfect_transcription(self):
        self.assertEqual(calculate_wer("the quick fox", "the quick fox"), 0)
        self.assertGreater(calculate_wer("the quick fox", "the slow fox"), 0)

    def test_evaluation_report_contains_per_image_and_aggregate_scores(self):
        entries = [
            {"image": "clear.png", "ground_truth": "hello"},
            {"image": "difficult.png", "ground_truth": "world"},
        ]

        def recognize(image_path):
            return [(None, "hallo" if image_path == "clear.png" else "world", 1.0)]

        report = evaluate_ocr(entries, recognize)
        self.assertEqual(len(report["per_image"]), 2)
        self.assertGreater(report["per_image"][0]["cer"], 0)
        self.assertIn("cer", report["aggregate"])
        self.assertIn("wer", report["aggregate"])


if __name__ == "__main__":
    unittest.main()
