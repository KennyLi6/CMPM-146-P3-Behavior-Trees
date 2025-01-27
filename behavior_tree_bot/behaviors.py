import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

close_distance = 8

def attack_weakest_enemy_planet(state):
    enemy_planets = [planet for planet in state.enemy_planets()
                  if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(enemy_planets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        required_ships = weakest_planet.num_ships + \
                                 state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)


def spread_to_weakest_neutral_planet(state):
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(neutral_planets, key=lambda p: p.num_ships, default=None)



    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        required_ships = weakest_planet.num_ships + \
                                 state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)


def spread_to_close_weakest_neutral_planet(state):
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find all close netural planets
    available_planets = []
    neutral_planets = [planet for planet in state.neutral_planets()
                  if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for planet in neutral_planets:
        if state.distance(planet.ID, strongest_planet.ID) < close_distance:
            available_planets.append(planet)
    
    # (4) Find the weakest neutral close planet.
    weakest_planet = min(available_planets, key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        required_ships = weakest_planet.num_ships + \
                                 state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        # (5) Send the required ships + 1 from my strongest planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)
    

def attack_close_weakest_enemy_planet(state):
    enemy_planets = [planet for planet in state.enemy_planets()
                  if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find all close enemy planets
    available_planets = []
    for planet in enemy_planets:
        if state.distance(planet.ID, strongest_planet.ID) < close_distance:
            available_planets.append(planet)
    
    # (4) Find the weakest enemy close planet.
    weakest_planet = min(available_planets, key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        required_ships = weakest_planet.num_ships + \
                                 state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        # (5) Send the required ships + 50% from my strongest planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)