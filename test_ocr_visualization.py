import unittest

from PIL import Image

from ocr_visualization import annotate_results


class OCRVisualizationTest(unittest.TestCase):
    def test_draws_regions_without_mutating_the_original_image(self):
        image = Image.new("RGB", (100, 60), "white")
        results = [
            ([(10, 10), (80, 10), (80, 30), (10, 30)], "Hello", 0.95),
        ]

        annotated = annotate_results(image, results)

        self.assertIsNot(annotated, image)
        self.assertEqual(image.getpixel((10, 10)), (255, 255, 255))
        self.assertNotEqual(annotated.tobytes(), image.tobytes())

    def test_returns_an_unchanged_copy_when_no_regions_are_detected(self):
        image = Image.new("RGB", (40, 30), "white")

        annotated = annotate_results(image, [])

        self.assertIsNot(annotated, image)
        self.assertEqual(annotated.tobytes(), image.tobytes())

    def test_long_label_on_a_small_image_does_not_change_image_dimensions(self):
        image = Image.new("RGB", (12, 12), "white")
        results = [
            ([(0, 0), (11, 0), (11, 11), (0, 11)], "Long recognized text", 0.95),
        ]

        annotated = annotate_results(image, results)

        self.assertEqual(annotated.size, image.size)


if __name__ == "__main__":
    unittest.main()
