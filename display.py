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

    def game_loop(self):
        while True:

            # for fps
            self.text_surf = self.text.render(
                f"{self.clock.get_fps():.0f}", False, "white"
            )

            # ===============

            # check end window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # ================

            self.redraw()

            self.clock.tick(30)

    def redraw(self) -> None:

        self.window.fill("black")
        old_x = 0
        sep = 200  # seperator between hubs
        for v in self.hubs.values():

            # make me less ugly
            if old_x == v.x:
                pass
            else:
                sep += 400
            old_x = v.x
            self.window.blit(
                v.surface,
                (
                    v.x * 100 + sep,
                    v.y * 200 + 400,
                ),
            )

            self.window.blit(
                v.text,
                (
                    v.x * 100 + sep + 30,
                    v.y + self.screen_height / 2 - 10,
                ),
            )

        self.window.blit(self.text_surf, (0, 0))

        pygame.display.update()
