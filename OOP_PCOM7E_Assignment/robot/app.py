from robot.services.planning import AStarPlanner
from robot.services.navigation import Navigator
from robot.services.events import EventBus

def main():
    bus = EventBus()
    nav = Navigator(AStarPlanner())
    # bus.subscribe("lidar.obstacle", lambda m: nav.handle_obstacle(m))  # optioneel
    nav.navigate((0,0), (10,10))

if __name__ == "__main__":
    main()
