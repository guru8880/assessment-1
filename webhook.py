import requests

WEBHOOK_URL = "https://your-webhook-endpoint.com"

def trigger_webhook(request_id, output_csv_path):
    payload = {
        "request_id": request_id,
        "output_csv": output_csv_path
    }
    requests.post(WEBHOOK_URL, json=payload)
