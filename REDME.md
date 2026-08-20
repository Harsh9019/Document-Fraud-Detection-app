# Document Fraud Detection

## Structure

  model.py     # CLIP zero-shot + ELA detection logic
  schemas.py   # Pydantic response models
  main.py      # FastAPI REST endpoint (POST /detect)
streamlit_app.py  # Streamlit UI, reuses app/model.py directly
requirements.txt
```

## Why this structure
- `app/model.py` is the single source of truth for detection logic — both the
  REST API and the Streamlit UI call the same `analyze()` function, so there's
  no duplicated logic to keep in sync.
- FastAPI (`app/main.py`) satisfies the "REST endpoint, JSON response" requirement.
- Streamlit gives a quick visual demo on top of the same logic.

## Run locally
```bash
pip install -r requirements.txt

# REST API
uvicorn app.main:app --reload
# POST http://localhost:8000/detect  (multipart file upload) -> JSON

# Streamlit UI
streamlit run streamlit_app.py
```

## Deploy
- **Streamlit UI** → push repo to GitHub → share.streamlit.io → New app → main file `streamlit_app.py`.
- **FastAPI** → deploy `app/main.py` (uvicorn) on Render/Railway/HF Spaces (Docker) for the REST endpoint requirement.

## Before submitting
- Test on 20+ real images, record actual accuracy/latency.
- Tune `CONF_THRESHOLD` in `app/model.py` based on that testing.
- Write the submission email honestly, matching observed behavior.
