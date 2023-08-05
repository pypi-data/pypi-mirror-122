"""Tests standard tap features using the built-in SDK tests library."""

from unittest.mock import patch

import pytest
import responses
from singer_sdk.testing import get_standard_tap_tests

from tap_fabdb.streams import CardsStream
from tap_fabdb.tap import TapFabDb


class TestFabDbStream:
    """Test specifics of the FabDbStream base class."""

    @pytest.fixture
    def stream(self):
        """Stream fixture."""
        return CardsStream(tap=TapFabDb(), name="cards")

    @patch("tap_fabdb.streams.requests.Response")
    def test_get_next_page_token(self, mock_response, stream):
        """Test the overriden get_next_page_token functionality."""
        mock_response.json.return_value = {"links": {"next": "https://api.fabdb.net/cards?page=2"}}
        next_page_token = stream.get_next_page_token(mock_response, None)
        assert next_page_token == 2
        mock_response.json.return_value = {"links": {"next": None}}
        next_page_token = stream.get_next_page_token(mock_response, 2)
        assert next_page_token is None

    def test_get_url_params(self, stream):
        """Test the overriden get_url_params functionality."""
        params = stream.get_url_params(context={}, next_page_token=2)
        assert params["per_page"] == 100
        assert params["page"] == 2

    def test_post_process(self, stream):
        """Test the post-processing functionality as it relates to Card stats."""
        empty_stats = {"identifier": "foo", "stats": []}
        processed = stream.post_process(empty_stats)
        assert processed["stats"] == {}

        normal_stats = {"identifier": "foo", "stats": {"cost": "1", "defense": "1"}}
        processed = stream.post_process(normal_stats)
        assert processed["stats"] == {"cost": "1", "defense": "1"}


@responses.activate
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    responses.add(
        responses.GET,
        url="https://api.fabdb.net/cards",
        status=200,
        json={
            "data": [
                {
                    "identifier": "foo",
                    "name": "foo",
                    "stats": {"cost": "1", "defense": "1", "attack": "1", "resource": "1"},
                }
            ]
        },
    )
    tests = get_standard_tap_tests(TapFabDb)
    for test in tests:
        test()
