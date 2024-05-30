from common_imports import np, cv2
from sklearn.cluster import KMeans

class PlayerJerseyClassifier:
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.kmeans_model = None
        
    def _extract_color_features(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mean_color = np.mean(hsv_image, axis=(0, 1))
        return mean_color

    def _remove_white_color(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])  # Lower threshold for white in HSV
        upper_white = np.array([180, 80, 255])  # Upper threshold for white in HSV
        mask = cv2.inRange(hsv_image, lower_white, upper_white)
        image_no_white = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
        return image_no_white

    def _remove_green_color(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([30, 50, 50])
        upper_green = np.array([90, 255, 255])
        mask = cv2.inRange(hsv_image, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)
        image_no_green = cv2.bitwise_and(image, image, mask=mask_inv)
        return image_no_green

    def _increase_brightness(self, image, value=10):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        brightened_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return brightened_image

    def train_kmeans_model(self, player_images):
        features = []
        for image in player_images:
            height, width = image.shape[:2]
            top_cutoff = int(0.1 * height)
            bottom_cutoff = int(0.6 * height)
            left_cutoff = int(0.1 * width)
            right_cutoff = int(0.9 * width)
            cropped_image = image[top_cutoff:bottom_cutoff, left_cutoff:right_cutoff]
            
            # Increase brightness of the cropped image
            brightened_image = self._increase_brightness(cropped_image)
            
            # Remove white color from the brightened image
            image_no_white = self._remove_white_color(brightened_image)
            
            # Remove green color from the image
            image_no_green = self._remove_green_color(image_no_white)
            
            # Extract features from the image with green and white colors removed
            feature = self._extract_color_features(image_no_green)
            features.append(feature)

        if not features:
            raise ValueError("No valid features extracted to train the model.")
        
        # Convert features to numpy array
        features = np.array(features)

        # Train KMeans model
        self.kmeans_model = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.kmeans_model.fit(features)

    def get_trained_model(self):
        return self.kmeans_model

    def classify_jersey(self, image):
        if self.kmeans_model is None:
            raise ValueError("The KMeans model has not been trained yet.")
        height, width = image.shape[:2]
        top_cutoff = int(0.1 * height)
        bottom_cutoff = int(0.6 * height)
        left_cutoff = int(0.1 * width)
        right_cutoff = int(0.9 * width)
        cropped_image = image[top_cutoff:bottom_cutoff, left_cutoff:right_cutoff]
        brightened_image = self._increase_brightness(cropped_image)
        image_no_white = self._remove_white_color(brightened_image)
        image_no_green = self._remove_green_color(image_no_white)
        feature = self._extract_color_features(image_no_green)
        cluster_label = self.kmeans_model.predict([feature])[0]
        if cluster_label == 0:
            return 'Team 1'
        else:
            return 'Team 2'
    
    def classify_player_image(self, player_image):
        return self.classify_jersey(player_image)
