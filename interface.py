import pygame

from globals import FONT_FAMILY_PATH, SCREEN_HEIGHT, SCREEN_WIDTH


class MenuSection:
    def __init__(
        self,
        horizontal_margin: int,
        vertical_margin: int,
        menu_horizontal_size: int,
        menu_vertical_size: int,
        sections_number: int,
        index: int,
        color: str,
        text: str,
    ):

        self.horizontal_size = menu_horizontal_size - horizontal_margin * 2
        self.vertical_size = (
            menu_vertical_size - (vertical_margin * 2) * sections_number
        ) / sections_number

        self.index = index

        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))
        self.color = color

        self.text = text
        self.font = pygame.font.Font(FONT_FAMILY_PATH, int((SCREEN_WIDTH * 40) // 1920))
        self.text_surf = self.font.render(
            text, True, "black" if index == 0 else "white"
        )

    def change_text(self, color: str):
        self.text_surf = self.font.render(self.text, True, color)


class MenuWindow:

    def __init__(self, horizontal_margin: int, vertical_margin: int) -> None:

        self.horizontal_size = SCREEN_WIDTH * 0.25 - horizontal_margin * 2
        self.vertical_size = SCREEN_HEIGHT - vertical_margin * 2

        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))

        self.horizontal_sections_margin = 20
        self.vertical_sections_margin = 50

        self.selected_section = 0
        self.sections: list[MenuSection] = []

    def init_sections(self):

        sections = ["Solve", "Select", "Settings", "Exit"]
        for i, name in enumerate(sections):
            self.sections.append(
                MenuSection(
                    self.horizontal_sections_margin,
                    self.vertical_sections_margin,
                    self.horizontal_size,
                    self.vertical_size,
                    len(sections),
                    i,
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


class SimWindow:
    def __init__(self, horizontal_margin: int, vertical_margin: int) -> None:

        self.horizontal_size = SCREEN_WIDTH * 0.75 - horizontal_margin * 2
        self.vertical_size = SCREEN_HEIGHT - vertical_margin * 2

        self.surf = pygame.Surface((self.horizontal_size, self.vertical_size))
