from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, ImageProcessingRequest
from celery_worker import celery
import os
import uuid

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    request_id = str(uuid.uuid4())
    file_path = os.path.join(Config.UPLOAD_FOLDER, f"{request_id}.csv")
    file.save(file_path)

    new_request = ImageProcessingRequest(id=request_id, csv_filename=file.filename)
    db.session.add(new_request)
    db.session.commit()

    # Use the correct task name
    celery.send_task("tasks.process_images", args=[request_id, file_path])

    return jsonify({"request_id": request_id}), 202

@app.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    request_data = ImageProcessingRequest.query.get(request_id)
    if not request_data:
        return jsonify({"error": "Invalid request ID"}), 404

    response = {"request_id": request_id, "status": request_data.status}
    if request_data.output_csv:
        response["output_csv"] = request_data.output_csv

    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
