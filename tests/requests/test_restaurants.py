import unittest
import unittest.mock
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from pyjowi.api_client.requests import JowiClient
from pyjowi.dto import Restaurant

from ..common import load_jsondata

DATA_DIR = Path(__file__).parent / "fixtures"


class TestRestaurants(unittest.TestCase):
    def test_list_restaurants(self):
        expected_response = load_jsondata(DATA_DIR / "list_restaurants_response.json")
        test_api_key = str(uuid4())
        test_api_secret = str(uuid4())

        client = JowiClient(test_api_key, test_api_secret)
        with client:
            with unittest.mock.patch.object(client._session, "get") as mock_get:
                mock_get.return_value.json.return_value = deepcopy(expected_response)
                restaurants = client.list_restaurants()
                expected_list = Restaurant.from_jowi_response(expected_response)
                self.assertEqual(restaurants, expected_list)
