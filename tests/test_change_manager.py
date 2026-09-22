"""Tests for the network change management engine."""

from src.netops.change_manager import ChangeManager


def test_create_change():
    manager = ChangeManager()

    change = manager.create_change(
        change_id="CHG-001",
        device="ORL-CORE-01",
        description="Add VLAN 120",
        configuration="vlan 120\nname ENGINEERING",
    )

    assert change.change_id == "CHG-001"
    assert change.status == "PENDING"


def test_approve_change():
    manager = ChangeManager()

    manager.create_change(
        change_id="CHG-002",
        device="ORL-DIST-01",
        description="Update trunk configuration",
        configuration="switchport trunk allowed vlan add 120",
    )

    change = manager.approve_change("CHG-002")

    assert change.status == "APPROVED"


def test_dry_run():
    manager = ChangeManager()

    manager.create_change(
        change_id="CHG-003",
        device="ORL-CORE-01",
        description="Add management VLAN",
        configuration="vlan 200",
    )

    manager.approve_change("CHG-003")

    result = manager.dry_run("CHG-003")

    assert result["mode"] == "DRY-RUN"
    assert result["would_execute"] is True


def test_execute_change():
    manager = ChangeManager()

    manager.create_change(
        change_id="CHG-004",
        device="ORL-CORE-01",
        description="Modify interface configuration",
        configuration="interface Gi1/0/1",
    )

    manager.approve_change("CHG-004")
    change = manager.execute_change("CHG-004")

    assert change.status == "EXECUTED"


def test_rollback_change():
    manager = ChangeManager()

    manager.create_change(
        change_id="CHG-005",
        device="ORL-CORE-01",
        description="Test configuration change",
        configuration="interface Gi1/0/1",
    )

    manager.approve_change("CHG-005")
    manager.execute_change("CHG-005")

    change = manager.rollback_change(
        "CHG-005",
        rollback_configuration="interface Gi1/0/1\nshutdown",
    )

    assert change.status == "ROLLED_BACK"
