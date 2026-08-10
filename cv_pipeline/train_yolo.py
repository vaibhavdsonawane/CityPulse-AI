import os
import logging
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def train_citypulse_vision():
    """Trains a custom YOLOv8 model for Smart City Issue Detection."""
    logging.info("Initializing YOLOv8 Nano model...")
    
    # Load the base model (Nano version is best for fast web inference)
    model = YOLO('yolov8n.pt') 

    # Paths
    yaml_path = os.path.join(os.path.dirname(__file__), 'data.yaml')
    save_dir = os.path.join('saved_models', 'cv_models')
    os.makedirs(save_dir, exist_ok=True)

    logging.info("Starting training process...")
    # Train the model
    # Note: 'epochs' should be 50-100 for production. Set to 1 just to test the script.
    results = model.train(
        data=yaml_path,
        epochs=50, 
        imgsz=640,
        batch=16,
        project=save_dir,
        name='citypulse_detector'
    )
    
    logging.info(f"Training complete. Model saved in {save_dir}/citypulse_detector")

if __name__ == '__main__':
    train_citypulse_vision()