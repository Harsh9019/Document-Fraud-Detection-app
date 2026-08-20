# import io
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# from PIL import Image, UnidentifiedImageError

# from model import analyze, is_blank

# app = FastAPI(title="Document Fraud Detection API")

# MIN_SIDE, MAX_SIDE = 32, 4000


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.post("/detect")
# async def detect(file: UploadFile = File(...)):
#     raw = await file.read()

#     # corrupted / unsupported file
#     try:
#         img = Image.open(io.BytesIO(raw))
#         img.verify()
#         img = Image.open(io.BytesIO(raw))
#         img.load()
#     except (UnidentifiedImageError, OSError, ValueError):
#         return JSONResponse(status_code=400, content={
#             "error": "corrupted_or_unsupported_file",
#             "message": "Could not read this file as a valid JPG/PNG image.",
#         })

#     if img.mode not in ("RGB", "L", "RGBA"):
#         img = img.convert("RGB")

#     w, h = img.size
#     if w < MIN_SIDE or h < MIN_SIDE:
#         return JSONResponse(status_code=400, content={
#             "error": "image_too_small", "message": f"Image must be at least {MIN_SIDE}px per side."})
#     if w > MAX_SIDE or h > MAX_SIDE:
#         return JSONResponse(status_code=400, content={
#             "error": "image_too_large", "message": f"Image must be under {MAX_SIDE}px per side."})

#     if is_blank(img):
#         return {"fraud_score": 0.0, "category": "none detected",
#                 "explanation": "Image appears blank/uniform; nothing to analyze."}

#     return analyze(img)

import io
from fastapi import FastAPI, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from model import analyze, is_blank

app = FastAPI(title="Document Fraud Detection API")

MIN_SIDE, MAX_SIDE = 32, 4000

@app.get("/")
def read_root():
    return {"message": "hello there"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    raw = await file.read()

    try:
        img = Image.open(io.BytesIO(raw))
        img.load()  
    except (UnidentifiedImageError, OSError, ValueError):
        return JSONResponse(status_code=400, content={
            "error": "corrupted_or_unsupported_file",
            "message": "Could not read this file as a valid JPG/PNG image.",
        })

    if img.mode not in ("RGB", "L", "RGBA"):
        img = img.convert("RGB")

    w, h = img.size
    if w < MIN_SIDE or h < MIN_SIDE:
        return JSONResponse(status_code=400, content={
            "error": "image_too_small", "message": f"Image must be at least {MIN_SIDE}px per side."})
    if w > MAX_SIDE or h > MAX_SIDE:
        return JSONResponse(status_code=400, content={
            "error": "image_too_large", "message": f"Image must be under {MAX_SIDE}px per side."})

    if is_blank(img):
        return {"fraud_score": 0.0, "category": "none detected",
                "explanation": "Image appears blank/uniform; nothing to analyze."}

    # Offload heavy PyTorch CPU processing to a thread pool so it won't block FastAPI
    return await run_in_threadpool(analyze, img)