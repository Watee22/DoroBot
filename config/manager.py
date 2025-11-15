from __future__ import annotations
import os
import json
from typing import Any, Callable, Dict, Optional, List

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # 延迟错误，首次使用时报错提示安装 pyyaml

from .schema import ConfigDict, DEFAULT_CONFIG, generate_json_schema
from .migrations import apply_migrations
from .compat import import_old_json, export_ini

Subscriber = Callable[[ConfigDict], None]

class ConfigManager:
    def __init__(self, path: str = "config.yaml"):
        self.path = path
        self._config: ConfigDict = DEFAULT_CONFIG.copy()
        self._subscribers: List[Subscriber] = []
        self.load()

    @property
    def data(self) -> ConfigDict:
        return self._config

    def subscribe(self, cb: Subscriber) -> None:
        self._subscribers.append(cb)

    def _notify(self) -> None:
        for cb in list(self._subscribers):
            try:
                cb(self._config)
            except Exception:
                pass

    def _ensure_yaml(self) -> None:
        if yaml is None:
            raise RuntimeError("Missing dependency: pyyaml. Please install pyyaml to use YAML-based config.")

    def load(self) -> None:
        self._ensure_yaml()
        merged: ConfigDict = json.loads(json.dumps(DEFAULT_CONFIG))
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or {}
            if not isinstance(loaded, dict):
                loaded = {}
            for k, v in loaded.items():
                if k in ("vision", "tasks", "toggles", "numeric_settings", "meta") and isinstance(v, dict):
                    merged[k].update(v)
                else:
                    merged[k] = v
        # 旧 JSON 迁移
        legacy = import_old_json()
        for k in ("toggles", "numeric_settings"):
            if k in legacy:
                merged[k].update(legacy[k])
        self._config = merged
        self._notify()

    def save(self) -> None:
        self._ensure_yaml()
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self._config, f, allow_unicode=True, sort_keys=False)
        export_ini(self._config, "settings.ini")

    def update(self, section: str, key: str, value: Any) -> None:
        if section not in self._config:
            self._config[section] = {}
        if isinstance(self._config[section], dict):
            self._config[section][key] = value
        self.save()
        self._notify()

    def get(self, *path: str, default: Any = None) -> Any:
        cur: Any = self._config
        for p in path:
            if not isinstance(cur, dict):
                return default
            cur = cur.get(p)
            if cur is None:
                return default
        return cur

    def generate_schema_file(self, out_path: str = "config.schema.json") -> None:
        schema = generate_json_schema()
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)