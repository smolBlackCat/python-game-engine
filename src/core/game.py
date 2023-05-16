"""Base Game class."""

import pygame

from . import scene


class Game:
    """Base class for implementing specific game instances."""

    FPS = 60

    def __init__(self, screen_width: int, screen_height: int, name: str,
                 icon: pygame.Surface = None):
        pygame.init()
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__name = name

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(name)
        if icon is not None:
            pygame.display.set_icon(icon)
        self.scene_manager = scene.SceneManager()
        self.clock = pygame.time.Clock()

    def add_scene(self, scene_id, scene):
        """Adds scene to game."""

        self.scene_manager.add(scene_id, scene)

    def set_initial_view(self, scene_id):
        """Set the initial scene of the game"""

        self.scene_manager.initial_view(scene_id)

    def start(self) -> None:
        """Main loop of the game."""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.scene_manager.update_on_event(event)

            self.scene_manager.show()
            self.scene_manager.update()

            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()

    @property
    def name(self) -> str:
        """Get game's name."""

        return self.__name

    @property
    def width(self) -> int:
        """Get the game screen width."""

        return self.__screen_width

    @property
    def height(self) -> int:
        """Get the game screen height."""

        return self.__screen_height
