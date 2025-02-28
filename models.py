from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImageProcessingRequest(db.Model):
    id = db.Column(db.String, primary_key=True)
    csv_filename = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Pending")
    output_csv = db.Column(db.String, nullable=True)  # Stores the processed CSV path
