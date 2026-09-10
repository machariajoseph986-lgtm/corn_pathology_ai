"""
Plant Health Maize Project
Flask web application entry point.
"""

import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from werkzeug.utils import secure_filename

from cnn.database_integration import diagnose_from_image


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diagnosis")
def diagnosis():
    return render_template("diagnosis.html")


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    response = None

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        if question:
            from knowledge_base.chatbot import chatbot_response

            response = chatbot_response(
                question
            )

    return render_template(
        "chatbot.html",
        response=response
    )


@app.route("/diagnose", methods=["POST"])
def diagnose():

    if "image" not in request.files:
        return redirect(
            url_for("diagnosis")
        )

    image = request.files["image"]

    if image.filename == "":
        return redirect(
            url_for("diagnosis")
        )

    if not allowed_file(
        image.filename
    ):
        return redirect(
            url_for("diagnosis")
        )

    original_filename = secure_filename(
        image.filename
    )

    if not original_filename:
        return redirect(
            url_for("diagnosis")
        )

    file_extension = os.path.splitext(
        original_filename
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(image_path)

    result = diagnose_from_image(
        image_path
    )

    return render_template(
        "diagnosis.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=False)