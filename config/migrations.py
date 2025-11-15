from __future__ import annotations
from typing import Callable, Dict, Any

MigrationFn = Callable[[Dict[str, Any]], Dict[str, Any]]

_REGISTRY: Dict[int, MigrationFn] = {}

def register_migration(from_version: int, fn: MigrationFn) -> None:
    _REGISTRY[from_version] = fn

def apply_migrations(config: Dict[str, Any], target_version: int | None = None) -> Dict[str, Any]:
    current = int(config.get("meta", {}).get("version", 1))
    if target_version is None:
        target_version = current
    while current < target_version:
        fn = _REGISTRY.get(current)
        if fn is None:
            break
        config = fn(config)
        current += 1
        config.setdefault("meta", {})["version"] = current
    return config