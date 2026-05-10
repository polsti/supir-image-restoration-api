# SUPIR Image Restoration API

REST API and web interface for image restoration and super-resolution using SUPIR.

---

# Project Overview

This project provides:

- FastAPI backend for image restoration
- Streamlit frontend GUI
- Image upload and download support
- Mock restoration pipeline
- SUPIR integration architecture
- Modular service-based backend design

The application allows users to upload low-quality images, configure restoration settings, and receive restored images through a web interface.

---

# Architecture

```text
Frontend (Streamlit)
        ↓
FastAPI REST API
        ↓
Service Layer
        ↓
SUPIR Integration
```

---

# Technologies Used

## Backend

- FastAPI
- Uvicorn
- Python 3.11

## Frontend

- Streamlit
- Requests

## Image Processing

- Pillow (PIL)

## Version Control

- Git
- GitHub
- Git branches
- Pull Requests

---

# Project Structure

```text
supir-image-restoration-api/
│
├── app/
│   ├── main.py
│   ├── supir_service.py
│   └── utils.py
│
├── frontend/
│   └── streamlit_app.py
│
├── external/
│   └── SUPIR/
│
├── inputs/
├── outputs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Backend Features

## FastAPI API

Implemented endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/restore` | Image restoration |

---

## Restore Endpoint

The `/restore` endpoint accepts:

- image upload
- upscale factor
- restoration mode
- SUPIR model type

Example parameters:

| Parameter | Type | Example |
|---|---|---|
| image | file | image.png |
| upscale | integer | 2 |
| mode | string | mock |
| model_type | string | Q |

---

# Frontend Features

The Streamlit frontend provides:

- image upload
- restoration settings
- original image preview
- restored image preview
- image download button

---

# Current Restoration Modes

## Mock Mode

Current implementation uses mock restoration:

- uploaded image is copied
- output filename is generated automatically
- backend pipeline is fully functional

This mode is used to validate:
- API flow
- frontend-backend communication
- image handling
- file responses
- system architecture

---

# SUPIR Integration

The project includes SUPIR as a Git submodule:

```bash
git submodule add https://github.com/Fanghua-Yu/SUPIR.git external/SUPIR
```

Current implementation prepares the architecture for real SUPIR subprocess execution.

---

# Installation

## Clone repository

```bash
git clone https://github.com/polsti/supir-image-restoration-api.git
cd supir-image-restoration-api
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Backend

Run FastAPI server:

```bash
python3 -m uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Frontend

In a second terminal:

```bash
python3 -m streamlit run frontend/streamlit_app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# Example Workflow

1. Start FastAPI backend
2. Start Streamlit frontend
3. Upload image
4. Select upscale factor
5. Select restoration mode
6. Send request to backend
7. Receive restored image
8. Download restored image

---

# Git Workflow

The project uses:

- feature branches
- pull requests
- isolated backend/frontend development
- modular commits

Example branches:

- `backend-skeleton`
- `backend-mock-restoration`
- `backend-supir-subprocess`
- `frontend-streamlit-gui`
- `docs-readme-setup`

---

# Future Improvements

Planned improvements:

- real SUPIR inference
- GPU support
- asynchronous processing
- Docker support
- deployment
- image history
- user authentication
- queue system for heavy processing

---

# Demo Status

Current demo includes:

- working backend
- working frontend
- image upload pipeline
- restoration request pipeline
- restored image delivery

The system architecture is production-oriented and prepared for real SUPIR integration.