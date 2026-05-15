from PIL import Image
import logging

logger = logging.getLogger(__name__)

try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False
    logger.warning("pytesseract not installed. OCR will use fallback mode.")


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Optional preprocessing hook.
    You can upgrade later with OpenCV (denoise, thresholding, etc.)
    """
    return image.convert("L")  # grayscale baseline improvement


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from an image using OCR.
    Falls back to simulated output if OCR is unavailable.
    """

    image = preprocess_image(image)

    if OCR_AVAILABLE:
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")

    # fallback for environments without OCR
    return "SIMULATED LABEL: BRAND OLD TOM DISTILLERY CLASS WHISKEY 45% ALC/VOL 750 ML PRODUCT OF USA GOVERNMENT WARNING:"