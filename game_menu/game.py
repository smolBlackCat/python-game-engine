"""My Game menu implementation.

This is not a game actually, it's just my own implementation of a
game main menu.
"""

import os

import pygame


def intro_view() -> None:
    pass


def setup_main_menu_view(screen_rect, game_title_rect, play_button_off_rect,
                         settings_button_off_rect,
                         quit_button_off_rect) -> None:
    """Setups the sprites related to the main menu."""

    padding = 10
    game_title_rect.centerx = screen_rect.centerx
    game_title_rect.top = screen_rect.top + padding

    play_button_off_rect.midleft = screen_rect.midleft
    play_button_off_rect.x += padding

    settings_button_off_rect.midleft = screen_rect.midleft
    settings_button_off_rect.y += 35 + padding
    settings_button_off_rect.x += padding

    quit_button_off_rect.midleft = screen_rect.midleft
    quit_button_off_rect.y += 80 + padding
    quit_button_off_rect.x += padding


def main_menu_view(screen, game_title_image, play_button_off_image,
                   settings_button_off_image, quit_button_off_image,
                   game_title_rect, play_button_off_rect,
                   settings_button_off_rect, quit_button_off_rect) -> None:
    """Draws the sprites."""

    screen.blit(game_title_image, game_title_rect)
    screen.blit(play_button_off_image, play_button_off_rect)
    screen.blit(settings_button_off_image, settings_button_off_rect)
    screen.blit(quit_button_off_image, quit_button_off_rect)


def main() -> None:
    """Main Program."""

    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    screen_rect = screen.get_rect()

    # Load images
    game_icon_image = pygame.image.load(os.path.join("game_data", "icon.png"))
    game_title_image = pygame.image.load(
        os.path.join("game_data", "game_title.png"))
    play_button_off_image = pygame.image.load(
        os.path.join("game_data", "play_button_off.png"))
    settings_button_off_image = pygame.image.load(
        os.path.join("game_data", "settings_button_off.png"))
    quit_button_off_image = pygame.image.load(
        os.path.join("game_data", "quit_button_off.png"))

    game_title_rect = game_title_image.get_rect()
    play_button_off_rect = play_button_off_image.get_rect()
    settings_button_off_rect = settings_button_off_image.get_rect()
    quit_button_off_rect = quit_button_off_image.get_rect()

    setup_main_menu_view(screen_rect, game_title_rect, play_button_off_rect,
                         settings_button_off_rect, quit_button_off_rect)

    pygame.display.set_caption("Game Main Menu Sample")
    pygame.display.set_icon(game_icon_image)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((170, 170, 170))
        main_menu_view(screen, game_title_image, play_button_off_image,
                       settings_button_off_image, quit_button_off_image,
                       game_title_rect, play_button_off_rect,
                       settings_button_off_rect, quit_button_off_rect)
        pygame.display.update()
