# -----------------------------------------------
# Set operations + Linear Search (IoT / Robotics)
# -----------------------------------------------
from typing import Iterable, Any

def linear_search(data_list: Iterable[Any], target: Any) -> int:
    """
    Performs a linear (sequential) search over data_list.
    Returns the 0-based index of the first match; -1 if not found.
    """
    for idx, val in enumerate(data_list):
        if val == target:
            return idx
    return -1


def demo_set_operations():
    """
    Demonstrates Union, Intersection, Difference, Symmetric Difference
    in a humanoid robot / IoT scenario.
    """
    # Example domain:
    # - The robot perceives objects with multiple sensors.
    # - The cloud/RTLS holds a registry of expected objects/IDs in the area.
    vision_detections = {"box_101", "box_102", "pallet_A", "human_1"}
    lidar_detections  = {"box_101", "pallet_A", "pillar_7"}
    rtls_registry     = {"box_101", "box_102", "box_999", "pallet_A"}  # "ground truth" from RTLS/cloud

    print("=== Set Operations (IoT / Humanoid Robot) ===")

    # 1) UNION: combine detections from multiple sensors → broader situational awareness
    fused_perception = vision_detections.union(lidar_detections)
    print("Union (vision ∪ LiDAR):", fused_perception)
    # Use: full list of perceived obstacles/objects for planning.

    # 2) INTERSECTION: cross-validate detections between sensors → higher confidence
    cross_validated = vision_detections.intersection(lidar_detections)
    print("Intersection (vision ∩ LiDAR):", cross_validated)
    # Use: objects confirmed by multiple sensors for safer navigation.

    # 3) DIFFERENCE: pending tasks, anomalies, or missing items
    # Example A-B: items expected by RTLS but not seen → potential missing/occluded
    missing_locally = rtls_registry.difference(fused_perception)
    print("Difference (RTLS − perceived):", missing_locally)
    # Use: triggers re-scan or operator notification.

    # 4) SYMMETRIC DIFFERENCE: discrepancies between sources (inconsistencies)
    # Items seen locally but not in RTLS, OR in RTLS but not locally
    discrepancies = rtls_registry.symmetric_difference(fused_perception)
    print("Symmetric difference (RTLS Δ perceived):", discrepancies)
    # Use: inventory mismatch, map desync, or sensor drift diagnostics.


def demo_linear_search():
    """
    Demonstrates linear_search on a simple list.
    """
    items = ["box_101", "box_102", "pallet_A", "pillar_7", "human_1"]
    target = "pallet_A"
    idx = linear_search(items, target)
    print("\n=== Linear Search ===")
    if idx != -1:
        print(f"Target '{target}' found at index {idx}")
    else:
        print(f"Target '{target}' not found")


if __name__ == "__main__":
    demo_set_operations()
    demo_linear_search()
