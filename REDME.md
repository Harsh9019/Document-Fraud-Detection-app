<img width="1575" height="538" alt="image" src="https://github.com/user-attachments/assets/25628b11-6958-4c07-8d44-30d848e4ace6" />
# Document Fraud Detection

# What is used:-
CLIP (openai/clip-vit-base-patch32, via HuggingFace transformers) — zero-shot image classifier
ELA (Error Level Analysis) — a classic image-forensics trick using PIL
FastAPI — REST API (POST /detect)
Streamlit — web UI, calls the same logic

# Structure:-
 model.py     # CLIP zero-shot + ELA detection logic
schemas.py   # Pydantic response models
main.py      # FastAPI REST endpoint (POST /detect)


# Why this structure:-
- FastAPI (`app/main.py`) satisfies the "REST endpoint, JSON response" requirement.
- Streamlit gives a quick visual demo on top of the same logic.

# Run locally:-
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
