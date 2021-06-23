import json
import os
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import bottle
import pytz

app = bottle.app()

DEBUG = str(os.getenv("TS_DEBUG", "")).lower() == "true"
bottle.debug(DEBUG)

bottle.TEMPLATE_PATH.insert(0, os.path.join(Path(__file__).resolve().parent, "templates"))

# get the timezones ordered by offset, -12-0-+12
ordered_timezones = tuple(sorted(pytz.all_timezones, key=lambda tz: pytz.timezone(tz).utcoffset(datetime.now())))

# create a dictionary of areas with a list the locations.
timezone_areas = defaultdict(list)
for zone in ordered_timezones:
    if "/" in zone:
        area, location = zone.split("/", 1)
        timezone_areas[area].append(location)

# create a mapping of lower case areas to their properly named keys
tz_areas_keys_lowercase_map = {k.lower(): k for k in timezone_areas.keys()}


def parse_to_offset(time_str: str):
    """
    Convert an offset String to a timezone.

    :param time_str: offset string +0300
    :type time_str: str

    :return: The utc offset as a timedelta
    :rtype: timedelta

    :raises ValueError: string could not be parsed.
    """
    if not time_str:
        raise ValueError

    is_negative = False
    time_str = time_str.lstrip("+")
    if time_str[0] == "-":
        is_negative = True
    time_str = time_str.lstrip("-")

    if int(time_str) == 0:
        return timedelta(hours=0, minutes=0)

    if 3 <= len(time_str) <= 4:
        minutes = int(time_str[-2:])
        if minutes not in {0, 30, 45}:
            raise ValueError
        hours = int(time_str[:-2])
    else:
        minutes = 0
        hours = int(time_str)

    if not (-12 <= hours <= 12):
        raise ValueError

    if is_negative:
        hours = hours * -1

    return timedelta(hours=hours, minutes=minutes)


def get_offset_str(tz: str):
    """
    Return the timezone offset as a string

    :param tz: A timezone
    :type tz: str

    :return: The offset from UTC
    :rtype: str
    """
    return datetime.now(pytz.timezone(tz)).strftime("%z")


def get_timezones_with_offset():
    """
    Get a map of time zones with offset

    :returns: a dict of timezone name: offset values
    :rtype: dict
    """
    zones = OrderedDict()
    for tz in ordered_timezones:
        zones[tz] = get_offset_str(tz)

    return zones


def render_zones(zones: dict):
    """Render the zones based on accept header"""
    requested_types = bottle.request.headers.get("Accept")

    if "application/json" in requested_types:
        output = json.dumps(zones)
        content_type = "application/json"
    elif "text/html" in requested_types:
        output = bottle.template("zones", zones=zones)
        content_type = "text/html"
    elif "text/csv" in requested_types:
        output = '"timezone","UTC offset"\n' + "\n".join(f'"{k}","{v}"' for k, v in zones.items()) + "\n"
        content_type = "text/csv"
    else:
        output = "\n".join([f"{k}: {v}" for k, v in zones.items()])
        content_type = "text/plain"

    bottle.response.set_header("Content-Type", f"{content_type}; charset=UTF-8")
    return output


@bottle.route("/timezones")
@bottle.route("/timezones/")
@bottle.route("/timezones/<tz_filter:path>")
def get_timezones(tz_filter=None):
    tz_filter = tz_filter.lower().rstrip("/") if tz_filter else tz_filter
    if not tz_filter:
        zones = get_timezones_with_offset()
    elif tz_filter in tz_areas_keys_lowercase_map.keys():
        area_key = tz_areas_keys_lowercase_map[tz_filter]
        zones = OrderedDict()
        for _location in timezone_areas[area_key]:
            tz = f"{area_key}/{_location}"
            zones[tz] = get_offset_str(tz)
    else:
        try:
            utc_offset = parse_to_offset(tz_filter)
        except ValueError:
            utc_offset = None

        if utc_offset is not None:
            now = datetime.now(pytz.utc)
            zones = OrderedDict()
            for tz in map(pytz.timezone, ordered_timezones):
                if now.astimezone(tz).utcoffset() == utc_offset:
                    zones[tz.zone] = get_offset_str(tz.zone)
        else:
            zones = get_timezones_with_offset()

    return render_zones(zones)


@bottle.route("/help")
@bottle.route("/help/")
@bottle.route("/info")
@bottle.route("/info/")
def get_help():
    return bottle.template("help")


@bottle.route("/health")
@bottle.route("/health/")
def health():
    return "OK"


@bottle.route("/")
@bottle.route("/<timezone:path>")
def get_time(timezone="UTC"):
    tz_info = pytz.timezone("UTC")
    timezone = str(timezone).strip()
    if timezone != "UTC":
        if timezone and timezone in pytz.all_timezones:
            tz_info = pytz.timezone(timezone)
    return datetime.now(tz_info).isoformat()


if __name__ == "__main__":  # pragma: no cover
    host = os.getenv("TS_HOST", "127.0.0.1")  # pragma: no cover
    port = os.getenv("TS_PORT", 8182)  # pragma: no cover
    bottle.run(app, server="bjoern", host=host, port=port)  # pragma: no cover
