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

        self.horizontal_margin = 50
        self.vertical_margin = 100

        self.menu = MenuWindow(
            (self.horizontal_margin, self.vertical_margin),
            self.horizontal_margin,
            self.vertical_margin,
        )

        self.menu.init_sections()

        self.sim_window = SimWindow(
            (
                self.menu.horizontal_size + (self.horizontal_margin * 3),
                self.vertical_margin,
            ),
            self.horizontal_margin,
            self.vertical_margin,
        )

        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.map_file = self.text.render(map_file_name, False, "white", "black")
        self.move = 0

    def _dispose(self):
        pygame.quit()
        sys.exit()

    def __manage_pressed_event(self):

        match self.menu.sections[self.menu.selected_section].text:
            case "Exit":
                self._dispose()

            case "Solve":
                self.move += 1
                self.sim.move(self.move)

    def __check_key_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._dispose()

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self._dispose()

                    case pygame.K_UP:
                        self.menu.move_up()

                    case pygame.K_DOWN:
                        self.menu.move_down()

                    case pygame.K_RETURN:
                        self.__manage_pressed_event()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__manage_pressed_event()

            elif event.type == pygame.MOUSEMOTION:

                mouse_x, mouse_y = event.pos
                for section in self.menu.sections:
                    if (
                        mouse_x >= section.x_pos
                        and mouse_x <= section.x_pos + section.horizontal_size
                    ) and (
                        mouse_y >= section.y_pos
                        and mouse_y <= section.y_pos + section.vertical_size
                    ):
                        self.menu.change_selected_section(section.index)

    def game_loop(self) -> None:
        while True:

            self.clock.tick(0)

            self.__check_key_events()
            self._redraw()

    def _redraw(
        self,
    ) -> None:
        self.window.fill("black")

        self._draw_connections()
        self._draw_hubs()
        self._draw_drones()
        self._draw_mapfile_name()

        self._draw_interface()
        self._draw_debug_lines()

        pygame.display.update()

    def _draw_mapfile_name(self):
        self.window.blit(
            self.map_file,
            self.map_file.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT)),
        )

    def _draw_debug_lines(self):
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

    def _draw_interface(self):

        # menu part
        pygame.draw.rect(
            self.window,
            "white",
            self.menu.surf.get_rect(topleft=(self.menu.x_pos, self.menu.y_pos)),
            5,
            10,
        )

        # graph part
        pygame.draw.rect(
            self.window,
            "white",
            self.sim_window.rect,
            5,
            10,
        )

        # sections part
        for section in self.menu.sections:

            pygame.draw.rect(
                self.window,
                section.color,
                section.rect,
                0 if self.menu.selected_section == section.index else 5,
                100,
                20 if self.menu.selected_section == section.index else 100,
            )

            self.window.blit(section.text_surf, section.text_rect)

    def __get_random_coordinates(self, coordinates: tuple) -> tuple:
        return tuple(c + random.randint(0, 3) for c in coordinates)

    def _draw_drones(self):
        for drone in self.drones:
            self.window.blit(
                drone.surf,
                drone.surf.get_rect(
                    center=self.__get_random_coordinates(
                        self.__get_correct_coordinates(drone.x, drone.y)
                    ),
                ),
            )

    def _draw_connections(self):

        for c in self.mapdata.connections:
            pygame.draw.line(
                self.window,
                CONNECTION_LINE_COLOR,
                self.__get_correct_coordinates(*c.start_pos),
                self.__get_correct_coordinates(*c.end_pos),
                CONNECTION_LINE_SIZE,
            )

    def _draw_hubs(self):

        for hub in self.mapdata.hubs.values():

            pygame.draw.circle(
                self.window,
                hub.color,
                self.__get_correct_coordinates(hub.x, hub.y),
                30,
            )

            # display hub text
            self.window.blit(
                hub.text_surf,
                hub.text_surf.get_rect(
                    center=self.__get_correct_coordinates(hub.x, hub.y, True)
                ),
            )

    def __get_correct_coordinates(self, x: int, y: int, is_text: bool = False):
        horizontal_hubs = self.mapdata.horizontal_hubs_number
        vertical_hubs = self.mapdata.vertical_hubs_number

        horizontal_gap = (self.sim_window.horizontal_size) // horizontal_hubs
        vertical_gap = (self.sim_window.vertical_size) // vertical_hubs

        HORIZONTAL_SHIFT = self.sim_window.rect.left
        VERTICAL_SHIFT = self.sim_window.rect.centery

        return (
            x * horizontal_gap + HORIZONTAL_SHIFT,
            y * vertical_gap + VERTICAL_SHIFT,
        )
