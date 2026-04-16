import pygame
import sys
from models import MapData


class Display:
    def __init__(self, map_data: MapData) -> None:

        self.screen_width, self.screen_height = 1920, 1080
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.text = pygame.font.Font(None, 100)
        self.hubs = map_data.hubs
        self.connections = map_data.connections

    def game_loop(self) -> None:
        while True:

            # for fps
            self.text_surf = self.text.render(
                f"{self.clock.get_fps():.0f}", False, "white"
            )

            # ===============

            # check end window to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # ================

            self.redraw()
            print(self.clock.tick(60))

    def redraw(self) -> None:
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        self.window.fill("black")
        self.window.blit(self.text_surf, (0, 0))

        # draw each hub on the screen
        for hub in self.hubs.values():

            # display hub
            self.window.blit(hub.surf, hub.rect)

            # display hub text
            self.window.blit(hub.text_surf, hub.text_rect)

        pygame.display.update()
