import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

MODEL_PATH = "model/plant_disease_model.h5"
CLASS_MAP_PATH = "model/class_indices.json"
IMG_SIZE = (128, 128)

_model = None
_idx_to_class = None

TREATMENT_TIPS = {
    "Pepper__bell___Bacterial_spot": "Remove infected leaves, avoid overhead watering, apply copper-based bactericide.",
    "Pepper__bell___healthy": "No disease detected. Continue regular monitoring and good watering practices.",
    "Potato___Early_blight": "Remove infected lower leaves, rotate crops yearly, apply fungicide if severe.",
    "Potato___Late_blight": "Destroy infected plants immediately, ensure good drainage, use resistant varieties.",
    "Potato___healthy": "No disease detected. Continue regular monitoring and good watering practices.",
    "Tomato_Bacterial_spot": "Remove infected leaves, avoid overhead watering, apply copper-based bactericide.",
    "Tomato_Early_blight": "Remove lower infected leaves, mulch around base, apply fungicide if spreading.",
    "Tomato_Late_blight": "Remove and destroy infected plants, avoid wetting foliage, apply fungicide promptly.",
    "Tomato_Leaf_Mold": "Improve air circulation, reduce humidity, apply fungicide if severe.",
    "Tomato_Septoria_leaf_spot": "Remove infected lower leaves, avoid overhead watering, apply fungicide.",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Spray with water to dislodge mites, consider insecticidal soap or miticide.",
    "Tomato__Target_Spot": "Remove infected leaves, improve air circulation, apply fungicide if spreading.",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Remove infected plants, control whiteflies (the virus's carrier), use resistant varieties.",
    "Tomato__Tomato_mosaic_virus": "Remove and destroy infected plants, disinfect tools, wash hands between handling plants.",
    "Tomato_healthy": "No disease detected. Continue regular monitoring and good watering practices."
}
DEFAULT_TIP = "Isolate affected plants and consult a local agricultural extension officer for confirmation."

def _load():
    global _model, _idx_to_class
    if _model is None:
        _model = load_model(MODEL_PATH)
        with open(CLASS_MAP_PATH) as f:
            class_indices = json.load(f)
        _idx_to_class = {v: k for k, v in class_indices.items()}
    return _model, _idx_to_class

def predict(image_path: str):
    model, idx_to_class = _load()

    img = load_img(image_path, target_size=IMG_SIZE)
    arr = img_to_array(img)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr, verbose=0)[0]
    top_idx = int(np.argmax(preds))
    disease = idx_to_class[top_idx]
    confidence = float(preds[top_idx])

    return {
        "disease": disease,
        "confidence": round(confidence, 4),
        "treatment_tip": TREATMENT_TIPS.get(disease, DEFAULT_TIP)
    }

