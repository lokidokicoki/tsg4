"""
TSG4 - a little life simulation
"""
from configparser import ConfigParser
from typing import List, Tuple

import pygame as pg

import plots
from tsg import Dims, TSGConfig, World

TITLE = "TSG4"


def evaluate_dims(resolution: Tuple[int, int], world: Tuple[int, int]) -> Dims:
    """
    Get base cell width and height base on resolution and world dimensions
    """
    return Dims(resolution[0] / world[0], resolution[1] / world[1])


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
        self.paused = False
        self.last_update = 0
        self.num_ticks = 0
        self.font = pg.font.SysFont("Arial", 20)
        self.world = World(self.config, self.surface, self.cell_dims)
        self.log_stats: List[str] = ["tick,Tmx,Live"]

    def main(self):
        """
        Main entry point and set up
        """

        self.world.place()
        while self.loop:
            self.main_loop()

        ancestry: List[str] = []
        for element in self.world.lineages:
            ancestry.append(f"{element[0]}, {element[1]}")
        with open("ancestry.csv", mode="w", encoding="utf-8") as csv:
            csv.write("\n".join(ancestry))

        with open("tsg.csv", mode="w", encoding="utf-8") as csv:
            csv.write("\n".join(self.log_stats))

        plots.draw_plot()

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
        if self.world.stats["T"] == 0:
            self.paused = True

        if not self.paused:
            self.clock.tick(30)
            self.surface.fill((0, 0, 0))
            # has enough time passed to perform an action?
            do_actions = False
            now = pg.time.get_ticks() / self.config.tick_speed
            if now - self.last_update > self.config.update_period:
                do_actions = True
                self.last_update = now
                self.num_ticks += 1

                if self.num_ticks % self.config.growth_period == 0:
                    self.world.growth_season()

            # render alternating grid
            for row in range(self.config.world_width):
                for col in range(row % 2, self.config.world_height, 2):
                    rect = (
                        row * self.cell_dims.w,
                        col * self.cell_dims.h,
                        self.cell_dims.w,
                        self.cell_dims.h,
                    )
                    pg.draw.rect(self.surface, (40, 40, 40), rect)

            self.world.cull()
            self.world.process(do_actions)
            self.log_stats.append(
                f"{self.num_ticks},{self.world.stats['Tmx']},{self.world.stats['T']}"
            )

            tick_text = f"Tick: {self.num_ticks}"
            stat_text = f"Live: {self.world.stats}"
            total_text = f"All:  {self.world.counters}"
            ren = self.font.render(tick_text, 0, (250, 240, 230), (5, 5, 5))
            self.surface.blit(ren, (10, 10))
            ren = self.font.render(stat_text, 0, (250, 240, 230), (5, 5, 5))
            self.surface.blit(ren, (10, 30))
            ren = self.font.render(total_text, 0, (250, 240, 230), (5, 5, 5))
            self.surface.blit(ren, (10, 50))

        # handle events
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.loop = False
                case pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.loop = False
                    elif event.key == pg.K_SPACE:
                        self.paused = not self.paused
                case pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    self.world.dump_cell_contents(pos)
        pg.display.update()


if __name__ == "__main__":
    _config = ConfigParser()
    _config.read("./config.ini")
    _tsg_config = TSGConfig(
        _config.getfloat("tsg", "update_period"),
        _config.getint("tsg", "growth_period"),
        _config.getint("tsg", "tick_speed"),
        _config.getint("tsg", "resolution_w"),
        _config.getint("tsg", "resolution_h"),
        _config.getint("tsg", "world_width"),
        _config.getint("tsg", "world_height"),
        _config.getfloat("tsg", "stuff_chance"),
        _config.getfloat("tsg", "gack_chance"),
        _config.getint("tsg", "gack_size"),
        _config.getfloat("tsg", "thing_chance"),
    )
    game = Game(_tsg_config)
    game.main()
