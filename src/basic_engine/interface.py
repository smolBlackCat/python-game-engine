"""Module that provides some widgets and functions to deal with the
game interface.
"""

import textwrap

from pygame import constants, font, mouse, sprite, surface


class Button(sprite.Sprite):
    """This class represents a interface button on a game. The button can have
    any look, as it has the off and on variants.
    """

    def __init__(self, screen, button_images, action=None):
        """Initialises the Button object.

        Args:
            screen:
                A pygame Surface object that represents the screen.

            button_images:
                A tuple containing the three loaded sprites for the
                button in three states: on, off, clicked

            action:
                A function that is always executed when the button is
                pressed.
        """

        super().__init__()

        self.screen = screen
        self.button_on_image, self.button_off_image, self.button_clicked_image = button_images
        self.current_sprite = self.button_off_image
        self.rect = self.current_sprite.get_rect()
        self.action = action

    def draw(self):
        """Draws the button on the screen."""

        self.screen.blit(self.current_sprite, self.rect)

    def update_on_event(self, event):
        """Does a given action for each mouse right button releases on
        the button.

        Args:

            event: pygame.event.Event object fetched from the event
                   loop.
        """

        if event.type == constants.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.current_sprite = self.button_off_image
                if self.action is not None:
                    self.action()

    def update(self):
        """Updates the button according to the user actions.

        User actions == Hover the mouse on the button, Click the
        button and etc.
        """

        if self.rect.collidepoint(mouse.get_pos()):
            self.current_sprite = self.button_on_image
            if mouse.get_pressed()[0]:
                self.current_sprite = self.button_clicked_image
        else:
            self.current_sprite = self.button_off_image


class Label(sprite.Sprite):
    """Class that represents a label on a game."""

    def __init__(self, screen, text, **text_attrs):
        """Initialises the Label object.

        Args:
            screen:
                A Surface object representing the game window.

            text:
                str object containing the text to be generated for
                this label.

            text_attrs:
                A dict object containing general attributes of the
                text.
        """
        super().__init__()

        self.screen = screen
        self.text_attrs = text_attrs | {
            "size": 14,
            "colour": (255, 255, 255),
            "chars_per_line": 40,
            "ypadding": 2,
            "bold": False,
            "italic": False,
            "antialised": True}
        self.image = self.__create_image(text, self.text_attrs)
        self.rect = self.image.get_rect()

    def draw(self):
        """Draws the text into screen"""

        self.screen.blit(self.image, self.rect)

    def update_text(self, new_text):
        """It updates the text, therefore updating the surface.

        Important to mention that the new surface, will use the
        already defined text attributes, like colour and size.

        Args:

            new_text:
                The new text rendered in the image attribute.
        """

        self.image = self.__create_image(new_text, self.text_attrs)
        self.rect = self.image.get_rect()

    def __create_image(self, text, text_attrs):
        """Generates a Surface object that contains a wrapped text.

        Args:

            text:
                The text to be created on the surface.

            colour:
                The text colour

            size:
                The size of the text font

            text_attrs:
                A dict object containing general attributes of the
                text, that's one of:

                colour:
                    tuple object containing the three values,
                    indicating their respective R, G and B values.

                size:
                    The character size.

                chars_per_line:
                    The amount of characters in each line.

                y_padding:
                    The amount of vertical padding from line to line.

                bold:
                    Indicates if the text is bold.

                italic:
                    Indicates if the text is italic.

                antialised:
                    Indicates if the text in the surface is
                    antialised.

        Returns:
            A Surface object with a blitted Surface object that is in
            fact the rendered text.
        """

        text_font = font.SysFont(
            None, text_attrs["size"], text_attrs["bold"], text_attrs["italic"])
        rendered_paragraph = [
            text_font.render(phrase, text_attrs["antialised"],
                             text_attrs["colour"])
            for phrase in textwrap.wrap(text, text_attrs["chars_per_line"])
        ]

        height = sum(
            (phrase.get_height() + text_attrs["ypadding"]
             for phrase in rendered_paragraph)
        )
        width = max((phrase.get_width() for phrase in rendered_paragraph))
        text_bg = surface.Surface((width, height), constants.SRCALPHA)

        row = 0
        for phrase in rendered_paragraph:
            rect = phrase.get_rect()
            rect.y = row
            text_bg.blit(phrase, rect)
            row += text_font.get_height() + text_attrs["ypadding"]

        return text_bg
