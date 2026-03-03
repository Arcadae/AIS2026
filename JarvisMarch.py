from Map import Map

class JarvisMarch:
    def jarvis_march(cities: Map) -> list[tuple[int, int]]:
        if len(cities) < 3:
            return cities
        points: list[tuple[int, int]] = [(city.x, city.y) for city in cities]

        def rotate( p: tuple[int, int],
                    q: tuple[int, int],
                    r: tuple[int, int]
                    ) -> int:
            val: int = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0: return 0
            return 1 if val > 0 else 2
        
        def distance(p: tuple[int, int],
                     q: tuple[int, int]
                     ) -> int:
            return (p[0] - q[0])**2 + (p[1] - q[1])**2
        
        start_point: tuple[int, int] = points[0]
        for p in points[1:]:
            if p[1] < start_point[1] or (p[1] == start_point[1] and p[0] < start_point[0]):
                start_point = p
        hull: list[tuple[int, int]] = []
        current_point: tuple[int, int] = start_point
        
        while True:
            hull.append(current_point)
            next_point: tuple[int, int] = points[0]
            for candidate in points[1:]:
                if candidate == current_point:
                    continue
                    
                if next_point == current_point:
                    next_point = candidate
                    continue
                    
                o: int = rotate(current_point, next_point, candidate)
                
                if o == 2:
                    next_point = candidate
                elif o == 0:
                    if distance(current_point, candidate) > distance(current_point, next_point):
                        next_point = candidate
            current_point = next_point
            
            if current_point == start_point:
                break
        return hull