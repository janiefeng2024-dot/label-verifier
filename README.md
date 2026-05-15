# 🍾 Alcohol Label Verification System

An OCR + rule-based compliance checker for alcohol beverage labels using FastAPI.

---

## 🚀 Features

- Image upload (single & batch)
- OCR text extraction (Tesseract)
- Rule-based compliance validation
- Confidence scoring
- FastAPI backend

---

## ▶️ Run Locally

### Backend
uvicorn main:app --reload

http://127.0.0.1:8000/docs

### Frontend
http://localhost:5500

---

## 📸 Screenshots

### 1. Frontend Upload Page
![Frontend Upload Page](screenshots/frontend_upload.png)

### 2. Swagger API (FastAPI Docs)
![Swagger UI](screenshots/swagger_ui.png)

### 3. Valid Label Result
![Valid Result](screenshots/valid_result.png)

### 4. Invalid Label Result
![Invalid Result](screenshots/invalid_result.png)

### 5. Batch Upload Result
![Batch Result](screenshots/batch_result.png)

---

## 📸 Demo

### Example PASS Case
![PASS Case](test_images/pass_label001.png)

### Example FAIL Case
![FAIL Case](test_images/fail_label001.jpeg)

---

## 🧠 Notes

- OCR accuracy depends on image quality
- Government warning must include keyword "GOVERNMENT WARNING"
