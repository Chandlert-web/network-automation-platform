"""Tests for the network validation engine."""

from src.netops.validation import ValidationEngine


def test_reachability_passes():
    engine = ValidationEngine("ORL-CORE-01")

    result = engine.check_reachability(True)

    assert result.status == "PASS"


def test_reachability_fails():
    engine = ValidationEngine("ORL-CORE-01")

    result = engine.check_reachability(False)

    assert result.status == "FAIL"


def test_interface_validation():
    engine = ValidationEngine("ORL-CORE-01")

    result = engine.check_interface_state(
        interface="GigabitEthernet1/0/1",
        state="up",
    )

    assert result.status == "PASS"


def test_required_configuration():
    engine = ValidationEngine("ORL-CORE-01")

    configuration = """
    aaa new-model
    ip ssh version 2
    """

    results = engine.check_required_configuration(
        configuration,
        [
            "aaa new-model",
            "ip ssh version 2",
        ],
    )

    assert all(
        result.status == "PASS"
        for result in results
    )
