import pygame
import sys
from models import MapData, Drone
from pprint import pprint


class Display:

    def __init__(self, map_data: MapData, drone: Drone) -> None:

        self.screen_width, self.screen_height = 1920 / 2, 1080 / 2
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.text = pygame.font.Font("assets/Tiny5.ttf", 30)
        self.hubs = map_data.hubs
        self.connections = map_data.connections
        self.drone = drone
        self.fps_surf = self.text.render("0", False, "white")
        self.frametime_surf = self.text.render("0", False, "white")
        self.current_frametime = 0
        self.moves = 0

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

                # handle zoom later

                # elif event.type == pygame.MOUSEWHEEL:
                #     if event.y > 0:
                #         print("Scrolling up", event.y)
                #         for h in self.hubs.values():
                #             h.size += 50
                #             h.surf = pygame.Surface((h.size, h.size))
                #             h.surf.fill("grey")
                #     elif event.y < 0:
                #         print("Scrolling down", event.y)
                #         for h in self.hubs.values():
                #             h.size -= 50
                #             h.surf = pygame.Surface((h.size, h.size))
                #             h.surf.fill("grey")

            # draw hubs
            self.redraw()

            # set current frame time
            self.current_frametime = self.clock.tick(60)

    def redraw(self) -> None:
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        self.window.fill("black")
        self.window.blit(self.fps_surf, (0, 0))
        self.window.blit(self.frametime_surf, (0, 32))

        # draw connections here ...
        for c in self.connections:
            pygame.draw.line(self.window, "grey", c.start, c.end, 5)
        # draw each hub on the screen
        for hub in self.hubs.values():

            # display hub
            self.window.blit(hub.surf, hub.rect)

            # display hub text
            self.window.blit(hub.text_surf, hub.text_rect)

        # draw drones here ...
        self.window.blit(self.drone.surf, self.drone.rect)

        pygame.display.update()
