from fastapi import FastAPI


app = FastAPI(
    title="SUPIR Image Restoration API",
    description="REST API for image restoration and super-resolution using SUPIR.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "SUPIR Image Restoration API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }