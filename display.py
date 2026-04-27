from pprint import pprint
import random

import pygame
import sys
from algo import Simulator
from globals import *

from model import Connection, Hub, Drone


class Display:

    def __init__(self, sim: Simulator, map_file_name: str) -> None:

        self.window = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
        )

        self.hubs: list[Hub] = [hub for hub in sim.mapdata.hubs.values()]
        self.connections: list[Connection] = sim.mapdata.connections
        self.drones: list[Drone] = sim.drones
        self.sim: Simulator = sim
        self.clock = pygame.time.Clock()

        # ========== those just for debugging ================
        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.fps_surf = self.text.render("0", False, "white")
        self.frametime_surf = self.text.render("0", False, "white")
        self.map_file = self.text.render(map_file_name, False, "white", "black")
        self.current_frametime = 0
        # =============================================
        self.move = 0

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
                        self.move += 1
                        self.sim.move(self.move)

            # draw hubs
            self.redraw()

            # set current frame time
            self.current_frametime = self.clock.tick(60)

    def redraw(
        self,
    ) -> None:
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        self.window.fill("black")

        self.draw_connections()
        self.draw_hubs()
        self.draw_drones()
        self.window.blit(self.fps_surf, (0, 0))
        self.window.blit(self.frametime_surf, (0, 50))
        self.window.blit(
            self.map_file,
            self.map_file.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)),
        )

        pygame.display.update()

    def get_random_coordinates(self, coordinates: tuple) -> tuple:
        return tuple(c + random.randint(0, 3) for c in coordinates)

    def draw_drones(self):
        for drone in self.drones:
            self.window.blit(
                drone.surf,
                drone.surf.get_rect(
                    center=self.get_random_coordinates(
                        self.get_correct_coordinates(drone.x, drone.y)
                    ),
                ),
            )

    def draw_connections(self):
        for c in self.connections:
            pygame.draw.line(
                self.window,
                CONNECTION_LINE_COLOR,
                self.get_correct_coordinates(*c.start_pos),
                self.get_correct_coordinates(*c.end_pos),
                CONNECTION_LINE_SIZE,
            )

    def draw_hubs(self):
        for hub in self.hubs:

            # display hub
            self.window.blit(
                hub.surf,
                hub.surf.get_rect(center=self.get_correct_coordinates(hub.x, hub.y)),
            )

            # display hub text
            self.window.blit(
                hub.text_surf,
                hub.text_surf.get_rect(
                    center=self.get_correct_coordinates(hub.x, hub.y, True)
                ),
            )

    def get_correct_coordinates(self, x: int, y: int, is_text: bool = False):
        return (
            x * (100 + HUB_GAP_HORIZONTAL) + HORIZONTAL_SHIFT,
            (
                y * (100 + HUB_GAP_VERTICAL)
                + VERTICAL_SHIFT
                + HUB_GAP_VERTICAL
                + (HUB_SIZE + 20 if is_text else 0)
            ),
        )
