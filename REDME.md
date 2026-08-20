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


## Fraud not Detected:- 
<img width="558" height="796" alt="Screenshot 2026-08-20 113422" src="https://github.com/user-attachments/assets/4f73fc7a-46ee-444a-9a73-b5bc79025e49" />

## Fraud Detected:- 
Misaligned elements
<img width="602" height="822" alt="Screenshot 2026-08-20 113608" src="https://github.com/user-attachments/assets/6cdbc968-2254-47f6-90ee-3aee3cf9f7f5" />

# Check in Api response:-
<img width="1575" height="538" alt="image" src="https://github.com/user-attachments/assets/2a2527d5-a34b-48cc-bbbf-f80f5685eb6b" />

# Check in Api response in json formate:-
<img width="1522" height="510" alt="image" src="https://github.com/user-attachments/assets/510e38d4-eade-4935-b009-ee6dfbb5804d" />

