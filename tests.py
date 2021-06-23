from collections import OrderedDict
from datetime import datetime, timedelta

import pytest
import pytz
from freezegun import freeze_time

import timeservice


def test_health():
    assert timeservice.health() == "OK"


def test_get_help(mocker):
    mocked_template_fn = mocker.patch("timeservice.bottle.template", return_value="<html>")
    help_rtn = timeservice.get_help()
    mocked_template_fn.assert_called_with("help")
    assert help_rtn == "<html>"


@pytest.mark.parametrize(
    ("offset_str", "return_value"),
    (
        ("+0500", timedelta(hours=5)),
        ("+0530", timedelta(hours=5, minutes=30)),
        ("+05", timedelta(hours=5)),
        ("5", timedelta(hours=5)),
        ("0", timedelta(hours=0)),
        ("-0000", timedelta(hours=0)),
        ("+0000", timedelta(hours=0)),
        ("+5", timedelta(hours=5)),
        ("-5", timedelta(hours=-5)),
        ("-05", timedelta(hours=-5)),
    ),
)
def test_parse_to_offset(offset_str, return_value):
    assert timeservice.parse_to_offset(offset_str) == return_value


@pytest.mark.parametrize("invalid_offset_str", ("+1204", "-1400", "12000", "", "NaN", "$4"))
def test_parse_to_offset_raises(invalid_offset_str):
    with pytest.raises(ValueError):
        timeservice.parse_to_offset(invalid_offset_str)


def test_get_offset_str():
    timezone = "America/New_York"

    # freeze time to show differences with DST
    with freeze_time("2021-01-01 00:00:00", tz_offset=0):
        assert timeservice.get_offset_str(timezone) == "-0500"

    with freeze_time("2021-05-01 00:00:00", tz_offset=0):
        assert timeservice.get_offset_str(timezone) == "-0400"


@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def test_get_timezones_with_offset(mocker):
    mocker.patch.object(timeservice, "ordered_timezones", ["America/New_York", "UTC", "Asia/Tehran"])
    zones = timeservice.get_timezones_with_offset()
    expected = OrderedDict([("America/New_York", "-0500"), ("UTC", "+0000"), ("Asia/Tehran", "+0330")])
    assert zones == expected


@pytest.mark.parametrize(
    ("accept", "expected", "content_type"),
    (
        (
            "application/json",
            '{"America/New_York": "-0500", "UTC": "+0000", "Asia/Tehran": "+0330"}',
            "application/json",
        ),
        ("text/html", "template:zones", "text/html"),
        (
            "text/csv",
            '"timezone","UTC offset"\n"America/New_York","-0500"\n"UTC","+0000"\n"Asia/Tehran","+0330"\n',
            "text/csv",
        ),
        ("text/plain", "America/New_York: -0500\nUTC: +0000\nAsia/Tehran: +0330", "text/plain"),
        ("application/pdf", "America/New_York: -0500\nUTC: +0000\nAsia/Tehran: +0330", "text/plain"),
    ),
)
def test_render_zones(accept, expected, content_type, mocker):
    mocker.patch("timeservice.bottle.request.headers.get", return_value=accept)
    set_header = mocker.patch("timeservice.bottle.response.set_header")
    zones = {"America/New_York": "-0500", "UTC": "+0000", "Asia/Tehran": "+0330"}
    if str(expected).startswith("template:"):
        expected = timeservice.bottle.template(expected[9:], zones=zones)
    output = timeservice.render_zones(zones)
    set_header.assert_called_with("Content-Type", f"{content_type}; charset=UTF-8")
    assert output == expected


@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def test_get_time():
    tzinfo = pytz.timezone("UTC")
    utc = datetime.now(tzinfo).isoformat()
    assert timeservice.get_time() == utc

    tzinfo = pytz.timezone("America/New_York")
    nyc = datetime.now(tzinfo).isoformat()
    assert timeservice.get_time("America/New_York") == nyc

    assert timeservice.get_time("Unknown") == utc


@freeze_time("2021-01-01 00:00:00", tz_offset=0)
@pytest.mark.parametrize(
    ("zone", "expected"),
    (
        (None, OrderedDict([("America/New_York", "-0500"), ("UTC", "+0000"), ("Asia/Tehran", "+0330")])),
        ("-05", OrderedDict([("America/New_York", "-0500")])),
        ("asia", OrderedDict([("Asia/Tehran", "+0330")])),
        ("exception", OrderedDict([("America/New_York", "-0500"), ("UTC", "+0000"), ("Asia/Tehran", "+0330")])),
    ),
)
def test_get_timezones(zone, expected, mocker):
    def patched_render_zones(zones, *args, **kwargs):
        return zones

    mocker.patch("timeservice.render_zones", side_effect=patched_render_zones)
    mocker.patch.object(timeservice, "ordered_timezones", ["America/New_York", "UTC", "Asia/Tehran"])
    mocker.patch.object(timeservice, "timezone_areas", {"America": ["New_York"], "Asia": ["Tehran"]})
    mocker.patch.object(timeservice, "tz_areas_keys_lowercase_map", {"america": "America", "asia": "Asia"})
    returned_zones = timeservice.get_timezones(zone)
    assert returned_zones == expected
