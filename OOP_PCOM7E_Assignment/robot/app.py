"""Application entrypoint for the humanoid robot demo."""
from robot.services.planning import AStarPlanner
from robot.services.navigation import Navigator

def main() -> None:
    """Compose the application and run a simple navigation demo."""
    nav = Navigator(AStarPlanner())
    nav.navigate((0, 0), (10, 10))

if __name__ == "__main__":
    main()
