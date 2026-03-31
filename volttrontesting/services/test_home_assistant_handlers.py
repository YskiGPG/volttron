import pytest

from services.core.PlatformDriverAgent.platform_driver.interfaces.home_assistant import (
    SwitchHandler,
    LockHandler,
    CoverHandler,
    FanHandler,
    LightHandler,
    ClimateHandler,
    InputBooleanHandler,
    HandlerRegistry,
)


class TestSwitchHandler:
    def test_supports_switch_domain(self):
        handler = SwitchHandler()
        assert handler.supports("switch") is True
        assert handler.supports("lock") is False

    def test_get_service_endpoint_turn_on(self):
        handler = SwitchHandler()
        assert handler.get_service_endpoint("turn_on") == "/api/services/switch/turn_on"

    def test_get_service_endpoint_turn_off(self):
        handler = SwitchHandler()
        assert handler.get_service_endpoint("turn_off") == "/api/services/switch/turn_off"

    def test_get_service_endpoint_invalid_command(self):
        handler = SwitchHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call(self):
        handler = SwitchHandler()
        payload = handler.build_service_call("switch.lamp", "turn_on", 1)
        assert payload == {"entity_id": "switch.lamp"}

    def test_value_to_command_on(self):
        handler = SwitchHandler()
        assert handler.value_to_command(1, "state") == "turn_on"

    def test_value_to_command_off(self):
        handler = SwitchHandler()
        assert handler.value_to_command(0, "state") == "turn_off"

    def test_value_to_command_invalid_value(self):
        handler = SwitchHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")


class TestLockHandler:
    def test_supports_lock_domain(self):
        handler = LockHandler()
        assert handler.supports("lock") is True
        assert handler.supports("switch") is False

    def test_get_service_endpoint_lock(self):
        handler = LockHandler()
        assert handler.get_service_endpoint("lock") == "/api/services/lock/lock"

    def test_get_service_endpoint_unlock(self):
        handler = LockHandler()
        assert handler.get_service_endpoint("unlock") == "/api/services/lock/unlock"

    def test_get_service_endpoint_invalid_command(self):
        handler = LockHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call(self):
        handler = LockHandler()
        payload = handler.build_service_call("lock.front_door", "lock", 1)
        assert payload == {"entity_id": "lock.front_door"}

    def test_value_to_command_lock(self):
        handler = LockHandler()
        assert handler.value_to_command(1, "state") == "lock"

    def test_value_to_command_unlock(self):
        handler = LockHandler()
        assert handler.value_to_command(0, "state") == "unlock"

    def test_value_to_command_invalid_value(self):
        handler = LockHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")

    def test_value_to_command_invalid_entity_point(self):
        handler = LockHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(1, "position")


class TestCoverHandler:
    def test_supports_cover_domain(self):
        handler = CoverHandler()
        assert handler.supports("cover") is True
        assert handler.supports("fan") is False

    def test_get_service_endpoint_open(self):
        handler = CoverHandler()
        assert handler.get_service_endpoint("open_cover") == "/api/services/cover/open_cover"

    def test_get_service_endpoint_close(self):
        handler = CoverHandler()
        assert handler.get_service_endpoint("close_cover") == "/api/services/cover/close_cover"

    def test_get_service_endpoint_set_position(self):
        handler = CoverHandler()
        assert handler.get_service_endpoint("set_cover_position") == "/api/services/cover/set_cover_position"

    def test_get_service_endpoint_invalid_command(self):
        handler = CoverHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call_open(self):
        handler = CoverHandler()
        payload = handler.build_service_call("cover.blinds", "open_cover", 1)
        assert payload == {"entity_id": "cover.blinds"}

    def test_build_service_call_close(self):
        handler = CoverHandler()
        payload = handler.build_service_call("cover.blinds", "close_cover", 0)
        assert payload == {"entity_id": "cover.blinds"}

    def test_build_service_call_set_position(self):
        handler = CoverHandler()
        payload = handler.build_service_call("cover.blinds", "set_cover_position", 75)
        assert payload == {
            "entity_id": "cover.blinds",
            "position": 75,
        }

    def test_value_to_command_open(self):
        handler = CoverHandler()
        assert handler.value_to_command(1, "state") == "open_cover"

    def test_value_to_command_close(self):
        handler = CoverHandler()
        assert handler.value_to_command(0, "state") == "close_cover"

    def test_value_to_command_set_position(self):
        handler = CoverHandler()
        assert handler.value_to_command(50, "position") == "set_cover_position"

    def test_value_to_command_invalid_state_value(self):
        handler = CoverHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")

    def test_value_to_command_invalid_position_value_high(self):
        handler = CoverHandler()
        with pytest.raises(ValueError, match="Expected integer 0-100"):
            handler.value_to_command(101, "position")

    def test_value_to_command_invalid_position_value_low(self):
        handler = CoverHandler()
        with pytest.raises(ValueError, match="Expected integer 0-100"):
            handler.value_to_command(-1, "position")

    def test_value_to_command_invalid_entity_point(self):
        handler = CoverHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(1, "brightness")


class TestFanHandler:
    def test_supports_fan_domain(self):
        handler = FanHandler()
        assert handler.supports("fan") is True
        assert handler.supports("cover") is False

    def test_get_service_endpoint_turn_on(self):
        handler = FanHandler()
        assert handler.get_service_endpoint("turn_on") == "/api/services/fan/turn_on"

    def test_get_service_endpoint_turn_off(self):
        handler = FanHandler()
        assert handler.get_service_endpoint("turn_off") == "/api/services/fan/turn_off"

    def test_get_service_endpoint_set_percentage(self):
        handler = FanHandler()
        assert handler.get_service_endpoint("set_percentage") == "/api/services/fan/set_percentage"

    def test_get_service_endpoint_invalid_command(self):
        handler = FanHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call_turn_on(self):
        handler = FanHandler()
        payload = handler.build_service_call("fan.ceiling_fan", "turn_on", 1)
        assert payload == {"entity_id": "fan.ceiling_fan"}

    def test_build_service_call_turn_off(self):
        handler = FanHandler()
        payload = handler.build_service_call("fan.ceiling_fan", "turn_off", 0)
        assert payload == {"entity_id": "fan.ceiling_fan"}

    def test_build_service_call_set_percentage(self):
        handler = FanHandler()
        payload = handler.build_service_call("fan.ceiling_fan", "set_percentage", 80)
        assert payload == {
            "entity_id": "fan.ceiling_fan",
            "percentage": 80,
        }

    def test_value_to_command_turn_on(self):
        handler = FanHandler()
        assert handler.value_to_command(1, "state") == "turn_on"

    def test_value_to_command_turn_off(self):
        handler = FanHandler()
        assert handler.value_to_command(0, "state") == "turn_off"

    def test_value_to_command_set_percentage(self):
        handler = FanHandler()
        assert handler.value_to_command(60, "percentage") == "set_percentage"

    def test_value_to_command_invalid_state_value(self):
        handler = FanHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")

    def test_value_to_command_invalid_percentage_high(self):
        handler = FanHandler()
        with pytest.raises(ValueError, match="Expected integer 0-100"):
            handler.value_to_command(101, "percentage")

    def test_value_to_command_invalid_percentage_low(self):
        handler = FanHandler()
        with pytest.raises(ValueError, match="Expected integer 0-100"):
            handler.value_to_command(-1, "percentage")

    def test_value_to_command_invalid_entity_point(self):
        handler = FanHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(1, "temperature")


class TestLightHandler:
    def test_supports_light_domain(self):
        handler = LightHandler()
        assert handler.supports("light") is True
        assert handler.supports("switch") is False

    def test_get_service_endpoint_turn_on(self):
        handler = LightHandler()
        assert handler.get_service_endpoint("turn_on") == "/api/services/light/turn_on"

    def test_get_service_endpoint_turn_off(self):
        handler = LightHandler()
        assert handler.get_service_endpoint("turn_off") == "/api/services/light/turn_off"

    def test_get_service_endpoint_invalid_command(self):
        handler = LightHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call_state(self):
        handler = LightHandler()
        payload = handler.build_service_call("light.lamp", "turn_on", 1)
        assert payload == {"entity_id": "light.lamp"}

    def test_build_service_call_brightness(self):
        handler = LightHandler()
        payload = handler.build_service_call("light.lamp", "turn_on", 128)
        assert payload == {
            "entity_id": "light.lamp",
            "brightness": 128,
        }

    def test_value_to_command_on(self):
        handler = LightHandler()
        assert handler.value_to_command(1, "state") == "turn_on"

    def test_value_to_command_off(self):
        handler = LightHandler()
        assert handler.value_to_command(0, "state") == "turn_off"

    def test_value_to_command_brightness(self):
        handler = LightHandler()
        assert handler.value_to_command(128, "brightness") == "turn_on"

    def test_value_to_command_invalid_state_value(self):
        handler = LightHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")

    def test_value_to_command_invalid_brightness_value(self):
        handler = LightHandler()
        with pytest.raises(ValueError, match="Expected integer 0-255"):
            handler.value_to_command(300, "brightness")

    def test_value_to_command_invalid_entity_point(self):
        handler = LightHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(1, "temperature")


class TestInputBooleanHandler:
    def test_supports_input_boolean_domain(self):
        handler = InputBooleanHandler()
        assert handler.supports("input_boolean") is True
        assert handler.supports("light") is False

    def test_get_service_endpoint_turn_on(self):
        handler = InputBooleanHandler()
        assert handler.get_service_endpoint("turn_on") == "/api/services/input_boolean/turn_on"

    def test_get_service_endpoint_turn_off(self):
        handler = InputBooleanHandler()
        assert handler.get_service_endpoint("turn_off") == "/api/services/input_boolean/turn_off"

    def test_get_service_endpoint_invalid_command(self):
        handler = InputBooleanHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call(self):
        handler = InputBooleanHandler()
        payload = handler.build_service_call("input_boolean.test", "turn_on", 1)
        assert payload == {"entity_id": "input_boolean.test"}

    def test_value_to_command_on(self):
        handler = InputBooleanHandler()
        assert handler.value_to_command(1, "state") == "turn_on"

    def test_value_to_command_off(self):
        handler = InputBooleanHandler()
        assert handler.value_to_command(0, "state") == "turn_off"

    def test_value_to_command_invalid_value(self):
        handler = InputBooleanHandler()
        with pytest.raises(ValueError, match="Expected 0"):
            handler.value_to_command(2, "state")

    def test_value_to_command_invalid_entity_point(self):
        handler = InputBooleanHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(1, "brightness")


class TestClimateHandler:
    def test_supports_climate_domain(self):
        handler = ClimateHandler()
        assert handler.supports("climate") is True
        assert handler.supports("fan") is False

    def test_get_service_endpoint_set_hvac_mode(self):
        handler = ClimateHandler()
        assert handler.get_service_endpoint("set_hvac_mode") == "/api/services/climate/set_hvac_mode"

    def test_get_service_endpoint_set_temperature(self):
        handler = ClimateHandler()
        assert handler.get_service_endpoint("set_temperature") == "/api/services/climate/set_temperature"

    def test_get_service_endpoint_invalid_command(self):
        handler = ClimateHandler()
        with pytest.raises(ValueError, match="unsupported command"):
            handler.get_service_endpoint("bad_command")

    def test_build_service_call_off(self):
        handler = ClimateHandler()
        payload = handler.build_service_call("climate.room", "set_hvac_mode", 0)
        assert payload == {"entity_id": "climate.room", "hvac_mode": "off"}

    def test_build_service_call_heat(self):
        handler = ClimateHandler()
        payload = handler.build_service_call("climate.room", "set_hvac_mode", 2)
        assert payload == {"entity_id": "climate.room", "hvac_mode": "heat"}

    def test_build_service_call_cool(self):
        handler = ClimateHandler()
        payload = handler.build_service_call("climate.room", "set_hvac_mode", 3)
        assert payload == {"entity_id": "climate.room", "hvac_mode": "cool"}

    def test_build_service_call_auto(self):
        handler = ClimateHandler()
        payload = handler.build_service_call("climate.room", "set_hvac_mode", 4)
        assert payload == {"entity_id": "climate.room", "hvac_mode": "auto"}

    def test_build_service_call_temperature(self):
        handler = ClimateHandler()
        payload = handler.build_service_call("climate.room", "set_temperature", 72)
        assert payload == {"entity_id": "climate.room", "temperature": 72}

    def test_value_to_command_state(self):
        handler = ClimateHandler()
        assert handler.value_to_command(0, "state") == "set_hvac_mode"
        assert handler.value_to_command(2, "state") == "set_hvac_mode"
        assert handler.value_to_command(3, "state") == "set_hvac_mode"
        assert handler.value_to_command(4, "state") == "set_hvac_mode"

    def test_value_to_command_temperature(self):
        handler = ClimateHandler()
        assert handler.value_to_command(72, "temperature") == "set_temperature"

    def test_value_to_command_invalid_state_value(self):
        handler = ClimateHandler()
        with pytest.raises(ValueError, match="Expected 0, 2, 3, or 4"):
            handler.value_to_command(1, "state")

    def test_value_to_command_invalid_entity_point(self):
        handler = ClimateHandler()
        with pytest.raises(ValueError, match="unsupported entity_point"):
            handler.value_to_command(72, "percentage")


class TestHandlerRegistry:
    def test_register_and_get_switch_handler(self):
        registry = HandlerRegistry()
        switch_handler = SwitchHandler()
        registry.register(switch_handler)

        handler = registry.get_handler("switch")
        assert handler is switch_handler

    def test_register_and_get_multiple_handlers(self):
        registry = HandlerRegistry()
        switch_handler = SwitchHandler()
        lock_handler = LockHandler()
        cover_handler = CoverHandler()
        fan_handler = FanHandler()
        light_handler = LightHandler()
        climate_handler = ClimateHandler()
        input_boolean_handler = InputBooleanHandler()

        registry.register(switch_handler)
        registry.register(lock_handler)
        registry.register(cover_handler)
        registry.register(fan_handler)
        registry.register(light_handler)
        registry.register(climate_handler)
        registry.register(input_boolean_handler)

        assert registry.get_handler("switch") is switch_handler
        assert registry.get_handler("lock") is lock_handler
        assert registry.get_handler("cover") is cover_handler
        assert registry.get_handler("fan") is fan_handler
        assert registry.get_handler("light") is light_handler
        assert registry.get_handler("climate") is climate_handler
        assert registry.get_handler("input_boolean") is input_boolean_handler

    def test_get_handler_unregistered_domain(self):
        registry = HandlerRegistry()
        registry.register(SwitchHandler())

        with pytest.raises(ValueError, match="no handler registered"):
            registry.get_handler("sensor")