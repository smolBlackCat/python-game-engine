import pygame

# TODO: Implement transition class
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


def floating_animation(*args):
    """Simulates a floating object with a given sprite rect.
    
    It utilises only three arguments: a component object, that is
    custom object like Label and Button, y_limit_bottom and
    y_limit_top respectively.
    """

    component = args[0]
    y_limit_bottom = args[1]
    y_limit_top = args[2]

    if component.rect.bottom >= y_limit_bottom \
    or component.rect.top <= y_limit_top:
        component.yspeed *= -1
    component.rect.y += component.yspeed
