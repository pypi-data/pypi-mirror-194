import asyncio
from unittest.mock import Mock

import pytest

from aipo.message import Message
from aipo.task import Task, TaskManager


def dummy_func():
    pass


class DummyTaskManager:
    def __init__(self):
        self.publish_task = Mock()


class DummyBroker:
    def __init__(self):
        self.started = False
        self.publish = Mock()
        self.ack = Mock()
        self.stop_iterator = Mock()

    def is_ready(self):
        return self.started

    async def start(self):
        self.started = True

    async def subscribe(self, queues):
        for queue in queues:
            yield Message("id", "test_task.dummy_func", (), {}, queue)


def test_task_init():
    task_manager = DummyTaskManager()
    task = Task(queue="queue", func=dummy_func, manager=task_manager)

    assert task.queue == "queue"
    assert task.name == "test_task.dummy_func"
    assert task._func == dummy_func
    assert task._manager == task_manager


@pytest.mark.asyncio
async def test_task_execute():
    func = Mock()
    func.__name__ = "dummy_func"
    task = Task(queue="queue", func=func, manager=None)

    await task.execute(1, 2)

    func.assert_called_once_with(1, 2)


@pytest.mark.asyncio
async def test_task_call(monkeypatch):
    uuid = "4d0f3eb1-9d4f-4d15-befd-5252c254ef4f"
    monkeypatch.setattr("aipo.task.uuid.uuid4", lambda: uuid)
    task_manager = DummyTaskManager()
    task_manager.publish_task.return_value = asyncio.sleep(0.1)
    task = Task(queue="queue", func=dummy_func, manager=task_manager)

    await task(1, 2)

    task_manager.publish_task.assert_called_once()
    msg = task_manager.publish_task.call_args.args[0]
    assert msg.id == uuid
    assert msg.name == "test_task.dummy_func"
    assert msg.args == (1, 2)
    assert msg.kwargs == {}
    assert msg.queue == "queue"


def test_task_manager_bind(dummy_app):
    tm = TaskManager(loop=None, broker=None, app=dummy_app)
    task = Task(queue="queue", func=dummy_func, manager=tm)
    tm.bind(task)
    assert tm._tasks["test_task.dummy_func"] == task


@pytest.mark.asyncio
async def test_task_manager_publish_task(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    tm._broker.publish.return_value = asyncio.sleep(0)
    msg = Message("id", "name", (1, 2), {"a": 1}, "queue")
    await tm.publish_task(msg)
    assert tm._broker.publish.call_count == 1
    assert tm._broker.publish.call_args.args[0] is msg
    assert tm._broker.started


@pytest.mark.asyncio
async def test_task_manager_execute_success(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    tm._broker.ack.return_value = asyncio.sleep(0)
    task = Mock()
    task.name = "test_task.dummy_func"
    task.execute = Mock()
    executed = asyncio.Event()
    task.execute.return_value = executed.wait()
    tm.bind(task)
    msg = Message("id", "test_task.dummy_func", (1, 2), {"a": 1}, "queue")
    await tm.execute(msg)
    assert len(tm._running) == 1
    assert not list(tm._running.values())[0].done()
    executed.set()
    await list(tm._running.keys())[0]
    task.execute.assert_called_once_with(1, 2, a=1)
    tm._broker.ack.assert_called_once_with(msg.id)
    assert len(tm._running) == 0


@pytest.mark.asyncio
async def test_task_manager_execute_error(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    task = Mock()
    task.name = "test_task.dummy_func"
    task.execute = Mock()
    task.execute.side_effect = Exception("error")
    tm.bind(task)
    msg = Message("id", "test_task.dummy_func", (1, 2), {"a": 1}, "queue")
    await tm.execute(msg)
    await asyncio.sleep(0.1)
    assert len(tm._running) == 0
    task.execute.assert_called_once_with(1, 2, a=1)
    tm._broker.ack.assert_not_called()


@pytest.mark.asyncio
async def test_task_manager_wait(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    tm._broker.ack.return_value = asyncio.sleep(0)
    task = Mock()
    task.name = "test_task.dummy_func"
    task.execute = Mock()
    task.execute.return_value = asyncio.sleep(0.2)
    tm.bind(task)
    msg = Message("id", "test_task.dummy_func", (1, 2), {"a": 1}, "queue")
    await tm.execute(msg)
    await tm.execute(msg)
    await tm.execute(msg)
    assert len(tm._running) == 3
    await tm.wait()
    assert len(tm._running) == 0


@pytest.mark.asyncio
async def test_task_manager_drain_events(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    task = Task(queue="queue", func=dummy_func, manager=tm)
    tm.bind(task)
    tm.execute = Mock()
    tm.execute.return_value = asyncio.sleep(0.1)
    await tm.drain_events()
    assert tm.execute.call_count == 1
    msg = tm.execute.call_args.args[0]
    assert msg.name == "test_task.dummy_func"
    assert msg.queue == "queue"


@pytest.mark.asyncio
async def test_task_manager_stop_draining(dummy_app):
    tm = TaskManager(
        loop=asyncio.get_running_loop(), broker=DummyBroker(), app=dummy_app
    )
    tm.stop_draining_events()
    tm._broker.stop_iterator.assert_called_once()
