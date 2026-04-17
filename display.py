from pprint import pprint

import pygame
import sys
from models import MapData


class Display:

    def __init__(
        self,
        map_data: MapData,
        screen_w,
        screen_h,
    ) -> None:

        self.screen_width, self.screen_height = screen_w, screen_h
        self.window = pygame.display.set_mode(
            (self.screen_width + 500, self.screen_height + 500)
        )
        self.clock = pygame.time.Clock()
        self.text = pygame.font.Font("assets/Anto.ttf", 30)
        self.hubs = map_data.hubs
        self.fps_surf = self.text.render("0", False, "white")
        self.frametime_surf = self.text.render("0", False, "white")
        self.current_frametime = 0
        pprint(self.__dict__)

    def game_loop(self) -> None:
        while True:

            # for fps
            self.fps_surf = self.text.render(
                f"fps: {self.clock.get_fps():.0f}", False, "white"
            )
            self.frametime_surf = self.text.render(
                f"ft: {self.current_frametime:.0f}", False, "white"
            )
            # ===============

            # check end window to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # ================

            self.redraw()
            self.current_frametime = self.clock.tick(60)

    def redraw(self) -> None:
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        self.window.fill("black")
        self.window.blit(self.fps_surf, (0, 0))
        self.window.blit(self.frametime_surf, (0, 32))
        # draw each hub on the screen
        for hub in self.hubs.values():

            # display hub
            self.window.blit(hub.surf, hub.rect)

            # display hub text
            self.window.blit(hub.text_surf, hub.text_rect)

        pygame.display.update()
