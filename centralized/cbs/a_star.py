"""

AStar search

author: Ashwin Bose (@atb033)

"""
from datetime import datetime
import time


class AStar():
    def __init__(self, env):
        self.agent_dict = env.agent_dict
        self.admissible_heuristic = env.admissible_heuristic
        self.is_at_goal = env.is_at_goal
        self.get_neighbors = env.get_neighbors
        self.cost = env.cost

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def search(self, agent_name):
        """
        low level search 
        """
        print('%s searching path for %s from %s to %s' % (datetime.now(), agent_name, self.agent_dict[agent_name]["start"], self.agent_dict[agent_name]["goal"]))
        initial_state = self.agent_dict[agent_name]["start"]
        step_cost = 1
        # print('initial state is %s' % initial_state)
        
        closed_set = set()
        open_set = {initial_state}

        came_from = {}

        g_score = {} 
        g_score[initial_state] = 0

        f_score = {} 

        f_score[initial_state] = self.admissible_heuristic(initial_state, agent_name)

        while open_set:
            temp_dict = {open_item: f_score.setdefault(open_item, float("inf")) for open_item in open_set}
            # print('temp dict is %s' % temp_dict)
            current = min(temp_dict, key=temp_dict.get)
            # print('astar current is %s' % current)

            if self.is_at_goal(current, agent_name):
                print('%s path found for %s' % (datetime.now(), agent_name))
                return self.reconstruct_path(came_from, current)

            open_set -= {current}
            closed_set |= {current}

            neighbor_list = self.get_neighbors(current)
            # print('%s neighbors:%s' % (datetime.now(), [state.location.name for state in neighbor_list]))

            for neighbor in neighbor_list:
                #print('%s neighbor %s' % (datetime.now(), neighbor))
                if neighbor in closed_set:
                    #print('%s neighbor already reached' % datetime.now())
                    continue
                
                tentative_g_score = g_score.setdefault(current, float("inf")) + self.cost(current.location.name, neighbor.location.name)
                #print('%s tentative g score is %s' % (datetime.now(), tentative_g_score))

                if neighbor not in open_set:
                    open_set |= {neighbor}
                    #print('%s neighbor not in open set, added' % datetime.now())
                elif tentative_g_score >= g_score.setdefault(neighbor, float("inf")):
                    #print('%s tentative g score is larger, continue' % datetime.now())
                    continue

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.admissible_heuristic(neighbor, agent_name)
        return False

