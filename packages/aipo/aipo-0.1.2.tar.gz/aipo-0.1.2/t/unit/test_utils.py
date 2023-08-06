import pytest

from aipo import utils


def test_get_fully_qualified_name():
    from aipo.app import AipoApp

    assert utils.get_fully_qualified_name(AipoApp) == "aipo.app.AipoApp"
    assert (
        utils.get_fully_qualified_name(utils.get_fully_qualified_name)
        == "aipo.utils.get_fully_qualified_name"
    )


@pytest.mark.asyncio
async def test_ensure_async():
    async def async_func():
        return 1

    def sync_func():
        return 2

    assert (await utils.ensure_async(async_func)) == 1
    assert (await utils.ensure_async(sync_func)) == 2


def test_import_from_string():
    assert (
        utils.import_from_string("aipo.app.AipoApp")
        == utils.import_from_string("aipo.app").AipoApp
    )
    assert (
        utils.import_from_string("aipo.utils.get_fully_qualified_name")
        == utils.get_fully_qualified_name
    )
