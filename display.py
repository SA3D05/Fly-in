from pprint import pprint
import random

import pygame
import sys
from algo import Simulator
from globals import *

from model import Connection, Hub, Drone, MapData
from interface import *


class Display:

    def __init__(self, sim: Simulator, map_file_name: str, mapdata: MapData) -> None:

        self.window = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
        )

        self.mapdata = mapdata
        self.drones: list[Drone] = sim.drones
        self.sim: Simulator = sim

        self.clock = pygame.time.Clock()

        self.horizontal_margin = 10
        self.vertical_margin = 50

        self.menu = MenuWindow(
            self.horizontal_margin,
            self.vertical_margin,
        )
        self.menu.init_sections()

        self.sim_window = SimWindow(self.horizontal_margin, self.vertical_margin)

        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.map_file = self.text.render(map_file_name, True, "white", "black")
        self.fps = 60

        self.move = 0

    def check_key_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    case pygame.K_SPACE:
                        self.move += 1
                        self.sim.move(self.move)
                    case pygame.K_UP:
                        self.menu.move_up()
                    case pygame.K_DOWN:
                        self.menu.move_down()

    def game_loop(self) -> None:
        while True:

            self.clock.tick(60)
            self.fps = self.clock.get_fps()

            self.check_key_events()
            self.redraw()

            # set current frame time

    def redraw(
        self,
    ) -> None:
        self.window.fill("black")

        # self.draw_connections()
        # self.draw_hubs()
        # self.draw_drones()
        self.draw_mapfile_name()

        self.draw_menu()
        self.draw_debug_lines()

        pygame.display.update()

    def draw_mapfile_name(self):
        self.map_file = self.text.render(f"{self.fps:.0f}", True, "white", "black")
        self.window.blit(
            self.map_file,
            self.map_file.get_rect(topleft=(0, 0)),
        )

    def draw_debug_lines(self):
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (SCREEN_WIDTH / 2, 0),
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
            CONNECTION_LINE_SIZE,
        )
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (0, SCREEN_HEIGHT / 2),
            (SCREEN_WIDTH, SCREEN_HEIGHT / 2),
            CONNECTION_LINE_SIZE,
        )

    def draw_menu(self):

        # menu part
        pygame.draw.rect(
            self.window,
            "red",
            self.menu.surf.get_rect(
                topleft=(self.horizontal_margin, self.vertical_margin)
            ),
            5,
            10,
        )

        # graph part
        pygame.draw.rect(
            self.window,
            "blue",
            self.sim_window.surf.get_rect(
                topleft=(
                    self.menu.horizontal_size + (self.horizontal_margin * 3),
                    self.vertical_margin,
                ),
            ),
            5,
            10,
        )

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # sections part
        for section in self.menu.sections:

            section_x = self.horizontal_margin + self.menu.horizontal_sections_margin
            section_y = (self.vertical_margin + self.menu.vertical_sections_margin) + (
                section.index
                * (section.vertical_size + (self.menu.vertical_sections_margin * 2))
            )

            if (
                mouse_x >= section_x and mouse_x <= section_x + section.horizontal_size
            ) and (
                mouse_y >= section_y and mouse_y <= section_y + section.vertical_size
            ):
                self.menu.change_selected_section(section.index)
                self.menu.selected_section = section.index

            pygame.draw.rect(
                self.window,
                section.color,
                section.surf.get_rect(topleft=(section_x, section_y)),
                0 if self.menu.selected_section == section.index else 5,
                20,
            )
            self.window.blit(
                section.text_surf,
                section.text_surf.get_rect(
                    center=(
                        (
                            self.horizontal_margin
                            + self.menu.horizontal_sections_margin
                            + section.horizontal_size / 2
                        ),
                        (self.vertical_margin + self.menu.vertical_sections_margin)
                        + (
                            section.index
                            * (
                                section.vertical_size
                                + (self.menu.vertical_sections_margin * 2)
                            )
                        )
                        + section.vertical_size / 2,
                    )
                ),
            )

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

        for c in self.mapdata.connections:
            pygame.draw.line(
                self.window,
                CONNECTION_LINE_COLOR,
                self.get_correct_coordinates(*c.start_pos),
                self.get_correct_coordinates(*c.end_pos),
                CONNECTION_LINE_SIZE,
            )

    def draw_hubs(self):
        for hub in self.mapdata.hubs.values():

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
