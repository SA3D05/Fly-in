import pygame
import sys
from globals import (
    CONNECTION_LINE_COLOR,
    CONNECTION_LINE_SIZE,
    FONT_FAMILY_PATH,
    HORIZONTAL_SHIFT,
    HUB_GAP_HORIZONTAL,
    HUB_GAP_VERTICAL,
    HUB_SIZE,
    MITRIX_TEXT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    VERTICAL_SHIFT,
)
from model import MapData, Drone


class Display:

    def __init__(self, map_data: MapData, drone: Drone) -> None:

        self.window = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
        )

        self.clock = pygame.time.Clock()

        # those just for debugging
        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.fps_surf = self.text.render("0", False, "white")
        self.frametime_surf = self.text.render("0", False, "white")
        self.current_frametime = 0
        self.moves = 0

        self.hubs = map_data.hubs
        self.connections = map_data.connections
        self.drone = drone

    def game_loop(self) -> None:
        while True:

            # fps
            self.fps_surf = self.text.render(
                f"fps: {self.clock.get_fps():.0f}", False, "white"
            )

            # frame time
            self.frametime_surf = self.text.render(
                f"ft: {self.current_frametime:.0f}", False, "white"
            )

            # check end window to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.drone.move()
                        self.moves += 1
                        print("cutrrent move:", self.moves)

            # draw hubs
            self.redraw()

            # set current frame time
            self.current_frametime = self.clock.tick(60)

    def redraw(self) -> None:
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        self.window.fill("black")
        self.window.blit(self.fps_surf, (0, 0))
        self.window.blit(self.frametime_surf, (0, 32))

        # # draw connections here ...
        for c in self.connections:
            pygame.draw.line(
                self.window,
                CONNECTION_LINE_COLOR,
                self.get_correct_coordinates(*c.start_pos),
                self.get_correct_coordinates(*c.end_pos),
                CONNECTION_LINE_SIZE,
            )
        # draw each hub on the screen
        for hub in self.hubs.values():

            # display hub
            self.window.blit(
                hub.surf,
                self.get_correct_coordinates(hub.x, hub.y),
            )

            # display hub text
            self.window.blit(
                hub.text_surf,
                self.get_correct_coordinates(hub.x, hub.y, True),
            )

        # draw drones here ...
        self.window.blit(
            self.drone.surf,
            self.get_correct_coordinates(self.drone.x, self.drone.y),
        )

        pygame.display.update()

    def get_correct_coordinates(self, x: int, y: int, is_text: bool = False):
        return (
            x * (100 + HUB_GAP_HORIZONTAL) + HORIZONTAL_SHIFT,
            (
                y * (100 + HUB_GAP_VERTICAL)
                + VERTICAL_SHIFT
                + HUB_GAP_VERTICAL
                + (HUB_SIZE if is_text else 0)
            ),
        )
