# OCR Evaluation Set

The evaluation set is stored in `evaluation_set.json`. Each entry has:

- `image`: a path to the image, relative to this directory or absolute.
- `ground_truth`: the exact expected text.

Example:

```json
[
  {
    "image": "images/clear-sign.png",
    "ground_truth": "Welcome"
  }
]
```

The set is intentionally empty until representative, non-sensitive images are
added. Use text-only test fixtures for unit tests and local image files for
repeatable OCR checks.
