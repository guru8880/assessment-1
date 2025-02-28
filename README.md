### **📄 README.md**  

# **📦 Asynchronous Image Processing API**  
A **Flask + Celery + SQLite** backend system for processing images asynchronously from a CSV file. The system:  
✅ Accepts a CSV file with product names and image URLs  
✅ Compresses images asynchronously using **Celery**  
✅ Stores processed image details in **SQLite**  
✅ Provides an API to check processing status  
✅ Supports **webhook notifications** after processing  

---

## **🚀 Tech Stack**
- **Backend:** Flask  
- **Asynchronous Processing:** Celery (Redis as the broker)  
- **Database:** SQLite  
- **Image Processing:** Pillow  
- **API Testing:** Postman  

---

## **📁 Project Structure**
```
/backend
│── app.py                 # Main Flask API
│── celery_worker.py        # Celery worker setup
│── config.py               # Configuration settings
│── models.py               # Database models
│── tasks.py                # Celery tasks for image processing
│── webhook.py              # Webhook handler
│── database.db             # SQLite database (auto-created)
│── uploads/                # Folder to store images
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
```

---

## **📌 API Endpoints**

### **1️⃣ Upload CSV**
- **📍 Endpoint:** `POST /upload`  
- **📩 Request Type:** `multipart/form-data`  
- **🔢 Parameters:**  
  - `file`: CSV file with **`Serial Number, Product Name, Input Image Urls`**  
- **📤 Response:**
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```
- **📌 Description:** Uploads a CSV file and returns a unique `request_id`.  

---

### **2️⃣ Check Processing Status**
- **📍 Endpoint:** `GET /status/<request_id>`  
- **📩 Request Type:** `GET`  
- **🔢 Parameters:**  
  - `request_id` (string): Unique ID from the upload request  
- **📤 Response (Processing)**  
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "Processing"
  }
  ```
- **📤 Response (Completed)**  
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "Completed",
    "output_csv": "uploads/123e4567-e89b-12d3-a456-426614174000_processed.csv"
  }
  ```
- **📌 Description:** Returns processing status; provides the processed CSV file link when complete.  

---

### **3️⃣ Webhook (Triggered After Processing)**
- **📍 Endpoint:** `POST <Webhook_URL>`  
- **📩 Request Type:** `POST`  
- **📤 Payload:**  
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "output_csv": "uploads/123e4567-e89b-12d3-a456-426614174000_processed.csv"
  }
  ```
- **📌 Description:** This webhook is automatically triggered after processing.

---

## **📝 Sample CSV File**
```csv
Serial Number,Product Name,Input Image Urls
1,SKU1,https://via.placeholder.com/300,https://via.placeholder.com/400
2,SKU2,https://via.placeholder.com/600,https://via.placeholder.com/700
```

---

## **🛠 Setup & Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/guru8880/assessment-1.git
cd assessment-1
```

### **2️⃣ Create & Activate a Virtual Environment**
#### **🔹 Windows**
```sh
python -m venv venv
venv\Scripts\activate
```
#### **🔹 Linux/macOS**
```sh
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Start Redis (Required for Celery)**
#### **🔹 If using WSL/Linux**
```sh
redis-server
```
#### **🔹 If using Windows**
- Install Redis via [Memurai](https://www.memurai.com/get-memurai)
- Run:
  ```sh
  memurai-server.exe
  ```

### **5️⃣ Initialize the Database**
```sh
python -c "from app import db, app; with app.app_context(): db.create_all()"
```

### **6️⃣ Start Flask API**
```sh
python app.py
```

### **7️⃣ Start Celery Worker**
```sh
celery -A celery_worker worker --loglevel=info --pool=solo
```

### **8️⃣ Test APIs in Postman**
- **Upload CSV:** `POST http://127.0.0.1:5000/upload`
- **Check Status:** `GET http://127.0.0.1:5000/status/<request_id>`

---

## **🎯 Troubleshooting**
| **Issue** | **Solution** |
|-----------|-------------|
| Celery doesn’t process tasks | Use `--pool=solo` when starting Celery |
| Redis not running | Start Redis using `redis-server` or `memurai-server.exe` |
| Flask API not updating status | Ensure `app_context()` is used in `tasks.py` |

---

## **🎯 Features Implemented**
✔ **Flask API**  
✔ **SQLite Database**  
✔ **Asynchronous Image Processing with Celery**  
✔ **CSV Parsing with Pandas**  
✔ **Image Compression with Pillow**  
✔ **Webhook Trigger after Processing**  

---

## **📌 Future Enhancements**
- ✅ Migrate from SQLite to **PostgreSQL** or **MongoDB** for scalability  
- ✅ Add **Docker Support**  
- ✅ Implement **Retry Mechanism** for failed image downloads  

