| PSO1 | PSO2 |
| :---: | :---: |

FINAL YEAR PROJECT SYNOPSIS

Technology Domain / Theme: Artificial Intelligence (Computer Vision & NLP), Full-Stack Web Development, and Geospatial Information Systems (GIS)
Project Title: CityPulse AI – Smart Urban Infrastructure Management Platform

Problem Statement:
In rapidly expanding cities like Nashik, municipal corporations rely on slow manual logging and physical field inspections, often taking 7 to 15 days just to verify civic defects like monsoon road craters, leaking water mains, and overflowing garbage bins. Because current portals lack spatial mapping and objective priority scoring, multiple citizens report the same defect, causing maintenance crews to waste fuel and labor on duplicate visits while urgent road hazards near hospitals and schools remain unattended.

What Problems Does the Project Solve?
• Eliminates Manual Site Verification Delays: Uses YOLOv8 image detection to instantly verify defect photos, cutting verification time from days to seconds.
• Removes Subjective Complaint Handling: Replaces arbitrary first-come-first-served queues with an automated 0–100 priority score based on text severity, road risk, and commuter impact.
• Stops Duplicate Work Orders: Uses the Haversine formula to detect and auto-merge repeated reports within a 50-meter radius into a single dispatch ticket.
• Prevents Uncoordinated Field Trips: Groups clustered civic issues within 350 meters into visual hazard hotspots on a satellite map so crews can resolve multiple defects in one visit.
• Restores Citizen Visibility: Replaces zero-feedback complaint portals with a live 6-step visual progress bar that shows citizens every stage of the repair.

Project Objectives:
• To enable citizens to report civic defects with geotagged map pins and photo evidence.
• To automate defect verification by scanning photos using the YOLOv8 object detection model.
• To assign an objective 0–100 Priority Score to every complaint using NLP text analysis.
• To auto-merge duplicate complaints within 50 meters and identify 350-meter hazard hotspots using the Haversine formula.
• To provide an administrative dashboard for fast department dispatching using non-reloading AJAX forms.
• To provide real-time repair tracking for citizens via a 6-step visual status stepper.

Scope of the Project:
• Features and Functionalities Included:
  - Dual-portal web interface: Citizen Portal and Municipal Admin Command Center.
  - AI defect detection across five civic categories: potholes, garbage piles, broken streetlights, water leaks, and fallen trees.
  - Human-in-the-Loop (HITL) review queue to hold low-confidence image detections (< 60%) for manual staff confirmation.
  - Interactive satellite GIS map displaying color-coded priority pins and glowing hazard clusters.
  - Gamified citizen reward system featuring unlockable civic badges and resolution star ratings.
• Limitations or Boundaries:
  - The system is configured for the Nashik municipal boundary and will not support other cities in this version.
  - The platform uses a local SQLite database for demonstration and testing rather than distributed cloud clustering.
  - Defect detection depends on user-uploaded photos; hardware-based IoT road sensors are not included in this version.

System Requirements:
• Hardware Requirements:
  - Minimum Configuration: Intel Core i3 / AMD Ryzen 3, 4 GB RAM, 10 GB free hard disk space, standard monitor, active internet connection.
  - Recommended Configuration: Intel Core i5 / AMD Ryzen 5 or higher, 8 GB RAM, 20 GB SSD storage, dedicated GPU for faster model inference.
• Software Requirements:
  - Operating System: Windows 10/11 or Ubuntu Linux 20.04+.
  - Programming Languages: Python 3.11+, JavaScript (ES6+), HTML5, CSS3.
  - Web Framework: Flask 3.0+ (MVC pattern).
  - Database Engine: SQLite3 with SQLAlchemy ORM.
  - AI & ML Libraries: Ultralytics YOLOv8, OpenCV, Scikit-Learn, Pandas, NumPy.
  - Mapping & UI Tools: Leaflet.js, Bootstrap 5.3.
  - Development Environment: Visual Studio Code, Git.

Modules of the System:
• Citizen Reporting Module: Enables citizens to register, log in, drop a geotagged map pin, upload defect photos, and track repair status via a 6-step progress bar.
• AI Computer Vision Module: Processes uploaded images using YOLOv8, detects defect classes (potholes, garbage, water leaks, streetlights, fallen trees), and flags low-confidence images (< 60%) for manual staff review.
• NLP Priority Scoring Module: Analyzes complaint text using TF-IDF and Logistic Regression to compute an objective 0–100 Priority Score based on severity, location risk, and public impact.
• Spatial GIS & Clustering Module: Applies the Haversine formula to auto-merge duplicate complaints within 50 meters and group nearby issues within 350 meters into glowing hazard hotspots.
• Admin Command Center Module: Displays a real-time satellite threat map, provides a Human-in-the-Loop review queue, and enables instant department dispatching without page reloads using AJAX.

Expected Output / Deliverables:
• A responsive web application featuring separate, role-secured Citizen and Municipal Admin portals.
• An automated image verification engine that outputs annotated photos with detected defect boxes and confidence percentages.
• An interactive satellite GIS map displaying color-coded incident markers and animated hotspot zones.
• A structured relational SQLite database containing user accounts, geotagged complaints, AI detection logs, and lifecycle audit histories.

Conclusion:
• Replaces slow physical site inspections with automated AI photo verification, cutting verification delays from weeks to seconds.
• Eliminates duplicate work orders and saves municipal fuel and labor by auto-merging repeated reports within 50 meters.
• Removes subjective human bias by prioritizing critical road and utility hazards using an objective 0–100 scoring formula.
• Restores public trust in local governance by giving citizens step-by-step visibility into repair progress.

References:
• Ultralytics, "YOLOv8 Architecture and Usage Guide," Ultralytics Documentation, 2023.
• Pallets Projects, "Flask Web Framework Documentation (v3.0.x)," Pallets Community, 2024.
• F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, 2011.
• Leaflet, "Leaflet.js API Reference (v1.9.4) – Interactive Mapping Library," 2023.
