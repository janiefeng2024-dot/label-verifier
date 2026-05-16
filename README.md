# 🍾 Alcohol Label Verification System

An OCR-powered, rule-based compliance checker for alcohol beverage labels built with FastAPI.  
This project provides an end-to-end system for extracting text from label images and validating regulatory requirements, with support for batch processing and production-style deployment.

---

## 🌐 Deployed Application

👉 [https://label-verifier-production.up.railway.app/](https://label-verifier-production.up.railway.app/)  

---

## 🚀 Features

- Image upload (single & batch processing)
- OCR text extraction using Tesseract
- Rule-based compliance validation engine
- Confidence scoring for results
- FastAPI backend API
- Frontend UI integrated with backend
- Railway deployment ready

---

## 🧠 Approach

This system automates alcohol label compliance checking using OCR + rule-based validation.

### Pipeline Flow:
1. User uploads image(s)
2. FastAPI receives request
3. Tesseract OCR extracts text from image
4. Text is cleaned and normalized
5. Rule-based engine validates:
   - Brand name presence
   - Alcohol content format
   - Government warning requirement
   - Label completeness
6. API returns structured JSON response
7. Frontend displays PASS/FAIL result

### Key Design Decisions:
- Rule-based approach chosen for speed and interpretability
- OCR used instead of ML model for <5s response requirement
- Stateless architecture (no database required)
- Batch processing included for scalability
- FastAPI chosen for lightweight high-performance API

---

## 🛠️ Tools Used

- FastAPI (Backend framework)
- Uvicorn (ASGI server)
- Tesseract OCR (text extraction)
- Pillow (image processing)
- Regex (validation rules)
- HTML / CSS / JavaScript (frontend)
- Railway (deployment)

---

## 📌 Assumptions

- Input images are reasonably clear and readable
- Labels follow standard alcohol compliance structure
- OCR accuracy depends on image quality and lighting
- No database required (stateless system)
- Prototype focuses on validation logic, not authentication/security

---

## ▶️ Run Locally

### ⚠️ IMPORTANT (Version Requirement)

To run the exact working version of this project locally, checkout the tested commit:

```bash
git checkout 59037e0dc82a2f4770af829b6748918230b563f0
```

This commit contains the fully working local version before final deployment changes.


---

### Backend (Python / FastAPI)

```bash
# install dependencies (if not installed)
pip install -r requirements.txt

# start backend server
uvicorn main:app --reload --port 8000
```

Backend will run at:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

---

### Frontend

```bash
python -m http.server 5500
```

Open:
- http://localhost:5500/frontend/

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

## 📸 Demo Test Cases

Test images are available in the `test_images/` directory for quick local verification of both PASS and FAIL scenarios.

### PASS Example
<img src="test_images/pass_label001.png" width="500"/>

### FAIL Example
<img src="test_images/fail_label001.jpeg" width="500"/>

---

## ⚠️ Notes

- First request may take a few seconds due to OCR initialization (cold start on Railway)
- OCR accuracy depends on image quality, lighting, and angle
- Batch processing supported for multiple labels
