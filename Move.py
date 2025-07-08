
LOCATIONS = {
    1: {
        "description": "Hooker Street. Someone actually named it that...",
        "monster": None
    },
    2: {
        "description": "Lincoln Car Wash. If you owned a car, it would definitely be dirty!",
        "monster": {
            "type": " delinquent",
            "strength": 5,
            "speed": 2,
            "weapon": "an empty vape",
            "hitpoints": 8,
            "max_hitpoints": 8,
            "is_alive": True
        },
    },
    3: {
        "description": "Taco Factory. I can't wait until Tuesday.",
        "monster": {
            "type": "n American Expat",
            "strength": 7,
            "speed": 1,
            "weapon": "voter's remorse",
            "hitpoints": 12,
            "max_hitpoints": 12,
            "is_alive": True
        },
    },
    4: {
        "description": "Historical Museum. :yawn:",
        "monster": {
            "type": " Torontonian",
            "strength": 5,
            "speed": 1,
            "weapon": "disdain for anything not GTA, and even then...",
            "hitpoints": 8,
            "max_hitpoints": 8,
            "is_alive": True
        },
    },
    5: {
        "description": "The Rex Hotel. In the distance, a dog barks.",
        "monster": {
            "type": " Rogers Saleskid",
            "strength": 4,
            "speed": 3,
            "weapon": "improbable promises",
            "hitpoints": 6,
            "max_hitpoints": 6,
            "is_alive": True
        }
    }

}

NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"

MAP_CONNECTIONS = {
    # From Location 1 (Hooker Street - SW / Start)
    1: {NORTH: 2},  # Only N from here

    # From Location 2 (Lincoln Car Wash - NW)
    2: {NORTH: 3, EAST:5, SOUTH: 1},

    # From Location 3 (Taco Factory - North of 2)
    3: {SOUTH: 2, EAST: 4},  # Can go South back to 2, East to 4

    # From Location 4 (Historical Museum - East of 3)
    4: {WEST: 3, SOUTH: 5},  # Can go West back to 3 or South to 5

    # From Location 5 (The Rex Hotel - SE)
    5: {NORTH: 4, WEST: 2}  # User can go North to 4, or West to 1
}


