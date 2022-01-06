"""My Game menu implementation.

This is not a game actually, it's just my own implementation of a
game main menu.
"""

import os
import sys

from . import interface

import pygame


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


def main_menu_view(screen, game_title_label, play_button, settings_button,
                   quit_button):
    screen.fill((0, 0, 80))
    interface.main_menu_view(game_title_label, play_button, settings_button,
        quit_button
    )
    game_title_label.update()


def main_menu_settings_view(screen, info_label, return_button):
    screen.fill((12, 12, 12))
    info_label.draw()
    return_button.draw()


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
    screen_rect = screen.get_rect()

    # Intro view setup
    logo_icon = interface.Label.from_image(screen,
    generate_image("moura_cat.png"))
    logo_title = interface.Label.from_image(screen,
    generate_image("logo_title.png"))
    interface.setup_intro_view(screen_rect, logo_icon, logo_title)

    # Main Menu view setup
    game_title_label = interface.Label.from_image(screen,
        generate_image("game_title.png"),
        interface.floating_animation,
        120, screen_rect.top)
    play_button = interface.Button(screen,
        generate_image("play_button_on.png"),
        generate_image("play_button_off.png"),
        generate_image("play_button_clicked.png"))
    settings_button = interface.Button(screen,
        generate_image("settings_button_on.png"),
        generate_image("settings_button_off.png"),
        generate_image("settings_button_clicked.png"))
    quit_button = interface.Button(screen,
        generate_image("quit_button_on.png"),
        generate_image("quit_button_off.png"),
        generate_image("quit_button_clicked.png"),
        quit_game)
    interface.setup_main_menu_view(screen_rect, game_title_label, play_button,
                                   settings_button, quit_button
    )

    # Main Menu settings view setup
    info_label = interface.Label.from_text(screen,
        "This is the settings. You can change whatever you want here, as long"
        + " it feels useful to do that. For now, this setting view doesn't "
        + "have anything that interesting, just this return button below this "
        +"text.", (255, 255, 255), 32, 40, 2, antialised=True)
    return_button = interface.Button(screen,
        generate_image("return_button_on.png"),
        generate_image("return_button_off.png"),
        generate_image("return_button_clicked.png"))
    info_label.rect.midtop = screen_rect.midtop
    return_button.rect.midbottom = screen_rect.midbottom

    views = {
        "main_menu": lambda: main_menu_view(
            screen, game_title_label, play_button, settings_button, quit_button
        ),
        "main_menu_settings": lambda: main_menu_settings_view(
            screen, info_label,return_button
        ),
        "main_menu_play": None,
        "current_view": "main_menu"
    }

    settings_button.action = lambda: views.update(
        current_view="main_menu_settings"
    )
    return_button.action = lambda: views.update(current_view="main_menu")

    white_background = pygame.Surface(SCREEN_SIZE)
    white_background = white_background.convert_alpha()
    white_background_rect = white_background.get_rect()
    white_background_rect.center = screen_rect.center

    alpha_value = 255
    factor = 2
    backwards = False
    on_intro = True
    fade_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            
            if views["current_view"] == "main_menu":
                play_button.update(event)
                settings_button.update(event)
                quit_button.update(event)
            elif views["current_view"] == "main_menu_settings":
                return_button.update(event)

        screen.fill((255, 255, 255))
        if on_intro:
            # Introduction
            if fade_counter == 3:
                # Draw and animate the next view while fades out.
                main_menu_view(screen, game_title_label, play_button,
                    settings_button, quit_button
                )
            else:
                interface.intro_view(logo_icon, logo_title)

            # Controls the fade alpha value
            alpha_value += factor
            if (alpha_value > 255 and not backwards) \
            or (alpha_value < 0 and backwards):
                backwards = not backwards
                factor *= -1
                fade_counter += 1

            # Draw the fade effect
            white_background.set_alpha(alpha_value)
            white_background.fill((255, 255, 255))
            screen.blit(white_background, white_background_rect)

            if fade_counter == 4:
                # Ends fade effect completely
                on_intro = False
        else:
            # Game loop
            current_view = views["current_view"]
            views[current_view]()

        clock.tick(60)
        pygame.display.update()
