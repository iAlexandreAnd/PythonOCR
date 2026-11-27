from typing import Sequence

from PIL import Image, ImageDraw, ImageFont

OCRResult = tuple[Sequence[Sequence[float]], str, float]


def annotate_results(image: Image.Image, results: Sequence[OCRResult]) -> Image.Image:
    annotated_image = image.copy()
    draw = ImageDraw.Draw(annotated_image)
    font = ImageFont.load_default()

    for index, (bounding_box, text, confidence) in enumerate(results, start=1):
        points = [(int(round(point[0])), int(round(point[1]))) for point in bounding_box]
        draw.line(points + [points[0]], fill="green", width=2)

        label = f"{index}. {text} ({confidence:.2f})"
        label_bounds = draw.textbbox((0, 0), label, font=font)
        label_width = label_bounds[2] - label_bounds[0]
        label_height = label_bounds[3] - label_bounds[1]
        padding = 2
        max_x = max(0, image.width - label_width - padding * 2)
        x = min(max(min(point[0] for point in points), 0), max_x)
        y = min(point[1] for point in points) - label_height - padding * 2
        if y < 0:
            y = min(point[1] for point in points) + padding
        max_y = max(0, image.height - label_height - padding * 2)
        y = min(max(y, 0), max_y)

        draw.rectangle(
            (x, y, x + label_width + padding * 2, y + label_height + padding * 2),
            fill="green",
        )
        draw.text((x + padding, y + padding), label, fill="white", font=font)

    return annotated_image
