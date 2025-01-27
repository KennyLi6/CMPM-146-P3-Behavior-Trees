import logging

MAX_DISTANCE = 10

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_close_neutral_planet_available(state):
    # Don't bother checking if no neutral planets
    if not if_neutral_planet_available(state):
        return False

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet:
        return False
    # Find all planets that are within MAX_DISTANCE
    close_planets = [p for p in state.neutral_planets() if state.distance(strongest_planet.ID, p.ID) < MAX_DISTANCE]

    if len(close_planets) < 1:
        # No legal source or destination
        return False
    else:
        # Can spread to a close neutral planet
        return True

def if_close_weak_enemy_planet(state):
    if not have_largest_fleet(state):
        return False
    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet:
        return False
    # Find all planets that are within MAX_DISTANCE
    close_planets = [p for p in state.enemy_planets() if state.distance(strongest_planet.ID, p.ID) < MAX_DISTANCE]

    if len(close_planets) < 1:
        # No legal source or destination
        return False
    else:
        # Can attack close enemy planet
        return True

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

