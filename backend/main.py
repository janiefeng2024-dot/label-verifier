from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from PIL import Image
import io
import logging
import time

from ocr import extract_text_from_image
from matcher import LabelMatcher

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# App setup
# -----------------------------
app = FastAPI(
    title="Alcohol Label Verification API",
    version="1.0.0",
    description="OCR + rule-based compliance system for alcohol labels"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Initialize matcher
# -----------------------------
matcher = LabelMatcher()


def load_image(file: UploadFile) -> Image.Image:
    """
    Convert uploaded file into PIL image
    """
    try:
        contents = file.file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        return image
    except Exception as e:
        logger.error(f"Image load error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image file")


def process_image(image: Image.Image) -> Dict[str, Any]:
    """
    Full pipeline:
    1. OCR extraction
    2. Label validation
    """
    start = time.time()
    text = extract_text_from_image(image)
    validation = matcher.validate(text)

    return {
        "extracted_text": text,
        "validation": validation,
        "processing_time_ms": round((time.time() - start) * 1000, 2)
    }

# -----------------------------
# Health endpoints
# -----------------------------
@app.get("/")
def root():
    return {
        "service": "Alcohol Label Verification API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Single verification
# -----------------------------
@app.post("/verify")
def verify_single(file: UploadFile = File(...)):
    logger.info(f"Single file received: {file.filename}")

    try:
        image = load_image(file)
        result = process_image(image)

        return {
            "filename": file.filename,
            "status": "success",
            "data": result
        }

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")

        return {
            "filename": file.filename,
            "status": "failed",
            "error": str(e)
        }

# -----------------------------
# Batch verification endpoint
# -----------------------------
@app.post("/verify/batch")
async def verify_batch(
    files: List[UploadFile] = File(..., media_type="multipart/form-data")
):
    logger.info(f"Batch request received: {len(files)} files")

    results = []

    for file in files:
        try:
            # reset pointer safety (important for multiple reads)
            file.file.seek(0)

            image = load_image(file)
            result = process_image(image)

            results.append({
                "filename": file.filename,
                "status": "success",
                "data": result
            })

        except Exception as e:
            logger.error(f"Error processing {file.filename}: {str(e)}")

            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return {
        "total_files": len(files),
        "results": results
    }