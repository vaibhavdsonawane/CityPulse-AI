# CityPulse AI — Smart Urban Infrastructure Management Platform
An AI-powered civic governance and predictive urban analytics platform built using Python (Flask), YOLOv8 Computer Vision, Scikit-Learn NLP, and Leaflet Geospatial GIS. The system automates civic defect verification from uploaded photos, calculates an objective 0–100 Priority Score from complaint text, clusters geographic hazard hotspots via the Haversine formula, and dispatches field teams through an administrative command center.
---
## 📌 Table of Contents
1. [Core Features](#-core-features)
2. [Tech Stack](#-tech-stack)
3. [System Prerequisites](#-system-prerequisites)
4. [Step-by-Step Installation on a New Device](#-step-by-step-installation-on-a-new-device)
5. [Default User Credentials](#-default-user-credentials)
6. [Project Directory Structure](#-project-directory-structure)
7. [Mathematical Formulations](#-mathematical-formulations)
8. [Troubleshooting & Common Issues](#-troubleshooting--common-issues)
9. [Project Attribution](#-project-attribution)
---
## 🚀 Core Features
* **AI Visual Verification (Ultralytics YOLOv8):** Scans uploaded defect photos to detect potholes, garbage heaps, broken streetlights, water pipeline bursts, and fallen trees with bounding box coordinates and confidence metrics. Low-confidence predictions (< 60%) route to a Human-in-the-Loop (HITL) queue.
* **NLP Priority Scoring Engine (TF-IDF & Logistic Regression):** Parses citizen description text in real time to calculate a deterministic 0–100 Priority Score based on Severity, Location Risk, Impact, and Historical Frequency.
* **Spatial GIS & Hotspot Clustering (Haversine Formula):** Automatically merges duplicate complaints within a 50-meter radius and highlights high-density hazard clusters (3+ incidents within 350 meters) on an interactive satellite threat map.
* **Non-Reloading AJAX Dispatching:** Municipal administrators assign complaints to field departments (*Roads, Sanitation, Water, Electrical, Forestry*) via asynchronous JavaScript `fetch()` calls without full page reloads.
* **Citizen Lifecycle Tracking & Badges:** Citizens track repair workflows via an interactive 6-step progress bar (*Submitted → AI Analyzed → Assigned → Investigating → Work Started → Resolved*) and earn unlockable civic reward badges.
---
## 🛠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Backend Framework** | Python 3.10+ / 3.11+, Flask 3.0+ |
| **Database & ORM** | SQLite3, SQLAlchemy ORM |
| **Computer Vision** | Ultralytics YOLOv8, OpenCV, PyTorch |
| **Machine Learning / NLP** | Scikit-Learn (TF-IDF, Logistic Regression), NumPy, Pandas |
| **Frontend & UI** | HTML5, CSS3 Tokens, Bootstrap 5.3, JavaScript (ES6+) |
| **Mapping Engine** | Leaflet.js (v1.9.4), Esri World Imagery Satellite Tiles |
| **Analytics & Charts** | Plotly.js |

---
## 📋 System Prerequisites
Before setting up CityPulse AI on a new device, ensure the following software is installed:
1. **Git:** [Download Git](https://git-scm.com/downloads)
2. **Python 3.10 or 3.11:** [Download Python](https://www.python.org/downloads/)
   * ⚠️ **Important on Windows:** During installation, make sure to check the box **"Add Python to PATH"**.
3. **Code Editor:** [Visual Studio Code](https://code.visualstudio.com/) (Recommended)
---
## 💻 Step-by-Step Installation on a New Device
Open your terminal (Command Prompt, PowerShell, or macOS/Linux Terminal) and follow these steps:
### Step 1: Clone the GitHub Repository
```bash
git clone [https://github.com/vaibhavdsonawane/CityPulse-AI.git](https://github.com/vaibhavdsonawane/CityPulse-AI.git)
cd CityPulse-AI
```
### Step 2: Create a Python Virtual Environment
* **On Windows:**
  ```bash
  python -m venv venv
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```
### Step 3: Activate the Virtual Environment
* **On Windows (Command Prompt `cmd`):**
  ```cmd
  venv\Scripts\activate
  ```
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you get a script execution policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
* **On macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
### Step 4: Upgrade pip & Install Required Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Step 5: Initialize and Seed the Database
```bash
python scripts/setup_db.py
```
*(Or if your project uses a seeder: `python scripts/seed_data.py`)*
### Step 6: Launch the Flask Application
```bash
python run.py
```
### Step 7: Access the Platform in Your Browser
Open your browser and navigate to:
```text
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
```
---
## 🔑 Default User Credentials
### 1. Municipal Administrator (Command Center)
* **URL:** `http://127.0.0.1:5000/admin/dashboard`
* **Email:** `admin@nashik.gov.in`
* **Password:** `admin123`
* **Access Scope:** Satellite GIS threat map, Human-in-the-Loop review queue, department dispatch board, and ML risk sandbox.
### 2. Citizen User (Citizen Portal)
* **URL:** `http://127.0.0.1:5000/citizen/dashboard`
* **Email:** `naresh.k1@nashik.gov.in` (or register any new account)
* **Password:** `citizen123`
* **Access Scope:** Report complaints with map pins and photos, view live calculated priority scores, monitor the 6-step progress stepper, and view civic badges.
---
## 📂 Project Directory Structure
```text
CityPulse-AI/
├── app/
│   ├── __init__.py              # Flask app factory & extensions
│   ├── models.py                # SQLAlchemy relational database models
│   ├── routes/
│   │   ├── auth_routes.py       # Authentication (Register, Login, Logout)
│   │   ├── citizen_routes.py    # Complaint reporting, status tracking, badges
│   │   ├── admin_routes.py      # GIS Command Center & AJAX dispatch queue
│   │   └── api_routes.py        # JSON endpoints for real-time map data
│   ├── services/
│   │   ├── cv_service.py        # YOLOv8 defect detection & bbox annotations
│   │   ├── nlp_service.py       # TF-IDF & Logistic Regression scoring engine
│   │   └── hotspot_service.py   # Haversine distance clustering (50m/350m)
│   ├── static/
│   │   ├── css/                 # Custom design tokens & layout stylesheets
│   │   ├── js/                  # Leaflet map scripts, AJAX dispatch handlers
│   │   └── uploads/             # Citizen photo uploads & annotated results
│   └── templates/
│       ├── base.html            # Core layout wrapper with navbar & alerts
│       ├── citizen/             # Citizen portal views (report, view, badges)
│       └── admin/               # Admin dashboard, GIS satellite view, HITL queue
├── scripts/
│   ├── setup_db.py              # Database initialization & table creation
│   └── seed_data.py             # Realistic test data generator (Nashik ward data)
├── models/
│   └── yolov8n.pt               # Pre-trained/fine-tuned YOLO model weights
├── citypulse.db                 # Local SQLite relational database (auto-generated)
├── requirements.txt             # Python library dependencies
├── run.py                       # Main application entry point
├── .gitignore                   # Excludes venv, pycache, and temp artifacts
└── README.md                    # Project documentation
```
---
## 🧮 Mathematical Formulations
### 1. Multi-Factor Priority Score Formulation
$$Priority = \min(100, \; S + L + I + F)$$
* **Severity (S):** 10 to 40 points derived from NLP keyword analysis.
* **Location Risk (L):** 10 to 30 points based on road hierarchy and proximity to schools/hospitals.
* **Public Impact (I):** 5 to 20 points estimating affected commuter volume.
* **Historical Frequency (F):** 5 to 10 points tracking repeat issues in the area.
### 2. Spatial Haversine Distance
$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$
$$c = 2 \cdot \arctan2\left(\sqrt{a}, \; \sqrt{1-a}\right), \quad d = R \cdot c$$
* **$d \le 50\text{ m}$:** Auto-merge duplicate report.
* **$3+$ issues within $350\text{ m}$:** Active Hazard Hotspot zone.
---
## 🔧 Troubleshooting & Common Issues
* **PowerShell Execution Error:** Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell.
* **Port 5000 in use:** Launch with `flask run --port 5001`.
* **Missing OpenCV dependencies on Linux:** Run `sudo apt update && sudo apt install -y libgl1-mesa-glx libglib2.0-0`.
---
## 👨‍💻 Project Attribution
* **Project Title:** CityPulse AI — Smart Urban Infrastructure Management Platform
* **Academic Program:** Diploma in Information Technology[span_1](start_span)[span_1](end_span)
* **Board:** Maharashtra State Board of Technical Education (MSBTE)[span_2](start_span)[span_2](end_span)
* **Institution:** Mahavir Polytechnic, Nashik[span_3](start_span)[span_3](end_span)
* **Academic Year:** 2026–2027[span_4](start_span)[span_4](end_span)
* **Candidate Name:** Vaibhav Dipak Sonawane (Enrollment No: 246112204496)[span_5](start_span)[span_5](end_span)
* **Project Guide:** Mr. Vaibhav Desai[span_6](start_span)[span_6](end_span)
