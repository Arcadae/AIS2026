import numpy as np
import random
from City import City
from Map import Map
from typing import Optional

class CustomKMeans:
    def __init__(self, k: int, max_iterations: int = 100, tolerance: float = 1e-4, 
                 random_seed: Optional[int] = None):
        self.k = k
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.random_seed = random_seed
        self.centroids = None
        self.cluster_centers = None
        self.is_fitted = False

    def fit(self, cities: Map) -> list[list[City]]:
        if self.is_fitted: return self._get_clusters(cities)
        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)

        for city in cities:
            city.cluster_id = -1
        points = np.array([[city.x, city.y] for city in cities])
        n_samples = len(cities)
        random_indices = random.sample(range(n_samples), self.k)
        self.centroids = points[random_indices].copy()
        self.cluster_centers = self.centroids.copy()
        for _ in range(self.max_iterations):
            distances = self._calculate_distances(points)
            labels = np.argmin(distances, axis=1)
        for i, city in enumerate(cities):
            city.cluster_id = labels[i]
        new_centroids = np.zeros_like(self.centroids)
        for i in range(self.k):
            cluster_indices = np.where(labels == i)
            if len(cluster_indices) > 0:
                cluster_points = points[cluster_indices]
                new_centroids[i] = np.mean(cluster_points, axis=0)
            
            centroid_shift = np.sum((new_centroids - self.centroids) ** 2)
            nonzero_rows = [row for row in new_centroids if not np.all(row == 0)]
            result = np.array([
                nonzero_rows[i] if i < len(nonzero_rows) else new_centroids[i] 
                for i in range(len(self.centroids))
            ])
            self.cluster_centers = result.copy()
            if centroid_shift < self.tolerance:
                break
        self.is_fitted = True
        return self._get_clusters(cities)
    
    def fit_predict(self, cities: Map) -> list[list[City]]:
        return self.fit(cities)
    
    def _calculate_distances(self, points: np.ndarray) -> np.ndarray:
        distances = np.zeros((len(points), self.k))
        for i, centroid in enumerate(self.centroids):
            distances[:, i] = np.linalg.norm(points - centroid, axis=1)
        return distances
    
    def _get_clusters(self, cities: Map) -> list[list[City]]:
        clusters = [[] for _ in range(self.k)]
        for city in cities:
            if city.cluster_id != -1:
                clusters[city.cluster_id].append(city)
        return clusters
    
    def get_cluster_centers(self) -> np.ndarray:
        return self.cluster_centers if self.cluster_centers is not None else np.array([])
    
    def get_cluster_colors(self, n_colors: Optional[int] = None) -> list[tuple]:
        if n_colors is None:
            n_colors = self.k
        colors = []
        for i in range(n_colors):
            hue = (i * (360 / n_colors)) / 360
            colors.append(self._hsv_to_rgb(hue, 0.8, 0.9))
        return colors
    
    def _hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return(v,v,v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i %= 6
        match i:
            case 0: return (int(v * 255), int(t * 255), int(p * 255))
            case 1: return (int(q * 255), int(v * 255), int(p * 255))
            case 2: return (int(p * 255), int(v * 255), int(t * 255))
            case 3: return (int(p * 255), int(q * 255), int(v * 255))
            case 4: return (int(t * 255), int(p * 255), int(v * 255))
            case 5: return (int(v * 255), int(p * 255), int(q * 255))