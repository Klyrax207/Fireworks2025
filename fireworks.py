import pygame
import random
import numpy as np
from math import sin, cos, pi
import os

pygame.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("New Year Fireworks 2025! ")

COLORS = [
    (255, 50, 50), (50, 255, 50), (50, 50, 255),
    (255, 255, 50), (255, 50, 255), (50, 255, 255),
    (255, 165, 0), (255, 192, 203), (148, 0, 211),
    (255, 215, 0), (0, 255, 127), (138, 43, 226)
]

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, 2 * pi)
        self.speed = random.uniform(6, 12)
        self.velocity_x = cos(self.angle) * self.speed
        self.velocity_y = sin(self.angle) * self.speed
        self.lifetime = 255
        self.gravity = 0.15
        self.size = random.uniform(1.5, 3)
        self.decay_rate = random.uniform(3, 6)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.lifetime -= self.decay_rate
        return self.lifetime > 0

    def draw(self, screen):
        alpha = max(0, min(255, self.lifetime))
        color = (self.color[0], self.color[1], self.color[2], alpha)
        pos = (int(self.x), int(self.y))
        
        glow_size = int(self.size * 2)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        glow_color = (color[0], color[1], color[2], int(alpha * 0.3))
        pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
        screen.blit(glow_surface, (pos[0] - glow_size, pos[1] - glow_size))
        
        surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (int(self.size), int(self.size)), int(self.size))
        screen.blit(surface, (pos[0] - int(self.size), pos[1] - int(self.size)))

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(COLORS)
        self.particles = []
        self.exploded = False
        self.velocity_y = random.uniform(-18, -15)
        self.trail_particles = []

    def create_trail(self):
        if not self.exploded:
            self.trail_particles.append(Particle(self.x, self.y, self.color))
            if len(self.trail_particles) > 10:
                self.trail_particles.pop(0)

    def explode(self):
        num_particles = random.randint(80, 120)
        for _ in range(num_particles):
            self.particles.append(Particle(self.x, self.y, self.color))
        self.exploded = True

    def update(self):
        if not self.exploded:
            self.y += self.velocity_y
            self.velocity_y += 0.3
            self.create_trail()
            if self.velocity_y >= 0:
                self.explode()
        else:
            self.particles = [p for p in self.particles if p.update()]
            self.trail_particles = [p for p in self.trail_particles if p.update()]
        return len(self.particles) > 0 or not self.exploded or len(self.trail_particles) > 0

    def draw(self, screen):
        for particle in self.trail_particles:
            particle.draw(screen)
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
        for particle in self.particles:
            particle.draw(screen)

def draw_text(screen):
    try:
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Pacifico.ttf")
        if os.path.exists(font_path):
            font = pygame.font.Font(font_path, 74)
        else:
            font = pygame.font.SysFont("arial", 74, bold=True)
        
        text = font.render("Happy New Year 2025!", True, (255, 255, 255))
        glow_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        glow_color = (255, 255, 255, 50)
        glow_text = font.render("Happy New Year 2025!", True, glow_color)
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_surface.blit(glow_text, offset)
        
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/4))
        screen.blit(glow_surface, text_rect)
        screen.blit(text, text_rect)
    except Exception as e:
        print(f"Font error: {e}")
        font = pygame.font.Font(None, 74)
        text = font.render("Happy New Year 2025!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/4))
        screen.blit(text, text_rect)

def main():
    clock = pygame.time.Clock()
    fireworks = []
    running = True
    auto_launch_timer = 0
    
    trails = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "fonts"), exist_ok=True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    fireworks.append(Firework(x, HEIGHT))

        auto_launch_timer += 1
        if auto_launch_timer >= 20:
            if random.random() < 0.4:
                fireworks.append(Firework(random.randint(50, WIDTH-50), HEIGHT))
            auto_launch_timer = 0

        screen.fill((0, 0, 0))
        
        trails.fill((0, 0, 0, 10), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(trails, (0, 0))

        fireworks = [fw for fw in fireworks if fw.update()]
        for firework in fireworks:
            firework.draw(screen)

        draw_text(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
