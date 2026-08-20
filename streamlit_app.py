import io
import streamlit as st
from PIL import Image, UnidentifiedImageError

from model import analyze, is_blank

st.set_page_config(page_title="Document Fraud Detector", layout="centered")
st.title("📄 Document Fraud Detection")

MIN_SIDE, MAX_SIDE = 32, 4000

file = st.file_uploader("Upload document image", type=["jpg", "jpeg", "png"])

if file:
    raw = file.read()
    try:
        img = Image.open(io.BytesIO(raw))
        img.verify()
        img = Image.open(io.BytesIO(raw))
        img.load()
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("Corrupted or unsupported image file.")
        st.stop()

    if img.mode not in ("RGB", "L", "RGBA"):
        img = img.convert("RGB")

    w, h = img.size
    if w < MIN_SIDE or h < MIN_SIDE:
        st.error(f"Image must be at least {MIN_SIDE}px per side.")
        st.stop()
    if w > MAX_SIDE or h > MAX_SIDE:
        st.error(f"Image must be under {MAX_SIDE}px per side.")
        st.stop()

    if is_blank(img):
        st.warning("Image appears blank/uniform; nothing to analyze.")
        st.stop()

    st.image(img, caption="Uploaded document", use_container_width=True)

    with st.spinner("Analyzing..."):
        result = analyze(img)

    st.metric("Fraud likelihood", result["fraud_score"])
    st.metric("Latency", f"{result['latency_ms']} ms")

    if result["category"] == "none detected":
        st.success(f"✅ {result['category']} — {result['explanation']}")
    else:
        st.error(f"❌ {result['category']} — {result['explanation']}")

    st.subheader("JSON Response")
    st.json(result)