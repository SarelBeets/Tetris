import pygame
import numpy as np
import math

class MotocrossEnv:
    """Simple 1D motocross environment with optional rendering."""

    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        self.track_length = 100.0
        self.amplitude = 20.0
        self.dt = 0.1
        self.screen = None
        self.reset()

    def reset(self):
        self.pos = 0.0
        self.vel = 0.0
        self.steps = 0
        return self._get_state()

    def _get_state(self):
        slope = math.cos(self.pos / 3.0) * self.amplitude / 3.0
        return np.array([self.pos, self.vel, slope], dtype=np.float32)

    def step(self, action):
        # action: -1 (brake), 0 (coast), 1 (accelerate)
        self.vel += 0.1 * float(action)
        # simple friction
        self.vel *= 0.99
        self.pos += self.vel
        self.pos = max(0.0, min(self.track_length, self.pos))
        self.steps += 1
        done = self.pos >= self.track_length or self.steps >= 1000
        reward = self.vel - 0.1 * abs(action)
        return self._get_state(), float(reward), done

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.screen = None
                return
        self.screen.fill((0, 0, 0))
        points = []
        for x in range(self.width):
            track_x = self.track_length * x / self.width
            y = self.height - (math.sin(track_x / 3.0) * self.amplitude + 50)
            points.append((x, int(y)))
        pygame.draw.lines(self.screen, (200, 200, 200), False, points, 2)
        bike_x = int(self.pos / self.track_length * self.width)
        bike_y = int(self.height - (math.sin(self.pos / 3.0) * self.amplitude + 50))
        pygame.draw.circle(self.screen, (255, 0, 0), (bike_x, bike_y), 5)
        pygame.display.flip()
