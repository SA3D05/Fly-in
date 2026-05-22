"""Display and UI handling for the simulation using pygame."""

import random
import pygame
import sys
from algo import Simulator
from enums import Config
from interface import MenuWindow, SimWindow
from models import MapData


class Display:
    """Manage the graphical display, input and the main game loop.

    Args:
        sim: The `Simulator` instance providing simulation state.
        map_file_name: Display name of the currently loaded map file.
        mapdata: The `MapData` instance containing hubs and connections.
    """

    def __init__(
        self,
        sim: Simulator,
        map_file_name: str,
        mapdata: MapData,
    ) -> None:
        info = pygame.display.Info()
        self.screen_width, self.screen_height = (
            info.current_w,
            info.current_h,
        )

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.FULLSCREEN
        )

        self.mapdata = mapdata
        self.__set_hubs_surf()
        self.sim: Simulator = sim
        self.clock = pygame.time.Clock()
        self.delta: float = 0
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
        self.map_file_text = self.text_base.render(
            map_file_name, False, Config.PRIME_COLOR.value
        )
        self.current_steps_text = self.text_base.render(
            "Steps: 0", False, Config.PRIME_COLOR.value
        )
        self.sim_timer: float = 0
        self.color_timer: float = 0

        self.current_step: int = 0
        self.max_steps: int = -1

    def __set_hubs_surf(self) -> None:
        """Prepare and assign surface images for each hub.

        Loads the hub sprite, applies the hub color and scales the image
        to the configured hub size.
        """

        for hub in self.mapdata.hubs.values():
            img = pygame.image.load(Config.HUB_SPRITE.value).convert_alpha()
            img.fill(
                hub.color if hub.color != "rainbow" else "white",
                special_flags=pygame.BLEND_RGBA_MIN,
            )
            hub.surf = pygame.transform.scale(
                img, (Config.HUB_SIZE.value, Config.HUB_SIZE.value)
            )

    def __dispose(self) -> None:
        """Cleanly quit pygame and exit the program."""
        pygame.quit()
        sys.exit()

    def __update_steps(self) -> None:
        """Refresh the rendered text that shows the current step count."""

        self.current_steps_text = self.text_base.render(
            f"Steps: {self.current_step}",
            False,
            (
                "green"
                if self.current_step == self.max_steps
                else Config.PRIME_COLOR.value
            ),
        )

    def __manage_pressed_event(self) -> None:
        """Handle actions when a menu section is activated/pressed."""

        match self.menu.sections[self.menu.selected_section].text:
            case "Exit":
                self.__dispose()

            case "Start":
                self.run_sim = True

            case "Forward":
                if self.max_steps != -1 and self.sim.forward():
                    self.current_step += 1
                    self.__update_steps()

            case "Restart":
                self.run_sim = False
                self.current_step = 0
                self.max_steps = -1
                self.__update_steps()
                self.sim.reset()

            case "Backward":
                if self.max_steps != -1 and self.sim.backward():
                    self.current_step -= 1
                    self.__update_steps()

    def __check_key_events(self) -> None:
        """Process pygame events for keyboard and mouse input."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__dispose()

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self.__dispose()

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

    def __simulate_rainbow_color(self) -> None:
        """Randomize colors for hubs marked with the special 'rainbow' color.

        This is a cosmetic helper used to periodically change hub colors.
        """

        rainbow = (
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        )

        for hub in self.mapdata.hubs.values():

            if hub.color == "rainbow":
                img = pygame.image.load(
                    Config.HUB_SPRITE.value,
                ).convert_alpha()

                img.fill(
                    random.choice(rainbow),
                    special_flags=pygame.BLEND_RGBA_MIN,
                )

                hub.surf = pygame.transform.scale(
                    img, (Config.HUB_SIZE.value, Config.HUB_SIZE.value)
                )

    def game_loop(self) -> None:
        """Main loop that advances simulation and updates the display.

        Runs indefinitely until the application exits via input.
        """

        while True:

            self.delta = self.clock.tick(60) / 1000
            self.sim_timer += self.delta
            self.color_timer += self.delta

            if self.run_sim and self.max_steps == -1:

                if self.sim.is_end():
                    self.max_steps = self.current_step
                    self.__update_steps()

                elif self.sim_timer >= Config.STEP_TIME.value:

                    self.sim.make_step()
                    self.current_step += 1
                    self.sim_timer = 0
                    self.__update_steps()

            if self.color_timer >= Config.CHANGE_COLOR_TIME.value:
                self.__simulate_rainbow_color()
                self.color_timer = 0

            self.__check_key_events()
            self.__redraw()

    def __redraw(
        self,
    ) -> None:
        """Redraw the entire screen: graph, hubs, drones and UI."""

        self.window.fill(Config.BACKGROUND_COLOR.value)

        self.__draw_connections()
        self.__draw_hubs()
        self.__draw_drones()
        self.__draw_mapfile_name()
        self.__draw_interface()

        pygame.display.update()

    def __draw_mapfile_name(self) -> None:
        """Draw the current map file name and steps text on screen."""

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

    def __draw_interface(self) -> None:
        """Draw menu, graph bounding box and menu sections."""

        # menu part
        pygame.draw.rect(
            self.window,
            Config.BORDERS_COLOR.value,
            self.menu.surf.get_rect(
                topleft=(self.menu.x_pos, self.menu.y_pos),
            ),
            5,
            10,
        )

        # graph part
        pygame.draw.rect(
            self.window,
            Config.BORDERS_COLOR.value,
            self.sim_window.rect,
            5,
            10,
        )

        # sections part
        for section in self.menu.sections:

            pygame.draw.rect(
                self.window,
                Config.PRIME_COLOR.value,
                section.rect,
                0 if self.menu.selected_section == section.index else 5,
                100,
                20 if self.menu.selected_section == section.index else 100,
            )

            self.window.blit(section.text_surf, section.text_rect)

    def __get_random_coordinates(self, coordinates: tuple) -> tuple:
        """Return a small random offset applied to a coordinate pair.

        Args:
            coordinates: Tuple of (x, y) integers.

        Returns:
            A new tuple with +/-1 random jitter applied to each value.
        """
        return tuple(c + random.randint(-1, 1) for c in coordinates)

    def __draw_drones(self) -> None:
        """Render all drones and their id labels on screen."""

        for drone in self.sim.drones:

            x, y = self.__convert_screen_coordinates(drone.x, drone.y)

            self.window.blit(
                drone.surf,
                drone.surf.get_rect(
                    center=self.__get_random_coordinates(
                        (x, y),
                    )
                ),
            )

            self.window.blit(
                drone.text_surf,
                drone.text_surf.get_rect(
                    center=self.__get_random_coordinates((x, y - 100))
                ),
            )

    def __draw_connections(self) -> None:
        """Draw lines representing connections between hubs."""

        for c in self.mapdata.connections:
            pygame.draw.line(
                self.window,
                Config.CONNECTION_COLOR.value,
                self.__convert_screen_coordinates(*c.start_coordinates),
                self.__convert_screen_coordinates(*c.end_coordinates),
                Config.CONNECTION_SIZE.value,
            )

    def __draw_hubs(self) -> None:
        """Draw all hubs and their labels,
          offsetting labels to avoid overlap."""

        levels: dict = dict()
        for hub in self.mapdata.hubs.values():

            if hub.surf is None:
                return

            self.window.blit(
                hub.surf,
                hub.surf.get_rect(
                    center=self.__convert_screen_coordinates(hub.x, hub.y)
                ),
            )

            if levels.get(hub.y) is None:
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

    def __convert_screen_coordinates(
        self, x: float, y: float, is_text: int = 0
    ) -> tuple:
        padding_x = Config.HUB_SIZE.value * 2
        padding_y = 100

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

        screen_x = (
            self.sim_window.rect.left + padding_x + (x - min_x) * scale_x
            )
        screen_y = (
            self.sim_window.rect.bottom - padding_y - (y - min_y) * scale_y
            )

        if is_text == 1:
            screen_y += 50
        elif is_text == 2:
            screen_y -= 50

        return (int(screen_x), int(screen_y))
