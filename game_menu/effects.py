import pygame


class FadeTransition:
    """Class responsible for manipulating the Surface in a way that
    the screens is fading.
    """
    
    def __init__(self, screen, bg_colour, scene_manager):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.scene_manager = scene_manager

        # Fade elements
        self.fade_bg = pygame.Surface(screen.get_size())
        self.fade_bg.set_alpha(0)
        self.fade_bg.fill(bg_colour)
        self.rect = self.fade_bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Fade params