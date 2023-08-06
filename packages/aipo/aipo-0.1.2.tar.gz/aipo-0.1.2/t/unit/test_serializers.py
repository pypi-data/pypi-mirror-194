from datetime import date, datetime, time

import pytest

from aipo.serializers import JSONSerializer


def test_json_encode():
    ser = JSONSerializer()
    assert ser.encode(
        {
            "int": 1,
            "float": 1.0,
            "str": "str",
            "bool": True,
            "none": None,
            "dict": {"key": "value"},
            "datetime": datetime(2020, 1, 1, 0, 0, 0),
            "date": date(2020, 1, 1),
            "time": time(0, 0, 0),
            "bytes": b"test",
            "list": [1, 2, 3],
            "tuple": (1, 2, 3),
            "nested": {
                "list": [1, (2, 3), 4],
                "tuple": (1, [2, 3]),
                "dict": {"key": "value"},
            },
        }
    ) == (
        "{"
        + ",".join(
            [
                '"int":1',
                '"float":1.0',
                '"str":"str"',
                '"bool":true',
                '"none":null',
                '"dict":{"value":{"key":"value"},"type":"dict"}',
                '"datetime":{"value":"2020-01-01T00:00:00","type":"datetime"}',
                '"date":{"value":"2020-01-01","type":"date"}',
                '"time":{"value":"00:00:00","type":"time"}',
                '"bytes":{"value":"dGVzdA==","type":"bytes","encoding":"base64"}',
                '"list":[1,2,3]',
                '"tuple":[1,2,3]',
                (
                    '"nested":{"value":{"list":[1,[2,3],4],'
                    '"tuple":[1,[2,3]],'
                    '"dict":{"value":{"key":"value"},"type":"dict"}},"type":"dict"}'
                ),
            ]
        )
        + "}"
    )


def test_json_decode():
    ser = JSONSerializer()
    assert ser.decode(
        (
            "{"
            + ",".join(
                [
                    '"int":1',
                    '"float":1.0',
                    '"str":"str"',
                    '"bool":true',
                    '"none":null',
                    '"dict":{"value":{"key":"value"},"type":"dict"}',
                    '"datetime":{"value":"2020-01-01T00:00:00","type":"datetime"}',
                    '"date":{"value":"2020-01-01","type":"date"}',
                    '"time":{"value":"00:00:00","type":"time"}',
                    '"bytes":{"value":"dGVzdA==","type":"bytes","encoding":"base64"}',
                    '"list":[1,2,3]',
                    '"tuple":[1,2,3]',
                    (
                        '"nested":{"value":{"list":[1,[2,3],4],'
                        '"tuple":[1,[2,3]],'
                        '"dict":{"value":{"key":"value"},"type":"dict"}},"type":"dict"}'
                    ),
                ]
            )
            + "}"
        )
    ) == {
        "int": 1,
        "float": 1.0,
        "str": "str",
        "bool": True,
        "none": None,
        "dict": {"key": "value"},
        "datetime": datetime(2020, 1, 1, 0, 0, 0),
        "date": date(2020, 1, 1),
        "time": time(0, 0, 0),
        "bytes": b"test",
        "list": [1, 2, 3],
        "tuple": [1, 2, 3],
        "nested": {
            "list": [1, [2, 3], 4],
            "tuple": [1, [2, 3]],
            "dict": {"key": "value"},
        },
    }


def test_json_encode_type_error():
    with pytest.raises(TypeError):
        JSONSerializer().encode({"key": object()})


def test_json_decode_type_error():
    with pytest.raises(TypeError):
        JSONSerializer().decode('{"key": {"value": "value", "type": "object"}}')
