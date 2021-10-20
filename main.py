"""My Game menu implementation.

This is not a game actually, it's just my own implementation of a
game main menu.
"""

import os

import pygame


def main():
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

    game_title_rect = game_title_image.get_rect()
    game_title_rect.centerx = screen_rect.centerx
    game_title_rect.top = screen_rect.top + 10

    play_button_off_rect = play_button_off_image.get_rect()
    play_button_off_rect.centerx = screen_rect.centerx
    play_button_off_rect.centery = screen_rect.centery

    settings_button_off_rect = settings_button_off_image.get_rect()
    settings_button_off_rect.midleft = screen_rect.midleft

    pygame.display.set_caption("Game Main Menu Sample")
    pygame.display.set_icon(game_icon_image)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((170, 170, 170))
        screen.blit(game_title_image, game_title_rect)
        screen.blit(play_button_off_image, play_button_off_rect)
        screen.blit(settings_button_off_image, settings_button_off_rect)
        pygame.display.update()


if __name__ == "__main__":
    main()
