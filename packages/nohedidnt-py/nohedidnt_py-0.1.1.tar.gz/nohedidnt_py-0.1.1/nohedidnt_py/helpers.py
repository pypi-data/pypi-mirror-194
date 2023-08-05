# -*- coding: utf-8 -*-
from nohedidnt_py.constants import *


# Logging -------------------------------------


def nhd_debug(msg: str, caller: str = const.PKG_ABBR) -> None:
    """NHD debug function"""

    msg = format_msg(msg, caller, length=const.DISPLAY_COLS)
    debug(msg)


# Data ----------------------------------------


def request_data(url: str = const.URL_STATUS, params: OptDict = None, content: bool = False) -> AnyNhdVal:
    response = requests.get(url, params=params, timeout=10.0, allow_redirects=False)

    if not response.status_code == 200:
        raise ValueError("Invalid status_code")

    if content is True:
        return response.content

    return response.json()


# Dates & Times -------------------------------


def datetime_now(frmt: OptStr = None, tzinfo: BaseTzInfo = UtcTz) -> AnyDateTime:
    dt = datetime.now(tz=tzinfo)

    if frmt is not None:
        return format_datetime(dt, frmt=frmt)

    return dt


def now_floor(miliseconds: bool = False, minutes: int = const.H_MINS, tzinfo: BaseTzInfo = UtcTz) -> OptInt:
    dt_now = datetime_now(tzinfo=tzinfo)

    if isinstance(dt_now, datetime):
        now_floored = math.floor(dt_now.minute / minutes) * minutes

        if miliseconds:
            return now_floored * const.MIN_SECS * const.SEC_MILSECS

        return now_floored

    return None


def timestamp_now(tzinfo: BaseTzInfo = UtcTz) -> OptInt:
    dt_now = datetime_now(tzinfo=tzinfo)

    if isinstance(dt_now, datetime):
        return timestamp_from_value(dt_now) * 1000

    return None


def get_total_time(name: str = const.PKG_NAME) -> float:
    if Timer.timers is None or len(Timer.timers) == 0:
        raise ValueError("Missing Timer.timers")

    if name not in Timer.timers.keys():
        raise KeyError("Invalid name")

    total_time = Timer.timers.total(name)
    if not isinstance(total_time, float):
        total_time = float()

    return total_time


# Factories -----------------------------------


@nhd_factories.register("box")
def nhd_box(box_type: NhdBoxType = NhdBoxType.default, keys: OptList = None, values: OptList = None) -> Box:
    if box_type == NhdBoxType.default:
        return_box = Box(default_box=True, default_box_none_transform=False)
    else:
        return_box = Box()

    if keys is not None and values is not None:
        if not len(keys) == len(values):
            raise ValueError("Different length of keys & values")

        for key in keys:
            return_box[key] = values[keys.index(key)]

    return return_box


@nhd_factories.register("timer")
def nhd_timer(name: str = const.PKG_ABBR, text: str = const.MESSAGES.get("timer", const.PKG_TITLE), logger: OptCallable = nhd_debug, start: bool = True) -> Timer:
    timer = Timer(name=name, text=text, logger=logger)  # type: ignore

    if start is True:
        timer.start()

    return timer


# Formatting ----------------------------------


def format_datetime(dt: datetime, frmt: str = const.DT_FORMAT) -> str:
    return dt.strftime(frmt)


def format_msg(msg: str, caller: str = const.PKG_ABBR, length: OptInt = None, frmt: str = const.MSG_FORMAT, title: bool = False) -> str:
    # Caller
    if caller in msg:
        msg = msg.replace(caller, "").strip()

    if len(caller) > const.CALL_LEN:
        caller = caller[: const.CALL_LEN - 1]

    # Convert to Title
    if title is True and caller.istitle() is False:
        caller = caller.title()

    # Shorten Message
    # TODO Use shorten_value()
    if length is not None:
        length -= len(caller) + len(const.CALL_CHR)

        if len(msg) > length:
            msg = msg[: length]

    return frmt.format(caller, msg)


def format_string(value: Any, length: OptInt = None, replacements: OptReplList = True, lower: bool = False, unquote: bool = False) -> str:
    if not isinstance(value, str):
        value = string_from_value(value)

        if not isinstance(value, str):
            raise ValueError("Invalid value")

    value = string_replace(value, replacements=replacements, unquote=unquote)

    if length is not None:
        value = shorten_value(value, length=length)

        if not isinstance(value, str):
            raise TypeError("Invalid value")

    if lower is True:
        value = value.lower()

    return value


# TypeConversions -----------------------------


@nhd_type_conversions.register("bool")
def bool_from_value(value: AnyVal) -> bool:
    if not isinstance(value, bool):
        value = bool(value) or False

    return value


@nhd_type_conversions.register("box")
def box_from_value(value: AnyNhdVal, keys: OptKeys = None) -> Box:
    if not isinstance(value, Box):
        result_box = nhd_box()
        keys = nhd_keys(keys)

        if isinstance(value, dict):
            return Box(**value)

        if not isinstance(value, list):
            value = list_from_value(value)

        if isinstance(value, list):
            for item in value:
                if keys is not None:
                    item_name = keys[value.index(item)]
                else:
                    item_name = nhd_cls_name(item, lower=True)

                if isinstance(item_name, str):
                    result_box[item_name] = item

        value = result_box

        if not isinstance(value, Box):
            raise TypeError("Invalid value")

    return value


@nhd_type_conversions.register("color")
def color_from_value(value: AnyVal) -> OptColor:
    if not isinstance(value, str):
        value = string_from_value(value)

        if not isinstance(value, str):
            raise ValueError("Invalid value")

    value = parse_value(value, empty=True)
    if value is None or not isinstance(value, str):
        raise ValueError("Invalid value")

    color = Color(value) or None
    
    if not isinstance(color, Color) and 2 < len(value) <= 6:
        if "#" not in value:
            value = f"#{value}"
        
        value = string_patterns(value, pattern_keys=["hex_color"])
    
    color = Color(value) or Color("black")

    return color


@nhd_type_conversions.register("continent")
def continent_from_value(value: AnyVal) -> Any:
    """Inspired by: https://stackoverflow.com/questions/55910004/get-continent-name-from-country-using-pycountry"""

    if not isinstance(value, str):
        value = string_from_value(value)

        if not isinstance(value, str):
            raise ValueError("Invalid value")

    alpha2 = pycountry_convert.country_name_to_country_alpha2(value)
    continent_code = pycountry_convert.country_alpha2_to_continent_code(alpha2)
    continent_name = pycountry_convert.convert_continent_code_to_continent_name(continent_code)

    if not isinstance(continent_name, str):
        raise TypeError("Invalid continent_name")

    return enum_from_value(NhdContinent, continent_name)


@nhd_type_conversions.register("country")
def country_from_value(value: AnyVal) -> Any:
    if not isinstance(value, str):
        value = string_from_value(value)

    return pycountry.countries.lookup(value)


@nhd_type_conversions.register("datetime")
def datetime_from_value(value: AnyVal, frmt: str = const.DT_FORMAT) -> AnyDateTime:
    dt: Any = datetime_now(frmt=frmt)

    if isinstance(value, datetime):
        dt = value

    if value is None or not isinstance(value, (float, int, str)):
        raise ValueError("Invalid value")

    if isinstance(value, int):
        if len(str(value)) == 13:
            value = value / 1000

        dt = datetime.utcfromtimestamp(value)

    elif isinstance(value, str):
        if isinstance(dt, str):
            value = format_string(value, length=len(dt), replacements=[("T", " "), ("Z", "")])
            dt = datetime.strptime(value, frmt)

    if isinstance(dt, datetime) and dt.tzinfo is None:
        dt = dt.astimezone(tz=UtcTz)

    return dt


@nhd_type_conversions.register("enum")
def enum_from_value(enum: Type[Enum], value: OptEnumValue) -> Optional[AnyEnum]:
    enum_item = enum(-99)
    checked_value = parse_value(value, empty=True)
    if checked_value is None or not isinstance(checked_value, (int, str)):
        raise ValueError("Invalid checked_value")

    value = checked_value
    enum_allowed = Box(
        name=[e.name for e in list(enum) if isinstance(e, Enum) and not e == enum_item],  # type: ignore
        value=[e.value for e in list(enum) if isinstance(e, Enum) and not e == enum_item],  # type: ignore
    )

    if isinstance(value, int) and value in enum_allowed.value:
        enum_item = enum(value)
    elif isinstance(value, str):
        value = format_string(value, replacements=[(" ", "_")], lower=True)

        if not (value == "default" and "default" not in enum_allowed.name) and value in enum_allowed.name:
            enum_item = enum[value]

    return enum_item


@nhd_type_conversions.register("float")
def float_from_value(value: AnyVal) -> float:
    if not isinstance(value, (datetime, float, property)):
        value = float(value) or float()

    if not isinstance(value, float):
        value = float()

    return value


@nhd_type_conversions.register("int")
def int_from_value(value: AnyVal) -> int:
    if not isinstance(value, (datetime, int, property)):
        if isinstance(value, str) and value.isdecimal() and "." in value:
            i = value.find(".")
            if i > 0:
                value = value[:i]

        value = int(value) or int()

    if not isinstance(value, int):
        value = int()

    return value


@nhd_type_conversions.register("list")
def list_from_value(value: AnyNhdVal) -> AnyList:
    if not isinstance(value, list):
        if isinstance(value, tuple):
            value = list(value)
        else:
            value = [value]

    if not isinstance(value, list):
        value = list()

    return value


@nhd_type_conversions.register("locale")
def locale_from_value(value: AnyVal) -> Locale:
    if not isinstance(value, str):
        value = string_from_value(value)

    return Locale.parse(value)


@nhd_type_conversions.register("path")
def path_from_value(value: AnyVal) -> Path:
    if not isinstance(value, Path):
        if not isinstance(value, str):
            value = string_from_value(value)

        if isinstance(value, str):
            value = Path(value)

    if not isinstance(value, Path):
        value = Path()

    return value


@nhd_type_conversions.register("string")
def string_from_value(value: AnyVal) -> str:
    value = parse_value(value, empty=True)
    if not isinstance(value, str):
        value = str(value) or str()

    return value


@nhd_type_conversions.register("territory")
def territory_from_value(value: AnyVal) -> Any:
    if not isinstance(value, str):
        value = string_from_value(value)
    
    if not value.isupper():
        value = value.upper()
    
    return const.LOCALE_DFT.territories[value]


@nhd_type_conversions.register("timestamp")
def timestamp_from_value(value: AnyVal) -> int:
    """
    DOCS Summary

    DOCS Description

    TODO Test(s)
    """

    if isinstance(value, str):
        dt = datetime_from_value(value)

        if isinstance(dt, datetime):
            value = dt

    if isinstance(value, datetime):
        return math.ceil(value.timestamp())

    return 0


# Parsing -------------------------------------


def convert_units(value: AnyNum, units_key: str) -> OptNum:
    swapped: bool = False

    if const.CONVERSIONS.factor is None or const.CONVERSIONS.precision is None or const.CONVERSIONS.offset is None:
        raise ValueError("Missing const.CONVERSIONS")

    if units_key not in const.CONVERSIONS.factor.keys():
        key_parts = units_key.split("_")

        if not len(key_parts) == 2:
            raise ValueError("Invalid key_parts")

        key_parts.reverse()
        swapped_key = "_".join(key_parts)

        if swapped_key not in const.CONVERSIONS.factor.keys():
            raise ValueError("Invalid swapped_key")

        swapped = True
        units_key = swapped_key

    precision = const.CONVERSIONS.precision.get(units_key, 2)
    factor = const.CONVERSIONS.factor.get(units_key, 1)
    offset = const.CONVERSIONS.offset.get(units_key, 0)

    if swapped is True:
        factor = round(1 / factor, const.FACTOR_PRECISION)

    return round((value * factor) + offset, precision)


def detect_encoding(value: AnyBytes) -> str:
    chardet_data = chardet.detect(value)
    if not isinstance(chardet_data, dict):
        raise TypeError("Invalid chardet_data")

    chardet_confidence = chardet_data.get("confidence", float())
    chardet_encoding = chardet_data.get("encoding", const.ENCODING_DFT)

    if chardet_confidence < 0.9:
        raise ValueError("Invalid chardet_confidence")

    if not isinstance(chardet_encoding, str):
        raise TypeError("Invalid chardet_encoding")

    return chardet_encoding


def find_empty_values(value: OptNhdVal = None, type_key: str = "str") -> AnyList:
    empty_vals: AnyList = [None]

    if value is not None and not isinstance(value, str):
        type_key = nhd_cls_name(value, lower=True)

    if isinstance(type_key, str):
        empties_vals = const.EMPTIES.get(type_key, list())

        if not isinstance(empties_vals, list):
            empties_vals = list_from_value(empties_vals)

        if isinstance(empties_vals, list):
            empty_vals.extend(const.EMPTIES.get(type_key, list()))

    return empty_vals


def kill_duplicates(value: AnyNhdVal) -> AnyNhdVal:
    keys: StrList = list()
    single, value = nhd_single_multi(value)
    
    if isinstance(value, (dict, list)):
        args_value = value.copy()

        if isinstance(value, dict):
            keys.extend(value.keys())
            value = list(value.values())

        if isinstance(value, list) and isinstance(args_value, list):
            for item in value.copy():
                count = value.count(item)
                index = args_value.index(item)

                while count > 1:
                    duplicate_index = value.index(item, index)

                    if len(keys) > 0:
                        keys.pop(duplicate_index)

                    value.pop(duplicate_index)
                    count = value.count(item)

                if isinstance(item, (dict, list)) and len(item) > 0:
                    item = kill_duplicates(item)

                value[index] = item

            if len(keys) > 0:
                value = nhd_box(box_type=NhdBoxType.default, keys=keys, values=value)

        if not isinstance(value, type(args_value)):
            # IDEA Log
            value = args_value

    if single is True and isinstance(value, list):
        value = value.pop(0)

    return value


def kill_empties(value: Any) -> Any:
    keys: StrList = list()
    single, value = nhd_single_multi(value)
    
    if isinstance(value, (dict, list)):
        args_value = value.copy()

        if isinstance(value, dict):
            keys.extend(value.keys())
            value = list(value.values())

        if isinstance(value, list):
            for item in value.copy():
                index = value.index(item)

                # TODO Use parse_value()
                if item in find_empty_values(item):
                    if len(keys) > 0:
                        keys.pop(index)

                    value.remove(item)
                    continue

                if isinstance(item, (dict, list)) and len(item) > 0:
                    item = parse_value(item, empty=True)

                value[index] = item

            if len(keys) > 0:
                value = nhd_box(box_type=NhdBoxType.default, keys=keys, values=value)

        if not isinstance(value, type(args_value)):
            # IDEA Log
            value = args_value

    if single is True and isinstance(value, list):
        value = value.pop(0)

    return value


def nhd_alternatives(value: AnyKeys) -> StrList:
    alternatives: StrList = list()

    if isinstance(value, list):
        for item in value:
            alternatives.extend([alt for alt in nhd_alternatives(item) if alt not in alternatives])

        return alternatives

    if not isinstance(value, str):
        value = string_from_value(value)

        if not isinstance(value, str):
            raise ValueError("Invalid value")

    if value not in alternatives:
        alternatives.append(value)

    if value.islower() is False:
        if value.lower() not in alternatives:
            alternatives.append(value.lower())

        if value.lower().title() not in alternatives:
            alternatives.append(value.lower().title())

    if value.istitle() is False and value.title() not in alternatives:
        alternatives.append(value.title())

    if value.isupper() is False and value.upper() not in alternatives:
        alternatives.append(value.upper())

    return alternatives


def nhd_cls_name(value: Any, replacements: OptReplList = True, lower: bool = False) -> str:
    value_cls = getattr(value, "__class__", None)
    if value_cls is not None:
        cls_name = getattr(value_cls, "__name__", None)
        if cls_name is not None and "Meta" not in cls_name:
            value = value_cls

    name = getattr(value, "__name__", const.PKG_ABBR)

    for dirty in const.DIRTIES.get("cls_name", list()):
        if dirty in name:
            raise ValueError(f"Invalid name: {name}")

    if lower is True:
        if const.PKG_ABBR in name and not name == const.PKG_ABBR:
            if replacements is None:
                replacements = list()

            if isinstance(replacements, list):
                replacements.append((const.PKG_ABBR, ""))

        name = string_kill_camel(name, replacements=replacements, lower=lower)

    return name


def nhd_keys(value: OptKeys = None, required: OptKeys = None) -> StrList:
    key_list: StrList = list()

    if value is None or not isinstance(value, list):
        value = list_from_value(value)

    if required is not None:
        if not isinstance(required, list):
            required = list_from_value(required)

        if isinstance(required, list):
            key_list.extend(required)

    if value is not None and len(value) > 0:
        key_list.extend(value)

    if len(key_list) > 0:
        clean_list = parse_value(key_list)
        if isinstance(clean_list, list):
            key_list = clean_list

        for item in key_list:
            item = format_string(item, length=const.KEY_LEN, replacements=False, lower=True)
            key_list[key_list.index(item)] = item

    return key_list


def nhd_replacements(value: OptKeys = None) -> ReplList:
    part_list: StrList = list()
    replace_list: ReplList = list()
    term_list: StrList = list()

    if value is None:
        value = [const.PKG_ABBR, const.PKG_AUTHOR, const.PKG_NAME]
    elif not isinstance(value, list):
        value = list_from_value(value)

    for item in value:
        part_list.extend([part for part in item.split("_") if part not in part_list] if "_" in item else list())
        term_list.extend([alt for alt in nhd_alternatives(item) if alt not in term_list])

    # Parts
    if len(part_list) > 0:
        part_list.sort()

        for part in part_list:
            term_list.extend([alt for alt in nhd_alternatives(part) if alt not in term_list])

    if isinstance(replace_list, list):
        # Chars
        for char in const.REPL_CHRS:
            replace_list.append((char, ""))

        # Terms
        if len(term_list) > 0:
            term_list.sort()

            for term in term_list:
                replace_list.append((term, ""))

    return replace_list


def nhd_single_multi(value: Any) -> SingleMultiTupl:
    single: bool = False
    
    if not isinstance(value, (dict, list)):
        single = True
        value = list_from_value(value)
    
    return single, value


def parse_value(value: Any, empty: bool = False) -> Any:
    keys: StrList = list()
    single, value = nhd_single_multi(value)

    if isinstance(value, (dict, list)):
        args_value = value.copy()

        if isinstance(value, dict):
            keys.extend(value.keys())
            value = list(value.values())

        if isinstance(value, list):
            clean_value = kill_duplicates(value)
            if isinstance(clean_value, list):
                value = clean_value

            if empty is True and isinstance(value, list):
                clean_value = kill_empties(value)
                if isinstance(clean_value, list):
                    value = clean_value

            if len(keys) > 0:
                value = nhd_box(box_type=NhdBoxType.default, keys=keys, values=value)

        if not isinstance(value, type(args_value)):
            # IDEA Log
            value = args_value

    if single is True and isinstance(value, list):
        value = value.pop(0)

    return value


def shorten_value(value: AnyNhdVal, length: int = 2) -> AnyNhdVal:
    """
    DOCS Summary

    DOCS Description

    TODO Test(s)
    """

    if not isinstance(value, (dict, list, str)):
        value = string_from_value(value)

    if isinstance(value, dict) and len(value) > length:
        keys = list(value.keys())[length:]

        for key in keys:
            del value[key]

    elif isinstance(value, (list, str)) and len(value) > length:
        value = value[: length]

    return value


def string_kill_camel(value: Any, replacements: OptReplList = True, lower: bool = True) -> str:
    value = format_string(value, replacements=replacements, unquote=True)
    value = string_patterns(value, pattern_keys=["first_cap", "all_cap"])
    value = string_patterns(value, pattern_keys=["space_cap"], lower=lower)

    return value


def string_kill_snake(value: str) -> str:
    """Inspired by: https://docs.pydantic.dev/usage/model_config/#alias-generator"""

    return "".join(word.capitalize() for word in value.split(const.SNK_CHR))


def string_kill_vowels(value: str, lower: bool = False) -> str:
    return string_patterns(value, pattern_keys=["vowels"], lower=lower)


def string_patterns(value: str, pattern_keys: OptKeys = None, lower: bool = False) -> str:
    pattern_keys = nhd_keys(pattern_keys)

    if lower is True:
        value = value.lower()

    if isinstance(pattern_keys, list):
        for key in pattern_keys:
            pattern_tuple = const.PATTERNS.get(key, None)

            if isinstance(pattern_tuple, tuple) and len(pattern_tuple) == 2:
                pattern_args: Any = list()
                pattern, pattern_method = pattern_tuple

                if pattern is None or not isinstance(pattern, Pattern):
                    raise ValueError("Invalid pattern")

                pattern_args.append(pattern)

                if pattern_method is None or not callable(pattern_method):
                    raise ValueError("Invalid pattern_method")

                if pattern_method == re.sub:
                    pattern_args.append(r"\1_\2")

                pattern_args.append(value)
                value = pattern_method(*pattern_args)

    return value


def string_replace(value: str, replacements: OptReplList = True, unquote: bool = False) -> str:
    if unquote is True:
        value = urllib.parse.unquote_plus(value)

    if replacements is True:
        replacements = nhd_replacements()

    if replacements is not False:
        if not isinstance(replacements, list):
            replacements = list_from_value(replacements)

        for replacement in replacements:
            if len(replacement) == 2 and not value == replacement[0]:
                value = value.replace(*replacement).strip()

    return value


def within_margin(value_a: Any, value_b: Any = None) -> bool:
    delta, margin = None, None

    if value_b is None:
        if isinstance(value_a, datetime):
            value_b = datetime_now()

            if value_a.tzinfo is None or not value_a.tzinfo == value_b.tzinfo:
                value_a = value_a.replace(tzinfo=value_b.tzinfo)

        elif isinstance(value_a, float):
            value_b = float()
        elif isinstance(value_a, int):
            value_b = int()

    if not isinstance(value_a, type(value_b)):
        raise TypeError("Invalid types")

    if value_a > value_b:
        delta = value_a - value_b
    else:
        delta = value_b - value_a

    if delta is not None:
        delta_key = string_kill_camel(nhd_cls_name(delta))

        if isinstance(delta_key, str):
            margin = const.MARGINS.get(delta_key)

    if margin is None:
        margin = max(value_a, value_b) * const.MARGIN_FACTOR

    if isinstance(value_a, int) and isinstance(margin, float):
        margin = round(margin)

    if delta is not None and margin is not None and isinstance(delta, type(margin)) and delta <= margin:
        return True

    return False


# Paths ---------------------------------------


def folder_contents(folder_path: Path, subfixxes: OptList = None, subfolders: bool = False) -> Box:
    folder_box = Box()
    
    for folder_item in folder_path.iterdir():
        if folder_item.name in const.DIRTIES.get("path_name", list()) or "cache" in folder_item.name:
            continue
        
        if folder_item.is_dir():
            if subfolders is True:
                folder_box[folder_item.name] = folder_contents(folder_item, subfixxes=subfixxes, subfolders=subfolders)
                continue
            
            folder_box[folder_item.name] = folder_item
        
        if folder_item.is_file():
            if subfixxes is not None and folder_item.suffix not in subfixxes:
                continue
            
            folder_box[folder_item.name] = folder_item
    
    return folder_box
