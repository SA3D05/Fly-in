from pprint import pprint
import random

import pygame
import sys
from algo import Simulator
from globals import *

from model import Drone, MapData
from interface import *


class Display:

    def __init__(self, sim: Simulator, map_file_name: str, mapdata: MapData) -> None:
        info = pygame.display.Info()
        self.screen_width, self.screen_height = (info.current_w, info.current_h)

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height),  # pygame.FULLSCREEN
        )
        self.mapdata = mapdata
        self.drones: list[Drone] = sim.drones

        for hub in mapdata.hubs.values():
            img = pygame.image.load("assets/hub.png").convert_alpha()
            img.fill(hub.color, special_flags=pygame.BLEND_RGBA_MIN)
            hub.surf = pygame.transform.scale(img, (50, 50))

        self.sim: Simulator = sim
        self.clock = pygame.time.Clock()

        self.horizontal_margin = 50
        self.vertical_margin = 100
        self.hub_size = 30
        self.menu = MenuWindow(
            self.screen_width,
            self.screen_height,
            (self.horizontal_margin, self.vertical_margin),
            self.horizontal_margin,
            self.vertical_margin,
        )

        self.menu.init_sections(self.screen_width)

        self.sim_window = SimWindow(
            self.screen_width,
            self.screen_height,
            (
                self.menu.horizontal_size + (self.horizontal_margin * 3),
                self.vertical_margin,
            ),
            self.horizontal_margin,
            self.vertical_margin,
        )

        self.text = pygame.font.Font(FONT_FAMILY_PATH, MITRIX_TEXT_SIZE)
        self.map_file_text = self.text.render(map_file_name, False, "white")
        self.steps_text = self.text.render("Steps: 0", False, "white")

        self.step = 0

    def _dispose(self):
        pygame.quit()
        sys.exit()

    def __manage_pressed_event(self):

        match self.menu.sections[self.menu.selected_section].text:
            case "Exit":
                self._dispose()
            # "Forward", "Backward"
            case "Start":
                self.step += 1
                self.sim.move(self.step)
                self.steps_text = self.text.render(
                    f"Steps: {self.step}", False, "white"
                )

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

            self.clock.tick(30)

            self.__check_key_events()
            self._redraw()

    def _redraw(
        self,
    ) -> None:
        self.window.fill((32, 32, 32))

        self._draw_connections()
        self._draw_hubs()
        self._draw_drones()
        self._draw_mapfile_name()

        self._draw_interface()
        # self._draw_debug_lines()

        pygame.display.update()

    def _draw_mapfile_name(self):
        self.window.blit(
            self.steps_text,
            self.steps_text.get_rect(topright=(self.screen_width, 0)),
        )
        self.window.blit(
            self.map_file_text,
            self.map_file_text.get_rect(
                midbottom=(self.screen_width // 2, self.screen_height)
            ),
        )

    def _draw_debug_lines(self):
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (self.screen_width / 2, 0),
            (self.screen_width / 2, self.screen_height),
            CONNECTION_LINE_SIZE,
        )
        pygame.draw.line(
            self.window,
            CONNECTION_LINE_COLOR,
            (0, self.screen_height / 2),
            (self.screen_width, self.screen_height / 2),
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
        return tuple(c + random.randint(-1, 1) for c in coordinates)

    def _draw_drones(self):
        for drone in self.drones:

            x, y = self.__convert_screen_coordinates(drone.x, drone.y)

            self.window.blit(
                drone.surf,
                drone.surf.get_rect(center=self.__get_random_coordinates((x, y))),
            )

            self.window.blit(
                drone.text_surf,
                drone.text_surf.get_rect(
                    center=self.__get_random_coordinates((x, y - 100))
                ),
            )

    def _draw_connections(self):

        for c in self.mapdata.connections:
            pygame.draw.line(
                self.window,
                CONNECTION_LINE_COLOR,
                self.__convert_screen_coordinates(*c.start_pos),
                self.__convert_screen_coordinates(*c.end_pos),
                CONNECTION_LINE_SIZE,
            )

    def _draw_hubs(self):

        levels = {}
        for hub in self.mapdata.hubs.values():

            if hub.surf is None:
                return

            self.window.blit(
                hub.surf,
                hub.surf.get_rect(
                    center=self.__convert_screen_coordinates(hub.x, hub.y)
                ),
            )

            if levels.get(hub.y) == None:
                levels[hub.y] = False
            else:
                levels[hub.y] = not levels[hub.y]

            # display hub text
            self.window.blit(
                hub.text_surf,
                hub.text_surf.get_rect(
                    center=self.__convert_screen_coordinates(
                        hub.x, hub.y, 1 if levels[hub.y] else 2
                    )
                ),
            )

    def __convert_screen_coordinates(self, x, y, is_text=0):
        padding_x = self.hub_size * 2  # hub radius
        padding_y = 100  # hub radius

        max_x = max(hub.x for hub in self.mapdata.hubs.values())
        min_x = min(hub.x for hub in self.mapdata.hubs.values())
        max_y = max(hub.y for hub in self.mapdata.hubs.values())
        min_y = min(hub.y for hub in self.mapdata.hubs.values())

        graph_w = max_x - min_x
        graph_h = max_y - min_y

        draw_w = self.sim_window.rect.width - padding_x * 2
        draw_h = self.sim_window.rect.height - padding_y * 2

        scale_x = draw_w / graph_w if graph_w != 0 else draw_w
        scale_y = draw_h / graph_h if graph_h != 0 else draw_h

        screen_x = self.sim_window.rect.left + padding_x + (x - min_x) * scale_x
        screen_y = self.sim_window.rect.bottom - padding_y - (y - min_y) * scale_y

        if is_text == 1:
            screen_y += 50
        elif is_text == 2:
            screen_y -= 50
        return (int(screen_x), int(screen_y))
