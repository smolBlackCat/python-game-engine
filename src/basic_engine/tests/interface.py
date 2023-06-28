import unittest
from random import choice, randint
from pygame import init
from pygame import constants

from .. import game, interface, scene

init()


class DebugScene(scene.Scene):
    """Scene for debugging the interface module."""

    def __init__(self, screen):
        super().__init__(screen)

        self.text_attrs = {"colour": (170, 170, 170), "size": 36, "chars_per_line": 20}
        self.scene_label = interface.Label(
            self.screen, "This is merely a test text.", **self.text_attrs
        )

        actions = [
            ("A* algorithm        ", lambda: print("fatal1")),
            ("Djikstra", lambda: print("fatal2")),
            ("Breadth-First Search", lambda: print("fatal3")),
            ("Depth-First Search", lambda: print("fatal4")),
        ]
        self.button_bar = interface.ButtonBar(screen, "This is a Button Bar",
                                              *actions)

        self.button_bar.bar_rect.centery = self.screen_rect.centery
        self.scene_label.rect.center = self.screen_rect.center

    def draw(self) -> None:
        self.screen.fill((255, 255, 0))
        self.button_bar.draw()
        self.scene_label.draw()

    def update(self):
        self.button_bar.update()

    def update_on_event(self, event) -> None:
        self.button_bar.update_on_event(event)
        if event.type == constants.KEYDOWN:
            if event.key == constants.K_c:
                # Change the text colour
                self.text_attrs.update(colour=[randint(0, 255) for n in range(3)])

                self.scene_label.update_text(
                    "This is merely a test text", **self.text_attrs
                )
            elif event.key == constants.K_u:
                messages = [
                    "Programming is cool",
                    "C++ is a lot faster",
                    "Java is for schizos",
                    "There's no need for you to say you're sorry, "
                    "goodbye I'm going home.",
                ]
                self.scene_label.update_text(choice(messages), **self.text_attrs)
                self.scene_label.rect.centerx = self.screen_rect.centerx
                self.scene_label.rect.centery = self.screen_rect.centery


class ButtonBarTestCase(unittest.TestCase):
    """Tests Functions related to the ButtonBar class"""

    def test_setup_buttons(self):
        options = [("string", str), ("integer", int), ("float", float)]

        output = interface.ButtonBar._create_buttons(None, options)

        self.assertEqual(len(output), 3)

        # Checks if the given button is indeed a button
        for option, button in zip(options, output):
            self.assertIsInstance(button, interface.Button)
            self.assertEqual(option[1], button.action)

    def test_create_button(self):
        output = interface.ButtonBar._create_button_sprite(
            "test", (150, 0, 0), (255, 165, 0)
        )

        label_image = interface.Label(None, "test").image

        self.assertEqual(
            output.get_height(),
            label_image.get_rect().height
            + (2 * interface.ButtonBar.BUTTON_BORDER_PADDING)
            + (2 * interface.ButtonBar.BUTTON_EXTRA_SPACE),
        )
        self.assertEqual(
            output.get_width(),
            label_image.get_rect().width
            + (2 * interface.ButtonBar.BUTTON_BORDER_PADDING)
            + (2 * interface.ButtonBar.BUTTON_EXTRA_SPACE),
        )


def main():
    """Main entry for testing the interface module."""

    app = game.Game(800, 600, "Interface Module Test")
    app.add_scene("main", DebugScene(app.screen))

    app.start()


if __name__ == "__main__":
    # unittest.main()
    main()
