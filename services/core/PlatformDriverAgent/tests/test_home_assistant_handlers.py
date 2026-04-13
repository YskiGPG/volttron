"""Unit tests for WriteHandler subclasses and HandlerRegistry.

These tests validate pure Python logic of the Strategy Pattern components
introduced in Sprints 2-3. They do not require a running Home Assistant instance.
"""

import pytest

from platform_driver.interfaces.home_assistant import (
    SwitchHandler,
    LockHandler,
    CoverHandler,
    FanHandler,
    HandlerRegistry,
    create_default_registry,
)


# ---------------------------------------------------------------------------
# SwitchHandler
# ---------------------------------------------------------------------------

class TestSwitchHandler:
    def setup_method(self):
        self.h = SwitchHandler()

    def test_supports(self):
        assert self.h.supports("switch")
        assert not self.h.supports("light")

    def test_value_to_command(self):
        assert self.h.value_to_command(1) == "turn_on"
        assert self.h.value_to_command(0) == "turn_off"

    def test_value_to_command_invalid(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(2)

    def test_get_service_endpoint(self):
        assert self.h.get_service_endpoint("turn_on") == "/api/services/switch/turn_on"
        assert self.h.get_service_endpoint("turn_off") == "/api/services/switch/turn_off"

    def test_get_service_endpoint_invalid(self):
        with pytest.raises(ValueError):
            self.h.get_service_endpoint("toggle")

    def test_build_service_call(self):
        payload = self.h.build_service_call("switch.plug", "turn_on", 1)
        assert payload == {"entity_id": "switch.plug"}


# ---------------------------------------------------------------------------
# LockHandler
# ---------------------------------------------------------------------------

class TestLockHandler:
    def setup_method(self):
        self.h = LockHandler()

    def test_value_to_command(self):
        assert self.h.value_to_command(1) == "lock"
        assert self.h.value_to_command(0) == "unlock"

    def test_value_to_command_invalid_value(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(5)

    def test_value_to_command_non_state_entity_point(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(1, entity_point="position")

    def test_endpoints(self):
        assert self.h.get_service_endpoint("lock") == "/api/services/lock/lock"
        assert self.h.get_service_endpoint("unlock") == "/api/services/lock/unlock"

    def test_endpoint_invalid(self):
        with pytest.raises(ValueError):
            self.h.get_service_endpoint("turn_on")


# ---------------------------------------------------------------------------
# CoverHandler
# ---------------------------------------------------------------------------

class TestCoverHandler:
    def setup_method(self):
        self.h = CoverHandler()

    def test_state_open_close(self):
        assert self.h.value_to_command(1, "state") == "open_cover"
        assert self.h.value_to_command(0, "state") == "close_cover"

    def test_state_invalid(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(2, "state")

    def test_position_valid(self):
        assert self.h.value_to_command(50, "position") == "set_cover_position"
        assert self.h.value_to_command(0, "position") == "set_cover_position"
        assert self.h.value_to_command(100, "position") == "set_cover_position"

    def test_position_out_of_range(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(-1, "position")
        with pytest.raises(ValueError):
            self.h.value_to_command(101, "position")

    def test_unknown_entity_point(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(1, "brightness")

    def test_build_service_call_position(self):
        payload = self.h.build_service_call("cover.blind", "set_cover_position", 75)
        assert payload == {"entity_id": "cover.blind", "position": 75}

    def test_build_service_call_state(self):
        payload = self.h.build_service_call("cover.blind", "open_cover", 1)
        assert payload == {"entity_id": "cover.blind"}


# ---------------------------------------------------------------------------
# FanHandler
# ---------------------------------------------------------------------------

class TestFanHandler:
    def setup_method(self):
        self.h = FanHandler()

    def test_state(self):
        assert self.h.value_to_command(1, "state") == "turn_on"
        assert self.h.value_to_command(0, "state") == "turn_off"

    def test_state_invalid(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(2, "state")

    def test_percentage(self):
        assert self.h.value_to_command(50, "percentage") == "set_percentage"

    def test_percentage_out_of_range(self):
        with pytest.raises(ValueError):
            self.h.value_to_command(-1, "percentage")
        with pytest.raises(ValueError):
            self.h.value_to_command(101, "percentage")

    def test_build_service_call_percentage(self):
        payload = self.h.build_service_call("fan.ceiling", "set_percentage", 40)
        assert payload == {"entity_id": "fan.ceiling", "percentage": 40}


# ---------------------------------------------------------------------------
# HandlerRegistry
# ---------------------------------------------------------------------------

class TestHandlerRegistry:
    def test_get_handler_registered(self):
        registry = HandlerRegistry()
        handler = SwitchHandler()
        registry.register(handler)
        assert registry.get_handler("switch") is handler

    def test_unknown_domain_raises(self):
        registry = HandlerRegistry()
        registry.register(SwitchHandler())
        with pytest.raises(ValueError):
            registry.get_handler("climate")

    def test_create_default_registry(self):
        registry = create_default_registry()
        for domain in ("switch", "lock", "cover", "fan"):
            assert registry.get_handler(domain) is not None
