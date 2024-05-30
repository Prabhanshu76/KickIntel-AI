from common_imports import np, cv2

class PlayerJerseyClassifier:
    def __init__(self, color_list, boundaries):
        self.color_list = color_list
        self.boundaries = boundaries

    def classify_player_jersey(self, image):
        image = cv2.GaussianBlur(image, (3, 3), 0)
        masked_images = []
        values = []

        for boundary in self.boundaries:
            mask = cv2.inRange(image, boundary[0], boundary[1])
            masked_images.append(cv2.bitwise_and(image, image, mask=mask))
            non_black_pixels = np.count_nonzero(mask)
            values.append(non_black_pixels)

        dominant_color = self.color_list[0] if values[0] > values[1] else self.color_list[1]

        return dominant_color
