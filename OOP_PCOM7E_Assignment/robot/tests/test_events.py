# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code

from robot.services.events import EventBus

def test_eventbus_calls_handlers():
    bus, seen = EventBus(), []

    def _append(msg):
        seen.append(msg)

    bus.subscribe("t", _append)
    bus.publish("t", {"x": 1})
    assert seen == [{"x": 1}]
