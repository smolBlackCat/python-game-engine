"""Module that provides some widgets and functions to deal with the
game interface.
"""

import textwrap

from pygame import constants, draw, font, mouse, sprite, surface


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
        (
            self.button_on_image,
            self.button_off_image,
            self.button_clicked_image,
        ) = button_images
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
        self.text_attrs = {
            "size": 14,
            "colour": (255, 255, 255),
            "chars_per_line": 40,
            "ypadding": 2,
            "bold": False,
            "italic": False,
            "antialised": True,
        } | text_attrs
        self.image = self.__create_image(text, self.text_attrs)
        self.rect = self.image.get_rect()

    def draw(self):
        """Draws the text into screen"""

        self.screen.blit(self.image, self.rect)

    def update_text(self, new_text, **text_attrs):
        """It updates the text, therefore updating the surface.

        Important to mention that the new surface, will use the
        already defined text attributes, like colour and size.

        Args:

            new_text:
                The new text rendered in the image attribute.

            text_attrs:
                The attributes to be update as well.
        """
        text_attrs = self.text_attrs | text_attrs

        self.image = self.__create_image(new_text, text_attrs)

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
            None, text_attrs["size"], text_attrs["bold"], text_attrs["italic"]
        )
        rendered_paragraph = [
            text_font.render(phrase, text_attrs["antialised"], text_attrs["colour"])
            for phrase in textwrap.wrap(text, text_attrs["chars_per_line"])
        ]

        height = sum(
            (
                phrase.get_height() + text_attrs["ypadding"]
                for phrase in rendered_paragraph
            )
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


class ButtonBar(sprite.Sprite):
    """Class that represents a right slidable bar of buttons located to the
    right of the screen.

    This implementation is not totally complete. A commom button bar would include:
        * A slider (in case there are more button than vertical space in the bar)
        * A cell system, separating each available node.
    """

    # FIXME: Find better names. Those are prone for misunderstanding
    PADDING = 4
    SPACING = 10

    BAR_COLOUR = (1, 38, 31)

    # TODO: Setup slidable setting
    def __init__(self, screen, label: str, position, *options):
        """Initialises the ButtonBar object.

        Args:
            label: a string title for the button bar title.

            options: a list of tuples containing the option name and
                     the function.

            position: Either "left" or "right"
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.active = False
        self.on_animation = False
        self.position = position
        self.label = Label(screen, label, size=36, antialised=True)
        self.buttons = self._create_text_buttons(screen, options)

        self.bar_image = self._create_bar_sprite(self.label, self.buttons)
        self.bar_rect = self.bar_image.get_rect()

        active_button_images = [
            self._create_button_sprite(
                (85, 110, 83),
                (21, 42, 56),
                (self.bar_rect.height - 32, 10),
            ),
            self._create_button_sprite(
                (41, 67, 92),
                (21, 42, 56),
                (self.bar_rect.height - 32, 10),
            ),
            self._create_button_sprite(
                (85, 110, 83),
                (209, 212, 201),
                (self.bar_rect.height - 32, 10),
            ),
        ]

        def button_bar_action():
            self.on_animation = True

        self.active_button = Button(screen, active_button_images, button_bar_action)

        self.speed = 4
        self.bar_rect.centery = self.screen_rect.centery
        if position == "right":
            self.bar_rect.left = self.screen_rect.right
        elif position == "left":
            self.bar_rect.right = self.screen_rect.left
        else:
            raise ValueError(f"{position} is not one of \"left\" or \"right\"")

        self._update()

    def draw(self):
        self.screen.blit(self.bar_image, self.bar_rect)
        self.active_button.draw()
        if self.active:
            self.label.draw()
            for button in self.buttons:
                button.draw()

    def update(self):
        self.active_button.update()
        if self.on_animation:
            self._slide()
            self._update()
        else:
            if self.active:
                for button in self.buttons:
                    button.update()

    def update_on_event(self, event):
        for button in self.buttons:
            button.update_on_event(event)
        self.active_button.update_on_event(event)
    
    def _slide(self):
        if self.active:
            # We slide it out of the screen
            if self.position == "right":
                if self.bar_rect.left >= self.screen_rect.right:
                    self.on_animation = False
                    self.active = False
                self.bar_rect.x += self.speed
            elif self.position == "left":
                if self.bar_rect.right <= self.screen_rect.left:
                    self.on_animation = False
                    self.active = False
                self.bar_rect.x -= self.speed
        else:
            # We make the button bar visible
            if self.position == "right":
                if self.bar_rect.right <= self.screen_rect.right:
                    self.on_animation = False
                    self.active = True
                self.bar_rect.x -= self.speed
            elif self.position == "left":
                if self.bar_rect.left >= self.screen_rect.left:
                    self.on_animation = False
                    self.active = True
                self.bar_rect.x += self.speed

    # TODO: Should the colours be fixed?
    @classmethod
    def _create_text_buttons(cls, screen, options) -> list[Button]:
        """Sets up a list of buttons to be included in the button
        bar.

        Args:
            options: list of tuples storing a name and a function.
        """

        output = []
        for option in options:
            outline, inline, inline_on, outline_clicked = (
                (60, 165, 157),
                (231, 156, 42),
                (90, 61, 85),
                (162, 222, 150),
            )
            button_images = [
                cls._create_text_button_sprite(option[0], inline_on, outline),
                cls._create_text_button_sprite(option[0], inline, outline),
                cls._create_text_button_sprite(option[0], inline_on, outline_clicked),
            ]
            output.append(Button(screen, button_images, option[1]))
        return output

    @classmethod
    def _create_button_sprite(cls, inline_c, outline_c, base_dimensions):
        """Creates a plain button sprite"""

        dimension_inline_h = base_dimensions[0] + (2 * cls.PADDING)
        dimension_inline_w = base_dimensions[1] + (2 * cls.PADDING)
        in_bt_surface = surface.Surface((dimension_inline_w, dimension_inline_h))
        in_bt_surface_rect = in_bt_surface.get_rect()

        in_bt_surface.fill(inline_c)

        dimension_outline_h = dimension_inline_h + (2 * cls.PADDING)
        dimension_outline_w = dimension_inline_w + (2 * cls.PADDING)

        out_bt_surface = surface.Surface((dimension_outline_w, dimension_outline_h))
        out_bt_surface_rect = out_bt_surface.get_rect()

        in_bt_surface_rect.center = out_bt_surface_rect.center

        out_bt_surface.fill(outline_c)
        out_bt_surface.blit(in_bt_surface, in_bt_surface_rect)

        return out_bt_surface

    @classmethod
    def _create_text_button_sprite(cls, text, inline_c, outline_c):
        """Creates the button image from a Label object."""

        text_image = Label(None, text, size=24).image
        text_rect = text_image.get_rect()

        button_sprite = cls._create_button_sprite(
            inline_c, outline_c, (text_rect.height, text_rect.width)
        )

        button_sprite_rect = button_sprite.get_rect()
        text_rect.center = button_sprite_rect.center
        button_sprite.blit(
            text_image, text_rect
        )

        return button_sprite

    @classmethod
    def _create_bar_sprite(cls, title, buttons) -> surface.Surface:
        """Sets up a bar sprite with the given buttons attached.

        Args:
            title: Label object

            buttons: list of Button objects to be attached to the bar
        """

        w_widest = max(
            buttons + [title], key=lambda button: button.rect.width
        ).rect.width

        bar_width = w_widest + 2 * cls.PADDING
        bar_height = cls._bar_height(buttons + [title])

        bar_sprite = surface.Surface((bar_width, bar_height))
        bar_sprite.fill(cls.BAR_COLOUR)
        draw.rect(bar_sprite, (35, 176, 158), bar_sprite.get_rect(), 4)

        return bar_sprite

    def _update(self):
        # Position the title
        self.label.rect.x = self.bar_rect.x
        self.label.rect.centerx = self.bar_rect.centerx
        self.label.rect.y = self.bar_rect.y + self.PADDING

        # Position the pull button
        if self.position == "left":
            self.active_button.rect.center = self.bar_rect.center
            self.active_button.rect.left = self.bar_rect.right
        elif self.position == "right":
            self.active_button.rect.center = self.bar_rect.center
            self.active_button.rect.right = self.bar_rect.left
        else:
            raise ValueError(f'{self.position} is not one of: "left" or "right"')

        # Position the buttons
        y = self.SPACING + self.label.rect.bottom
        for button in self.buttons:
            button.rect.centerx = self.bar_rect.centerx
            button.rect.y = y
            y = self.SPACING + button.rect.bottom

    @classmethod
    def _bar_height(cls, widgets):
        all_w_height = (
            sum(list(map(lambda button: button.rect.height, widgets)))
            + 2 * cls.PADDING
        )

        return 2 * all_w_height + 2 * cls.PADDING
