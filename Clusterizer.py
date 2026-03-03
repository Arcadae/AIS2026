import math
from City import City

class Clusterizer:
    def __init__(self) -> None:
        self.cluster_centers: list = []
        self.cluster_colors: list = [] 
        self.points: list[City] = []
        
    def set_points(self, points: list[City]) -> None:
        self.points = points
        
    def select_centers_from_hull(self, hull_points: list, k: int) -> list:
        if not hull_points or len(hull_points) < k:
            return []
        
        hull_size: int = len(hull_points)
        indices: list = []
        
        if k == 1:
            indices = [0]
        else:
            step = hull_size / k
            for i in range(k):
                idx = int(i * step) % hull_size
                indices.append(idx)
        
        self.cluster_centers = [hull_points[idx] for idx in indices]
        return self.cluster_centers
    
    def calculate_distance(self,
                           point1: tuple[int, int],
                           point2: tuple[int, int]
                           ) -> int:
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def assign_points_to_clusters(self) -> bool:
        if not self.cluster_centers or len(self.cluster_centers) < 2 or not self.points:
            return False
        
        for point in self.points:
            min_distance: float = float('inf')
            best_cluster = -1
            
            for i, center in enumerate(self.cluster_centers):
                dist = self.calculate_distance((point.x, point.y), center)
                if dist < min_distance:
                    min_distance = dist
                    best_cluster = i
            
            point.cluster_id = best_cluster
        
        self.generate_cluster_colors(len(self.cluster_centers))
        return True
    
    def generate_cluster_colors(self, num_clusters: int) -> None:
        self.cluster_colors: list = []
        for i in range(num_clusters):
            hue = (i * (360 / num_clusters)) % 360
            self.cluster_colors.append(self.hsv_to_rgb(hue, 0.8, 0.9))
    
    def hsv_to_rgb(self, h, s, v):
        h = h / 360
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i %= 6
        match i:
            case 0: return (int(v * 255), int(t * 255), int(p * 255))
            case 1: return (int(q * 255), int(v * 255), int(p * 255))
            case 2: return (int(p * 255), int(v * 255), int(t * 255))
            case 3: return (int(p * 255), int(q * 255), int(v * 255))
            case 4: return (int(t * 255), int(p * 255), int(v * 255))
            case 5: return (int(v * 255), int(p * 255), int(q * 255))
    
    def get_point_color(self, point: City):
        if point.cluster_id >= 0 and point.cluster_id < len(self.cluster_colors):
            return self.cluster_colors[point.cluster_id]
        return (0, 0, 0)
    
    def get_center_color(self, center_index):
        if center_index < len(self.cluster_colors):
            return self.cluster_colors[center_index]
        return (0, 0, 0)
    
    def reset_clusters(self):
        self.cluster_centers = []
        self.cluster_colors = []
        if self.points:
            for point in self.points:
                point.cluster_id = -1
    
    def get_cluster_info(self):
        if not self.cluster_centers:
            return 
        info = f"Кластеров: {len(self.cluster_centers)}\n"
        for i, center in enumerate(self.cluster_centers):
            count = sum(1 for p in self.points if p.cluster_id == i) if self.points else 0
            info += f"Кластер {i+1}: центр {center}, точек: {count}\n"
        return info