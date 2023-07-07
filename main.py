"""
TSG4 - a little life simulation
"""
from configparser import ConfigParser
from typing import Tuple

import pygame as pg

from tsg import GackManager, StuffManager, TSGConfig

TITLE = "TSG4"


def evaluate_dims(resolution: Tuple[int, int], world: Tuple[int, int]) -> Tuple[float, float]:
    """
    Get base cell width and height base on resolution and world dimensions
    """
    cell_width = resolution[0] / world[0]
    cell_height = resolution[1] / world[1]

    return (cell_width, cell_height)


class Game:
    """
    Manages the game
    - draws the substrate
    - handles TSG managers
    """

    def __init__(self, config: TSGConfig):
        pg.init()
        pg.display.set_caption(TITLE)
        self.config = config
        self.clock = pg.time.Clock()  # set to max FPS
        self.surface = pg.display.set_mode((self.config.resolution_w, self.config.resolution_h))
        self.cell_dims = evaluate_dims(
            (self.config.resolution_w, self.config.resolution_h),
            (self.config.world_width, self.config.world_height),
        )
        self.loop = True
        self.last_update = 0
        self.num_ticks = 0
        self.font = pg.font.SysFont("Arial", 20)
        self.stuff_manager = StuffManager(self.config, self.surface, self.cell_dims)
        self.gack_manager = GackManager(self.config, self.surface, self.cell_dims)

    def main(self):
        """
        Main entry point and set up
        """

        self.stuff_manager.place()
        self.gack_manager.place()
        while self.loop:
            self.main_loop()

        pg.quit()

    def main_loop(self):
        """
        Main loop
        - checks clock for next action tick
        - renders substrate
        - calls manager methods
        - displays number of action ticks so far
        - event handling
        """
        self.clock.tick(30)
        self.surface.fill((0, 0, 0))
        # has enough time passed to perform an action?
        do_actions = False
        now = pg.time.get_ticks() / self.config.tick_speed
        if now - self.last_update > self.config.update_period:
            do_actions = True
            self.last_update = now
            self.num_ticks += 1

        # render alternating grid
        for row in range(self.config.world_width):
            for col in range(row % 2, self.config.world_height, 2):
                rect = (
                    row * self.cell_dims[0],
                    col * self.cell_dims[1],
                    self.cell_dims[0],
                    self.cell_dims[1],
                )
                pg.draw.rect(self.surface, (40, 40, 40), rect)

        self.gack_manager.process(do_actions)
        self.stuff_manager.cull()
        self.stuff_manager.process(do_actions)

        tick_text = f"Tick: {self.num_ticks}"
        ren = self.font.render(tick_text, 0, (250, 240, 230), (5, 5, 5))
        self.surface.blit(ren, (10, 10))

        # handle events
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.loop = False
                case pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.loop = False
                case pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    print(pos)
        pg.display.update()


if __name__ == "__main__":
    _config = ConfigParser()
    _config.read("./config.ini")
    _tsg_config = TSGConfig(
        _config.getfloat("tsg", "update_period"),
        _config.getint("tsg", "tick_speed"),
        _config.getint("tsg", "resolution_w"),
        _config.getint("tsg", "resolution_h"),
        _config.getint("tsg", "world_width"),
        _config.getint("tsg", "world_height"),
        _config.getint("tsg", "stuff_chance"),
        _config.getint("tsg", "gack_chance"),
        _config.getint("tsg", "gack_size"),
    )
    game = Game(_tsg_config)
    game.main()
