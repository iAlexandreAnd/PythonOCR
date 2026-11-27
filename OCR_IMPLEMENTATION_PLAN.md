# OCR Practice Project: Implementation Plan

## Goal

Grow the current EasyOCR command-line reader and Streamlit image uploader into a
small OCR workbench for exploring recognition quality, preprocessing, and
downstream text extraction.

## Current starting point

- `ocr_basic.py` reads one image with EasyOCR in English and prints recognized
  text with confidence scores.
- `app.py` accepts one PNG or JPEG, caches an English EasyOCR reader, and
  displays the recognized text.
- `test_ocr.py` optionally runs against an image supplied through environment
  variables and can check for an expected phrase.

Keep the command-line behavior working as features are added. Prefer keeping
image processing and result formatting in small functions that can be tested
without launching the Streamlit app.

## Milestones

### 1. Create a repeatable OCR evaluation set

**Why first:** A consistent baseline makes it possible to tell whether
preprocessing or a different OCR engine actually improves recognition.

- [ ] Collect a small set of representative images and their ground-truth text.
- [x] Store the image-to-text mapping in a simple, documented format.
- [x] Add text normalization and character error rate (CER) and word error rate
  (WER) calculations.
- [x] Report per-image and aggregate scores, alongside the existing detection
  and expected-phrase checks.

**Done when:** The same sample set produces repeatable CER/WER scores, including
for an imperfect transcription, and existing optional image testing still
works.

### 2. Visualize detected text regions

- [x] Draw EasyOCR bounding boxes over the uploaded image.
- [x] Label regions with their recognized text and confidence.
- [x] Show the original and annotated image together.
- [x] Provide a readable per-region result list; consider region selection and
  text correction as a follow-up if the basic view is useful.

**Done when:** A user can match every displayed OCR result to its location in
the image, and images with no detected text still have a clear empty-state
message.

### 3. Experiment with image preprocessing

- [ ] Add optional preprocessing choices such as grayscale, contrast
  enhancement, thresholding, and rotation correction.
- [ ] Keep the original image available as the baseline.
- [ ] Show the processed image and its OCR output, and compare its CER/WER using
  the evaluation set.
- [ ] Avoid changing the default path until results show a consistent benefit.

**Done when:** Each option can be compared against the unprocessed image on the
same samples, and the evaluation report makes regressions visible.

### 4. Process batches and PDFs

- [ ] Support selecting multiple images and report results separately for each.
- [ ] Add PDF page rendering and OCR with page numbers in the output.
- [ ] Keep per-file and per-page failures visible rather than silently skipping
  them.
- [ ] Add a modest progress indicator for longer jobs.

**Done when:** A mixed batch preserves input and page order, reports
per-item results, and clearly identifies files or pages that could not be
processed.

### 5. Add OCR language selection

- [ ] Let the user select one or more supported languages.
- [ ] Create or reuse a reader configured for the selected language set.
- [ ] Make selected languages clear in the interface and any exported results.
- [ ] Test with representative text for each language offered.

**Done when:** Changing the language selection affects the reader used for
recognition and works on the corresponding evaluation samples.

### 6. Export OCR results

- [ ] Add plain-text and JSON downloads.
- [ ] Include recognized text and, where available, confidence and bounding-box
  coordinates in JSON.
- [ ] Preserve page or image identity and order for batch results.
- [ ] Keep the on-screen output available when a download is generated.

**Done when:** Text exports are readable, JSON is valid and contains the
documented fields, and multi-page or batch exports retain their structure.

### 7. Extract structured fields from receipts

- [ ] Start with a narrow set of fields, such as merchant, date, and total.
- [ ] Implement extraction separately from OCR so each part can be tested.
- [ ] Validate parsed dates and amounts, and flag missing or uncertain values
  for review instead of presenting them as confirmed.
- [ ] Add labeled receipt examples and measure field-level extraction accuracy.

**Done when:** The app displays extracted fields with their source text or
region, highlights values needing review, and tests cover missing and malformed
fields.

### 8. Compare OCR engines

- [ ] Add a second OCR engine behind a small common interface.
- [ ] Run each engine on the same evaluation images and comparable settings.
- [ ] Compare CER/WER, runtime, and any setup or language limitations.
- [ ] Display the engine and settings used with each result.

**Done when:** Both engines can be evaluated on the same labeled inputs and
their scores and runtime are reported without changing the existing EasyOCR
default.

## Suggested order and dependencies

Implement the milestones in order. The evaluation set (1) is the foundation for
preprocessing experiments (3), structured extraction evaluation (7), and engine
comparison (8). Region visualization (2) supports debugging both preprocessing
and field extraction. Batch/PDF support (4), language selection (5), and
exports (6) can be developed incrementally around the existing single-image
workflow.

## General validation checklist

- [ ] Run the existing unit test suite after each milestone.
- [ ] Add focused tests for new pure functions, including normalization,
  metrics, export formatting, and field parsing.
- [ ] Use a small, documented, non-sensitive evaluation set; do not rely only on
  visual inspection.
- [ ] Manually try the Streamlit workflow with a clear image, a difficult image,
  and an image with no detectable text.
- [ ] Keep optional tests that require external images clearly documented so
  they can be run locally.
