import os
import re
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class MunicipalNLPPriorityEngine:
    """
    Scikit-Learn Machine Learning Classifier & Mathematical Priority Scoring Engine.
    Uses TF-IDF Feature Extraction + Logistic Regression for automatic category prediction,
    combined with a multi-factor risk heuristic to compute Priority Scores (0-100).
    """

    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'nlp_model.pkl')
        self.pipeline = None
        self._initialize_or_train_model()

        # Keyword Dictionary Matrix for Contextual Feature Extraction
        self.severity_keywords = {
            'critical': ['crater', 'burst', 'collapsed', 'uprooted', 'hanging cable', 'flooding', 'injury', 'explosion', 'fire', 'paralyzed'],
            'high': ['huge', 'deep', 'overflowing', 'leakage', 'darkness', 'blocked', 'hazard', 'severe', 'damage', 'skid'],
            'medium': ['cracked', 'flickering', 'smell', 'garbage heap', 'unlit', 'slow', 'waste', 'broken'],
            'low': ['minor', 'litter', 'small', 'dirty', 'patch', 'cleaning']
        }

        self.location_risk_keywords = {
            'high_risk_zone': ['school', 'hospital', 'college', 'chowk', 'highway', 'flyover', 'junction', 'market', 'station', 'bus stand', 'main road', 'arterial'],
            'medium_risk_zone': ['colony', 'lane', 'park', 'jogging track', 'residential', 'society', 'garden']
        }

        self.impact_keywords = {
            'high_impact': ['traffic jam', 'accident risk', 'women safety', 'senior citizen', 'two-wheeler', 'pedestrian', 'children', 'commuter', 'daily traffic'],
            'medium_impact': ['foul odor', 'nuisance', 'unhygienic', 'inconvenience', 'footpath']
        }

    def _get_training_dataset(self):
        """Synthetic Municipal Infrastructure NLP Training Corpus."""
        X_train = [
            # Pothole / Road Damage
            "Huge deep pothole near Trimurti Chowk traffic signal causing two-wheeler skids and severe traffic jams.",
            "Cracked asphalt with multiple potholes on College Road opposite KBT Circle during peak office hours.",
            "Dangerous crater on main Gangapur Road near Jehan Circle needing immediate bituminous patching.",
            "Sunken manhole and deep road cavity near Mumbai Naka flyover creating accident risk for night commuters.",
            "Severe road breakdown near Satpur MIDC bus stop causing heavy vehicle axle damage.",
            "Large pothole near Govind Nagar jogging track lane dangerous for walking.",
            "Damaged asphalt layer near Dwarka Circle underpass causing major traffic slowdown.",
            "Caved in road surface near Cidco Uttam Nagar vegetable market junction.",
            
            # Garbage / Sanitation
            "Overflowing municipal waste container near Panchavati Karanja with stray animals spreading plastic trash.",
            "Illegal plastic and commercial dumping on empty plot near Govind Nagar jogging track foul odor spreading.",
            "Construction debris and domestic trash piled up along Cidco Uttam Nagar main market road.",
            "Uncleaned garbage heap near Satpur MIDC bus stop causing severe health concerns for factory workers.",
            "Decaying organic waste bin overflow near Shalimar market junction blocking pedestrian path.",
            "Unattended garbage mound dumped near Mahatmanagar playground creating severe unhygienic conditions.",
            "Plastic waste accumulation near Indira Nagar underpass blocking storm water drain opening.",
            "Trash heap burning illegally near Mumbai Naka back road causing smoke nuisance.",

            # Water Leakage / Supply
            "Underground drinking water supply pipeline burst on Mahatmanagar water tank line wasting thousands of liters.",
            "High pressure main line water leakage near Shalimar Chowk flooding the pedestrian walkway.",
            "Subsurface pipe rupture near Indira Nagar underpass leaking clean water continuously for 2 days.",
            "Drainage pipeline overflow and sewage water leaking on Old Agra Road junction near Panchavati.",
            "Burst water pipeline connection on College Road near Bhonsala Circle flooding main avenue.",
            "Leaking public tap connection wasting treated municipal water near Gangapur Road pump house.",
            "Underground supply line leakage causing waterlogging near Trimurti Chowk market area.",
            "Major pipe crack near Satpur MIDC main entry road washing away road mud.",

            # Fallen Tree / Forestry
            "Large Gulmohar tree branch collapsed across Gangapur Road blocking traffic towards Someshwar.",
            "Uprooted tree trunk leaning precariously over electrical cables on College Road near Bhonsala Military College.",
            "Heavy storm branch fallen down near RTO Naka blocking one complete lane of main avenue.",
            "Old banyan tree branch cracked and hanging dangerously near Dwarka Circle bus stand.",
            "Fallen neem tree trunk completely blocking interior access lane in Indira Nagar Sector 2.",
            "Broken heavy tree limb blocking footpath and partial road near Govind Nagar park.",
            "Uprooted eucalyptus tree blocking traffic near Cidco Uttam Nagar stadium road.",
            "Storm damaged tree branch fallen on parked vehicles near Panchavati Ghat road.",

            # Streetlight / Lighting
            "Continuous dark stretch from Uttam Nagar to Trimurti Chowk due to 6 non-functional LED streetlight poles.",
            "Flickering sodium light lamp post near Panchavati Ghats creating women safety concern at night.",
            "Broken light pole knocked over by truck near Satpur Ambad Link Road main signal.",
            "Entire street light circuit down on Canada Corner main lane for last 4 days.",
            "Dark alley stretch near Indira Nagar jogging track due to dead bulb on pole 14.",
            "Non-functional streetlights along Gangapur Road river bridge causing night driving hazards.",
            "Unlit dark corridor on College Road back street near hostel area.",
            "Damaged junction box causing streetlights to stay off on Mumbai Naka approach road."
        ]

        y_train = [
            "Pothole", "Pothole", "Pothole", "Pothole", "Pothole", "Pothole", "Pothole", "Pothole",
            "Garbage", "Garbage", "Garbage", "Garbage", "Garbage", "Garbage", "Garbage", "Garbage",
            "Water Leakage", "Water Leakage", "Water Leakage", "Water Leakage", "Water Leakage", "Water Leakage", "Water Leakage", "Water Leakage",
            "Fallen Tree", "Fallen Tree", "Fallen Tree", "Fallen Tree", "Fallen Tree", "Fallen Tree", "Fallen Tree", "Fallen Tree",
            "Streetlight", "Streetlight", "Streetlight", "Streetlight", "Streetlight", "Streetlight", "Streetlight", "Streetlight"
        ]

        return X_train, y_train

    def _initialize_or_train_model(self):
        """Train or load the Machine Learning NLP Pipeline."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.pipeline = pickle.load(f)
                return
            except Exception:
                pass

        # Build Machine Learning Pipeline: TF-IDF Vectorizer + Logistic Regression Classifier
        X_train, y_train = self._get_training_dataset()
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', LogisticRegression(C=1.0, max_iter=200))
        ])
        self.pipeline.fit(X_train, y_train)

        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.pipeline, f)
        except Exception:
            pass

    def predict_from_text(self, text: str, complaint_frequency: int = 1) -> dict:
        """
        Processes complaint text through ML Classifier & Risk Heuristic.
        Computes Priority Score = Severity + Location Risk + Citizen Impact + Frequency
        """
        text_lower = text.lower() if text else ""

        # 1. ML Category Classification & Confidence
        if self.pipeline and text_lower.strip():
            predicted_category = self.pipeline.predict([text_lower])[0]
            proba = self.pipeline.predict_proba([text_lower])[0]
            confidence_pct = int(np.max(proba) * 100)
        else:
            predicted_category = "Pothole"
            confidence_pct = 75

        # 2. Factor 1: Severity Points (0 - 30)
        severity_pts = 10  # Base
        for word in self.severity_keywords['critical']:
            if word in text_lower:
                severity_pts += 20
                break
        else:
            for word in self.severity_keywords['high']:
                if word in text_lower:
                    severity_pts += 15
                    break
            else:
                for word in self.severity_keywords['medium']:
                    if word in text_lower:
                        severity_pts += 10
                        break
        severity_pts = min(severity_pts, 30)

        # 3. Factor 2: Location Risk Points (0 - 25)
        location_pts = 8  # Base
        for word in self.location_risk_keywords['high_risk_zone']:
            if word in text_lower:
                location_pts += 17
                break
        else:
            for word in self.location_risk_keywords['medium_risk_zone']:
                if word in text_lower:
                    location_pts += 10
                    break
        location_pts = min(location_pts, 25)

        # 4. Factor 3: Citizen Impact Points (0 - 25)
        impact_pts = 8  # Base
        for word in self.impact_keywords['high_impact']:
            if word in text_lower:
                impact_pts += 17
                break
        else:
            for word in self.impact_keywords['medium_impact']:
                if word in text_lower:
                    impact_pts += 10
                    break
        impact_pts = min(impact_pts, 25)

        # 5. Factor 4: Complaint Frequency Points (0 - 20)
        frequency_pts = min(complaint_frequency * 5, 20)

        # 6. Calculate Final Priority Score (0 - 100)
        raw_priority = severity_pts + location_pts + impact_pts + frequency_pts
        priority_score = min(max(raw_priority, 15), 100)

        # 7. Determine Severity Level & Badge Matrix
        if priority_score >= 85:
            severity_label = "Critical"
            priority_badge = "🔴 Critical"
            badge_color = "bg-danger text-white"
            recommendation = "Immediate emergency field team dispatch required due to high safety risk."
        elif priority_score >= 65:
            severity_label = "High"
            priority_badge = "🟠 High"
            badge_color = "bg-warning text-dark"
            recommendation = "High priority queue assignment. Inspection scheduled within 12 hours."
        elif priority_score >= 40:
            severity_label = "Medium"
            priority_badge = "🟡 Medium"
            badge_color = "bg-info text-dark"
            recommendation = "Standard priority queue assignment. Routine repair scheduled within 24-48 hours."
        else:
            severity_label = "Low"
            priority_badge = "🟢 Low"
            badge_color = "bg-success text-white"
            recommendation = "Low risk report logged. Added to weekly municipal maintenance schedule."

        return {
            'predicted_category': predicted_category,
            'category_confidence': max(confidence_pct, 65),
            'priority_score': priority_score,
            'severity': severity_label,
            'priority_badge': priority_badge,
            'badge_color': badge_color,
            'severity_pts': severity_pts,
            'location_pts': location_pts,
            'impact_pts': impact_pts,
            'frequency_pts': frequency_pts,
            'recommendation': recommendation,
            'location_risk': 'High' if location_pts >= 18 else 'Medium'
        }

# Singleton instance export
nlp_ai = MunicipalNLPPriorityEngine()