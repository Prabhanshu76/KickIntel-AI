import configparser
from common_imports import torch, np, cv2, BYTETracker
from geometry_utilities import BaseAnnotator, Color, Detection, filter_detections_by_class
from colors import *
from text_annotator import TextAnnotator
from possession_maker import MarkerAnntator
from byte_tracker_args import BYTETrackerArgs
from player_in_possession import get_player_in_possession
from jersey_classifier_hsv import PlayerJerseyClassifier
from possession_calc import *
from pass_counter import *
from frame_count import *

def parse_config(config_file="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def load_model(weights_path):
    # Check if GPU is available
    if torch.cuda.is_available():
        device = 0
        print("Using GPU")
    else:
        device = 'cpu'
        print("Using CPU")

    model = torch.hub.load('ultralytics/yolov5', 'custom', weights_path, device=device)
    return model

def load_video_capture(source_video_path):
    cap = cv2.VideoCapture(source_video_path)
    return cap

def load_boundaries(config):
    boundaries_team1_min = [
        int(config['Boundaries_HSV']['TEAM1_H_MIN']),
        int(config['Boundaries_HSV']['TEAM1_S_MIN']),
        int(config['Boundaries_HSV']['TEAM1_V_MIN'])
    ]
    boundaries_team1_max = [
        int(config['Boundaries_HSV']['TEAM1_H_MAX']),
        int(config['Boundaries_HSV']['TEAM1_S_MAX']),
        int(config['Boundaries_HSV']['TEAM1_V_MAX'])
    ]

    boundaries_team2_min = [
        int(config['Boundaries_HSV']['TEAM2_H_MIN']),
        int(config['Boundaries_HSV']['TEAM2_S_MIN']),
        int(config['Boundaries_HSV']['TEAM2_V_MIN'])
    ]
    boundaries_team2_max = [
        int(config['Boundaries_HSV']['TEAM2_H_MAX']),
        int(config['Boundaries_HSV']['TEAM2_S_MAX']),
        int(config['Boundaries_HSV']['TEAM2_V_MAX'])
    ]

    boundaries = [
        (np.array(boundaries_team1_min), np.array(boundaries_team1_max)),
        (np.array(boundaries_team2_min), np.array(boundaries_team2_max))
    ]

    return boundaries

def load_objects(config, boundaries):
    jersey_classifier = PlayerJerseyClassifier(config['Teams']['COLOR_LIST'].split(','), boundaries)

    base_annotator = BaseAnnotator(
        colors=[
            BALL_COLOR,
            PLAYER_COLOR,
            PLAYER_COLOR_BLUE,
            PLAYER_COLOR_WHITE,
            REFEREE_COLOR
        ],
        thickness=THICKNESS)

    player_goalkeeper_text_annotator = TextAnnotator(
        PLAYER_COLOR, PLAYER_COLOR_BLUE, PLAYER_COLOR_WHITE, text_color=Color(255, 255, 255), text_thickness=2)

    ball_marker_annotator = MarkerAnntator(
        color=BALL_MARKER_FILL_COLOR)
    player_in_possession_marker_annotator = MarkerAnntator(
        color=PLAYER_MARKER_FILL_COLOR)
    player_marker_annotator = MarkerAnntator(color=PLAYER_MARKER_FILL_COLOR)

    byte_tracker = BYTETracker(BYTETrackerArgs())

    possession_calculator = PossessionCalculator()

    pass_tracker = PassTracker()
    frame_count = VideoFrameCounter(config['Paths']['SOURCE_VIDEO_PATH'])

    total_frames = frame_count.count_frames()

    return (
        jersey_classifier,
        base_annotator,
        player_goalkeeper_text_annotator,
        ball_marker_annotator,
        player_marker_annotator,
        byte_tracker,
        possession_calculator,
        pass_tracker
    )


def get_player_in_possession_proximity(config):
    return int(config['PROXIMITY']['PLAYER_IN_POSSESSION_PROXIMITY'])
