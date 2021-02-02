#!/usr/bin/env python3
import yaml
import argparse
from cbs.LucadParser import parse_lucad
from LucadAnimation import LucadAnimation
from Animation import Animation


def main_origin():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map")
    parser.add_argument("schedule", help="schedule for agents")
    parser.add_argument('--video', dest='video', default=None,
                      help="output video file (or leave empty to show on screen)")
    parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
    args = parser.parse_args()

    with open(args.map) as map_file:
        map = yaml.load(map_file, Loader=yaml.FullLoader)

    with open(args.schedule) as states_file:
        schedule = yaml.load(states_file, Loader=yaml.FullLoader)

    animation = Animation(map, schedule)

    if args.video:
        animation.save(args.video, args.speed)
    else:
        animation.show()


def main_lucad():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map")
    parser.add_argument("agents", help="input file containing agent initial position and goal position")
    parser.add_argument("schedule", help="schedule for agents")
    parser.add_argument('--video', dest='video', default=None,
                      help="output video file (or leave empty to show on screen)")
    parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
    args = parser.parse_args()

    points, edges = parse_lucad(args.map)

    with open(args.agents) as agents_file:
        agents = yaml.load(agents_file, Loader=yaml.FullLoader)

    with open(args.schedule) as states_file:
        schedule = yaml.load(states_file, Loader=yaml.FullLoader)

    animation = LucadAnimation(points, edges, agents, schedule)

    if args.video:
        animation.save(args.video, args.speed)
    else:
        animation.show()


if __name__ == "__main__":
  main_lucad()
