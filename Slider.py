import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.val = start_val
        self.dragging = False
        
        self.knob_rect = pygame.Rect(x, y - 5, 10, height + 10)
        self.update_knob_position()
        
    def update_knob_position(self):
        range_width = self.max - self.min
        if range_width == 0:
            pos = self.rect.x
        else:
            pos = self.rect.x + (self.val - self.min) / range_width * self.rect.width
        self.knob_rect.x = pos - self.knob_rect.width // 2
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.knob_rect.collidepoint(event.pos):
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.knob_rect.x = new_x - self.knob_rect.width // 2
                
                rel_x = new_x - self.rect.x
                self.val = self.min + (rel_x / self.rect.width) * (self.max - self.min)
                self.val = round(self.val)
    def draw(self, screen, font):

        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        pygame.draw.rect(screen, (0, 120, 255), self.knob_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.knob_rect, 2)
        
        val_text = f"K={int(self.val)}"
        text_surface = font.render(val_text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x, self.rect.y - 25))