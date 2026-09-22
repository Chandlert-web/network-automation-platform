"""Tests for the NetOps command-line interface."""

from src.netops.cli import build_parser


def test_inventory_command():
    parser = build_parser()

    args = parser.parse_args(["inventory"])

    assert args.command == "inventory"


def test_backup_command():
    parser = build_parser()

    args = parser.parse_args(["backup"])

    assert args.command == "backup"


def test_compliance_command():
    parser = build_parser()

    args = parser.parse_args(["compliance"])

    assert args.command == "compliance"


def test_validation_command():
    parser = build_parser()

    args = parser.parse_args(["validate"])

    assert args.command == "validate"


def test_change_command():
    parser = build_parser()

    args = parser.parse_args(["change"])

    assert args.command == "change"
