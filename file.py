from enum import IntEnum
from pathlib import Path
from typing import Dict, Generic, List, Tuple, TypeVar

from pydantic import BaseModel, Field

from basic_dirs import CONFIG_HOME


class GeneralPinType(IntEnum):
    aways_on_top = 0
    normal = 1
    aways_on_buttom = 2


class HideMode(IntEnum):
    no_hide = 0
    in_class = 1
    has_maximized_window = 2
    dynamic = 3


class HideMethod(IntEnum):
    overflow = 0
    close_window = 1
    to_small_window = 2


class ColorMode(IntEnum):
    light = 0
    dark = 1
    system = 2
    pass


class General(BaseModel):
    schedule: str = "新课表 - 1.json"
    pin_on_top: GeneralPinType = GeneralPinType.normal
    margin: int = 10
    time_offset: int = 0
    opacity: int = 95
    auto_startup: bool = False
    hide: HideMode = HideMode.no_hide
    hide_method: HideMethod = HideMethod.overflow
    color_mode: ColorMode = ColorMode.system
    enable_alt_schedule: bool = False
    blur_floating_countdown: bool = True
    blur_countdown: bool = False
    theme: str = "default"
    scale: float = 1
    excluded_lesson: bool = False

    # TODO: 转为列表格式并在 init 中定义避免出错
    excluded_lessons: str = ""

    enable_click: bool = True


class ToastPinType(IntEnum):
    buttom = 0
    top = 1


class Toast(BaseModel):
    wave: bool = True
    pin_on_top: ToastPinType = ToastPinType.top
    ringtone: int = 1
    prepare_minutes: int = 2
    attend_class: bool = True
    finish_class: bool = True
    prepare_class: bool = True
    after_school: bool = True
    smooth_volume: int = 0


class Weather(BaseModel):
    city: int = 0
    api: str = "xiaomi_weather"
    api_key: str = ""


class Color(BaseModel):
    floating_time: str = "959595"
    attend_class: str = "DD986F"
    finish_class: str = "46B878"
    prepare_class: str = "7065D8"


class Date(BaseModel):
    start_date: str = ""
    cd_text_custom: str = "自定义"
    countdown_date: str = ""
    countdown_upd_cd: int = 30
    countdown_custom_mode: int = 1


class Plugin(BaseModel):
    version: int = 2
    mirror: str = "gh_proxy"
    audo_delay: int = 5
    auto_enable_plugin: bool = True


class Audio(BaseModel):
    volume: int = 75
    attend_class: str = "attend_class.wav"
    finish_class: str = "finish_class.wav"
    prepare_class: str = "prepare_class.wav"


class Temp(BaseModel):
    set_week: str = ""
    temp_schedule: str = ""
    set_schedule: str = ""


class Others(BaseModel):
    do_not_log: bool = False
    safe_mode: bool = False
    initialstartup: bool = True
    multiple_programs: bool = False
    version_channel: int = 0
    auto_check_update: bool = True
    cses_version: int = 1
    version: str = "v1.1.7.2"


class Config(BaseModel):
    general: General = Field(alias="General", default=General())
    toast: Toast = Field(alias="Toast", default=Toast())
    weather: Weather = Field(alias="Weather", default=Weather())
    color: Color = Field(alias="Color", default=Color())
    plugin: Plugin = Field(alias="Plugin", default=Plugin())
    date: Date = Field(alias="Date", default=Date())
    audio: Audio = Field(alias="Audio", default=Audio())
    temp: Temp = Field(alias="Temp", default=Temp())
    others: Others = Field(alias="Others", default=Others())


class ScheduleTimeline(BaseModel):
    # '''注意：每个元素第一次使用的时候必须'''
    default: Dict[str, str] = dict()
    monday: Dict[str, str] = dict()
    tuesday: Dict[str, str] = dict()
    widnesday: Dict[str, str] = dict()
    thursday: Dict[str, str] = dict()
    friday: Dict[str, str] = dict()
    saturday: Dict[str, str] = dict()
    sunday: Dict[str, str] = dict()


class ClassNames(BaseModel):
    monday: List[str] = list()
    tuesday: List[str] = list()
    widnesday: List[str] = list()
    thursday: List[str] = list()
    friday: List[str] = list()
    saturday: List[str] = list()
    sunday: List[str] = list()


class Schedule(BaseModel):
    part: Dict[str, Tuple[int, int, str]] = dict()
    part_name: Dict[str, str] = dict()
    timeline: ScheduleTimeline = ScheduleTimeline()
    schedule: ClassNames = ClassNames()
    schedule_even: ClassNames = ClassNames()


State = TypeVar("State", bound=BaseModel)


class JsonFileState(Generic[State]):
    data: State
    path: Path

    def __init__(self, data: State, path: Path):
        self.data = data
        self.path = path
        if path.exists():
            self.load()
        else:
            self.save()

    def load(self):
        with self.path.open("r", encoding="utf-8") as i:
            self.data = self.data.model_validate_json(i.read())

    def save(self):
        with self.path.open("w", encoding="utf-8") as o:
            o.write(self.data.model_dump_json(indent=2, by_alias=True))


config_center = JsonFileState(Config(), CONFIG_HOME / "config.json")
schedule_center = JsonFileState(
    Schedule(), CONFIG_HOME / "schedule" / config_center.data.general.schedule
)
