import pygame
import sys
from src.settings import WIDTH, HEIGHT, FPS, WORLD_MAP
from src.debug import debug
from src.level import Level


class Game:
    def __init__(self):
        
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("y_project")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 

            self.screen.fill('#1ad829')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)