## v0.7.0 (2023-07-10)

### Feat

- **plots**: plots script can render either life/time or ancestry
- **graph, tree**: fiddling with anscestry charts
- **plots**: add plto script - called at end of game and can be run standalone

### Fix

- update lock and requirements files
- lineage is now a set. first instance nodes gain a parent of T0

## v0.6.0 (2023-07-09)

### Feat

- **main, world**: output file with thing stats

### Fix

- **main**: use growth_period from config
- **main,world**: every 500 ticks, seed new stuff at a lower chance
- **thing**: things get hungery. if hunger above a threshold, spin
- **stuff**: stuff will eat every 3 ticks
- **main**: if no things are left, pause game

## v0.5.1 (2023-07-09)

### Fix

- try again
- versioning again
- **pyproject**: sync poetry and commitzen versions

## v0.5.0 (2023-07-09)

### Feat

- **main,world**: stats for living items, display in game
- **thing**: things new use energy when the move, and they age. if the energy is over 60, they will spawn a new thing in the next free cell. they can die

### Fix

- update lock and requirements files
- **stuff**: stuff ages after all actions are prcocessed
- **thing**: baseline lifespan and spawn threshold. on spawn parent thing looses half energy. child gets default
- **config**: config cahnces are now probabilites
- **thing**: on move, after checking for another thing, check if we are headed into gack, if so, spin
- **stuff**: after a stuff is placed, check if it in gack, if so, die

## v0.4.0 (2023-07-08)

### Feat

- new `world` entity manager. reworked everthing to suit.

## v0.3.0 (2023-07-08)

### Feat

- **main**: all tsg items up and running
- **main**: init thing manager.
- **things**: add simple thing and thing manager
- add gack and gack manager. add to config. typing

### Fix

- update lock and requirements files
- **base_manager**: simplify get_next_free_cell to use get_facing_cell. sanitise var names
- **base_manager**: rework, add `get_faceing_cell`. TODO: convert ot world_manager

## v0.2.0 (2023-07-02)

### Feat

- split code into files, add config file

## v0.1.0 (2023-07-02)

### Feat

- **main**: Stuff live, spawn and die
- **main.py**: split stuff management into new class. add tick counter
- **main**: draw grid, randomly place stuff. draw stuff and boost enery per action tick. TODO: spawn new stuff

### Fix

- update lock and requirements files
