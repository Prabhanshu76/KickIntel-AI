
from common_imports import shutil, os, cv2, torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import parse_config, load_model, load_video_capture, load_boundaries, load_objects, get_player_in_possession_proximity
from geometry_utilities import Detection, filter_detections_by_class
from get_train_data import extract_player_images
from jersey_classifier_kmeans import PlayerJerseyClassifier
from detection_utility import detections2boxes, match_detections_with_tracks
import configparser

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

team1_passes = team2_passes = team1_possession_percentage = team2_possession_percentage = 0
config = parse_config("config.ini")
model = load_model(config['Paths']['WEIGHTS_PATH'])
video_file_path = ''

UPLOAD_DIRECTORY = "./uploaded_videos"
DEMO_VIDEOS_DIRECTORY = "./demo_videos"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, "uploaded_video.mp4")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    update_config_file(file_path)
    return {"filename": file.filename}

@app.get("/video-feed")
async def video_feed():
    def generate_frames():
        print("Code called")
        torch.cuda.empty_cache()
        config = parse_config("config.ini")
        cap = load_video_capture(config['Paths']['SOURCE_VIDEO_PATH'])
        boundaries = load_boundaries(config)
        objects = load_objects(config, boundaries)
        PLAYER_IN_POSSESSION_PROXIMITY = get_player_in_possession_proximity(config)

        jersey_classifier, base_annotator, player_goalkeeper_text_annotator, ball_marker_annotator, player_marker_annotator, byte_tracker, possession_calculator, pass_tracker = objects

        global team1_passes, team2_passes, team1_possession_percentage, team2_possession_percentage
        possession_team=""

        player_data=extract_player_images()
        print(player_data)
        pjc = PlayerJerseyClassifier()
        pjc.train_kmeans_model(player_data)

        player_in_possession_detection = None
        player_in_possession_track_id = None
        while True:
            success, frame = cap.read()

            if not success:
                break

            results = model(frame, size=1280)
            detections = Detection.from_results(
                pred=results.pred[0].cpu().numpy(),
                names=model.names)

            ball_detections = filter_detections_by_class(detections=detections, class_name="ball")
            referee_detections = filter_detections_by_class(detections=detections, class_name="referee")
            goalkeeper_detections = filter_detections_by_class(detections=detections, class_name="goalkeeper")
            player_detections = filter_detections_by_class(detections=detections, class_name="player")
            print(len(player_detections))

            annotated_image = frame.copy()
            player_classifications = []
            
            player_in_possession_detection = None

            print(possession_team)
            player_goalkeeper_detections = player_detections + goalkeeper_detections
            tracked_detections = player_detections + goalkeeper_detections + referee_detections  
            
            if len(detections2boxes(detections=tracked_detections)):
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
                        player_image = frame[y:y+height, x:x+width] 
                        jersey_color = pjc.classify_jersey(player_image)
                        player_classifications.append(jersey_color)
                        if len(ball_detections) != 1:
                            player_in_possession_detection = None
                            player_in_possession_track_id = None
                        elif player_detection.rect.pad(PLAYER_IN_POSSESSION_PROXIMITY).contains_point(point=ball_detections[0].rect.center):
                            possession_team=jersey_color
                            player_in_possession_detection = player_detection
                            player_in_possession_track_id = player_detection.tracker_id 

                    annotated_image = base_annotator.annotate(
                        image=annotated_image,
                        detections=tracked_detections)

                    annotated_image = player_goalkeeper_text_annotator.annotate(
                        image=annotated_image,
                        detections=tracked_goalkeeper_detections + tracked_player_detections,
                        jersey_colors=player_classifications)

                    annotated_image = ball_marker_annotator.annotate(
                        image=annotated_image,
                        detections=ball_detections)

                    annotated_image = player_marker_annotator.annotate(
                        image=annotated_image,
                        detections=[player_in_possession_detection] if player_in_possession_detection else [])

                    print(possession_team)
                    print("Player in Possession Track ID:", player_in_possession_track_id) 

                pass_tracker.update_pass(possession_team, player_in_possession_track_id)
                team1_passes, team2_passes = pass_tracker.get_passes()
                possession_calculator.update_possession(possession_team)
                current_frame = 1 + possession_calculator.team1_possession + possession_calculator.team2_possession
                team1_possession_percentage, team2_possession_percentage = possession_calculator.get_possession_stats(current_frame)

                print("Team 1 Passes:", team1_passes)
                print("Team 2 Passes:", team2_passes)


                print(f"Frame {current_frame}:")
                print("Team 1 Possession Percentage: {:.2f}%".format(team1_possession_percentage))
                print("Team 2 Possession Percentage: {:.2f}%".format(team2_possession_percentage))

            annotated_image = cv2.resize(annotated_image, (640, 480))
            ret, buffer = cv2.imencode('.jpg', annotated_image)
            frameA = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frameA + b'\r\n') 

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/data")
async def get_data():
    global team1_passes, team2_passes, team1_possession_percentage, team2_possession_percentage
    return JSONResponse(content={
        'team1_passes': team1_passes,
        'team2_passes': team2_passes,
        'team1_possession_percentage': team1_possession_percentage,
        'team2_possession_percentage': team2_possession_percentage
    })

@app.get("/demo-video/{demo_number}")
async def copy_demo_video(demo_number: int):
    if demo_number not in [1, 2]:
        raise HTTPException(status_code=400, detail="Demo number must be 1 or 2")

    demo_video_path = os.path.join(DEMO_VIDEOS_DIRECTORY, f"demo{demo_number}.mp4")
    if not os.path.exists(demo_video_path):
        raise HTTPException(status_code=404, detail=f"Demo{demo_number}.mp4 not found")

    target_path = os.path.join(UPLOAD_DIRECTORY, "uploaded_video.mp4")
    shutil.copyfile(demo_video_path, target_path)

    return {"message": f"Demo{demo_number}.mp4 copied and renamed to uploaded_video.mp4"}


def update_config_file(video_file_path):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('Paths', 'SOURCE_VIDEO_PATH', video_file_path)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

if __name__ == '__main__':
    app.run(debug=True)
