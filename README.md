#  Crop Disease Detector

A field diagnostic tool that identifies crop diseases from a leaf photo and recommends a treatment action — built for smallholder farmers who need a fast, accessible way to check plant health.

Upload a photo → get a diagnosis, a confidence score, and a treatment tip, in seconds.

## Live Demo

- **App**: https://crop-disease-mnf59vbax-muenis-projects.vercel.app
- **API**: https://crop-disease-app-usss.onrender.com
- **API docs (interactive)**: https://crop-disease-app-usss.onrender.com/docs

> **Note**: The backend is hosted on Render's free tier, which spins down after inactivity. The first request after idle time may take 30-60 seconds to respond while the service wakes up.

## Scope

This tool currently supports disease detection for **Pepper, Potato, and Tomato** crops, covering 15 classes (healthy and diseased states) from the [PlantVillage dataset](https://www.kaggle.com/datasets/emmarex/plantdisease). It is not trained to recognize other crops (e.g. maize, wheat) — uploading an unsupported crop type will return a low-confidence, unreliable result rather than a valid diagnosis.

## Why this exists

Crop disease is a major driver of yield loss for smallholder farmers, and diagnosis often requires specialist knowledge or a trip to an agricultural extension office. This tool puts a first-pass diagnostic check directly into a farmer's hands — not a replacement for expert advice, but a fast way to catch a problem early and know what to do next.

## Architecture

```
crop-disease-app/
├── model/
│   ├── train.py               # EfficientNetB0 training script
│   ├── predict.py             # Inference wrapper
│   ├── plant_disease_model.h5
│   ├── class_indices.json
│   └── notebooks/
│       └── training_exploration.ipynb
├── backend/
│   ├── main.py                 # FastAPI app (/health, /predict)
│   └── requirements.txt
├── frontend/                   # React + TypeScript (Vite)
│   └── src/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       └── types/
├── tests/
│   ├── test_api.py
│   └── sample_images/
├── .python-version
└── README.md
```

**Flow**: a user uploads a leaf photo in the React frontend → the image is sent to the FastAPI backend's `/predict` endpoint → the backend runs it through a fine-tuned EfficientNetB0 model → returns a disease label, confidence score, and treatment tip → the frontend displays the result.

Model research and comparison work (classical ML vs. CNNs vs. EfficientNetB0) lives in a separate repository: [plant-disease-classification](https://github.com/Muen1/plant-disease-classification). This app productionizes the best-performing model from that research.

## Tech stack

- **Model**: TensorFlow / Keras, EfficientNetB0 (transfer learning, fine-tuned)
- **Backend**: FastAPI, Python, deployed on Render
- **Frontend**: React, TypeScript, Vite, deployed on Vercel
- **Testing**: Pytest (backend), Vitest + Testing Library (frontend)

## Running it locally

### 1. Clone the repo

```bash
git clone https://github.com/Muen1/crop-disease-app.git
cd crop-disease-app
```

### 2. Set up the backend

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# or: source venv/bin/activate  # Mac/Linux

pip install -r backend/requirements.txt
```

Start the API:

```bash
uvicorn backend.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`. Check it's working by visiting `http://127.0.0.1:8000/docs` — FastAPI's interactive API explorer.

### 3. Set up the frontend

In a separate terminal:

```bash
cd frontend
npm install
```

Create a `.env` file (see `.env.example`):

```
VITE_API_URL=http://127.0.0.1:8000
```

Start the dev server:

```bash
npm run dev
```

Open the URL it prints (usually `http://localhost:5173`).

### 4. Try it

Upload any leaf photo — sample images are provided in `tests/sample_images/` if you don't have your own. Click **Run Diagnosis** and you'll get back a disease name, confidence percentage, and a recommended treatment action.

## Running the tests

**Backend:**

```bash
pytest tests/
```

**Frontend:**

```bash
cd frontend
npm run test
```

## Model performance

The production model (EfficientNetB0, fine-tuned) achieved **96.8% validation accuracy**. Full evaluation details, including confusion matrices and comparisons against classical ML baselines, are available in the [research repository](https://github.com/Muen1/plant-disease-classification).

## Limitations and future work

- Currently limited to 3 crop types (Pepper, Potato, Tomato) — expanding to more crops would require retraining on a broader dataset
- No confidence-threshold warning yet in the UI for out-of-scope images (planned)
- No user accounts or diagnosis history — each check is stateless
- Requires an internet connection — an offline-capable version (via TensorFlow Lite) would better serve farmers in areas with unreliable connectivity
- Treatment tips are general guidance, not a substitute for consulting a local agricultural extension officer
- Backend cold starts on Render's free tier add latency after idle periods — a paid tier or alternative host would remove this in production

## Author

Built by [Mueni Mutie](https://github.com/Muen1).