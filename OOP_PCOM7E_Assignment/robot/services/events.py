from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self._subs: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Any], None]): 
        self._subs[topic].append(handler)
    def publish(self, topic: str, payload: Any):
        for h in self._subs[topic]: h(payload)
