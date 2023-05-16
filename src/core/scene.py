"""Module for managing scenes."""

from pygame import event as pg_event, sprite, surface

from . import transition


class Scene:
    """Base scene class for implementing game scenes."""

    def __init__(self, screen: surface.Surface):
        """Initialises the Scene object.

        Args:

            screen:
                The Surface object where this scene will be drawn.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.scene_manager: SceneManager = None

        self.particles_groups: list[sprite.Group] = []

    def draw_particles(self) -> None:
        """Draws the particles generated by the scene."""

        for particles_group in self.particles_groups:
            particles_group.draw(self.screen)

    def update_particles(self) -> None:
        """Updates the particles generated by the scene."""

        for particles_group in self.particles_groups:
            if len(particles_group) == 0:
                self.particles_groups.remove(particles_group)
            particles_group.update()

    def draw(self) -> None:
        """Draws the components of this scene in the screen."""

    def update(self) -> None:
        """Updates the components everytime in the loop."""

    def update_on_event(self, event: pg_event.Event) -> None:
        """Updates the components if a event occur.

        Args:

            event: pygame.event.Event object fetched from the event
                   loop.
        """


class SceneManager:
    """Class for managing scenes within a game window.

    The SceneManager class has three essential tasks:

        * Drawing the current scene onto game screen
        * Updating the components of the current scene
        * Alternating from scene to scene.
    """

    def __init__(self):
        """Initialises SceneManager instance."""

        self.views: dict[str, Scene] = {}
        self.on_transition = False
        self.fx_object: transition.Transition = None
        self.current_scene: Scene = None

    def add(self, scene_id: str, scene: Scene) -> None:
        """Adds a scene to the scene manager.

        Args:

            scene_id: An id for the scene. It will be used for example
                      when a scene change is requested.

            scene: Any Scene object.
        """

        scene.scene_manager = self
        self.views[scene_id] = scene

    def show(self) -> None:
        """Shows the current view, handling possible transition
        requests automatically.
        """

        self.views[self.current_scene].draw()
        if self.on_transition:
            self.fx_object.animate()

    def update(self) -> None:
        """Updates the current scene components."""

        if not self.on_transition:
            self.views[self.current_scene].update()

    def update_on_event(self, event: pg_event.Event) -> None:
        """Updates scenes based on events being read by the for loop.

        Args:

            event: pygame.event.Event object fetched from the event
                   loop.
        """

        if not self.on_transition:
            self.views[self.current_scene].update_on_event(event)

    def _change_scene(self, scene_id: str) -> None:
        """It changes the current scene directly.

        Args:

            scene_id: Name of the scene from where the screen will
                      change to."""

        self.current_scene = scene_id

    def change_scene(self, scene_id: str,
                     transition_: transition.Transition = None) -> None:
        """It changes the current scene with a special effect or
        not.

        Args:

            scene_id: Name of the scene from where the screen will
                      change to.

            transition: Transition object that will animate a
                        transition from the current scene to the new
                        given one.
        """

        if scene_id != self.current_scene:
            if transition_ is not None:
                self.fx_object = transition_
                self.on_transition = True
            else:
                # Changes the view abruptly.
                self._change_scene(scene_id)

    def initial_view(self, scene_id: str) -> None:
        """Sets the initial view for the scene manager.

        Args:

            scene_id: Name of the scene to be drawn into the screen.
        """

        self.current_scene = scene_id
