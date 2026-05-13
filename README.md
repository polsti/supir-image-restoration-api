# SUPIR Image Restoration API

REST API and web interface for image restoration and super-resolution using SUPIR.

---

# Project Overview

This project simulates a lightweight version of the SUPIR image restoration workflow using classical computer vision techniques.

The goal of the project was to build a complete restoration system architecture with:

- backend API
- frontend GUI
- configurable restoration pipeline
- image enhancement logic
- modular SUPIR integration structure

Instead of running the original heavy SUPIR diffusion model, the project implements a lightweight restoration pipeline using OpenCV and PIL processing techniques that can run locally without GPU requirements.

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
| mode | string | balanced |
| model_type | string | Q |

---

# Frontend Features

The frontend allows users to configure restoration parameters before processing the image.

Supported controls include:

- upscale factor
- restoration mode
- SUPIR model type
- image preview
- restored image preview
- restored image download

---

# Restoration System

The restoration pipeline is based on classical image processing operations.

Implemented processing stages:

- denoising
- upscale resizing
- local contrast enhancement
- CLAHE histogram equalization
- sharpening
- color enhancement
- grayscale restoration for old photos

The pipeline was designed to imitate the behavior of image restoration models while remaining lightweight and runnable on local hardware.

## Restoration Modes

### Balanced
Default restoration profile with moderate denoising and sharpening.

Designed for:
- normal low-quality images
- compressed photos
- light blur correction

### Strong
More aggressive restoration profile.

Uses:
- stronger sharpening
- stronger contrast enhancement
- higher detail extraction

Designed for:
- blurry images
- noisy images
- compressed screenshots

### Old Photo
Special profile for historical and damaged photos.

Uses:
- grayscale restoration
- softer sharpening
- histogram equalization
- reduced color enhancement

Designed for:
- scanned photos
- vintage photographs
- damaged black-and-white images

## SUPIR Model Types

The frontend includes two simulated SUPIR model profiles:

### Q Model
Quality-oriented profile.

Uses:
- stronger sharpening
- stronger contrast enhancement
- more visually enhanced output

Designed for:
- visually impressive restoration
- sharper output images

### F Model
Fidelity-oriented profile.

Uses:
- softer processing
- lower sharpening
- more natural image preservation

Designed for:
- preserving original image appearance
- avoiding over-processing

## Upscale Factor

The upscale factor controls image resolution scaling.

Available options:

- 1x
- 2x
- 4x

Example:

- 300x300 image with 2x upscale becomes 600x600
- 300x300 image with 4x upscale becomes 1200x1200

Upscaling uses Lanczos interpolation for higher-quality resizing.

---

# SUPIR Integration

The project includes SUPIR as a Git submodule:

```bash
git submodule add https://github.com/Fanghua-Yu/SUPIR.git external/SUPIR
```

Current implementation includes a lightweight restoration pipeline and prepares the architecture for future real SUPIR model integration.

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
- 'frontend-streamlit-gui'
- 'improve-restoration-quality'
- 'kill-sharpening'
- 'lightweight-restoration-demo'
- 'restoration-models'
- 'restoration-enchancement',
- 'supir-runtime-setup'
---

# Limitations

The original SUPIR model requires:

- large GPU memory
- CUDA support
- high-end NVIDIA GPU
- heavy model weights

Because of hardware limitations and local macOS execution constraints, the current project uses a lightweight restoration pipeline instead of full diffusion-based SUPIR inference.

The project architecture, API flow, frontend, and restoration workflow remain fully compatible with future real SUPIR integration.

---

# Current Demo Status

Current demo includes:

- working FastAPI backend
- working Streamlit frontend
- image upload pipeline
- image restoration pipeline
- configurable restoration settings
- restoration modes
- simulated SUPIR model profiles
- upscale processing
- restored image delivery
- downloadable restored images

The current implementation uses lightweight CPU-based processing instead of the original GPU-heavy SUPIR diffusion model.

This approach was selected to allow local execution on standard hardware and macOS environments without requiring high-end GPU infrastructure.