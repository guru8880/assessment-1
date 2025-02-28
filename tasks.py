from celery_worker import celery
from models import db, ImageProcessingRequest
from flask import current_app
from PIL import Image
import requests
import os
import pandas as pd
from io import BytesIO
from webhook import trigger_webhook

@celery.task(name="tasks.process_images")  # Explicitly set task name
def process_images(request_id, file_path):
    from app import app  # Import inside the function to avoid circular import

    with app.app_context():
        request_data = ImageProcessingRequest.query.get(request_id)
        if not request_data:
            print(f"Task failed: No request found for {request_id}")
            return

        print(f"Processing task for request_id: {request_id}")
        request_data.status = "Processing"
        db.session.commit()

        df = pd.read_csv(file_path)
        df["Output Image Urls"] = ""

        for idx, row in df.iterrows():
            image_urls = row["Input Image Urls"].split(',')
            output_urls = []

            for img_url in image_urls:
                response = requests.get(img_url.strip())
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    output_filename = f"{request_id}_{os.path.basename(img_url.strip())}"
                    output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], output_filename)
                    image.save(output_path, quality=50)
                    output_urls.append(output_path)

            df.at[idx, "Output Image Urls"] = ', '.join(output_urls)

        output_csv_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{request_id}_processed.csv")
        df.to_csv(output_csv_path, index=False)

        request_data.status = "Completed"
        request_data.output_csv = output_csv_path
        db.session.commit()

        trigger_webhook(request_id, output_csv_path)

# Ensure Celery recognizes the task
celery.register_task(process_images)
