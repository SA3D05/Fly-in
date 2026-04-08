test = {
    "hub": [
        {"name": "waypoint1", "x": 1, "y": 0, "matadata": {"color": "blue"}},
        {"name": "waypoint2", "x": 2, "y": 0, "matadata": {"color": "blue"}},
    ],
    "connection": [
        {"from": "start", "to": "waypoint1"},
        {"from": "waypoint1", "to": "waypoint2"},
        {"from": "waypoint2", "to": "goal"},
        {
            "from": "gate_hell4",
            "to": "gate_hell5",
            "metadata": {"max_link_capacity": "1"},
        },
    ],
    "nb_drones": 2,
    "start_hub": {"name": "start", "x": 0, "y": 0, "matadata": {"color": "green"}},
    "end_hub": {"name": "goal", "x": 3, "y": 0, "matadata": {"color": "red"}},
}
