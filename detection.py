from IPython.display import display, clear_output
import PIL.Image
from common_imports import io, os, tqdm, cv2, torch, BYTETracker, np

from video_writer import VideoConfig, get_video_writer, generate_frames
from geometry_utilities import BaseAnnotator, Color, Detection, filter_detections_by_class
from colors import *
from text_annotator import TextAnnotator
from possession_maker import MarkerAnntator
from byte_tracker_args import BYTETrackerArgs
from player_in_possession import get_player_in_possession
from detection_utility import detections2boxes, match_detections_with_tracks
from jersey_classifier import PlayerJerseyClassifier
from possession_calc import *
from pass_counter import *
from frame_count import *


def detection(WEIGHTS_PATH, model, SOURCE_VIDEO_PATH, TARGET_VIDEO_PATH, color_list, boundaries):

    fcount=0

    # initiate video writer
    video_config = VideoConfig(
        fps=30,
        width=1920,
        height=1080)
    video_writer = get_video_writer(
        target_video_path=TARGET_VIDEO_PATH,
        video_config=video_config)

    # get fresh video frame generator
    frame_iterator = iter(generate_frames(video_file=SOURCE_VIDEO_PATH))

    # initiate annotators
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
        PLAYER_COLOR, PLAYER_COLOR_BLUE,PLAYER_COLOR_WHITE, text_color=Color(255, 255, 255), text_thickness=2)
    #referee_text_annotator = TextAnnotator(
    #    REFEREE_COLOR, text_color=Color(0, 0, 0), text_thickness=2)

    ball_marker_annotator = MarkerAnntator(
        color=BALL_MARKER_FILL_COLOR)
    player_in_possession_marker_annotator = MarkerAnntator(
        color=PLAYER_MARKER_FILL_COLOR)
    player_marker_annotator = MarkerAnntator(color=PLAYER_MARKER_FILL_COLOR)


    # initiate tracker
    byte_tracker = BYTETracker(BYTETrackerArgs())

    jersey_classifier = PlayerJerseyClassifier(color_list,boundaries)

    possession_calculator = PossessionCalculator()
    possession_team=""

    player_in_possession_detection = None
    player_in_possession_track_id = None


    pass_tracker = PassTracker()
    frame_count = VideoFrameCounter(SOURCE_VIDEO_PATH)

    total_frames = frame_count.count_frames()  # class to auto cal total frames


    # team1_passes = 0
    # team2_passes = 0


    # last_team1_possession_track_id = None
    # last_team2_possession_track_id = None
    # last_possession_team = None


    # Loop over frames
    for frame in tqdm(frame_iterator, total=total_frames):
        # Run detector
        results = model(frame, size=1280)
        detections = Detection.from_results(
            pred=results.pred[0].cpu().numpy(),
            names=model.names)

        # Filter detections by class
        ball_detections = filter_detections_by_class(detections=detections, class_name="ball")
        referee_detections = filter_detections_by_class(detections=detections, class_name="referee")
        goalkeeper_detections = filter_detections_by_class(detections=detections, class_name="goalkeeper")
        player_detections = filter_detections_by_class(detections=detections, class_name="player")
        print(len(player_detections))

        annotated_image = frame.copy()

        # Create a list to store the classifications of player jerseys
        player_classifications = []
        
        
        player_in_possession_detection = None
        # Classify player jerseys and store the result in player_classifications
        # for player_detection in player_detections:
        #     rect = player_detection.rect
        #     x, y, width, height = int(rect.x), int(rect.y), int(rect.width), int(rect.height)
        #     player_image = frame[y:y+height, x:x+width]  # Crop player image
        #     jersey_color = jersey_classifier.classify_player_jersey(player_image)
        #     player_classifications.append(jersey_color)
            
        #     if len(ball_detections) != 1:
        #         player_in_possession_detection = None
        #     elif player_detection.rect.pad(PLAYER_IN_POSSESSION_PROXIMITY).contains_point(point=ball_detections[0].rect.center):
        #         possession_team=jersey_color
        #         player_in_possession_detection = player_detection
        #         print("########################################################")
        #         print(player_detection)
        #         print("########################################################")
                

        print(possession_team)

        player_goalkeeper_detections = player_detections + goalkeeper_detections
        tracked_detections = player_detections + goalkeeper_detections + referee_detections

        
        
        
        if len(detections2boxes(detections=tracked_detections)):
            # trackcol
            tracks = byte_tracker.update(
                output_results=detections2boxes(detections=tracked_detections),
                img_info=frame.shape,
                img_size=frame.shape
            )

            if len(tracks):
                tracked_detections = match_detections_with_tracks(detections=tracked_detections, tracks=tracks)

                tracked_referee_detections = filter_detections_by_class(detections=tracked_detections, class_name="referee")
                tracked_goalkeeper_detections = filter_detections_by_class(detections=tracked_detections, class_name="goalkeeper")
                tracked_player_detections = filter_detections_by_class(detections=tracked_detections, class_name="player")

                for player_detection in tracked_player_detections:
                    rect = player_detection.rect
                    x, y, width, height = int(rect.x), int(rect.y), int(rect.width), int(rect.height)
                    player_image = frame[y:y+height, x:x+width]  # Crop player image
                    jersey_color = jersey_classifier.classify_player_jersey(player_image)
                    player_classifications.append(jersey_color)
                    if len(ball_detections) != 1:
                        player_in_possession_detection = None
                        player_in_possession_track_id = None
                    elif player_detection.rect.pad(PLAYER_IN_POSSESSION_PROXIMITY).contains_point(point=ball_detections[0].rect.center):
                        possession_team=jersey_color
                        player_in_possession_detection = player_detection
                        player_in_possession_track_id = player_detection.tracker_id  # Store the track ID of the player in possession

                        #print(tracked_player_detections)

                # Annotate video frame
                annotated_image = base_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_detections)

                annotated_image = player_goalkeeper_text_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_goalkeeper_detections + tracked_player_detections,
                    jersey_colors=player_classifications)  # Pass the jersey colors



                #annotated_image = referee_text_annotator.annotate(
                    #image=annotated_image,
                    #detections=tracked_referee_detections)

                annotated_image = ball_marker_annotator.annotate(
                    image=annotated_image,
                    detections=ball_detections)

                annotated_image = player_marker_annotator.annotate(
                    image=annotated_image,
                    detections=[player_in_possession_detection] if player_in_possession_detection else [])





                print(possession_team)
                print("Player in Possession Track ID:", player_in_possession_track_id)  # Print the track ID

                # Calculate passes for each team
                # if possession_team == 'Team 1':
                #     if (
                #         player_in_possession_track_id is not None
                #         and player_in_possession_track_id != last_team1_possession_track_id
                #     ):
                #         team1_passes += 1
                #         last_team1_possession_track_id = player_in_possession_track_id

                # elif possession_team == 'Team 2':
                #     if (
                #         player_in_possession_track_id is not None
                #         and player_in_possession_track_id != last_team2_possession_track_id
                #     ):
                #         team2_passes += 1
                #         last_team2_possession_track_id = player_in_possession_track_id


                # if possession_team != last_possession_team:
                #     last_possession_team = possession_team


                # if possession_team == 'Team 1':
                #     if (
                #         player_in_possession_track_id is not None
                #         and player_in_possession_track_id != last_team1_possession_track_id
                #         and last_possession_team == 'Team 1'  # Check if the last possession was also by Team 1
                #     ):
                #         team1_passes += 1
                #         last_team1_possession_track_id = player_in_possession_track_id

                # elif possession_team == 'Team 2':
                #     if (
                #         player_in_possession_track_id is not None
                #         and player_in_possession_track_id != last_team2_possession_track_id
                #         and last_possession_team == 'Team 2'  # Check if the last possession was also by Team 2
                #     ):
                #         team2_passes += 1
                #         last_team2_possession_track_id = player_in_possession_track_id

                # Print the passes for each team in the current frame

                # Inside the frame analysis loop
                pass_tracker.update_pass(possession_team, player_in_possession_track_id)





                team1_passes, team2_passes = pass_tracker.get_passes()
                print("Team 1 Passes:", team1_passes)
                print("Team 2 Passes:", team2_passes)




                ######combine player in possession detection and jersey detection in above for loop, so when the player is in possesion, jersey color will be save for that frame.
                possession_calculator.update_possession(possession_team)
                
                current_frame = 1 + possession_calculator.team1_possession + possession_calculator.team2_possession

                # Get possession statistics for the current frame
                team1_percentage, team2_percentage = possession_calculator.get_possession_stats(current_frame)

                # Print the possession percentages for the current frame
                print(f"Frame {current_frame}:")
                print("Team 1 Possession Percentage: {:.2f}%".format(team1_percentage))
                print("Team 2 Possession Percentage: {:.2f}%".format(team2_percentage))

        # save video frame
        #video_writer.write(annotated_image)

    # Close output video
    #video_writer.release()


        cv2.imshow("Annotated Video", annotated_image)

        # Press 'q' to quit the video display
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    

    team1_percentage, team2_percentage = possession_calculator.get_possession_stats(total_frames)
    total_percentage = team1_percentage + team2_percentage
    normalized_team1_percentage = (team1_percentage / total_percentage) * 100
    normalized_team2_percentage = (team2_percentage / total_percentage) * 100

    # Print the normalized possession percentages
    print("Team 1 Possession Percentage: {:.2f}%".format(normalized_team1_percentage))
    print("Team 2 Possession Percentage: {:.2f}%".format(normalized_team2_percentage))

    ## pass_tracker.reset()

    # close output video
    cv2.destroyAllWindows()
    video_writer.release()