from dataclasses import dataclass
from typing import Any, Dict, Union

import yaml

from .backends import get_backend_class


@dataclass(frozen=True, kw_only=True)
class Config:
    """App configuration."""

    broker_url: str
    broker_params: Dict[str, Any]
    broker_class: str
    logging: Dict[str, Any] | None
    default_queue: str = "aipo_default"
    max_concurrent_tasks: int = 100
    serializer_class: str = "aipo.serializers.JSONSerializer"

    @staticmethod
    def read_config(config: Union[Dict[str, Any], str]) -> "Config":
        if isinstance(config, str):
            config = Config._load_from_file(config)
        Config._validate(config)
        return Config(**config)

    @staticmethod
    def _load_from_file(path: str) -> Dict[str, Any]:
        with open(path) as f:
            return yaml.safe_load(f)

    @staticmethod
    def _validate(config: Dict[str, Any]) -> None:
        if not config.get("broker_url"):
            raise ValueError("broker_url is required")

        mct = config.get("max_concurrent_tasks")
        if mct and mct < 1:
            raise ValueError("max_concurrent_tasks must be greater than 0")

        if not config.get("broker_class"):
            config["broker_class"] = get_backend_class(config["broker_url"])

        if not config.get("broker_params"):
            config["broker_params"] = {}

        if not config.get("logging"):
            config["logging"] = None

        Config._parse_broker_url(config)

    @staticmethod
    def _parse_broker_url(config: Dict[str, Any]) -> None:
        config["broker_params"].update(
            {
                "hostname": config["broker_url"].split("//")[1].split(":")[0],
                "port": int(
                    config["broker_url"].split("//")[1].split(":")[1].split("/")[0]
                ),
            }
        )

        if config["broker_url"].startswith("redis://"):
            if "/" in config["broker_url"].split("//")[1]:
                db = config["broker_url"].split("//")[1].split("/")[1]
                config["broker_params"].update({"db": db})
