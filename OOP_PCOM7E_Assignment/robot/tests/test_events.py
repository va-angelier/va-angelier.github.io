from robot.services.events import EventBus

def test_eventbus_calls_handlers():
    bus, seen = EventBus(), []
    bus.subscribe("t", lambda m: seen.append(m))
    bus.publish("t", {"x":1})
    assert seen == [{"x":1}]
