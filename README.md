# PythonOCR

## Run with Docker

Build the image from the project root:

```powershell
docker build -t pythonocr .
```

Start the Streamlit server:

```powershell
docker run --rm -p 8501:8501 pythonocr
```

Open [http://localhost:8501](http://localhost:8501). The first OCR request
downloads EasyOCR's model files, so it needs network access and may take longer
than subsequent requests.
