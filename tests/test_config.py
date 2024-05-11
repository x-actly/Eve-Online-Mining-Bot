import sys

sys.path.append("..")

from Bot import config


def test_warping_time_is_added_to_default_cargo_loading_time_adjustment():
    cfg = config.ConfigHandler("tests/test_config_with_warping_time.properties")
    actual = cfg.get_cargo_loading_time_adjustment()
    expected = config._DEFAULT_CARGO_LOADING_TIME_ADJUSTMENT + cfg.get_warping_time()
    assert actual == expected
    assert actual == 490


def test_default_warping_time():
    cfg = config.ConfigHandler("tests/test_config_without_warping_time.properties")
    actual = cfg.get_warping_time()
    expected = config._DEFAULT_WARPING_TIME
    assert actual == expected
    assert actual == 70
