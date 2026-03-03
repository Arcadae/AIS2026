import pygame
import sys
from JarvisMarch import JarvisMarch
from Map import Map
from City import City
from Slider import Slider
from Clusterizer import Clusterizer
from CustomKMeans import CustomKMeans
import time

class Grid:
    width: int = 1400
    height: int = 1200
    cell_size: int = 20

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size
        self.cities: Map = Map()
        self.font = pygame.font.Font(None, 20)
        self.hull_points: list = []
        self.show_hull: bool = False
        self.clusterizer = Clusterizer()
        self.clusterizer.set_points(self.cities)
        self.kmeans = None
        self.show_kmeans = False
        self.slider = Slider(self.width - 200, 50, 200, 10, 2, 10, 3)
        pygame.display.set_caption("Карта")

    def draw_grid(self) -> None:
        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.screen.get_height()))

        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.screen.get_width(), y))
    
    def get_cell_from_mouse(self, pos):
        x, y = pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        return grid_x, grid_y
    
    def add_city(self, grid_x: int, grid_y: int) -> bool:
        for city in self.cities:
            if city.x == grid_x and city.y == grid_y:
                return False
        self.cities.append(City(grid_x, grid_y))
        self.show_hull = False
        self.clusterizer.reset_clusters()
        self.kmeans = None
        self.show_kmeans = False
        return True
    
    def draw_hull(self) -> None:
        if not self.show_hull or len(self.hull_points) < 3:
            return
        for i in range(len(self.hull_points)):
            start = self.hull_points[i]
            end = self.hull_points[(i + 1) % len(self.hull_points)]
            
            start_pixel = (
                start[0] * self.cell_size + self.cell_size // 2,
                start[1] * self.cell_size + self.cell_size // 2
            )
            end_pixel = (
                end[0] * self.cell_size + self.cell_size // 2,
                end[1] * self.cell_size + self.cell_size // 2
            )
            pygame.draw.line(self.screen, (0, 100, 255), start_pixel, end_pixel, 3)

    def draw_cities(self) -> None:
        for city in self.cities:
            center_x = city.x * self.cell_size + self.cell_size // 2
            center_y = city.y * self.cell_size + self.cell_size // 2
            if self.show_kmeans and self.kmeans is not None:
                colors = self.kmeans.get_cluster_colors()
                color = colors[city.cluster_id % len(colors)]
            else:
                color = self.clusterizer.get_point_color(city)
            pygame.draw.circle(self.screen, color, (center_x, center_y), 5)

            coord_text = f"({city.x},{city.y})"
            text_surface = self.font.render(coord_text, True, (100, 100, 100))

            text_x = center_x - text_surface.get_width() // 2 + 30
            text_y = center_y - 20

            self.screen.blit(text_surface, (text_x, text_y))

    def draw_cluster_centers(self):
        for i, center in enumerate(self.clusterizer.cluster_centers):
            pixel_x = center[0] * self.cell_size + self.cell_size // 2
            pixel_y = center[1] * self.cell_size + self.cell_size // 2
            color = self.clusterizer.get_center_color(i)
            pygame.draw.rect(self.screen, color, 
                           (pixel_x - 12, pixel_y - 12, 24, 24), 3)
            pygame.draw.circle(self.screen, color, (pixel_x, pixel_y), 6)
            center_text = f"C{i+1}"
            text_surface = self.font.render(center_text, True, (0, 0, 0))
            text_x = pixel_x - text_surface.get_width() // 2
            text_y = pixel_y - 25
            
            bg_rect = pygame.Rect(text_x - 2, text_y - 2, 
                                text_surface.get_width() + 4, 
                                text_surface.get_height() + 4)
            s = pygame.Surface((bg_rect.width, bg_rect.height))
            s.set_alpha(200)
            s.fill((255, 255, 255))
            self.screen.blit(s, (bg_rect.x, bg_rect.y))
            self.screen.blit(text_surface, (text_x, text_y))

        if self.show_kmeans and self.kmeans is not None:
            centers = self.kmeans.get_cluster_centers()
            if centers is not None:
                if len(centers.shape) == 2 and centers.shape[1] == 2:
                    for i, center in enumerate(centers):
                        center_x = float(center[0])
                        center_y = float(center[1])
                        pixel_x = int(center_x * self.cell_size + self.cell_size // 2)
                        pixel_y = int(center_y * self.cell_size + self.cell_size // 2)
                        colors = self.kmeans.get_cluster_colors()
                        color = colors[i % len(colors)]
                        pygame.draw.rect(self.screen, color, 
                                (pixel_x - 14, pixel_y - 14, 28, 28), 3)
                        pygame.draw.circle(self.screen, color, (pixel_x, pixel_y), 8)
                        center_text = f"K{i+1}"
                        text_surface = self.font.render(center_text, True, color)
                        text_x = pixel_x - text_surface.get_width() // 2
                        text_y = pixel_y - 25
                        
                        bg_rect = pygame.Rect(text_x - 2, text_y - 2, 
                                            text_surface.get_width() + 4, 
                                            text_surface.get_height() + 4)
                        s = pygame.Surface((bg_rect.width, bg_rect.height))
                        s.set_alpha(200)
                        s.fill((255, 255, 255))
                        self.screen.blit(s, (bg_rect.x, bg_rect.y))
                        self.screen.blit(text_surface, (text_x, text_y))
    
    def run(self) -> None:
        running = True
        hull_just_calculated = False
        k_pressed = False
        i_pressed = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.slider.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.slider.knob_rect.collidepoint(event.pos):
                            grid_x, grid_y = self.get_cell_from_mouse(pygame.mouse.get_pos())
                            if grid_x >= 0:
                                self.add_city(grid_x, grid_y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        if not hull_just_calculated:
                            if len(self.cities) >= 3:
                                self.hull_points = JarvisMarch.jarvis_march(self.cities)
                                self.show_hull = not self.show_hull
                    elif event.key == pygame.K_d:
                        if len(self.hull_points) >= 3:
                            k = int(self.slider.val)
                            if k <= len(self.hull_points):
                                self.clusterizer.select_centers_from_hull(self.hull_points, k)
                                self.clusterizer.assign_points_to_clusters()
                                self.show_kmeans = False
                    elif event.key == pygame.K_c:
                        self.clusterizer.reset_clusters()
                    elif event.key == pygame.K_k:
                        self.CustomKMeans = True
                        if len(self.cities) >= 3:
                            if not k_pressed:
                                k = int(self.slider.val)
                                random_seed = int(time.time())
                                self.kmeans = CustomKMeans(k, random_seed=random_seed)
                                self.kmeans.fit(self.cities)
                                self.show_kmeans = True
                            k_pressed = not k_pressed

                    elif event.key == pygame.K_n:
                        self.CustomKMeans = False
                        self.kmeans = None
                        self.show_kmeans = False
                        k_pressed = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_l:
                        hull_just_calculated = False
                        

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_cities()
            self.draw_hull()
            self.draw_cluster_centers()
            self.slider.draw(self.screen, self.font)
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()