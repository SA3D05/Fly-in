import pygame

from enums import Config


class MenuSection:
    def __init__(
        self,
        screen_width: int,
        coordinates: tuple[int, int],
        size: tuple[int, int],
        sections_number: int,
        index: int,
        color: str,
        text: str,
    ):

        self.x_pos, self.y_pos = coordinates
        self.horizontal_size, self.vertical_size = size

        self.index = index
        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))

        self.color = color

        self.text = text
        self.font = pygame.font.Font(
            Config.FONT_PATH.value, int((screen_width * 40) // 1920)
        )
        self.text_surf = self.font.render(
            text,
            True,
            "black" if index == 0 else "white",
        )
        self.text_rect = self.text_surf.get_rect(
            center=(
                (self.x_pos + self.horizontal_size // 2),
                (self.y_pos + self.vertical_size // 2),
            )
        )

    def change_text(self, color: str):
        self.text_surf = self.font.render(self.text, True, color)


class MenuWindow:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        coordinates: tuple[int, int],
        horizontal_margin: int,
        vertical_margin: int,
    ) -> None:

        self.x_pos, self.y_pos = coordinates

        self.horizontal_size: int = int(screen_width * 0.2 - horizontal_margin * 2)
        self.vertical_size = screen_height - (vertical_margin + 300) * 2

        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))

        self.horizontal_sections_margin = 50
        self.vertical_sections_margin = 10

        self.selected_section = 0
        self.sections: list[MenuSection] = []

    def init_sections(self, screen_width: int):
        sections = ["Start", "Backward", "Forward", "Exit"]

        for index, name in enumerate(sections):

            x_size = self.horizontal_size - (self.horizontal_sections_margin * 2)

            y_size = (
                self.vertical_size - (self.vertical_sections_margin * 2 * len(sections))
            ) // len(sections)

            x_pos = self.horizontal_margin + self.horizontal_sections_margin

            y_pos = (self.vertical_margin + self.vertical_sections_margin) + (
                y_size + self.vertical_sections_margin * 2
            ) * index

            self.sections.append(
                MenuSection(
                    screen_width,
                    (x_pos, y_pos),
                    (x_size, y_size),
                    len(sections),
                    index,
                    "white",
                    name,
                )
            )

    def move_up(self):
        current_idx = self.selected_section
        target_idx = current_idx - 1

        if target_idx < 0:
            self.selected_section = len(self.sections) - 1
        else:
            self.selected_section = target_idx

        self.sections[current_idx].change_text("white")
        self.sections[self.selected_section].change_text("black")

    def move_down(self):
        current_idx = self.selected_section
        target_idx = current_idx + 1

        if target_idx >= len(self.sections):
            self.selected_section = 0
        else:
            self.selected_section = target_idx

        self.sections[current_idx].change_text("white")
        self.sections[self.selected_section].change_text("black")

    def change_selected_section(self, section_idx: int):

        self.sections[self.selected_section].change_text("white")
        self.sections[section_idx].change_text("black")
        self.selected_section = section_idx


class SimWindow:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        coordinates: tuple[int, int],
        horizontal_margin: int,
        vertical_margin: int,
    ) -> None:

        self.horizontal_size = screen_width * 0.8 - horizontal_margin * 2
        self.vertical_size = screen_height - vertical_margin * 2
        self.x_pos, self.y_pos = coordinates

        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))
        self.rect = self.surf.get_rect(
            topleft=(self.x_pos, self.y_pos),
        )
