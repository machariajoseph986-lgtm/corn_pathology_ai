# PURPOSE: Provide the FastAPI foundation and CNN prediction endpoint.
# EXPECTED OUTPUT: GET /health confirms the API is running and
#                  POST /predict returns the V3 CNN prediction as JSON.

import os
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# PURPOSE: Disable TensorFlow XLA JIT to prevent native CPU/XLA crashes on the Render deployment.
# EXPECTED RESULT: TensorFlow runs inference without compiling the prediction through XLA.

os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=0"

from cnn.predictor import predict_image


app = FastAPI(
    title="Plant Health Maize API",
    description="API for the Plant Health Maize Project.",
    version="1.0.0"
)
# PURPOSE: Allow the frontend to communicate with the FastAPI backend during development.
# EXPECTED RESULT: Browser-based requests from the local frontend are accepted.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed image extension.
    """

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


@app.get("/health")
def health_check():
    """
    Confirm that the API is running.
    """

    return {
        "status": "ok",
        "service": "Plant Health Maize API"
    }


@app.post("/predict")
async def predict(
    image: UploadFile = File(...)
):
    """
    Run the V3 MobileNetV2 model on an uploaded image.
    """

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No image filename was provided."
        )

    if not allowed_file(image.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    file_extension = os.path.splitext(
        image.filename
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image_bytes = await image.read()

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            image_bytes
        )

    try:

        result = predict_image(
            image_path
        )

    except Exception as error:

        if os.path.exists(image_path):
            os.remove(image_path)

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )

    return {
        "class_index":
            result["class_index"],

        "class_name":
            result["class_name"],

        "confidence":
            result["confidence"],

        "confidence_threshold":
            result["confidence_threshold"],

        "confidence_status":
            result["confidence_status"],

        "caution_required":
            result["caution_required"],

        "caution_reason":
            result["caution_reason"],

        "health_problem_id":
            result["health_problem_id"],

        "is_healthy":
            result["is_healthy"]
    }

@app.post("/diagnose")
async def diagnose(
    image: UploadFile = File(...)
):
    """
    Run the complete maize-health diagnosis pipeline.

    CNN prediction
        ↓
    Knowledge-base mapping
        ↓
    PostgreSQL disease profile
    """

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No image filename was provided."
        )

    if not allowed_file(image.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    file_extension = os.path.splitext(
        image.filename
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image_bytes = await image.read()

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            image_bytes
        )

    try:

        from cnn.database_integration_postgresql import (
            diagnose_from_image
        )

        result = diagnose_from_image(
            image_path
        )

    except Exception as error:

        if os.path.exists(image_path):
            os.remove(image_path)

        raise HTTPException(
            status_code=500,
            detail=f"Diagnosis failed: {str(error)}"
        )

    return {
        "class_index":
            result["class_index"],

        "class_name":
            result["class_name"],

        "confidence":
            result["confidence"],

        "confidence_status":
            result["confidence_status"],

        "caution_required":
            result["caution_required"],

        "caution_reason":
            result["caution_reason"],

        "health_problem_id":
            result["health_problem_id"],

        "is_healthy":
            result["is_healthy"],

        "disease_profile":
            result["disease_profile"]
    }
    
@app.post("/chat")
async def chat(
    question: str
):
    """
    Send a user question to the PostgreSQL-backed
    Plant Health chatbot.
    """

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        from knowledge_base.chatbot import (
            chatbot_response
        )

        response = chatbot_response(
            question
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chatbot request failed: {str(error)}"
        )

    return {
        "question": question,
        "response": response
    }