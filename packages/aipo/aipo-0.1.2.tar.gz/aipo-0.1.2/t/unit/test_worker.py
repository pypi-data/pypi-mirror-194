import asyncio
from unittest.mock import Mock

import uvloop

from aipo.worker import Worker

app = None


def test_worker_contructor(dummy_app):
    global app
    app = dummy_app
    worker = Worker("test_worker:app")
    worker.loop.run_until_complete(asyncio.sleep(0.1))
    assert worker.app is dummy_app
    assert worker.loop is not None


def test_worker_constructor_loop(dummy_app):
    global app
    app = dummy_app
    worker = Worker("test_worker:app", "uvloop")
    assert worker.app is app
    assert worker.loop.__class__ == uvloop.Loop


def test_worker_exec_from_cmd(monkeypatch, dummy_app):
    global app
    app = dummy_app
    monkeypatch.setattr("aipo.worker.sys.exit", Mock())
    worker = Worker("test_worker:app")
    worker.app.start_server.return_value = asyncio.sleep(0.1)
    worker.app.stop_server.return_value = asyncio.sleep(0.1)
    worker._signal_handler()
    worker.exec_from_cmd()
    assert not worker.loop.is_running()
    assert worker.loop.is_closed()
    assert worker.start_future.done()
    assert worker.stop_future.done()
    app.start_server.assert_called_once()
    app.stop_server.assert_called_once()
