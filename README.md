# tsg4
"life" simulator in python - again

TSG stands for "Things, Stuff and Gack".

- Things: mobile life forms that feed on Stuff
- Stuff: sessile energy producing 'vegetation'
- Gack: environmental hazrds, similar to water or desert

The aim is to emulate a simple ecosystem where Things amble about eating Stuff (and maybe each other), avoiding/adapting to Gack and create new little Things.

The World that TSG takes place in is a grid of squares (or spaces), bounded by impenetrable walls.

We get a birds-eye view of the World and can interact with the various bits and bobs present.

The World of TSG is beset with environmental hazards whch (hopefully) exercise selection pressure on the Things.

Time passes in the world, for every 'tick' something happens.

## Stuff

Stuff grows on the substrate of the World. It is analogous to vegetation, and it is green. It is the bottom of the food chain, and provides energy for Things.

It comes in 3 flavours:
- NoGackStuff: basic version - found where Gack isn't.
- WetGackStuff: grows in WetGack, more energy rich, but slower spawn rate that NoGackStuff.
- DryGackStuff: grown on DryGack, les energy rich, but faster spawn rate than NoGackStuff.

A Stuff instance occupies a single space. Over time, it grows to maturity simply by existing; it is pulling nutrients of some descriptiong from the World substrate modified by the Gack present.

As it grows, it gains energy. The growth rate is 1 energy per 4 ticks, modified by its Gack type.

Once it reaches maturity, and it has sufficient energy, a Stuff instnace can spawn a new Stuff instnace in a free space surrounding it. It there is no free space, the Stuff instance dies.

Stuff has a base life span of many ticks (TBD but start at 100) modified by a LifeSpan factor (TBD).

If a Stuff is consumed by a Thing, it will be left with 1 energy and continue to grow, a bit like how grass survives being eaten by sheep.

## Gack

Gack represents different hazards in the World. Gack is immobile and potentially impenetrable to Things. 

It comes in 3 flavours:
- WetGack: its blue and wet. WetGackStuff grows here. Reduces movement rate.
- DryGack: its yellow and hot. DryGackStuff grows here. Increase energy cost to move.
- BadGack: its red and spicy. No Stuff grows here. Mutagenic. Rare.

Things have their Factors jumbled, and can acquire Traits, through spawning or coming into contact with BadGack.

## Things

Things are critters, gribblies, or creatures. They are move around the world and (initially) can only eat Stuff and spawn new Things. 

They have a single eye with a 90 degree viewing angle and can see at least 1 space ahead of them. This allows them to decide where to go.

Things gain energy as when they eat Stuff (and potentially other Things), this energy powers their movement and spawning.

### Stats

Things have Stats, these come in 2 forms, Base and Live (calculated from Base and Factors). 

The BaseStats are as follows:
- name: randomly allocated identifier
- energy: gained by eating, used in moving and spawning
- speed: how many squares can a Thing move
- age: number of ticks the Thign has existed for
- lineage: if a spawned Thing, this holds the parent(s) and spawn type
- spawn threshold: energy level require to spawn
- hunger: if a Thing hasn't eaten, this will go up, causes a Thing to Spin
- lifespan: how long a Thing can live for before it dies of natural causes.

### Factors

Things have Factors (think: genes) that modify their interactions with the World and can confer new Traits:
- DriftFactor: affects child Thing Factors during spawning
- SpeedFactor: affects spped atwhich a Thing can move
- SpinFactor: affects the direction a Thing will choose when it has to Spin
- SpawnFactor: affects spawn threshold - spawn earlier or later.
- LafeFactor: affects maximum lifespan.
- FissionFactor: affects when a Thing will spawn by Fission
- FusionFactor: affects when a Thing will spawn by Fusion
- HungerFactor: affects hunger - may allow Thing to travel further without food
- No/Wet/DryGackFactor: affect how well a Thing can tolerate a Gack type.
- ThingFactor: affects how a Thing feels about other Things, friend or food?
- StuffFactor: affects how a Thing feels about Stuff, food or bleurgh?

### Traits

Traits determine the actions a Thing will take, what Gack types it prefers and food preferences etc.
Traits are binary and are decided when a LiveStat reaches a certain limit (TBD)

- No/Wet/DryGackTrait: which Gack type the Things prefers to inhabit.
- ThingTrait: whether a Thing prefers to eat Things
- StuffTrait: whether a Thing likes to eat Stuff
- FissionTrait: whether a Thing prefers to spawn by Fission
- FusionTrait: whether a Thing prefers to spawn by Fusion






