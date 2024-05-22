from common_imports import List, Optional
from geometry_utilities import Detection

import math


# # resolves which player is currently in ball possession based on player-ball proximity
# def get_player_in_possession(
#     player_detections: List[Detection],
#     ball_detections: List[Detection],
#     proximity: int
# ) -> Optional[Detection]:
#     if len(ball_detections) != 1:
#         return None
#     ball_detection = ball_detections[0]
#     for player_detection in player_detections:
#         if player_detection.rect.pad(proximity).contains_point(point=ball_detection.rect.center):
#             return player_detection





def get_player_in_possession(
    player_detections: List[Detection],
    ball_detections: List[Detection],
    proximity: int
) -> Optional[Detection]:
    if len(ball_detections) != 1:
        return None

    ball_detection = ball_detections[0]
    ball_center = ball_detection.rect.center

    for player_detection in player_detections:
        # Calculate the bottom center of the player's rectangle
        player_bottom_center = (
            player_detection.rect.center[0],  # X-coordinate remains the same
            player_detection.rect.bottom      # Y-coordinate is the bottom of the rectangle
        )

        # Calculate the distance between the bottom center of the player and the center of the ball
        distance = math.sqrt(
            (player_bottom_center[0] - ball_center[0]) ** 2 +
            (player_bottom_center[1] - ball_center[1]) ** 2
        )

        # Check if the distance is within the specified proximity
        if distance <= proximity:
            return player_detection

    # Return None if no player is in possession
    return None
