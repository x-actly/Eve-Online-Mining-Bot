import configparser
import os
from typing import Any, Callable, List

from loguru import logger

# CONSTANTS

# IMPORTANT: this MUST be tested after any code change
# If an extra sleep is introduced, it might affect the total estimated time
_DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT = 350

# Default value for expected warping time to belt, the time to sleep after warping
_DEFAULT_WARPING_TIME = 70.0


class ConfigHandler:
    def __init__(self, config_path):  # type: ignore
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_log_level(self) -> str:
        return self._get_setting("log_level", self.config.get, "INFO")  # type: ignore

    def get_hardener_keys(self) -> List[str]:
        keys = self._get_setting("hardener_keys", self.config.get, "")
        return [key.strip() for key in keys.split(",") if key.strip()]

    def get_unlock_all_targets_key(self) -> str:
        return self._get_setting("unlock_all_targets_key", self.config.get, "")  # type: ignore

    def get_take_screenshots(self) -> bool:
        return self._get_boolean_setting("take_screenshots", False)

    def get_auto_reset_miners(self) -> bool:
        return self._get_boolean_setting("auto_reset_miners", True)

    def get_cargo_loading_time_adjustment(self) -> int:
        default = _DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT + self.get_warping_time()
        return self._get_setting("cargo_loading_time_adjustment", self.config.getint, default)  # type: ignore

    def get_mining_runs(self) -> int:
        return self._get_setting("mining_runs", self.config.getint, 0)  # type: ignore

    def get_undock_coo(self) -> List[int]:
        return self._get_coo("undock_coo")

    def get_mining_coo(self) -> List[List[int]]:
        return self._get_coo_list("mining_coo")

    def get_home_coo(self) -> List[int]:
        return self._get_coo("warp_to_coo")

    def get_clear_cargo_coo(self) -> List[int]:
        return self._get_coo("clear_cargo_coo")

    def get_target_one_coo(self) -> List[int]:
        return self._get_coo("target_one_coo")

    def get_target_two_coo(self) -> List[int]:
        return self._get_coo("target_two_coo")

    def get_mouse_reset_coo(self) -> List[int]:
        return self._get_coo("mouse_reset_coo")

    def get_mining_hold(self) -> int:
        return self._get_setting("mining_hold", self.config.getint, 0)  # type: ignore

    def get_mining_yield(self) -> float:
        return self._get_setting("mining_yield", self.config.getfloat, 0.0)  # type: ignore

    def get_mining_reset_timer(self) -> int:
        return 2 + self._get_setting("mining_reset_timer", self.config.getint, 120)  # type: ignore

    def get_warping_time(self) -> int:
        return self._get_setting("warping_time", self.config.getfloat, _DEFAULT_WARPING_TIME)  # type: ignore

    def set_mining_runs(self, value: str) -> None:
        self._set_setting("mining_runs", value)

    def set_undock_coo(self, value: str) -> None:
        self._set_position("undock_coo", value)

    def set_home_coo(self, value: str) -> None:
        self._set_position("warp_to_coo", value)

    def set_clear_cargo_coo(self, value: str) -> None:
        self._set_position("clear_cargo_coo", value)

    def set_target_one_coo(self, value: str) -> None:
        self._set_position("target_one_coo", value)

    def set_target_two_coo(self, value: str) -> None:
        self._set_position("target_two_coo", value)

    def set_mouse_reset_coo(self, value: str) -> None:
        self._set_position("mouse_reset_coo", value)

    def set_mining_hold(self, value: str) -> None:
        self._set_setting("mining_hold", value)

    def set_mining_yield(self, value: str) -> None:
        self._set_setting("mining_yield", value)

    def set_mining_coo(self, value: str) -> None:
        self._set_position("mining_coo", value)

    def save(self) -> None:
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def _get_boolean_setting(self, key: str, fallback: bool) -> bool:
        try:
            return self.config.getboolean("SETTINGS", key)
        except configparser.NoOptionError:
            logger.warning(
                "Couldn't read {key} from settings, using default: {fallback}",
                key=key,
                fallback=fallback,
            )
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
            logger.warning(
                "Couldn't read {key} from settings, using default: {fallback}",
                key=key,
                fallback=fallback,
            )
            return fallback

    def _get_coo(self, key: str) -> List[int]:
        coo = self.config.get("POSITIONS", key, fallback="")
        if coo == "":
            return []
        else:
            return [int(x.strip()) for x in coo.split(",")]

    def _get_coo_list(self, key: str) -> List[List[int]]:
        coo_list = self.config.get("POSITIONS", key, fallback="")
        if coo_list == "":
            return []
        else:
            return [
                [int(x.strip()) for x in coo.split(",")] for coo in coo_list.split("\n")
            ]

    def _set_setting(self, key: str, value: str) -> None:
        self.config.set("SETTINGS", key, value)

    def _set_position(self, key: str, value: str) -> None:
        self.config.set("POSITIONS", key, value)
