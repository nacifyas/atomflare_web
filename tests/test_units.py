from hub.main import app
from hub.dal.service import ServiceDAL
from httpx import AsyncClient
import pytest


@pytest.mark.anyo
async def test_one():
    ID: int = 11
    service_dal = await ServiceDAL.begin()
    assert await service_dal.get_by_id(ID) is not None