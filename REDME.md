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
pip install -r requirements.txt

# REST API
uvicorn main:app --reload
# POST http://localhost:8000/detect JSON

# Streamlit UI
streamlit run streamlit_app.py
```

## Deploy
- **Streamlit UI** → push repo to GitHub → share.streamlit.io → New app → main file `streamlit_app.py`.
- **FastAPI** → deploy `app/main.py` (uvicorn).


# Fraud not detected:- 

<img width="557" height="796" alt="image" src="https://github.com/user-attachments/assets/9ba3f782-7866-44bc-98eb-a308cdccb332" />

