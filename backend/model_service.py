
from pathlib import Path

import joblib
import torch
import torchvision.models as models

from torchvision.models import ResNet18_Weights


# -----------------------------------
# 1. Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "skin_model.joblib"


# -----------------------------------
# 2. Load Logistic Regression model
# -----------------------------------

model = joblib.load(MODEL_PATH)


# -----------------------------------
# 3. Load pretrained ResNet18
# -----------------------------------

device = torch.device("cpu")

weights = ResNet18_Weights.DEFAULT

feature_extractor = models.resnet18(weights=weights)

# Remove the final classification layer
feature_extractor.fc = torch.nn.Identity()

feature_extractor = feature_extractor.to(device)

feature_extractor.eval()

# Use the same preprocessing as training
preprocess = weights.transforms()


# -----------------------------------
# 4. Skin classes
# -----------------------------------

classes = {
    0: "acne",
    1: "dry",
    2: "oil"
}


# -----------------------------------
# 5. Extract image features
# -----------------------------------

def extract_image_features(image):

    image = image.convert("RGB")

    image_tensor = preprocess(image)

    image_tensor = image_tensor.unsqueeze(0)

    with torch.no_grad():

        features = feature_extractor(
            image_tensor.to(device)
        )

    return features.cpu().numpy()


# -----------------------------------
# 6. Predict skin type
# -----------------------------------

def predict_skin_type(image):

    features = extract_image_features(image)

    prediction = int(model.predict(features)[0])

    probabilities = model.predict_proba(features)[0]

    confidence = float(max(probabilities))

    return {
        "predicted_class": classes[prediction],
        "class_id": prediction,
        "confidence": round(confidence * 100, 2)
    }


# -----------------------------------
# 7. Model information
# -----------------------------------

def get_model_info():

    return {
        "model_type": type(model).__name__,
        "feature_extractor": "ResNet18",
        "number_of_features": int(model.n_features_in_),
        "classes": model.classes_.tolist()
    }
