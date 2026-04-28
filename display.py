from pprint import pprint
import random

import pygame
import sys
from algo import Simulator
from globals import *

from model import Connection, Hub, Drone, MapData


class Display:

    def __init__(self, sim: Simulator, map_file_name: str, mapdata: MapData) -> None:

        self.window = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
        )
        self.mapdata = mapdata
        self.hubs: list[Hub] = [hub for hub in sim.mapdata.hubs.values()]
        self.connections: list[Connection] = sim.mapdata.connections
        self.drones: list[Drone] = sim.drones
        self.sim: Simulator = sim
        self.clock = pygame.time.Clock()

        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.map_file = self.text.render(map_file_name, False, "white", "black")

        self.move = 0

    def game_loop(self) -> None:
        while True:

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
        self.window.fill("black")

        self.draw_connections()
        self.draw_hubs()
        self.draw_drones()

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
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (1920 / 2, 0),
            (1920 / 2, 1080),
            CONNECTION_LINE_SIZE,
        )
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (0, 1080 / 2),
            (1920, 1080 / 2),
            CONNECTION_LINE_SIZE,
        )
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

            pygame.draw.circle(
                self.window,
                hub.color,
                self.get_correct_coordinates(hub.x, hub.y),
                HUB_SIZE,
            )

            # display hub text
            self.window.blit(
                hub.text_surf,
                hub.text_surf.get_rect(
                    center=self.get_correct_coordinates(hub.x, hub.y, True)
                ),
            )

    def get_correct_coordinates(self, x: int, y: int, is_text: bool = False):
        h_n = self.mapdata.horizontal_hubs_number
        v_n = self.mapdata.vertical_hubs_number

        h_gap = 200
        v_gap = 200

        HORIZONTAL_SHIFT = (SCREEN_WIDTH - (h_n * ((HUB_SIZE / 2) + h_gap) - h_gap)) / 2
        VERTICAL_SHIFT = (SCREEN_HEIGHT - (v_n * ((HUB_SIZE / 2) + v_gap) - v_gap)) / 2

        return (
            x * h_gap + HORIZONTAL_SHIFT + HUB_SIZE,
            y * v_gap + VERTICAL_SHIFT + HUB_SIZE,
        )
