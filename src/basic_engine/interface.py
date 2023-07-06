"""Module that provides some widgets and functions to deal with the
game interface.
"""

import textwrap

from pygame import constants, draw, font, mouse, sprite, surface, time


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

    PADDING = 4
    SPACING = 10
    ANIMATION_SPEED = 20
    BAR_COLOUR = (1, 38, 31)
    BUTTON_SPRITE_RADIUS = 4

    def __init__(self, screen, label: str, position, *options, **colour_args):
        """Initialises the ButtonBar object.

        Args:
            label: a string title for the button bar title.

            options: a list of tuples containing the option name and
                     the function.

            position: Either "left" or "right"

            colour_args:
                a dictionary of colour arguments for each component in the
                ButtonBar. The key is str and the colour code is a
                tuple[R, G, B].

                Available keys:

                    * outline
                    * inline
                    * inline_on
                    * outline_clicked
                    * bar_surface_colour
                    * bar_outline_colour

        """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.active = False
        self.on_animation = False
        self.position = position
        self.label = Label(screen, label, size=36, antialised=True)
        self.buttons = self._create_text_buttons(
            screen,
            options,
            colour_args.get("outline") or (60, 165, 157),
            colour_args.get("inline") or (231, 156, 42),
            colour_args.get("inline_on") or (90, 61, 85),
            colour_args.get("outline_clicked") or (162, 222, 150),
        )

        self.bar_image = self._create_bar_sprite(
            self.label,
            self.buttons,
            colour_args.get("bar_surface_colour") or (0, 0, 0),
            colour_args.get("bar_outline_colour") or (78, 79, 235),
        )
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

        self.bar_rect.centery = self.screen_rect.centery
        if position == "right":
            self.bar_rect.left = self.screen_rect.right
        elif position == "left":
            self.bar_rect.right = self.screen_rect.left
        else:
            raise ValueError(f'{position} is not one of "left" or "right"')

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
                if self.bar_rect.x + self.ANIMATION_SPEED >= self.screen_rect.right:
                    self.bar_rect.left = self.screen_rect.right
                    self.on_animation = False
                    self.active = False
                else:
                    self.bar_rect.x += self.ANIMATION_SPEED
            elif self.position == "left":
                if self.bar_rect.right - self.ANIMATION_SPEED <= self.screen_rect.left:
                    self.bar_rect.right = self.screen_rect.left
                    self.on_animation = False
                    self.active = False
                else:
                    self.bar_rect.right -= self.ANIMATION_SPEED
        else:
            # We make the button bar visible
            if self.position == "right":
                if self.bar_rect.right - self.ANIMATION_SPEED <= self.screen_rect.right:
                    self.bar_rect.right = self.screen_rect.right
                    self.on_animation = False
                    self.active = True
                else:
                    self.bar_rect.right -= self.ANIMATION_SPEED
            elif self.position == "left":
                if self.bar_rect.x + self.ANIMATION_SPEED >= self.screen_rect.left:
                    self.bar_rect.left = self.screen_rect.left
                    self.on_animation = False
                    self.active = True
                else:
                    self.bar_rect.x += self.ANIMATION_SPEED

    @classmethod
    def _create_text_buttons(
        cls, screen, options, outline, inline, inline_on, outline_clicked
    ) -> list[Button]:
        """Sets up a list of buttons to be included in the button
        bar.

        Args:
            options: list of tuples storing a name and a function

            outline: tuple representing the outline RGB colour code

            inline: tuple representing the inline RGB colour code

            inline_on: tuple representing the inline RGB colour code
                       used when the mouse hovers on the button

            outline_clicked: tuple representing the outline RGB colour
                             code used when the button is clicked
        """

        labels = [Label(screen, option[0], size=24) for option in options]

        lg_label_w = max(labels, key=lambda label: label.image.get_width())
        lg_label_h = max(labels, key=lambda label: label.image.get_height())
        maximum_width = lg_label_w.image.get_width()
        maximum_height = lg_label_h.image.get_height()

        output = []
        for option in options:
            button_images = [
                cls._create_text_button_sprite(
                    option[0], inline_on, outline, (maximum_height, maximum_width)
                ),
                cls._create_text_button_sprite(
                    option[0], inline, outline, (maximum_height, maximum_width)
                ),
                cls._create_text_button_sprite(
                    option[0],
                    inline_on,
                    outline_clicked,
                    (maximum_height, maximum_width),
                ),
            ]
            output.append(Button(screen, button_images, option[1]))
        return output

    @classmethod
    def _create_button_sprite(cls, inline_c, outline_c, base_dimensions):
        """Creates a plain button sprite"""

        dimension_inline_h = base_dimensions[0] + (2 * cls.PADDING)
        dimension_inline_w = base_dimensions[1] + (2 * cls.PADDING)
        dimension_outline_h = dimension_inline_h + (2 * cls.PADDING)
        dimension_outline_w = dimension_inline_w + (2 * cls.PADDING)

        root_surface = surface.Surface((dimension_outline_w, dimension_outline_h))

        draw.rect(
            root_surface,
            inline_c,
            root_surface.get_rect(),
            border_radius=cls.BUTTON_SPRITE_RADIUS,
        )
        draw.rect(
            root_surface,
            outline_c,
            root_surface.get_rect(),
            cls.PADDING,
            border_radius=cls.BUTTON_SPRITE_RADIUS,
        )

        return root_surface

    @classmethod
    def _create_text_button_sprite(
        cls, text, inline_c, outline_c, base_dimensions=None
    ):
        """Creates the button image from a Label object."""

        text_image = Label(None, text, size=24).image
        text_rect = text_image.get_rect()

        button_sprite = cls._create_button_sprite(
            inline_c,
            outline_c,
            (
                (text_rect.height, text_rect.width)
                if base_dimensions is None
                else base_dimensions
            ),
        )

        button_sprite_rect = button_sprite.get_rect()
        text_rect.center = button_sprite_rect.center
        button_sprite.blit(text_image, text_rect)

        return button_sprite

    @classmethod
    def _create_bar_sprite(
        cls, title, buttons, bar_surface_colour, bar_outline_colour
    ) -> surface.Surface:
        """Sets up a bar sprite with the given buttons attached.

        Args:
            title: Label object

            buttons: list of Button objects to be attached to the bar

            bar_surface_colour: RGB colour code of the bar's surface
                                represented by a tuple

            bar_outline_colour: RGB colour code of the bar's outline
                                represented by a tuple
        """

        w_widest = max(
            buttons + [title], key=lambda button: button.rect.width
        ).rect.width

        bar_width = w_widest + 4 * cls.PADDING
        bar_height = cls._bar_height(buttons + [title])

        bar_sprite = surface.Surface((bar_width, bar_height))
        bar_sprite.fill(bar_surface_colour)
        draw.rect(bar_sprite, bar_outline_colour, bar_sprite.get_rect(), 4)

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
            sum(list(map(lambda button: button.rect.height, widgets))) + 2 * cls.PADDING
        )

        return 2 * all_w_height + 2 * cls.PADDING


class Chronometer(sprite.Sprite):
    """Graphical implementation of a Chronometer."""

    def __init__(self, screen, colour):
        """Initialises the Chronometer object"""

        super().__init__()

        self.screen = screen
        self.colour = colour
        self.label = Label(screen, "00:00", size=24, bold=True, colour=colour)
        self.rect = self.label.rect
        self.ticking = False
        self.starting_ticks = 0
        self.seconds = 0

    def draw(self):
        self.label.draw()
    
    def update(self):
        if self.ticking:
            self.seconds = (time.get_ticks() - self.starting_ticks) // 1000
            self.label.update_text(self.next_clock_text(self.seconds))

    def start(self):
        """Starts counting."""

        self.starting_ticks = time.get_ticks()
        self.ticking = True

    def reset(self):
        """Resets the clock to 0 seconds."""
        
        self.seconds = 0
        self.ticking = False
        self.label.update_text("00:00")

    def stop(self):
        """Stop counting."""

        self.ticking = False

    @classmethod
    def next_clock_text(cls, seconds):
        """Updates the clock text given the seconds."""

        minutes = round(seconds // 60)
        seconds = seconds - (minutes * 60)

        return "%02d:%02d" % (minutes, seconds)
