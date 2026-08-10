import os
import cv2
import json
import logging
from typing import Dict, Any, Tuple
from ultralytics import YOLO

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', '..', 'saved_models', 'cv_models')
# We look for your custom trained model, but fallback to the base YOLO model if it's not ready yet
CUSTOM_MODEL_PATH = os.path.join(MODEL_DIR, 'citypulse_detector', 'weights', 'best.pt')

class VisionPredictor:
    """Singleton class to load the YOLOv8 model for image inference."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionPredictor, cls).__new__(cls)
            cls._instance.model = None
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        try:
            if os.path.exists(CUSTOM_MODEL_PATH):
                self.model = YOLO(CUSTOM_MODEL_PATH)
                logging.info("Custom CityPulse YOLO model loaded successfully.")
            else:
                logging.warning("Custom YOLO model not found. Loading base YOLOv8n for testing.")
                self.model = YOLO('yolov8n.pt') # Downloads base model automatically
        except Exception as e:
            logging.error(f"Failed to load CV model: {str(e)}")

    def analyze_image(self, image_path: str) -> Tuple[str, float, str, str]:
        """
        Processes an image, draws bounding boxes, and returns detection data.
        Returns: (detected_class, confidence, bounding_box_json, annotated_image_filename)
        """
        if not self.model or not os.path.exists(image_path):
            return ("Unknown", 0.0, "[]", os.path.basename(image_path))

        try:
            # Run inference
            results = self.model(image_path)[0]
            
            # Extract top prediction
            detected_class = "None"
            confidence = 0.0
            bbox_data = []

            if len(results.boxes) > 0:
                # Get the box with the highest confidence
                best_box = results.boxes[0]
                class_id = int(best_box.cls[0])
                detected_class = results.names[class_id]
                confidence = float(best_box.conf[0])
                
                # Format bounding box for database [x1, y1, x2, y2]
                bbox_data = best_box.xyxy[0].tolist()
            
            # Draw the bounding boxes on the image and save it
            annotated_image = results.plot() # YOLO's built-in plotting tool
            
            # Create a new filename for the annotated image
            directory, filename = os.path.split(image_path)
            annotated_filename = f"ai_{filename}"
            annotated_filepath = os.path.join(directory, annotated_filename)
            
            # Save the annotated image using OpenCV
            cv2.imwrite(annotated_filepath, annotated_image)
            
            return (detected_class, confidence, json.dumps(bbox_data), annotated_filename)
            
        except Exception as e:
            logging.error(f"CV Analysis failed: {str(e)}")
            return ("Error", 0.0, "[]", os.path.basename(image_path))

# Expose instance
vision_ai = VisionPredictor()