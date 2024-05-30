from common_imports import np, cv2

class PlayerJerseyClassifier:
    def __init__(self, color_list, hsv_ranges):
        self.color_list = color_list
        self.hsv_ranges = hsv_ranges

    def classify_player_jersey(self, image):
        # Convert BGR image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_image = cv2.GaussianBlur(hsv_image, (3, 3), 0)

        masked_images = []
        values = []

        for hsv_range in self.hsv_ranges:
            mask = cv2.inRange(hsv_image, hsv_range[0], hsv_range[1])
            masked_images.append(cv2.bitwise_and(image, image, mask=mask))
            non_black_pixels = np.count_nonzero(mask)
            values.append(non_black_pixels)

        dominant_color = self.color_list[0] if values[0] > values[1] else self.color_list[1]

        return dominant_color
