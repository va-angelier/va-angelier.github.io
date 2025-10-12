from collections import defaultdict
from typing import Callable, Any

"""
@todo Not yet implemented; Needs to be in use when handeling multiple tasks, for example,
with different priorities. Or when on-route, encountering different obstacles.
"""

class EventBus:
    def __init__(self):
        self._subs: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Any], None]):
        """Subscribe to event, add handler.""" 
        self._subs[topic].append(handler)
    def publish(self, topic: str, payload: Any):
        """Publish/handle subscribed events"""
        for h in self._subs[topic]: h(payload)
