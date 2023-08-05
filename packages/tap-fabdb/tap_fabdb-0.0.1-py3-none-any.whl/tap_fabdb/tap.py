"""FaB DB tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_fabdb.streams import CardsStream

PLUGIN_NAME = "tap-fabdb"

STREAM_TYPES = [CardsStream]


class TapFabDb(Tap):
    """FaB DB tap class."""

    name = "tap-fabdb"

    config_jsonschema = th.PropertiesList(th.Property("api_key", th.StringType, required=False)).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


cli = TapFabDb.cli
