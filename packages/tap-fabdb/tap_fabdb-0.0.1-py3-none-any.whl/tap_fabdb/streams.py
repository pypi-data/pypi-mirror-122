"""Stream type classes for tap-fabdb."""

from typing import Any, Dict, Final, Optional

import requests
from singer_sdk import typing as th
from singer_sdk.streams import RESTStream


class FabDbStream(RESTStream):
    """FaB DB base stream class."""

    url_base = "https://api.fabdb.net"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[int]) -> Dict[str, Any]:
        """Override the RESTStream get_url_params method to support FaB DB pagination."""
        params = {
            "per_page": 100,
        }
        if next_page_token is not None:
            params["page"] = next_page_token
        return params

    def get_next_page_token(self, response: requests.Response, previous_token: Optional[int]) -> Optional[int]:
        """Override the RESTStream get_next_page_token method to support FaB DB pagination."""
        current_page = previous_token or response.json().get("current_page", 1)
        if response.json()["links"].get("next") is not None:
            return current_page + 1
        else:
            return None


class CardsStream(FabDbStream):
    """Cards stream representing FaB DB Cards."""

    name = "cards"
    path = "/cards"
    primary_keys = ["identifier"]
    records_jsonpath = "$.data[*]"
    stats = {"cost", "attack", "defense", "resource"}
    stats_properties = [th.Property(stat, th.StringType) for stat in stats]

    schema: Final = th.PropertiesList(
        th.Property("identifier", th.StringType, required=True),
        th.Property("name", th.StringType, required=True),
        th.Property("rarity", th.StringType, required=True),
        th.Property("keywords", th.ArrayType(th.StringType), required=True),
        th.Property("stats", th.ObjectType(*stats_properties), required=True),
        th.Property("text", th.StringType),
        th.Property("image", th.StringType),
        th.Property("totalSideboard", th.IntegerType),
        th.Property("printings", th.ArrayType(th.ObjectType())),
        th.Property("flavour", th.StringType),
        th.Property("comments", th.StringType),
        th.Property("banned", th.ArrayType(th.StringType)),
        th.Property("next", th.StringType),
        th.Property("prev", th.StringType),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure.

        Optional. This method gives developers an opportunity to "clean up" the results
        prior to returning records to the downstream tap - for instance: cleaning,
        renaming, or appending properties to the raw record result returned from the
        API.
        """
        if isinstance(row["stats"], list):
            row["stats"] = row["stats"].pop() if row["stats"] else {}

        for stat in self.stats:
            if stat in row["stats"]:
                row["stats"][stat] = str(row["stats"][stat])
        return row
