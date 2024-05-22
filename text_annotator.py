from common_imports import dataclass, List, cv2, np
from geometry_utilities import Detection, draw_filled_rect, draw_text, Rect, Point, Color


@dataclass
class TextAnnotator:
    col: Color
    team1_color: Color
    team2_color:Color
    text_color: Color
    text_thickness: int

    def annotate(self, image: np.ndarray, detections: List[Detection], jersey_colors: List[str]) -> np.ndarray:
        annotated_image = image.copy()
        for detection, jersey_color in zip(detections, jersey_colors):
            # if tracker_id is not assigned or jersey_color is not available, skip annotation
            if detection.tracker_id is None or jersey_color is None:
                continue

            # calculate text dimensions
            size, _ = cv2.getTextSize(
                f"{jersey_color}",
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                thickness=self.text_thickness)
            width, height = size

            # calculate text background position
            center_x, center_y = detection.rect.bottom_center.int_xy_tuple
            x = center_x - width // 2
            y = center_y - height // 2 + 10

            if jersey_color == "Team1":
                color = self.team1_color
            else:
                color = self.team2_color
                

            # draw background
            annotated_image = draw_filled_rect(
                image=annotated_image,
                rect=Rect(x=x, y=y, width=width, height=height).pad(padding=5),
                color=self.col)

            # draw text
            text = f"{jersey_color}"
            annotated_image = draw_text(
                image=annotated_image,
                anchor=Point(x=x, y=y + height),
                text=text,
                color=self.text_color,
                thickness=self.text_thickness)
        return annotated_image