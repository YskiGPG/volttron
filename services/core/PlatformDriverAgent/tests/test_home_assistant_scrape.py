"""Unit tests for Interface._scrape_all() and Interface.get_point().

get_entity_data() is patched to return fixture data so these tests run
without a Home Assistant instance.
"""

from unittest.mock import patch

import pytest

from platform_driver.interfaces.home_assistant import (
    Interface,
    HomeAssistantRegister,
)


def _make_register(entity_id, entity_point, point_name=None, read_only=False):
    point_name = point_name or f"{entity_id.replace('.', '_')}_{entity_point}"
    return HomeAssistantRegister(
        read_only=read_only,
        pointName=point_name,
        units="",
        reg_type=int,
        attributes={},
        entity_id=entity_id,
        entity_point=entity_point,
    )


def _make_interface(register):
    iface = Interface()
    iface.ip_address = "127.0.0.1"
    iface.access_token = "token"
    iface.port = 8123
    iface.insert_register(register)
    return iface


def _run_scrape(iface, entity_data):
    with patch.object(Interface, "get_entity_data", return_value=entity_data):
        return iface._scrape_all()


# ---------------------------------------------------------------------------
# Switch
# ---------------------------------------------------------------------------

def test_scrape_switch_on():
    reg = _make_register("switch.plug", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "on", "attributes": {}})
    assert result[reg.point_name] == 1


def test_scrape_switch_off():
    reg = _make_register("switch.plug", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "off", "attributes": {}})
    assert result[reg.point_name] == 0


# ---------------------------------------------------------------------------
# Lock
# ---------------------------------------------------------------------------

def test_scrape_lock_locked():
    reg = _make_register("lock.front", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "locked", "attributes": {}})
    assert result[reg.point_name] == 1


def test_scrape_lock_unlocked():
    reg = _make_register("lock.front", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "unlocked", "attributes": {}})
    assert result[reg.point_name] == 0


# ---------------------------------------------------------------------------
# Cover
# ---------------------------------------------------------------------------

def test_scrape_cover_open():
    reg = _make_register("cover.blind", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "open", "attributes": {}})
    assert result[reg.point_name] == 1


def test_scrape_cover_closed():
    reg = _make_register("cover.blind", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "closed", "attributes": {}})
    assert result[reg.point_name] == 0


# ---------------------------------------------------------------------------
# Fan
# ---------------------------------------------------------------------------

def test_scrape_fan_on():
    reg = _make_register("fan.ceiling", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "on", "attributes": {}})
    assert result[reg.point_name] == 1


def test_scrape_fan_attribute_percentage():
    reg = _make_register("fan.ceiling", "percentage")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "on", "attributes": {"percentage": 75}})
    assert result[reg.point_name] == 75


# ---------------------------------------------------------------------------
# Climate / Light / Input boolean regressions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("state,expected", [("off", 0), ("heat", 2), ("cool", 3), ("auto", 4)])
def test_scrape_climate_states(state, expected):
    reg = _make_register("climate.thermo", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": state, "attributes": {}})
    assert result[reg.point_name] == expected


@pytest.mark.parametrize("state,expected", [("on", 1), ("off", 0)])
def test_scrape_light_states(state, expected):
    reg = _make_register("light.kitchen", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": state, "attributes": {}})
    assert result[reg.point_name] == expected


def test_scrape_input_boolean_on():
    reg = _make_register("input_boolean.test", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "on", "attributes": {}})
    assert result[reg.point_name] == 1


# ---------------------------------------------------------------------------
# Unknown domain & invalid state
# ---------------------------------------------------------------------------

def test_scrape_unknown_domain_stores_raw_state():
    reg = _make_register("sensor.temp", "state")
    iface = _make_interface(reg)
    result = _run_scrape(iface, {"state": "23.5", "attributes": {}})
    assert result[reg.point_name] == "23.5"


def test_scrape_invalid_state_logged_not_crashing(caplog):
    reg = _make_register("switch.plug", "state")
    iface = _make_interface(reg)
    # Invalid state: scrape should log the error and skip this register
    # (errors are caught inside the per-register try block).
    result = _run_scrape(iface, {"state": "bogus", "attributes": {}})
    assert reg.point_name not in result


# ---------------------------------------------------------------------------
# get_point()
# ---------------------------------------------------------------------------

def test_get_point_reads_state():
    reg = _make_register("light.kitchen", "state", point_name="light_state")
    iface = _make_interface(reg)
    with patch.object(Interface, "get_entity_data", return_value={"state": "on", "attributes": {}}):
        assert iface.get_point("light_state") == "on"


def test_get_point_reads_attribute():
    reg = _make_register("light.kitchen", "brightness", point_name="light_brightness")
    iface = _make_interface(reg)
    with patch.object(
        Interface,
        "get_entity_data",
        return_value={"state": "on", "attributes": {"brightness": 128}},
    ):
        assert iface.get_point("light_brightness") == 128
