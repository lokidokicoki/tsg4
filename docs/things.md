# Things

Things are critters, gribblies, or creatures. They are move around the world and (initially) can only eat Stuff and spawn new Things.

They have a single eye with a 90 degree viewing angle and can see at least 1 space ahead of them. This allows them to decide where to go.

Things gain energy as when they eat Stuff (and potentially other Things), this energy powers their movement and spawning.

## Stats

Things have Stats, these come in 2 forms, Base and Live (calculated from Base and Factors).

The BaseStats are as follows:

- name: randomly allocated identifier
- energy: gained by eating, used in moving and spawning, has a maximum value (TBD). If it drop to 0, the Thing is dead and removed from the World.
- speed: how many squares can a Thing move
- age: number of ticks the Thing has existed for
- lineage: if a spawned Thing, this holds the parent(s) and spawn type
- spawn threshold: energy level require to spawn
- lifespan: how long a Thing can live for before it dies of natural causes.

## Factors

Things have Factors (think: genes) that modify their interactions with the World and can confer new Traits:

- DriftFactor: affects child Thing Factors during spawning
- SpeedFactor: affects speed at which a Thing can move
- SpinFactor: affects the direction a Thing will choose when it has to Spin
- SpawnFactor: affects spawn threshold - spawn earlier or later.
- FeedFactor: affects how much energy is gained from feeding
- LifeFactor: affects maximum lifespan.
- FissionFactor: affects when a Thing will spawn by Fission
- FusionFactor: affects when a Thing will spawn by Fusion
- HungerFactor: affects the urge to eat
- No/Wet/DryGackFactor: affect how well a Thing can tolerate a Gack type.
- ThingFactor: affects how a Thing feels about other Things, friend or food?
- StuffFactor: affects how a Thing feels about Stuff, food or bleurgh?

## Traits

Traits determine the actions a Thing will take, what Gack types it prefers and food preferences etc.
Traits are binary and are decided when a LiveStat reaches a certain limit (TBD)

- No/Wet/DryGackTrait: which Gack type the Things prefers to inhabit.
- ThingTrait: whether a Thing prefers to eat Things
- StuffTrait: whether a Thing likes to eat Stuff
- FissionTrait: whether a Thing prefers to spawn by Fission
- FusionTrait: whether a Thing prefers to spawn by Fusion

## Spawning

Spawning is how Things propagate. There are two methods of spawning, Fission and Fusion.

### Fission

Fission is when a Thing divides in two. This occurs under the following conditions:

- if the FissionTrait is positive.
- if has sufficient energy to spawn (energy \* SpawnFactor) > spawn threshold
- is not in contact with a Thing in its surrounding spaces

Fission produces a child with the following:

**BaseStats**

- name: new random name
- energy: 1/2 of the parent Thing rounded down
- speed: same as parent
- age: set to 0
- lineage: 'parent lineage => parent name'
- spawn threshold: same as parent
- lifespan: same as parent

**Factors**

The Factors may be modified in a random direction by the parent DriftFactor

For each factor of the parent, drift occurs when a random number between 0 and 1 is greater that the DriftFactor.
This will result in the DriftFactor being either added or subtracted from the parent Factor. This value is then applied to the child Thing.

**Traits**

The child will have its Traits recalculated from the LiveStats.

### Fusion

Fusion is when two Things fuse to produce two new offspring. After Fusion, the parent Things go their merry ways. Fusion occurs under the following conditions:

- if both Things FusionTraits are positive.
- if both Things have the same ThingTrait.
- if both Things have sufficient enrgy to spawn (energy \* spawnFactor) > spawn threshold
- if both Things are touching, i.e. are in each others surrounding squares.

Fusion produces two child Things with the following stats:

**BaseStats**

- name: new random name
- energy: 1/4 of the sum of parents energy rounded down
- speed: average of parents
- age: set to 0
- lineage: 'parent lineage => parent name 1 + parent name 2'
- spawn threshold: average of parents
- lifespan: average of parents

**Factors**

The Factors are randomly picked from the parents, and maybe modified in a random direction by the other parent DriftFactor, use opposite values for the other child.

**Traits**

The child will have its Traits recalculated from the LiveStats.

## Feeding

Things will want to eat when their energy goes below a limit. That limit is the max energy modified by the Thing's HungerFactor.

If a Thing is on a square with some Stuff it will eat the Stuff under this conditions:

- it has the StuffTrait,
- it is hungry
  The Thing will gain the total Stuff energy -1 modified by the FeedFactor rounded down.

If a Thing is on a square next to another Thing (directly in front of it) and it has the ThingTrait, it will eat the other Thing.
The Thing will gain the prey Things energy modified by the FeedFactor rounded down. The prey Ting is dead and will be removed from the World.

## Senses

Things can see the square directly in front of them, according to their last direction of travel.

## Movement

Things can move in one of 8 directions. The initial move direction is randomly picked.
Things move at the speed of 1 square per tick, this is modified by their SpeedFactor rounded down.
Moving depletes the Things energy at 1 energy per square modfied by the SpeedFactor rounded up.
Things will continue to move in the same direction until they hit an obstacle (such as the edge of the World, or some Gack they are intolerant of) or they decide to spin (choose a new random direction modified by SpinFactor) due to hunger.
Things can only move into a square not occupied by another Thing, this will cause them to spin.
