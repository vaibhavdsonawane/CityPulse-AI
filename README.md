# 🏙️ CityPulse AI

> **An AI-powered prototype for intelligent city issue detection, severity assessment, and predictive urban analytics.**

CityPulse AI is a complete, end-to-end Machine Learning web application designed to modernize municipal infrastructure repair. It allows citizens to report issues (like potholes or water leaks) and utilizes a multi-model AI pipeline to automatically verify the image, assess the severity, and route the issue to the correct city department.

---

### 🧠 Core Artificial Intelligence Architecture

Instead of relying on a single model, this prototype utilizes a multi-stage AI pipeline:

1. **Computer Vision (YOLOv8):** Extracts bounding boxes and classification confidences from citizen-uploaded images to verify the issue exists.
2. **Natural Language Processing (Heuristic NLP):** Parses the citizen's text description for urgency keywords (e.g., "school," "danger," "crash") to generate a priority multiplier.
3. **Machine Learning (XGBoost):** A trained gradient-boosted tree that calculates a dynamic "Severity Score" based on engineered GIS features (traffic density, proximity to hospitals, weather, and historical crime rates).
4. **Time-Series Forecasting (Scikit-Learn):** A Linear Regression model that projects the next 7 days of complaint volume to help city administrators budget and staff appropriately.

---

### 🏗️ Advanced System Design Features

* **Human-in-the-Loop (HITL) & Active Learning:** The system does not blindly trust the AI. If the YOLO vision model falls below a 60% confidence threshold, the report is flagged for manual review. If the Administrator corrects the AI's mistake, the database logs the true class, creating a "Data Flywheel" for future model retraining.
* **Geospatial Deduplication (Haversine Formula):** Prevents database bloat and UI clutter. If multiple citizens report the same pothole within a 50-meter radius, the system automatically groups them into a single parent ticket.
* **Synchronous Monolithic Architecture:** Built for simplicity and reliability as a V1 prototype. Eliminates the overhead of complex microservices or message queues (like Celery/Redis) while maintaining a snappy user experience.
* **Event Sourcing (Audit Trails):** Every status change, AI prediction, and human verification is logged with a timestamp in a `ComplaintStatusHistory` table to ensure full municipal accountability.

---

### 💻 Technology Stack

* **Backend:** Python, Flask, SQLAlchemy, SQLite
* **Data Science:** Pandas, NumPy, Scikit-Learn, XGBoost, Ultralytics (YOLO)
* **Frontend:** Bootstrap 5, Jinja2, Leaflet.js (Esri Satellite Maps), Plotly.js
* **Security:** Flask-Login, Werkzeug Password Hashing, CSRF Protection

---

### 🚀 Getting Started (Local Development)

**1. Clone the repository and set up a virtual environment:**
```bash
git clone [https://github.com/yourusername/citypulse-ai.git](https://github.com/yourusername/citypulse-ai.git)
cd citypulse-ai
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`