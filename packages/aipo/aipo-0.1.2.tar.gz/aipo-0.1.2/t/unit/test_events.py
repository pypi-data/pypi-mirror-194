from unittest.mock import Mock

import pytest

from aipo.events import EventManager


def test_event_manager_init():
    em = EventManager(["test"], None)
    assert em._receivers == {"test": []}


@pytest.mark.asyncio
async def test_event_manager_register_and_trigger():
    em = EventManager(["test1", "test2"], None)

    receiver1 = Mock()
    receiver2 = Mock()

    em.register("test1", receiver1)
    em.register("test1", receiver2)

    await em.trigger("test1")
    await em.trigger("test2")

    receiver1.assert_called_once()
    receiver2.assert_called_once()
