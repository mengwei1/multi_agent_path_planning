import matplotlib
import pickle
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from decimal import Decimal

Colors = ['orange', 'blue', 'green']


class LucadAnimation:
    def __init__(self, points, edges, agents, schedule):
        self.points = points
        self.edges = edges
        self.agents = agents
        self.schedule = schedule
        self.combined_schedule = {}
        self.combined_schedule.update(self.schedule['schedule'])

        self.fig = plt.figure(frameon=False)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)

        self.agents = dict()
        self.agent_names = dict()
        self.patches = []
        self.artists = []

        self.T = 0

        for d, i in zip(agents['agents'], range(0, len(agents['agents']))):
            goal_x = self.points[str(d['goal'])].x
            goal_y = self.points[str(d['goal'])].y
            self.patches.append(Rectangle((float(goal_x), float(goal_y)), 0.5, 0.5, facecolor=Colors[0], edgecolor='black', alpha=0.5))

        for d, i in zip(agents["agents"], range(0, len(agents["agents"]))):
            self.T = max(self.T, schedule["schedule"][d['name']][-1]["t"])
            name = d['name']
            start_x = self.points[str(d['start'])].x
            start_y = self.points[str(d['start'])].y
            self.agents[name] = Circle((float(start_x), float(start_y)), 0.3, facecolor=Colors[0], edgecolor='black')
            self.agents[name].original_face_color = Colors[0]
            self.patches.append(self.agents[name])

            self.agent_names[name] = self.ax.text(float(start_x), float(start_y), name.replace('agent', ''))
            self.agent_names[name].set_horizontalalignment('center')
            self.agent_names[name].set_verticalalignment('center')
            self.artists.append(self.agent_names[name])

        self.init_plt()
        print('starting animation, total frame is %s' % self.T)
        self.anim = animation.FuncAnimation(self.fig, self.animate,
                                            init_func=self.init_func,
                                            frames=int(self.T + 1) * 10,
                                            interval=10,
                                            blit=True)

    def init_func(self):
        print('init_func')
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)
        return self.patches + self.artists

    def animate(self, i):
        for agent_name, agent in self.combined_schedule.items():
            pos = self.get_state(i / 10, agent)
            p = (pos[0], pos[1])
            self.agents[agent_name].center = p
            self.agent_names[agent_name].set_position(p)

        for _, agent in self.agents.items():
            agent.set_facecolor(agent.original_face_color)

        agents_array = [agent for _, agent in self.agents.items()]
        for i in range(0, len(agents_array)):
            for j in range(i + 1, len(agents_array)):
                d1 = agents_array[i]
                d2 = agents_array[j]
                pos1 = np.array(d1.center)
                pos2 = np.array(d2.center)
                if np.linalg.norm(pos1 - pos2) < 0.7:
                    d1.set_facecolor('red')
                    d2.set_facecolor('red')
                    print("COLLISION! (agent-agent) ({}, {})".format(i, j))
                    exit()
        return self.patches + self.artists

    def get_state(self, t, d):
        idx = 0
        while idx < len(d) and d[idx]["t"] < t:
            idx += 1
        if idx == 0:
            return np.array([float(self.points[d[0]['position']].x), float(self.points[d[0]['position']].y)])
        elif idx < len(d):
            posLast = np.array([float(self.points[d[idx - 1]['position']].x), float(self.points[d[idx - 1]['position']].y)])
            posNext = np.array([float(self.points[d[idx]['position']].x), float(self.points[d[idx]['position']].y)])
        else:
            return np.array([float(self.points[d[-1]['position']].x), float(self.points[d[-1]['position']].y)])
        dt = d[idx]["t"] - d[idx - 1]["t"]
        t = (t - d[idx - 1]["t"]) / dt
        pos = (posNext - posLast) * t + posLast
        return pos

    def init_plt(self):
        for point in self.points.values():
            plt.scatter([Decimal(point.x)], [Decimal(point.y)], color='b')

        for point in self.edges.keys():
            for edge in self.edges[point]:
                start_x = Decimal(self.points[edge.start].x)
                start_y = Decimal(self.points[edge.start].y)
                end_x = Decimal(self.points[edge.end].x)
                end_y = Decimal(self.points[edge.end].y)
                plt.plot([start_x, end_x], [start_y, end_y], color='r')

    def show(self):
        plt.show()
