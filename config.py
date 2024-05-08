import configparser
import os

# IMPORTANT: this MUST be tested after any code change
# If an extra sleep is introduced, it might affect the total estimated time
DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT = 420


class ConfigHandler:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_hardener_keys(self):
        keys = self._get_setting("hardener_keys", self.config.get, "")
        return [key.strip() for key in keys.split(",") if key.strip()]

    def get_unlock_all_targets_key(self):
        return self._get_setting("unlock_all_targets_key", self.config.get, "")

    def get_disable_if_no_eve_windows(self):
        return self._get_boolean_setting("disable_if_no_eve_windows", True)

    def get_take_screenshots(self):
        return self._get_boolean_setting("take_screenshots", False)

    def get_cargo_loading_time_adjustment(self):
        return self._get_setting(
            "cargo_loading_time_adjustment",
            self.config.getint,
            DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT,
        )

    def get_mining_runs(self):
        return self._get_setting("mining_runs", self.config.getint, 0)

    def get_undock_coo(self):
        return self._get_coo("undock_coo")

    def get_mining_coo(self):
        return self._get_coo_list("mining_coo")

    def get_warp_to_coo(self):
        return self._get_coo("warp_to_coo")

    def get_clear_cargo_coo(self):
        return self._get_coo("clear_cargo_coo")

    def get_target_one_coo(self):
        return self._get_coo("target_one_coo")

    def get_target_two_coo(self):
        return self._get_coo("target_two_coo")

    def get_mouse_reset_coo(self):
        return self._get_coo("mouse_reset_coo")

    def get_mining_hold(self):
        return self._get_setting("mining_hold", self.config.getint, 0)

    def get_mining_yield(self):
        mining_yield = self._get_setting("mining_yield", self.config.get, "0")
        return float(mining_yield.replace(",", "."))

    def get_mining_reset_timer(self):
        mining_reset_timer = self._get_setting(
            "mining_reset_timer", self.config.get, "120"
        )
        return 2 + int(mining_reset_timer)

    def set_mining_runs(self, value):
        self._set_setting("mining_runs", value)

    def set_undock_coo(self, value):
        self._set_position("undock_coo", value)

    def set_hardener_key(self, value):
        self._set_setting("hardener_key", value)

    def set_warp_to_coo(self, value):
        self._set_position("warp_to_coo", value)

    def set_clear_cargo_coo(self, value):
        self._set_position("clear_cargo_coo", value)

    def set_target_one_coo(self, value):
        self._set_position("target_one_coo", value)

    def set_target_two_coo(self, value):
        self._set_position("target_two_coo", value)

    def set_mouse_reset_coo(self, value):
        self._set_position("mouse_reset_coo", value)

    def set_mining_hold(self, value):
        self._set_setting("mining_hold", str(value))

    def set_mining_yield(self, value):
        self._set_setting("mining_yield", str(value))

    def set_mining_reset_timer(self, value):
        self._set_setting("mining_reset_timer", str(value))

    def set_mining_coo(self, value):
        self._set_position("mining_coo", value)

    def save(self):
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def _get_boolean_setting(self, key, fallback):
        try:
            return self.config.getboolean("SETTINGS", key)
        except configparser.NoOptionError:
            return fallback

    def _get_setting(self, key, conversion_func, fallback):
        try:
            value = self.config.get("SETTINGS", key)
            if value == "":
                return fallback
            else:
                return conversion_func("SETTINGS", key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def _get_coo(self, key):
        coo = self.config.get("POSITIONS", key, fallback="")
        if coo == "":
            return []
        else:
            return [int(x.strip()) for x in coo.split(",")]

    def _get_coo_list(self, key):
        coo_list = self.config.get("POSITIONS", key, fallback="")
        if coo_list == "":
            return []
        else:
            return [
                [int(x.strip()) for x in coo.split(",")] for coo in coo_list.split("\n")
            ]

    def _set_setting(self, key, value):
        self.config.set("SETTINGS", key, str(value))

    def _set_position(self, key, value):
        self.config.set("POSITIONS", key, str(value))
