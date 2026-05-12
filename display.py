from pprint import pprint
import random
from time import sleep

import pygame
import sys
from algo import Simulator

from enums import Config
from models import Drone, MapData
from interface import *


class Display:

    def __init__(self, sim: Simulator, map_file_name: str, mapdata: MapData) -> None:
        info = pygame.display.Info()
        # self.screen_width, self.screen_height = (1920, 1080)
        # self.window = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.screen_width, self.screen_height = (info.current_w, info.current_h)

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.FULLSCREEN
        )
        self.mapdata = mapdata
        self.drones: list[Drone] = sim.drones

        for hub in mapdata.hubs.values():
            img = pygame.image.load(Config.HUB_SPRITE.value).convert_alpha()
            img.fill(hub.color, special_flags=pygame.BLEND_RGBA_MIN)
            hub.surf = pygame.transform.scale(
                img, (Config.HUB_SIZE.value, Config.HUB_SIZE.value)
            )

        self.sim: Simulator = sim
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.run_sim = False
        self.horizontal_margin = 50
        self.vertical_margin = 100
        self.menu = MenuWindow(
            self.screen_width,
            self.screen_height,
            (self.horizontal_margin, self.vertical_margin),
            self.horizontal_margin,
            self.vertical_margin,
        )

        self.menu.init_sections(self.screen_width)
        self.delta = 0
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

        self.text_base = pygame.font.Font(
            Config.FONT_PATH.value, Config.INFO_TEXT_SIZE.value
        )
        self.map_file_text = self.text_base.render(map_file_name, False, "white")
        self.current_steps_text = self.text_base.render("Steps: 0", False, "white")
        self.timer = 0
        self.time_between = 0.1
        self.current_step = 0
        self.max_steps = -1

    def _dispose(self):
        pygame.quit()
        sys.exit()

    def __update_steps(self):

        self.current_steps_text = self.text_base.render(
            f"Steps: {self.current_step}",
            False,
            "green" if self.current_step == self.max_steps else "white",
        )

    def __manage_pressed_event(self):

        match self.menu.sections[self.menu.selected_section].text:
            case "Exit":
                self._dispose()

            # "Forward", "Backward"

            case "Start":

                self.run_sim = not self.run_sim

            case "Forward":
                if self.max_steps != -1 and self.sim.forward():
                    self.current_step += 1
                    self.__update_steps()
                else:
                    self.sim.make_step()
                    self.current_step += 1
                    self.__update_steps()

                print("For:", self.sim.forward_stack)
                print("Back:", self.sim.backward_stack)
                print("+" * 20)

            case "Backward":
                if self.max_steps != -1 and self.sim.backward():
                    self.current_step -= 1
                    self.__update_steps()
                print("For:", self.sim.forward_stack)
                print("Back:", self.sim.backward_stack)
                print("+" * 20)

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

            self.delta = self.clock.tick(60) / 1000
            self.timer += self.delta

            for drone in self.sim.drones:
                if drone.x > drone.target_x:
                    drone.x -= self.delta * Config.DRONES_SPEED.value
                if drone.y > drone.target_y:
                    drone.y -= self.delta * Config.DRONES_SPEED.value
            if self.run_sim:

                if self.sim.is_end():
                    self.run_sim = False
                    if self.max_steps == -1:
                        self.max_steps = self.current_step
                        self.__update_steps()

                elif self.timer >= self.time_between:

                    self.sim.make_step()
                    self.current_step += 1
                    self.__update_steps()
                    self.timer = 0

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
            self.current_steps_text,
            self.current_steps_text.get_rect(topright=(self.screen_width, 0)),
        )
        self.window.blit(
            self.map_file_text,
            self.map_file_text.get_rect(
                midbottom=(self.screen_width // 2, self.screen_height)
            ),
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
                Config.CONNECTION_COLOR.value,
                self.__convert_screen_coordinates(*c.start_coordinates),
                self.__convert_screen_coordinates(*c.end_coordinates),
                Config.CONNECTION_SIZE.value,
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
        padding_x = Config.HUB_SIZE.value * 2  # hub radius
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
