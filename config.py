import configparser
import os
from typing import Any, Callable

# IMPORTANT: this MUST be tested after any code change
# If an extra sleep is introduced, it might affect the total estimated time
DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT = 420


class ConfigHandler:
    def __init__(self, config_path): # type: ignore
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_hardener_keys(self) -> list[str]:
        keys = self._get_setting("hardener_keys", self.config.get, "")
        return [key.strip() for key in keys.split(",") if key.strip()]

    def get_unlock_all_targets_key(self) -> str:
        return str(self._get_setting("unlock_all_targets_key", self.config.get, ""))

    def get_take_screenshots(self) -> bool:
        return self._get_boolean_setting("take_screenshots", False)

    def get_cargo_loading_time_adjustment(self) -> int:
        return int(
            self._get_setting(
                "cargo_loading_time_adjustment",
                self.config.getint,
                DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT,
            )
        )

    def get_mining_runs(self) -> int:
        return int(self._get_setting("mining_runs", self.config.getint, 0))

    def get_undock_coo(self) -> list[int]:
        return self._get_coo("undock_coo")

    def get_mining_coo(self) -> list[list[int]]:
        return self._get_coo_list("mining_coo")

    def get_warp_to_coo(self) -> list[int]:
        return self._get_coo("warp_to_coo")

    def get_clear_cargo_coo(self) -> list[int]:
        return self._get_coo("clear_cargo_coo")

    def get_target_one_coo(self) -> list[int]:
        return self._get_coo("target_one_coo")

    def get_target_two_coo(self) -> list[int]:
        return self._get_coo("target_two_coo")

    def get_mouse_reset_coo(self) -> list[int]:
        return self._get_coo("mouse_reset_coo")

    def get_mining_hold(self) -> int:
        return int(self._get_setting("mining_hold", self.config.getint, 0))

    def get_mining_yield(self) -> float:
        mining_yield = self._get_setting("mining_yield", self.config.get, "0")
        return float(mining_yield.replace(",", "."))

    def get_mining_reset_timer(self) -> int:
        mining_reset_timer = self._get_setting(
            "mining_reset_timer", self.config.get, "120"
        )
        return 2 + int(mining_reset_timer)

    def set_mining_runs(self, value: int) -> None:
        self._set_setting("mining_runs", value)

    def set_undock_coo(self, value: list[int]) -> None:
        self._set_position("undock_coo", value)

    def set_hardener_key(self, value: str) -> None:
        self._set_setting("hardener_key", value)

    def set_warp_to_coo(self, value: list[int]) -> None:
        self._set_position("warp_to_coo", value)

    def set_clear_cargo_coo(self, value: list[int]) -> None:
        self._set_position("clear_cargo_coo", value)

    def set_target_one_coo(self, value: list[int]) -> None:
        self._set_position("target_one_coo", value)

    def set_target_two_coo(self, value: list[int]) -> None:
        self._set_position("target_two_coo", value)

    def set_mouse_reset_coo(self, value: list[int]) -> None:
        self._set_position("mouse_reset_coo", value)

    def set_mining_hold(self, value: int) -> None:
        self._set_setting("mining_hold", str(value))

    def set_mining_yield(self, value: float) -> None:
        self._set_setting("mining_yield", str(value))

    def set_mining_reset_timer(self, value: int) -> None:
        self._set_setting("mining_reset_timer", str(value))

    def set_mining_coo(self, value: list[list[int]]) -> None:
        self._set_position("mining_coo", value)

    def save(self) -> None:
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def _get_boolean_setting(self, key: str, fallback: bool) -> bool:
        try:
            return self.config.getboolean("SETTINGS", key)
        except configparser.NoOptionError:
            return fallback

    def _get_setting(
        self, key: str, conversion_func: Callable[[str, str], Any], fallback: Any
    ) -> Any:
        try:
            value = self.config.get("SETTINGS", key)
            if value == "":
                return fallback
            else:
                return conversion_func("SETTINGS", key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def _get_coo(self, key: str) -> list[int]:
        coo = self.config.get("POSITIONS", key, fallback="")
        if coo == "":
            return []
        else:
            return [int(x.strip()) for x in coo.split(",")]

    def _get_coo_list(self, key: str) -> list[list[int]]:
        coo_list = self.config.get("POSITIONS", key, fallback="")
        if coo_list == "":
            return []
        else:
            return [
                [int(x.strip()) for x in coo.split(",")] for coo in coo_list.split("\n")
            ]

    def _set_setting(self, key: str, value: Any) -> None:
        self.config.set("SETTINGS", key, str(value))

    def _set_position(self, key: str, value: list[Any]) -> None:
        self.config.set("POSITIONS", key, str(value))
