import os
import unittest

from ocr_basic import read_text

IMAGE_PATH = os.environ.get("OCR_TEST_IMAGE")
EXPECTED_TEXT = os.environ.get("OCR_EXPECTED_TEXT")


@unittest.skipUnless(IMAGE_PATH, "Set OCR_TEST_IMAGE to run the image OCR test.")
class OCRImageTest(unittest.TestCase):
    def test_image_text_is_detected(self):
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


if __name__ == "__main__":
    unittest.main()
