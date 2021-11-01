"""My Game menu implementation.

This is not a game actually, it's just my own implementation of a
game main menu.
"""

import os

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


def setup_intro_view(screen_rect, logo_icon_rect, logo_title_rect):
    """Setups the rects of the sprites to the assigned positions."""

    logo_icon_rect.centerx = screen_rect.centerx
    logo_icon_rect.centery = screen_rect.centery

    logo_title_rect.centerx = screen_rect.centerx
    logo_title_rect.centery = screen_rect.centery + 74


def intro_view(screen, logo_icon_image, logo_title_image, logo_icon_rect,
               logo_title_rect) -> None:
    """Draws the sprites of the introduction view."""

    screen.blit(logo_icon_image, logo_icon_rect)
    screen.blit(logo_title_image, logo_title_rect)


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
    """Draws the sprites of the main view."""

    screen.blit(game_title_image, game_title_rect)
    screen.blit(play_button_off_image, play_button_off_rect)
    screen.blit(settings_button_off_image, settings_button_off_rect)
    screen.blit(quit_button_off_image, quit_button_off_rect)


def main() -> None:
    """Main Program."""

    pygame.init()

    SCREEN_SIZE = (600, 400)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen_rect = screen.get_rect()

    logo_icon_image = generate_image("moura_cat.png")
    logo_title_image = generate_image("logo_title.png")
    game_icon_image = generate_image("icon.png")
    game_title_image = generate_image("game_title.png")
    play_button_image = generate_image("play_button_off.png")
    settings_button_image = generate_image("settings_button_off.png")
    quit_button_image = generate_image("quit_button_off.png")

    white_background = pygame.Surface(SCREEN_SIZE)
    white_background = white_background.convert_alpha()

    logo_icon_rect = logo_icon_image.get_rect()
    logo_title_rect = logo_title_image.get_rect()
    game_title_rect = game_title_image.get_rect()
    play_button_rect = play_button_image.get_rect()
    settings_button_rect = settings_button_image.get_rect()
    quit_button_rect = quit_button_image.get_rect()

    white_background_rect = white_background.get_rect()
    white_background_rect.center = screen_rect.center

    setup_intro_view(screen_rect, logo_icon_rect, logo_title_rect)
    setup_main_menu_view(screen_rect, game_title_rect, play_button_rect,
                         settings_button_rect, quit_button_rect)

    pygame.display.set_caption("Game Main Menu Sample")
    pygame.display.set_icon(game_icon_image)

    yspeed = 7
    # FIXME: It needs to be decided what it's better: Use more CPU or RAM
    def animate_main_menu_view():
        """Animate the buttons of the menu view."""
        nonlocal yspeed
        nonlocal screen_rect
        nonlocal game_title_rect
        nonlocal play_button_image
        nonlocal settings_button_image
        nonlocal quit_button_image

        mouse_pos = pygame.mouse.get_pos()
        if game_title_rect.bottom >= 120 \
           or game_title_rect.top <= screen_rect.top:
            yspeed *= -1
        game_title_rect.y += int(yspeed)

        if play_button_rect.collidepoint(mouse_pos):
            play_button_image = generate_image("play_button_on.png")
        else:
            play_button_image = generate_image("play_button_off.png")

        if settings_button_rect.collidepoint(mouse_pos):
            settings_button_image = generate_image("settings_button_on.png")
        else:
            settings_button_image = generate_image("settings_button_off.png")

        if quit_button_rect.collidepoint(mouse_pos):
            quit_button_image = generate_image("quit_button_on.png")
        else:
            quit_button_image = generate_image("quit_button_off.png")

    alpha_value = 255
    factor = 1

    backwards = False
    on_intro = True
    fade_counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((255, 255, 255))

        if on_intro:
            # Draw and animate the next view while fades out.
            if fade_counter == 3:
                main_menu_view(screen, game_title_image, play_button_image,
                          settings_button_image, quit_button_image,
                          game_title_rect, play_button_rect,
                          settings_button_rect, quit_button_rect)
                animate_main_menu_view()
            else:
                intro_view(screen, logo_icon_image, logo_title_image,
                           logo_icon_rect, logo_title_rect)
            screen.blit(white_background, white_background_rect)
            alpha_value += factor
            if (alpha_value > 255 and not backwards) \
            or (alpha_value < 0 and backwards):
                backwards = not backwards
                factor *= -1
                fade_counter += 1
            white_background.set_alpha(alpha_value)
            white_background.fill((255, 255, 255))

            if fade_counter == 4:
                on_intro = False
        else:
            main_menu_view(screen, game_title_image, play_button_image,
                          settings_button_image, quit_button_image,
                          game_title_rect, play_button_rect,
                          settings_button_rect, quit_button_rect)
            animate_main_menu_view()
        
        print(fade_counter)

        clock.tick(60)
        pygame.display.update()
