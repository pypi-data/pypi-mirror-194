import asyncio
import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from aipo.backends.redis import RedisBroker
from aipo.message import Message


@pytest.fixture
def config():
    class Config:
        broker_params = {}
        serializer_class = ""

    return Config()


@pytest.fixture(scope="function")
def redis_broker(config, monkeypatch):
    monkeypatch.setattr("aipo.broker.import_from_string", Mock())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    rb = RedisBroker(loop, config)
    rb._client = Mock()

    return rb


def test_redis_get_conn_params(redis_broker):
    # Test the default values
    params = redis_broker._get_conn_params()
    assert params == {
        "host": None,
        "port": 6379,
        "username": None,
        "password": None,
        "max_connections": 10,
        "socket_timeout": None,
        "socket_connect_timeout": None,
        "socket_keepalive": None,
        "socket_keepalive_options": None,
        "health_check_interval": 25,
    }

    # Test the custom values
    redis_broker.config.broker_params = {
        "hostname": "localhost",
        "port": 6380,
        "username": "user",
        "password": "password",
        "max_connections": 20,
        "socket_timeout": 10,
        "socket_connect_timeout": 5,
        "socket_keepalive": True,
        "socket_keepalive_options": (1, 1, 1),
        "health_check_interval": 30,
    }
    params = redis_broker._get_conn_params()
    assert params == {
        "host": "localhost",
        "port": 6380,
        "username": "user",
        "password": "password",
        "max_connections": 20,
        "socket_timeout": 10,
        "socket_connect_timeout": 5,
        "socket_keepalive": True,
        "socket_keepalive_options": (1, 1, 1),
        "health_check_interval": 30,
    }


@pytest.mark.asyncio
async def test_redis_start(redis_broker, monkeypatch):
    mock = Mock()
    mock.return_value = mock
    mock.ping = Mock()
    mock.ping.return_value = asyncio.sleep(0)

    monkeypatch.setattr("aipo.backends.redis.Redis", mock)
    redis_broker._client = None
    await redis_broker.start()
    assert redis_broker._client is not None
    mock.ping.assert_called_once()


@pytest.mark.asyncio
async def test_redis_close(redis_broker):
    redis_broker._restore_visibility_task = asyncio.Future()
    redis_broker._restore_visibility_task.set_result(None)
    redis_broker._client.close.return_value = asyncio.Future()
    redis_broker._client.close.return_value.set_result(None)

    client = redis_broker._client

    await redis_broker.close()

    assert redis_broker._stopped.is_set()
    assert redis_broker._client is None
    client.close.assert_called_once()


@pytest.mark.asyncio
async def test_redis_publish(redis_broker):
    redis_broker.serializer.encode.return_value = "encoded"
    redis_broker._client.lpush.return_value = asyncio.Future()
    redis_broker._client.lpush.return_value.set_result(None)

    msg = Message("id", "test.func", tuple(), {}, "queue")
    await redis_broker.publish(msg)

    redis_broker.serializer.encode.assert_called_once_with(
        {
            "id": "id",
            "name": "test.func",
            "args": tuple(),
            "kwargs": {},
        }
    )
    redis_broker._client.lpush.assert_called_once_with("queue", "encoded")


@pytest.mark.asyncio
async def test_redis_ack(redis_broker):
    pipeline = MagicMock()
    pipeline.execute.return_value = asyncio.Future()
    pipeline.execute.return_value.set_result(None)
    pipeline.__aenter__.return_value = pipeline
    redis_broker._client.pipeline.return_value = pipeline

    redis_broker._unacked["123"] = "message"
    await redis_broker.ack("123")

    assert "123" not in redis_broker._unacked
    pipeline.hdel.assert_called_once_with(redis_broker.unacked_hash, "123")
    pipeline.zrem.assert_called_once_with(redis_broker.unacked_set, "123")
    pipeline.execute.assert_called_once()


def test_redis_is_ready(redis_broker):
    assert redis_broker.is_ready() is True
    redis_broker._client = None
    assert redis_broker.is_ready() is False


@pytest.mark.asyncio
async def test_redis_restore_unacked(redis_broker):
    redis_broker._unacked = {
        "1": "message",
        "2": "message",
    }
    redis_broker.serializer = Mock()
    redis_broker.serializer.decode.return_value = {
        "data": "message",
        "queue": "queue",
    }

    pipe = MagicMock()
    pipe.hdel.return_value = asyncio.Future()
    pipe.hdel.return_value.set_result(None)
    pipe.zrem.return_value = asyncio.Future()
    pipe.zrem.return_value.set_result(None)
    pipe.rpush.return_value = asyncio.Future()
    pipe.rpush.return_value.set_result(None)
    pipe.execute.return_value = asyncio.Future()
    pipe.execute.return_value.set_result(None)
    pipe.__aenter__.return_value = pipe
    redis_broker._client.pipeline.return_value = pipe

    await redis_broker._restore_unacked()

    pipe.hdel.call_count == 2
    pipe.zrem.call_count == 2
    pipe.rpush.call_count == 2
    pipe.execute.call_count == 2


@pytest.mark.asyncio
async def test_redis_restore_visibility_acquire_fails(redis_broker):
    lock = Mock()
    lock.acquire.return_value = asyncio.Future()
    lock.acquire.return_value.set_result(False)
    redis_broker._client.lock.return_value = lock

    await redis_broker._restore_visibility()

    lock.acquire.assert_called_once_with(blocking=False)
    lock.release.assert_not_called()
    redis_broker._client.zrange.assert_not_called()


@pytest.mark.asyncio
async def test_restore_visibility(redis_broker):
    lock = Mock()
    lock.acquire.return_value = asyncio.Future()
    lock.acquire.return_value.set_result(True)
    lock.release.return_value = asyncio.Future()
    lock.release.return_value.set_result(None)
    redis_broker._client.lock.return_value = lock
    redis_broker.serializer = Mock()
    redis_broker.serializer.decode = json.loads
    pipe = MagicMock()
    pipe.hdel.return_value = asyncio.Future()
    pipe.hdel.return_value.set_result(None)
    pipe.zrem.return_value = asyncio.Future()
    pipe.zrem.return_value.set_result(None)
    pipe.rpush.return_value = asyncio.Future()
    pipe.rpush.return_value.set_result(None)
    pipe.execute.return_value = asyncio.Future()
    pipe.execute.return_value.set_result(None)
    pipe.__aenter__.return_value = pipe
    redis_broker._client.pipeline.return_value = pipe

    redis_broker._client.zrange = Mock()
    redis_broker._client.zrange.return_value = asyncio.Future()
    redis_broker._client.zrange.return_value.set_result(
        [json.dumps({"data": '{"id": "1"}', "queue": "test"}).encode()]
    )

    await redis_broker._restore_visibility()

    lock.acquire.assert_called_once_with(blocking=False)
    lock.release.assert_called_once()
    redis_broker._client.pipeline.assert_called_once()
    redis_broker._client.zrange.assert_called_once()
    pipe.hdel.assert_called_once_with(redis_broker.unacked_hash, "1")
    pipe.zrem.assert_called_once_with(redis_broker.unacked_set, "1")
    pipe.rpush.assert_called_once_with("test", '{"id": "1"}')
    pipe.execute.assert_called_once()


@pytest.mark.asyncio
async def test_redis_subscribe(redis_broker):
    redis_broker._restore_visibility_loop = lambda: asyncio.sleep(0)
    redis_broker._wait_message = Mock()
    redis_broker._wait_message.return_value = asyncio.Future()
    redis_broker._wait_message.return_value.set_result(
        Message("id", "test.func", tuple(), {}, "queue")
    )

    iterator = redis_broker.subscribe(["queue"])

    msg = await iterator.__anext__()
    assert msg.id == "id"
    assert msg.name == "test.func"
    assert msg.args == tuple()
    assert msg.kwargs == {}
    assert msg.queue == "queue"

    assert redis_broker._restore_visibility_task is not None
    assert redis_broker._stopped.is_set() is False
    assert redis_broker._queues == ["queue"]

    redis_broker._wait_message.return_value = asyncio.Future()
    redis_broker._wait_message.return_value.set_result(None)

    with pytest.raises(StopAsyncIteration):
        await iterator.__anext__()


@pytest.mark.asyncio
async def test_redis_stop_iterator(redis_broker):
    redis_broker._get_message = asyncio.sleep(1000000)
    redis_broker._curr_fetch = asyncio.create_task(redis_broker._wait_message())
    redis_broker._stopped.clear()

    redis_broker.stop_iterator()
    await asyncio.sleep(0)

    assert redis_broker._curr_fetch.cancelled() is True
    assert redis_broker._stopped.is_set() is True


@pytest.mark.asyncio
async def test_redis_get_message(redis_broker):
    redis_broker._client.brpop.return_value = asyncio.Future()
    redis_broker._client.brpop.return_value.set_result(
        (b"queue", b'{"id": "1", "name": "test.func", "args": [], "kwargs": {}}')
    )
    redis_broker.serializer = Mock()
    redis_broker.serializer.decode = json.loads
    redis_broker._add_to_unacked = Mock()
    redis_broker._add_to_unacked.return_value = asyncio.Future()
    redis_broker._add_to_unacked.return_value.set_result(None)
    redis_broker._queues = ["queue"]

    msg = await redis_broker._get_message()

    assert msg.id == "1"
    assert msg.name == "test.func"
    assert msg.args == []
    assert msg.kwargs == {}
    assert msg.queue == "queue"
    redis_broker._client.brpop.assert_called_once_with(["queue"], timeout=0)
    redis_broker._add_to_unacked.assert_called_once_with(
        "1", '{"id": "1", "name": "test.func", "args": [], "kwargs": {}}', "queue"
    )


@pytest.mark.asyncio
async def test_redis_wait_message(redis_broker):
    msg = Message("id", "test.func", tuple(), {}, "queue")

    async def _get_message():
        return msg

    redis_broker._get_message = _get_message
    redis_broker._stopped.clear()

    returned_message = await redis_broker._wait_message()

    assert returned_message == msg


@pytest.mark.asyncio
async def test_redis_wait_message_broker_stopped(redis_broker):
    redis_broker._get_message = Mock()
    redis_broker._get_message.return_value = asyncio.sleep(1000000)
    redis_broker._stopped.clear()

    task = asyncio.create_task(redis_broker._wait_message())
    await asyncio.sleep(0)
    assert task.done() is False
    redis_broker.stop_iterator()
    msg = await task

    assert msg is None


@pytest.mark.asyncio
@patch("aipo.backends.redis.time.time", return_value=10000)
async def test_redis_add_to_unacked(time_mock, redis_broker):
    pipe = MagicMock()
    pipe.hset.return_value = asyncio.Future()
    pipe.hset.return_value.set_result(None)
    pipe.zadd.return_value = asyncio.Future()
    pipe.zadd.return_value.set_result(None)
    pipe.execute.return_value = asyncio.Future()
    pipe.execute.return_value.set_result(None)
    pipe.__aenter__.return_value = pipe
    redis_broker._client.pipeline.return_value = pipe
    redis_broker.serializer = Mock()
    redis_broker.serializer.encode = json.dumps

    await redis_broker._add_to_unacked("1", '{"id": "1"}', "queue")

    redis_broker._client.pipeline.assert_called_once()
    pipe.hset.assert_called_once_with(
        redis_broker.unacked_hash,
        "1",
        json.dumps({"data": '{"id": "1"}', "queue": "queue"}),
    )
    pipe.zadd.assert_called_once_with(redis_broker.unacked_set, {"1": 10000})
    pipe.execute.assert_called_once()
    assert "1" in redis_broker._unacked
    assert redis_broker._unacked["1"] == json.dumps(
        {"data": '{"id": "1"}', "queue": "queue"}
    )


def test_redis_queue_rotation(redis_broker):
    redis_broker._queues = ["1"]
    redis_broker._queue_rotation()
    assert redis_broker._queues == ["1"]

    redis_broker._queues = ["1", "2"]
    redis_broker._queue_rotation()
    assert redis_broker._queues == ["2", "1"]

    redis_broker._queues = ["1", "2", "3"]
    redis_broker._queue_rotation()
    assert redis_broker._queues == ["3", "1", "2"]
    redis_broker._queue_rotation()
    assert redis_broker._queues == ["2", "3", "1"]
    redis_broker._queue_rotation()
    assert redis_broker._queues == ["1", "2", "3"]
