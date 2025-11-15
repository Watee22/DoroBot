from __future__ import annotations
from typing import TypedDict, Dict, Any, Optional

class VisionConfig(TypedDict, total=False):
    default_confidence: float
    default_timeout: int
    default_interval: float

class TasksConfig(TypedDict, total=False):
    test_task: bool
    shop_task: bool
    arena_task: bool
    simulation_task: bool
    interception_task: bool
    reward_task: bool
    event_task: bool
    tower_task: bool
    cleanup_task: bool
    login_task: bool

class TogglesConfig(TypedDict, total=False):
    AutoStartNikke: int
    Timedstart: int
    ShopCash: int
    ShopCashFree: int
    ShopCashFreePackage: int
    ShopGeneral: int
    ShopGeneralFree: int
    ShopGeneralDust: int
    ShopGeneralPackage: int
    ShopArena: int
    ShopArenaBookFire: int
    ShopArenaBookWater: int
    ShopArenaBookWind: int
    ShopArenaBookElec: int
    ShopArenaBookIron: int
    ShopArenaBookBox: int
    ShopArenaPackage: int
    ShopArenaFurnace: int
    ShopRecycling: int
    ShopRecyclingGem: int
    ShopRecyclingVoucher: int
    ShopRecyclingResources: int
    ShopRecyclingTeamworkBox: int
    ShopRecyclingKitBox: int
    ShopRecyclingArms: int
    SimulationNormal: int
    SimulationOverClock: int
    AwardArena: int
    ArenaRookie: int
    ArenaSpecial: int
    ArenaChampion: int
    TowerCompany: int
    TowerUniversal: int
    InterceptionNormal: int
    InterceptionAnomaly: int
    InterceptionScreenshot: int
    InterceptionRedCircle: int
    InterceptionExit7: int
    InterceptionReminder: int
    AwardOutpost: int
    AwardOutpostDispatch: int
    AwardAdvise: int
    AwardAdviseAward: int
    AwardAppreciation: int
    AwardFriendPoint: int
    AwardMail: int
    AwardRanking: int
    AwardDaily: int
    AwardPass: int
    AwardFreeRecruit: int
    AwardCooperate: int
    AwardSoloRaid: int
    AutoFill: int
    EventSmall: int
    EventSmallChallenge: int
    EventSmallStory: int
    EventSmallMission: int
    EventLarge: int
    EventLargeSign: int
    EventLargeChallenge: int
    EventLargeStory: int
    EventLargeCooperate: int
    EventLargeMinigame: int
    EventLargeDaily: int
    EventSpecial: int
    EventSpecialSign: int
    EventSpecialChallenge: int
    EventSpecialStory: int
    EventSpecialCooperate: int
    EventSpecialMinigame: int
    EventSpecialDaily: int
    ClearRed: int
    ClearRedRecycling: int
    ClearRedSynchro: int
    ClearRedSynchroForce: int
    ClearRedLimit: int
    ClearRedCube: int
    ClearRedNotice: int
    ClearRedShop: int
    ClearRedWallpaper: int
    ClearRedProfile: int
    ClearRedBla: int
    OpenBlablalink: int
    CheckEvent: int
    DoroClosing: int
    CheckAuto: int
    StoryModeAutoChoose: int
    StoryModeAutoStar: int
    TestModeInitialization: int

class NumericSettings(TypedDict, total=False):
    StartupPath: str
    StartupTime: str
    InterceptionBoss: int
    InterceptionBossNormal: int
    UserLevel: int
    UserGroup: str
    doroGuiX: int
    doroGuiY: int
    TestModeValue: int

class ConfigDict(TypedDict, total=False):
    meta: Dict[str, Any]
    vision: VisionConfig
    tasks: TasksConfig
    toggles: TogglesConfig
    numeric_settings: NumericSettings

DEFAULT_CONFIG: ConfigDict = {
    "meta": {"version": 1},
    "vision": {"default_confidence": 0.8, "default_timeout": 10, "default_interval": 0.5},
    "tasks": {"test_task": True},
    "toggles": {
        "AutoStartNikke": 0,
        "Timedstart": 0,
        "ShopCash": 1,
        "ShopCashFree": 0,
        "ShopCashFreePackage": 0,
        "ShopGeneral": 1,
        "ShopGeneralFree": 0,
        "ShopGeneralDust": 0,
        "ShopGeneralPackage": 0,
        "ShopArena": 1,
        "ShopArenaBookFire": 0,
        "ShopArenaBookWater": 0,
        "ShopArenaBookWind": 0,
        "ShopArenaBookElec": 0,
        "ShopArenaBookIron": 0,
        "ShopArenaBookBox": 0,
        "ShopArenaPackage": 0,
        "ShopArenaFurnace": 0,
        "ShopRecycling": 1,
        "ShopRecyclingGem": 0,
        "ShopRecyclingVoucher": 0,
        "ShopRecyclingResources": 0,
        "ShopRecyclingTeamworkBox": 0,
        "ShopRecyclingKitBox": 0,
        "ShopRecyclingArms": 0,
        "SimulationNormal": 1,
        "SimulationOverClock": 0,
        "AwardArena": 1,
        "ArenaRookie": 0,
        "ArenaSpecial": 0,
        "ArenaChampion": 0,
        "TowerCompany": 1,
        "TowerUniversal": 1,
        "InterceptionNormal": 1,
        "InterceptionAnomaly": 0,
        "InterceptionScreenshot": 0,
        "InterceptionRedCircle": 0,
        "InterceptionExit7": 0,
        "InterceptionReminder": 0,
        "AwardOutpost": 1,
        "AwardOutpostDispatch": 0,
        "AwardAdvise": 0,
        "AwardAdviseAward": 0,
        "AwardAppreciation": 0,
        "AwardFriendPoint": 1,
        "AwardMail": 1,
        "AwardRanking": 0,
        "AwardDaily": 1,
        "AwardPass": 0,
        "AwardFreeRecruit": 0,
        "AwardCooperate": 0,
        "AwardSoloRaid": 0,
        "AutoFill": 0,
        "EventSmall": 0,
        "EventSmallChallenge": 0,
        "EventSmallStory": 0,
        "EventSmallMission": 0,
        "EventLarge": 0,
        "EventLargeSign": 0,
        "EventLargeChallenge": 0,
        "EventLargeStory": 0,
        "EventLargeCooperate": 0,
        "EventLargeMinigame": 0,
        "EventLargeDaily": 0,
        "EventSpecial": 0,
        "EventSpecialSign": 0,
        "EventSpecialChallenge": 0,
        "EventSpecialStory": 0,
        "EventSpecialCooperate": 0,
        "EventSpecialMinigame": 0,
        "EventSpecialDaily": 0,
        "ClearRed": 1,
        "ClearRedRecycling": 0,
        "ClearRedSynchro": 0,
        "ClearRedSynchroForce": 0,
        "ClearRedLimit": 0,
        "ClearRedCube": 0,
        "ClearRedNotice": 0,
        "ClearRedShop": 0,
        "ClearRedWallpaper": 0,
        "ClearRedProfile": 0,
        "ClearRedBla": 0,
        "OpenBlablalink": 0,
        "CheckEvent": 0,
        "DoroClosing": 0,
        "CheckAuto": 0,
        "StoryModeAutoChoose": 0,
        "StoryModeAutoStar": 0,
        "TestModeInitialization": 0,
    },
    "numeric_settings": {
        "StartupPath": "",
        "StartupTime": "",
        "InterceptionBoss": 1,
        "InterceptionBossNormal": 1,
        "UserLevel": 0,
        "UserGroup": "Free",
        "doroGuiX": 0,
        "doroGuiY": 0,
        "TestModeValue": 0,
    },
}

def generate_json_schema() -> Dict[str, Any]:
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "DoroBot Config",
        "type": "object",
        "properties": {
            "meta": {"type": "object", "properties": {"version": {"type": "integer"}}},
            "vision": {
                "type": "object",
                "properties": {
                    "default_confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "default_timeout": {"type": "integer", "minimum": 0},
                    "default_interval": {"type": "number", "minimum": 0},
                },
                "required": ["default_confidence", "default_timeout", "default_interval"],
            },
            "tasks": {"type": "object", "additionalProperties": {"type": "boolean"}},
            "toggles": {"type": "object", "additionalProperties": {"type": "integer", "enum": [0, 1]}},
            "numeric_settings": {"type": "object", "additionalProperties": {"type": ["integer", "number", "string"]}},
        },
        "required": ["meta", "vision", "tasks", "toggles", "numeric_settings"],
        "additionalProperties": False,
    }