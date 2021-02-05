from a_star import AStar
from LucadLocation import Location
from State import State
from Conflict import Conflict
from EdgeConstraint import EdgeConstraint
from VertexConstraint import VertexConstraint
from Constraints import Constraints
from math import fabs
from itertools import combinations
from decimal import Decimal
from Dijkstra import Dijkstra
import ast


class LucadEnvironment(object):
    def __init__(self, graph, agents):
        self.graph = graph
        self.min_cost_path_table = dict()
        with open('min_cost_table', 'r') as f:
            data = f.read()
            if data != '':
                self.min_cost_path_table = ast.literal_eval(data)
        if len(self.min_cost_path_table.keys()) == 0:
            dj = Dijkstra(graph)
            dj.traverse()
            self.min_cost_path_table = dj.paths
            with open('min_cost_table', 'w') as f:
                f.write(str(self.min_cost_path_table))

        self.agents = agents
        self.agent_dict = {}
        self.make_agent_dict()

        self.constraints = Constraints()
        self.constraint_dict = {}

        self.a_star = AStar(self)

    def get_neighbors(self, state):
        neighbors = []

        # TODO
        # 应该怎么处理time step,究竟是按照根据路线长度推算的时间(length / speed)来
        # 还是将每次运动的time step都视为1处理
        # 如果按照推算时间来,等待这个动作应该等待多久? 地图中最长路线的行驶时间?地图路线平均长度/速度?
        # 我觉得按照推算时间来可以作为优化方向
        # 现在先按照每次加1处理好了

        # Wait
        n = State(state.time + 1, state.location)
        if self.state_valid(n):
            neighbors.append(n)

        # neighbors in the graph
        for neighbor in self.graph.neighbors(state.location.name):
            # neighbor is actually path
            n = State(state.time + 1, Location(neighbor.end))
            if self.state_valid(n) and self.transition_valid(state, n):
                neighbors.append(n)
        return neighbors

    def cost(self, start, end):
        return self.graph.cost(start, end)

    def get_first_conflict(self, solution):
        max_t = max([len(plan) for plan in solution.values()])
        result = Conflict()
        for t in range(max_t):
            for agent_1, agent_2 in combinations(solution.keys(), 2):
                state_1 = self.get_state(agent_1, solution, t)
                state_2 = self.get_state(agent_2, solution, t)
                if state_1.is_equal_except_time(state_2):
                    result.time = t
                    result.type = Conflict.VERTEX
                    result.location_1 = state_1.location
                    result.agent_1 = agent_1
                    result.agent_2 = agent_2
                    return result

            for agent_1, agent_2 in combinations(solution.keys(), 2):
                state_1a = self.get_state(agent_1, solution, t)
                state_1b = self.get_state(agent_1, solution, t + 1)

                state_2a = self.get_state(agent_2, solution, t)
                state_2b = self.get_state(agent_2, solution, t + 1)

                if state_1a.is_equal_except_time(state_2b) and state_1b.is_equal_except_time(state_2a):
                    result.time = t
                    result.type = Conflict.EDGE
                    result.agent_1 = agent_1
                    result.agent_2 = agent_2
                    result.location_1 = state_1a.location
                    result.location_2 = state_1b.location
                    return result
        return False

    def create_constraints_from_conflict(self, conflict):
        constraint_dict = {}
        if conflict.type == Conflict.VERTEX:
            v_constraint = VertexConstraint(conflict.time, conflict.location_1)
            constraint = Constraints()
            constraint.vertex_constraints |= {v_constraint}
            constraint_dict[conflict.agent_1] = constraint
            constraint_dict[conflict.agent_2] = constraint

        elif conflict.type == Conflict.EDGE:
            constraint1 = Constraints()
            constraint2 = Constraints()

            e_constraint1 = EdgeConstraint(conflict.time, conflict.location_1, conflict.location_2)
            e_constraint2 = EdgeConstraint(conflict.time, conflict.location_2, conflict.location_1)

            constraint1.edge_constraints |= {e_constraint1}
            constraint2.edge_constraints |= {e_constraint2}

            constraint_dict[conflict.agent_1] = constraint1
            constraint_dict[conflict.agent_2] = constraint2

        return constraint_dict

    def get_state(self, agent_name, solution, t):
        if t < len(solution[agent_name]):
            return solution[agent_name][t]
        else:
            return solution[agent_name][-1]

    def state_valid(self, state):
        return str(state.location.name) in self.graph.points.keys() \
            and VertexConstraint(state.time, state.location) not in self.constraints.vertex_constraints

    def transition_valid(self, state_1, state_2):
        return EdgeConstraint(state_1.time, state_1.location, state_2.location) not in self.constraints.edge_constraints

    def is_solution(self, agent_name):
        pass

    def admissible_heuristic(self, state, agent_name):
        # goal = self.agent_dict[agent_name]['goal']
        # points = self.graph.points
        # try:
        #     start_x = Decimal(points[str(state.location.name)].x)
        #     start_y = Decimal(points[str(state.location.name)].y)
        #     goal_x = Decimal(points[str(goal.location.name)].x)
        #     goal_y = Decimal(points[str(goal.location.name)].y)
        # except Exception as e:
        #     print(e)
        # return fabs(start_x - goal_x) + fabs(start_y - goal_y)
        goal = self.agent_dict[agent_name]['goal']
        if state.is_equal_except_time(goal):
            return 0
        if state.location.name in self.min_cost_path_table.keys() and \
            goal.location.name in self.min_cost_path_table[state.location.name].keys():
            return self.min_cost_path_table[state.location.name][goal.location.name]['cost']
        else:
            print('some thing goes wrong')


    def is_at_goal(self, state, agent_name):
        goal_state = self.agent_dict[agent_name]['goal']
        return state.is_equal_except_time(goal_state)

    def make_agent_dict(self):
        for agent in self.agents:
            start_state = State(0, Location(agent['start']))
            goal_state = State(0, Location(agent['goal']))

            self.agent_dict.update({agent['name']: {'start': start_state, 'goal': goal_state}})

    def compute_solution(self):
        solution = {}
        for agent in self.agent_dict.keys():
            self.constraints = self.constraint_dict.setdefault(agent, Constraints())
            local_solution = self.a_star.search(agent)
            if not local_solution:
                return False
            solution.update({agent: local_solution})
        return solution

    def compute_solution_cost(self, solution):
        return sum([len(path) for path in solution.values()])










