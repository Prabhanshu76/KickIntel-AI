from common_imports import cv2
from detection_utility import detections2boxes
from config import parse_config, load_model, load_video_capture, load_boundaries, load_objects, get_player_in_possession_proximity
from geometry_utilities import Detection, filter_detections_by_class
import torch

def extract_player_images():
    # Clear CUDA cache
    torch.cuda.empty_cache()
    
    # Load configurations and model
    config = parse_config("config.ini")
    model = load_model(config['Paths']['WEIGHTS_PATH'])
    cap = load_video_capture(config['Paths']['SOURCE_VIDEO_PATH'])
    # boundaries = load_boundaries(config)
    # objects = load_objects(config, boundaries)
    # PLAYER_IN_POSSESSION_PROXIMITY = get_player_in_possession_proximity(config)
    
    # jersey_classifier, _, _, _, _, byte_tracker, _, _ = objects

    player_images = []
    frame_count = 0

    while frame_count < 35:
        success, frame = cap.read()
        if not success:
            break
        
        results = model(frame, size=1280)
        detections = Detection.from_results(
            pred=results.pred[0].cpu().numpy(),
            names=model.names)

        player_detections = filter_detections_by_class(detections=detections, class_name="player")

        for player_detection in player_detections:
            rect = player_detection.rect
            x, y, width, height = int(rect.x), int(rect.y), int(rect.width), int(rect.height)
            player_image = frame[y:y+height, x:x+width]
            player_images.append(player_image)
        
        frame_count += 1

    cap.release()
    return player_images
