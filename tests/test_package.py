import importlib
import importlib.metadata

import scp


def test_version_falls_back_when_package_metadata_is_unavailable(monkeypatch) -> None:
    def raise_package_not_found(_distribution_name: str) -> str:
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", raise_package_not_found)

    try:
        assert importlib.reload(scp).VERSION == "0+unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(scp)
