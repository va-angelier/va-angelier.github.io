import time, random
from robot.domain.models import Waypoint, Environment
from robot.services.planning import AStarPlanner, RRTPlanner, GreedyPlanner # adjust imports to your repo
from statistics import mean

def make_env(obstacles=30, size=20):
    env = Environment()
    env.obstacles = []
    while len(env.obstacles) < obstacles:
        env.obstacles.append((random.randrange(size), random.randrange(size)))
    return env

def bench(planner, trials=20, size=20):
    env = make_env(obstacles=size, size=size)
    times, solved = [], 0
    for _ in range(trials):
        s = Waypoint(0, 0); t = Waypoint(size-1, size-1)
        t0 = time.perf_counter()
        path = planner.compute(s, t, env)
        times.append(time.perf_counter() - t0)
        solved += 1 if path else 0
    return mean(times), solved, trials

if __name__ == "__main__":
    for p in (AStarPlanner(), GreedyPlanner()):
        m, ok, n = bench(p, trials=30, size=20)
        print(f"{p.__class__.name__ if hasattr(p,'name__') else p.__class__.__name__}: "
              f"{m*1000:.2f} ms avg, solved {ok}/{n}")
