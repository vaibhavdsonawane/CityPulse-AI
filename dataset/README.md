# CITYPULSE AI: Dataset Architecture & Provenance

To ensure the Machine Learning models learn from real-world urban distributions, this project utilizes a hybrid data approach combining real municipal records with derived target labels.

## 1. Computer Vision (YOLOv8) Dataset
* **Source:** [RDD2022 (Road Damage Dataset 2022)](https://github.com/sekilab/RoadDamageDetector) & [TACO (Trash Annotations in Context)](https://github.com/pedropro/TACO)
* **Description:** Real-world crowdsourced images of urban decay.
* **Classes Used:** `Pothole`, `Alligator Crack`, `Garbage`, `Illegal Dumping`.
* **Preprocessing:** Images resized to 640x640, bounding boxes normalized to YOLO format, augmented for varied lighting and mobile phone angles.

## 2. Machine Learning (Tabular) Dataset
Because a unified dataset containing *Complaints*, *Weather*, *Traffic*, and *Assigned Severity* does not exist publicly, we built a data engineering pipeline to create one.

### The Pipeline
1. **Real Data Ingestion:** We fetch live/historical 311 Service Requests directly from the **Chicago Open Data Portal API (Socrata)**. This provides real geographic distributions, timestamps, and real complaint categories (Potholes, Streetlights, Sanitation).
2. **Data Cleaning:** Removal of duplicate service request numbers, dropping records with missing GPS coordinates, and filtering for relevant Smart City categories.
3. **Feature Engineering:** Extracting `hour_of_day`, `month` (seasonality), and merging with historical weather probability distributions based on the timestamp.
4. **Derived Labels (Synthetic Target):** Since municipalities do not expose their internal "Severity/Priority" scores, we apply a deterministic rules engine to derive a `severity_level` (Low, Medium, High, Critical) based on the real weather, location, and issue type.

*This ensures the feature space (X) is 100% real-world data, while the target space (y) is derived using documented municipal logic.*