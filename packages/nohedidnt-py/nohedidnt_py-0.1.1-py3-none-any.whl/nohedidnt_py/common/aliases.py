# -*- coding: utf-8 -*-
from nohedidnt_py.common.imports import *


# Any -----------------------------------------

AnyBox = Union[Box, "AnyDict"]
AnyBytes = Union[bytes, bytearray]
AnyCallable = Callable[..., Any]
AnyData = Union[AnyBox, "AnyList", "AnyTupl"]
AnyDateTime = Union[datetime, str]
AnyDict = Dict[str, Any]
AnyDiffData = Union[DeepDiff, Delta]
AnyEnum = Union[Enum, IntEnum, "StrEnum"]
AnyEnumValue = Union[int, str]
AnyFileData = Union[AnyBox, AnyStr]
AnyKeys = Union["StrList", str]
AnyList = Union[BoxList, List[Any]]
AnyLogHandler = Union[NullHandler, RotatingFileHandler, StreamHandler]
AnyMulti = Union[AnyBox, AnyList, "AnyTupl"]
AnyNhdDate = Union[AnyDateTime, "AnyTimeDelta", "AnyNum"]
AnyNhdVal = Union[AnyData, AnyNhdDate, "AnyPath", "AnyTimezone", "AnyVal", Locale, Timer, type]
AnyNum = Union[float, int]
AnyPath = Union[Path, str]
AnySingleMulti = Union[AnyMulti, "AnyVal"]
AnyTimeDelta = Union[timedelta, AnyNum]
AnyTimezone = Union[BaseTzInfo, ShimTimezone]
AnyTupl = Tuple[Any, ...]
AnyVal = Union[AnyDateTime, AnyNum, AnyStr, property]


# TypeVar(s) ----------------------------------

StrEnum = TypeVar("StrEnum", str, Enum)


# Tuple(s) ------------------------------------

DynamicsTupl = Tuple[Path, Path, str]
HelperTupl = Tuple[AnyCallable, type]
ListTupl = Tuple[AnyList, ...]
PatternTuple = Tuple[Pattern, AnyCallable]
PkgTupl = Tuple[str, str, AnyPath, str]
ReplTupl = Tuple[str, str]
SingleMultiTupl = Tuple[bool, AnySingleMulti]
StrTupl = Tuple[str, ...]


# Dict(s) -------------------------------------

HelperDict = Dict[str, HelperTupl]


# List(s) -------------------------------------

DateTimeList = List[AnyDateTime]
EnumList = List[Type[AnyEnum]]
PathList = List[AnyPath]
ReplList = Union[List[ReplTupl], bool]
StrList = List[str]


# Optional ------------------------------------

OptBaseSettings = Optional[BaseSettings]
OptBool = Optional[bool]
OptBox = Optional[AnyBox]
OptBytes = Optional[AnyBytes]
OptCallable = Optional[AnyCallable]
OptColor = Optional[Color]
OptData = Optional[AnyData]
OptDateTime = Optional[AnyDateTime]
OptDict = Optional[AnyDict]
OptDiffData = Optional[AnyDiffData]
OptEnumValue = Optional[AnyEnumValue]
OptFileData = Optional[AnyFileData]
OptHttpUrl = Optional[AnyHttpUrl]
OptInt = Optional[int]
OptKeys = Optional[AnyKeys]
OptList = Optional[AnyList]
OptLocale = Optional[Locale]
OptLogger = Optional[Logger]
OptLogHandler = Optional[AnyLogHandler]
OptMulti = Optional[AnyMulti]
OptNhdDate = Optional[AnyNhdDate]
OptNhdVal = Optional[AnyNhdVal]
OptNum = Optional[AnyNum]
OptPath = Optional[AnyPath]
OptReplList = Optional[ReplList]
OptReplTupl = Optional[ReplTupl]
OptSingleMulti = Optional[AnySingleMulti]
OptStr = Optional[str]
OptTimeDelta = Optional[AnyTimeDelta]
OptTimer = Optional[Timer]
OptTimezone = Optional[AnyTimezone]
OptTupl = Optional[AnyTupl]
OptType = Optional[type]
OptTzInfo = Optional[BaseTzInfo]
OptVal = Optional[AnyVal]
