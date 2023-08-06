import asyncio
from unittest.mock import Mock

import pytest

from aipo.app import AipoApp
from aipo.task import Task


def dummy_task():
    pass


def test_app_init():
    app = AipoApp({"broker_url": "redis://localhost:6379/0"})
    assert app.loop is not None
    assert app.config is not None
    assert app._broker.__class__.__name__ == "RedisBroker"
    assert app._task_manager is not None
    assert app._event_manager is not None


def test_app_task_decorator(monkeypatch):
    c = Mock()
    c.default_queue = "default"
    c.max_concurrent_tasks = 100
    monkeypatch.setattr("aipo.app.Config.read_config", lambda _: c)
    monkeypatch.setattr("aipo.app.import_from_string", Mock())
    app = AipoApp({})
    task = app.task(dummy_task)
    assert type(task) is Task
    assert task._func is dummy_task
    assert task.queue == "default"
    assert app._task_manager._tasks["test_app.dummy_task"] is task


def test_app_task_decorator_args(monkeypatch):
    c = Mock()
    c.default_queue = "default"
    c.max_concurrent_tasks = 100
    monkeypatch.setattr("aipo.app.Config.read_config", lambda _: c)
    monkeypatch.setattr("aipo.app.import_from_string", Mock())
    app = AipoApp({})
    task = app.task(queue="custom")(dummy_task)
    assert type(task) is Task
    assert task._func is dummy_task
    assert task.queue == "custom"
    assert app._task_manager._tasks["test_app.dummy_task"] is task


def test_app_task_on_event(monkeypatch):
    em = Mock()
    monkeypatch.setattr("aipo.app.import_from_string", Mock())
    monkeypatch.setattr("aipo.app.Config", Mock())
    monkeypatch.setattr("aipo.app.TaskManager", Mock())
    monkeypatch.setattr("aipo.app.EventManager", lambda _, __: em)
    app = AipoApp({})
    func = app.on_event("startup")(dummy_task)
    assert func is dummy_task
    em.register.assert_called_once_with("startup", dummy_task)


@pytest.mark.asyncio
async def test_app_start_server(monkeypatch):
    monkeypatch.setattr("aipo.app.import_from_string", Mock())
    monkeypatch.setattr("aipo.app.Config", Mock())
    monkeypatch.setattr("aipo.app.EventManager", Mock())
    monkeypatch.setattr("aipo.app.TaskManager", Mock())
    monkeypatch.setattr("aipo.app.Broker", Mock())
    app = AipoApp({})
    app._event_manager.trigger = Mock()
    app._event_manager.trigger.return_value = asyncio.sleep(0)
    app._broker.start = Mock()
    app._broker.start.return_value = asyncio.sleep(0)
    app._task_manager.drain_events = Mock()
    app._task_manager.drain_events.return_value = asyncio.sleep(0)
    await app.start_server()
    app._event_manager.trigger.assert_called_once_with("startup")
    app._broker.start.assert_called_once_with()
    app._task_manager.drain_events.assert_called_once_with()


@pytest.mark.asyncio
async def test_app_stop_server(monkeypatch):
    monkeypatch.setattr("aipo.app.import_from_string", Mock())
    monkeypatch.setattr("aipo.app.Config", Mock())
    monkeypatch.setattr("aipo.app.EventManager", Mock())
    monkeypatch.setattr("aipo.app.TaskManager", Mock())
    monkeypatch.setattr("aipo.app.Broker", Mock())
    app = AipoApp({})
    app._event_manager.trigger = Mock()
    app._event_manager.trigger.return_value = asyncio.sleep(0)
    app._broker.close = Mock()
    app._broker.close.return_value = asyncio.sleep(0)
    app._task_manager.stop_draining_events = Mock()
    app._task_manager.wait = Mock()
    app._task_manager.wait.return_value = asyncio.sleep(0)
    await app.stop_server()
    app._task_manager.stop_draining_events.assert_called_once_with()
    app._task_manager.wait.assert_called_once_with()
    app._event_manager.trigger.assert_called_once_with("shutdown")
    app._broker.close.assert_called_once_with()
