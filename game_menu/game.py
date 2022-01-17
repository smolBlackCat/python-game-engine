"""My Game menu implementation.

This is not a game actually, it's just my own implementation of a
game main menu.
"""

import os
import sys

import pygame

from . import scene


def generate_image(filename):
    """Generates an image containing the sprite on the given
    filename.

    Args:
        filename: The .png file where the function will get the image.

    Returns:
        A pygame Surface object that contains the sprite of the file.
    """

    image = pygame.image.load(os.path.join("game_data", filename))
    return image


def quit_game():
    pygame.quit()
    sys.exit()


def main() -> None:
    """Main Program."""

    pygame.init()

    # Pygame setup
    SCREEN_SIZE = (600, 400)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game Main Menu Sample")
    pygame.display.set_icon(generate_image("icon.png"))

    # Game setup
    scene_manager = scene.SceneManager()
    intro_scene = scene.IntroScene(screen)
    main_menu_scene = scene.MainMenuScene(screen)
    scene_manager.add("game_intro", intro_scene)
    scene_manager.add("main_menu", main_menu_scene)
    scene_manager.initial_view("game_intro")
    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_game()
            if scene_manager.current_view == "game_intro":
                intro_scene.update_on_event(event)
            elif scene_manager.current_view == "main_menu":
                main_menu_scene.update_on_event(event)

        # Game loop
        scene_manager.show()

        pygame.display.update()
        clock.tick(60)
