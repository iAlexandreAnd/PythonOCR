import easyocr

reader = easyocr.Reader(["en"], gpu=False)

results = reader.readtext("C:\\Users\\Alexandre\\Pictures\\20250327_143747.jpg")

for box, text, confidence in results:
    print(f"{text} (confidence: {confidence:.2f})")