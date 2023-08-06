from unittest.mock import Mock

import pytest


@pytest.fixture
def dummy_app():
    class DummyConfig:
        def __init__(self):
            self.logging = None
            self.max_concurrent_tasks = 3

    class DummyApp:
        def __init__(self):
            self.start_server = Mock()
            self.stop_server = Mock()
            self.config = DummyConfig()

    return DummyApp()
