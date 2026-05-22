*This project has been created as part of the 42 curriculum by satifi.*

# Description

Fly-in is a simulation and visualization project that models multiple drones moving across a graph of hubs connected by links. The goal is to route a configurable number of drones from a designated start hub to a designated end hub while respecting hub capacities, link capacities, and zone-based traversal rules.

The program parses map file, computes best routes, and animates the drones using pygame to help visualize routing decisions and capacity constraints.


# Features

- Parser for human-readable map files describing hubs, connections and metadata (colors, zones, capacities).
- Path selection preferring minimal cost routes (costs depend on `ZoneType`).
- Step-by-step simulation with replay support (backward/forward stacks).
- Pygame-based visualization with hub sprites, drone sprites, animated color modes and a side menu for simple controls.

# Algorithm choices and implementation strategy

Overview:
- Graph representation: The map is loaded into a `MapData` container (hubs + connections). `Simulator` builds an adjacency list where edges are assigned traversal costs depending on the destination hub's `ZoneType`.

Path computation:
- Current approach (implemented in `Simulator.init_path()`): enumerate all simple paths from the `start` hub to the `end` hub using a DFS-like search, compute the total cost for each path (sum of destination node costs), and retain all paths that have the minimum total cost.

- Zone cost mapping (used in `Simulator.init_graph()`):
  - `ZoneType.NORMAL` → cost 1
  - `ZoneType.PRIORITY` → cost 0
  - `ZoneType.RESTRICTED` → cost 2
  - `ZoneType.BLOCKED` → cost -1 (treated as non-traversable)

- Rationale: enumerating all minimal-cost paths preserves multiple equally-good routes and is simple to reason about for the project scope.

Simulation strategy:
- Drones are instantiated at the start hub and moved synchronously in discrete steps via `Simulator.make_step()`.
- For each drone, `__choose_correct_path()` finds the next hub on one of the retained minimal paths; movement checks hub capacities (`Hub.can_enter()`) and link capacities (`Connection.can_pass()`).
- Restricted hubs: drones perform a half-move and occupy the connection before fully entering restricted hubs. End hubs always accept drones.
- Undo/redo: each step records drone coordinates into `backward_stack` and `forward_stack` to support stepping backward and forward in the simulation.

Implementation notes:
- The project models hubs and connections as objects (`Hub`, `Connection`) with counters used to enforce capacity rules.
- The adjacency list is created from `MapData.connections` and references `Hub` instances directly.

# Visual representation features and UX

The visualization is implemented using `pygame` and includes the following elements to improve clarity and user experience:

- Hub sprites and colorization:
  - Each hub uses a sprite image (`hub.png`) and can be colored via map metadata. A special `rainbow` color mode cycles hub colors periodically for visual interest.
  - Hub labels are rendered with the hub name and positioned to avoid overlapping by alternating offsets.

- Drone sprites and labeling:
  - Drones use a sprite (`drone.png`) and the drone id is rendered above the sprite to help track individuals.
  - Slight random jitter is applied to the drone render position to make overlapping drones easier to distinguish.

- Connections visualization:
  - Links are drawn as lines between hub centers. Connection width and color are configurable via `Config` values.

- UI and controls:
  - A side menu provides simple controls: Start, Backward, Forward, Restart, Exit.
  - Step counter and map file name are displayed for context.

How visuals help:
- Color and sprites make hubs and drones immediately identifiable.
- Animated color modes and jittered positions make congested areas and drone clusters visually apparent.
- The side menu + step control enable deterministic inspection (replay and step-wise debugging).

# Instructions

Requirements:
- Python 3.10+
- pygame

Quick setup and run (example):

```bash
make install
python main.py map_config.txt
```
# Resources

Relevant references and documentation:
- pygame documentation: https://www.pygame.org/docs/
- Graph Traversals tutorial: https://www.youtube.com/watch?v=pcKY4hjDrxk
- Edge List, Adjacency Matrix, Adjacency List, etc: https://www.youtube.com/watch?v=4jyESQDrpls&t=1592s

AI usage disclosure:
- An AI assistant (GPT-based) was used to help annotate the code with PEP 257 Google-style docstrings across the project files, and to draft this README. The AI assisted with documentation and refactoring tasks only — no production logic changes were introduced by the assistant unless explicitly requested.

# Where to look in the code

- Parser: `parser.py` — file format parsing and validation.
- Data models: `models.py` — `Hub`, `Connection`, `MapData`, `Drone`.
- Core algorithm / simulation: `algo.py` — `Simulator` (graph building, path computation, simulation steps).
- Visualization and UI: `display.py`, `interface.py` — pygame rendering and menu components.
- Configuration constants: `enums.py`.
