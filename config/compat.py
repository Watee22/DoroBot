from __future__ import annotations
import os
import json
from typing import Dict, Any

from .schema import ConfigDict, DEFAULT_CONFIG

try:
    import configparser
except Exception:  # pragma: no cover
    configparser = None

def import_old_json(settings_file: str = "settings.json", numeric_file: str = "numeric_settings.json") -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data.setdefault("toggles", {}).update(json.load(f))
        except Exception:
            pass
    if os.path.exists(numeric_file):
        try:
            with open(numeric_file, "r", encoding="utf-8") as f:
                data.setdefault("numeric_settings", {}).update(json.load(f))
        except Exception:
            pass
    return data

def export_ini(config: ConfigDict, ini_path: str = "settings.ini") -> None:
    if configparser is None:
        # 简单写出 INI 格式，避免强依赖
        lines = ["[Toggles]"]
        for k, v in config.get("toggles", {}).items():
            lines.append(f"{k}={int(v)}")
        lines.append("[Numbers]")
        for k, v in config.get("numeric_settings", {}).items():
            lines.append(f"{k}={v}")
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return

    parser = configparser.ConfigParser()
    parser["Toggles"] = {k: str(int(v)) for k, v in config.get("toggles", {}).items()}
    parser["Numbers"] = {k: str(v) for k, v in config.get("numeric_settings", {}).items()}
    with open(ini_path, "w", encoding="utf-8") as f:
        parser.write(f)