from typing import Any
from typing import Optional

import requests
from intake.catalog import Catalog
from intake.catalog.local import CatalogParser

from . import __version__
from .exceptions import AnacondaCatalogsError

DEFAULT_BASE_URI = "https://anaconda.cloud/api"
API_VERSION = "2023.02.20"
USER_AGENT = f"anaconda-catalogs/{__version__}"


class AnacondaCatalog(Catalog):
    name = "anaconda_catalog"

    def __init__(self, name: str, base_uri: Optional[str] = None, **kwargs: Any):
        self.name = name
        self.base_uri = base_uri or DEFAULT_BASE_URI
        super().__init__(name=name, **kwargs)

    def _get_catalog_spec(self) -> str:
        """Load the catalog spec from the API."""
        # Note: This is split out as a separate method to enable easier mocking
        url = slash_join(self.base_uri, "catalogs", self.name)
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Api-Version": API_VERSION,
                "User-Agent": USER_AGENT,
            },
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise AnacondaCatalogsError(str(e))
        spec = response.json()["spec"]
        return spec

    def _load(self):
        """Populate the catalog by loading the spec from the catalogs service."""
        spec = self._get_catalog_spec()

        # Parse the catalog spec. This is the same way Intake parses YAML catalogs internally.
        context = {"root": self.name}
        result = CatalogParser(spec, context=context)

        self._entries = {}

        cfg = result.data
        for entry in cfg["data_sources"]:
            entry._catalog = self
            self._entries[entry.name] = entry

        self.metadata.update(cfg.get("metadata") or {})
        self.description = self.description or cfg.get("description")


# It really shouldn't be so complicated to safely create a URL from components...
# https://codereview.stackexchange.com/a/175423
def slash_join(*args):
    return "/".join(arg.strip("/") for arg in args)
