# SkyGraph

A Python + Pygame project that simulates and visualizes multiple drones
traveling across a network of hubs and bidirectional connections. The
simulator reads simple map configuration files, enforces hub/connection
capacities and zone rules, computes minimal-cost routes and animates the
movement of drones from a start hub to an end hub.

## Goal

The goal of this project is to provide a compact, educational tool to:
- Demonstrate routing and capacity constraints in a graph-like network.
- Visualize how simple rules (zones, capacities, priorities) affect paths.
- Provide an interactive playground for experimenting with different map
	configurations and drone counts.

## What it solves

SkyGraph helps explore how constrained resources (hub capacity and link
capacity) and zone costs influence path selection and throughput. It's
useful for learning algorithms, visual debugging of routing logic, or
demonstrating scheduling and congestion effects in a networked environment.

## Quick start

Requirements:
- Python 3.10+
- pygame (install with `pip install pygame`)

Run the simulator with a map file from the `maps/` directory:

```bash
python main.py maps/simple_fork.txt
```

Controls:
- Use the side menu (or keyboard): Arrow keys to navigate, `Enter` to
	activate a button.
- Menu options: `Start`, `Backward`, `Forward`, `Restart`, `Exit`.
- Press `q` to quit at any time.

## Map file format

Map files are plain text. Each meaningful line uses the form `key: value`.
Supported entries:

- `nb_drones: N` — number of drones to simulate (must appear before hubs).
- `start_hub: NAME X Y [metadata]` — define the start hub.
- `hub: NAME X Y [metadata]` — define a regular hub.
- `end_hub: NAME X Y [metadata]` — define the end hub.
- `connection: A-B [max_link_capacity=K]` — connect hub `A` and `B`.

Metadata for hubs (optional, placed inside square brackets):
- `color=COLOR` — pygame color name or `rainbow` for cycling colors.
- `zone=restricted|normal|blocked|priority` — affects traversal cost.
- `max_drones=K` — maximum drones allowed concurrently in that hub.

Example map snippet:

```
nb_drones: 3
start_hub: S 0 0 [color=green]
hub: A 10 0
hub: B 20 0 [zone=restricted max_drones=1]
end_hub: E 30 0
connection: S-A
connection: A-B [max_link_capacity=1]
connection: B-E
```

See the included `maps/` directory for full example maps and edge cases.

## Project layout

- `main.py` — program entry point and basic argument handling.
- `parser.py` — parses map files and validates configuration.
- `models.py` — `Hub`, `Connection`, `MapData`, and `Drone` data classes.
- `algo.py` — `Simulator` logic: graph building, path selection, and
	simulation stepping.
- `display.py` — Pygame-based rendering and UI loop.
- `interface.py` — menu and UI component layout.
- `maps/` — example map files used for testing and demonstration.

## Troubleshooting
- If the program exits with parsing errors, check the indicated map file
	and line for formatting issues (missing fields, invalid numbers, or
	unknown metadata values).
- Ensure `assets/` contains `font.ttf`, `hub.png` and `drone.png` used by
	the renderer.
