from pygame import constants
from .. import game, scene, interface

from random import randint, choice


class DebugScene(scene.Scene):
    """Scene for debugging the interface module."""

    def __init__(self, screen):
        super().__init__(screen)

        self.text_attrs = {"colour": (170, 170, 170), "size": 36,
                           "chars_per_line": 20}
        self.scene_label = interface.Label(self.screen,
                                           "This is merely a test text.",
                                           **self.text_attrs)
        self.scene_label.rect.center = self.screen_rect.center

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.scene_label.draw()
    
    def update_on_event(self, event) -> None:
        if event.type == constants.KEYDOWN:
            if event.key == constants.K_c:
                # Change the text colour
                self.text_attrs.update(colour=[randint(0, 255) for n in range(3)])

                self.scene_label.update_text("This is merely a test text",
                                             **self.text_attrs)
            elif event.key == constants.K_u:
                messages = ["Programming is cool", "C++ is a lot faster",
                            "Java is for schizos",
                            "There's no need for you to say you're sorry, "
                            "goodbye I'm going home."]
                self.scene_label.update_text(choice(messages),
                                             **self.text_attrs)
                self.scene_label.rect.centerx = self.screen_rect.centerx
                self.scene_label.rect.centery = self.screen_rect.centery



def main():
    """Main entry for testing the interface module."""

    app = game.Game(800, 600, "Interface Module Test")
    app.add_scene("main", DebugScene(app.screen))

    app.start()


if __name__ == "__main__":
    main()
