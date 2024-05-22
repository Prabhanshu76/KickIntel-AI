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

    def train_kmeans_model(self, player_images):
        features = []
        for image in player_images:
            feature = self._extract_color_features(image)
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
        feature = self._extract_color_features(image)
        cluster_label = self.kmeans_model.predict([feature])[0]
        if cluster_label == 0:
            return 'Team 1'
        else:
            return 'Team 2'
    
    def classify_player_image(self, player_image):
        return self.classify_jersey(player_image) 