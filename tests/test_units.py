import unittest
from hub.dal.service import ServiceDAL


class TestDalUnits(unittest.TestCase):
    
    async def test_get_existing_user(self):
        ID: int = 11
        service_dal = await ServiceDAL.begin()
        service = await service_dal.get_by_id(ID)
        self.assertIsNotNone(service)
        self.assertEqual(service.id, ID)


if __name__ == '__main__':
    unittest.main()