from pygame import draw, surface
from .. import game, scene


class MainScene(scene.Scene):
    """Main scene of a game."""

    def __init__(self, screen: surface.Surface):
        super().__init__(screen)

    def draw(self) -> None:
        self.screen.fill((0, 0, 178))
        draw.circle(self.screen, (170, 170, 170),
                    (self.screen.get_width() / 2,
                     self.screen.get_height() / 2), 30)


def main():
    game_ = game.Game(600, 400, "Game example")

    game_.add_scene("main_scene", MainScene(game_.screen))

    game_.start()


if __name__ == "__main__":
    main()
