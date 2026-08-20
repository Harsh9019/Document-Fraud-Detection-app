import io, time
import numpy as np
from PIL import Image, ImageChops
import torch
from transformers import CLIPModel, CLIPProcessor

CATEGORY_PROMPTS = {
    "copy-paste regions": "a document image with copy-pasted duplicated regions, cloned text or stamps",
    "inconsistent lighting": "a document image with inconsistent lighting or shadows suggesting editing",
    "misaligned elements": "a document image with misaligned text, fonts, or crooked elements",
    "digital artifacts": "a document image with digital editing artifacts, blur halos, or compression inconsistencies",
}
AUTHENTIC_PROMPT = "an authentic original unedited document photo, clean scan or photo of an ID, certificate, contract or invoice"
ALL_PROMPTS = [AUTHENTIC_PROMPT] + list(CATEGORY_PROMPTS.values())

CONF_THRESHOLD = 0.55 

_model = None
_processor = None


def load_model():
    global _model, _processor
    if _model is None:
        _model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return _model, _processor


def _clip_scores(img: Image.Image) -> dict:
    model, processor = load_model()
    inputs = processor(text=ALL_PROMPTS, images=img, return_tensors="pt", padding=True)
    with torch.no_grad():
        probs = model(**inputs).logits_per_image.softmax(dim=1)[0].tolist()
    return dict(zip(ALL_PROMPTS, probs))


def _ela_score(img: Image.Image, quality: int = 90) -> float:
    """Error Level Analysis: recompress and diff; higher = more inconsistent compression."""
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=quality)
    buf.seek(0)
    diff = ImageChops.difference(img.convert("RGB"), Image.open(buf))
    return float(np.array(diff, dtype=float).mean() / 255)


def is_blank(img: Image.Image, std_thresh: float = 3.0) -> bool:
    return float(np.array(img.convert("L"), dtype=float).std()) < std_thresh


def analyze(img: Image.Image) -> dict:
    t0 = time.time()
    scores = _clip_scores(img)
    fraud_score = round(1 - scores[AUTHENTIC_PROMPT], 4)

    cat_scores = {name: scores[prompt] for name, prompt in CATEGORY_PROMPTS.items()}
    top_category = max(cat_scores, key=cat_scores.get)
    category = top_category if fraud_score >= CONF_THRESHOLD else "none detected"

    ela = round(_ela_score(img), 4)
    explanation = (
        f"No strong manipulation signal detected (fraud_score {fraud_score} < threshold {CONF_THRESHOLD})."
        if category == "none detected" else
        f"CLIP flagged '{top_category}' as the most likely manipulation type "
        f"(fraud_score {fraud_score} >= threshold {CONF_THRESHOLD}); "
        f"ELA compression-inconsistency score {ela} supports further review."
    )

    return {
        "fraud_score": fraud_score,
        "category": category,
        "explanation": explanation,
        "ela_score": ela,
        "latency_ms": round((time.time() - t0) * 1000, 1),
        "category_breakdown": {k: round(v, 4) for k, v in cat_scores.items()},
    }