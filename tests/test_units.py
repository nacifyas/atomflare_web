from sqlalchemy import true
from hub.dal.service import ServiceDAL
import pytest


@pytest.mark.anyo
async def test_one():
    # ID: int = 11
    # service_dal = await ServiceDAL.begin()
    # assert await service_dal.get_by_id(ID) is not None
    assert True