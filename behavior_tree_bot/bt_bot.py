#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    close_plan = Selector(name='Close Planet Strategy')
    
    close_spread_sequence = Sequence(name='Close Spread Strategy')
    close_neutral_planet_check = Check(if_close_neutral_planet_available)
    close_spread_action = Action(spread_to_close_weakest_neutral_planet)

    close_attack_sequence = Sequence(name='Close Attack Strategy')
    close_enemy_planet_check = Check(if_close_weak_enemy_planet)
    close_attack_action = Action(attack_close_weakest_enemy_planet)

    close_plan.child_nodes = [close_spread_sequence, close_attack_sequence]
    close_spread_sequence.child_nodes = [close_neutral_planet_check, close_spread_action]
    close_attack_sequence.child_nodes = [close_enemy_planet_check, close_attack_action]

    far_plan = Sequence(name='Far Planet Strategy')

    far_spread_sequence = Sequence(name='Far Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    far_spread_action = Action(spread_to_weakest_neutral_planet)

    far_attack_sequence = Sequence(name='Far Attack Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)

    far_plan.child_nodes = [far_spread_sequence, far_attack_sequence]
    far_spread_sequence.child_nodes = [neutral_planet_check, far_spread_action]
    far_attack_sequence.child_nodes = [largest_fleet_check, attack]
    
    root.child_nodes = [close_plan, far_plan, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
