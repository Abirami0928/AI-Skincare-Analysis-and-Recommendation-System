
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model_service import get_model_info, predict_skin_type

from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pydantic import BaseModel, Field
from typing import Optional, List
from product_service import recommend_products_scored

app = FastAPI(
    title="AI Skincare Analysis API",
    description="Backend for skin analysis and skincare recommendations",
    version="1.0.0"
)
class RecommendationRequest(BaseModel):
    skin_label: str
    budget: float = 1000
    product_type: Optional[str] = None
    ingredient_keywords: List[str] = Field(default_factory=list)
    top_n: int = 5

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Skincare Analysis API is running!"
    }


# Health endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Model information endpoint
@app.get("/model-info")
def model_info():
    return get_model_info()


# Skin image prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check image file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    # Read uploaded image
    image_bytes = await file.read()

    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()

        # Reopen image after verification
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image."
        )

    # Predict skin type
    try:
        result = predict_skin_type(image)
        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )
@app.post("/recommendations")
def get_recommendations(request: RecommendationRequest):

    try:
        results = recommend_products_scored(
            skin_label=request.skin_label,
            budget=request.budget,
            product_type=request.product_type,
            ingredient_keywords=request.ingredient_keywords,
            top_n=request.top_n
        )

        return {
            "total_results": len(results),
            "recommendations": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(error)}"
        )


from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

from rag_service import answer_question

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        result = answer_question(user_message)
        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(error)}"
        )