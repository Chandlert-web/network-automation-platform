"""
Network device inventory management.

Provides structured loading and validation of network device inventory
data used by the NetOps platform.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List
import yaml


@dataclass
class Device:
    """Represents a managed network device."""

    hostname: str
    vendor: str
    platform: str
    role: str
    site: str
    management_ip: str


class Inventory:
    """Loads and manages network device inventory."""

    def __init__(self, inventory_path: str):
        self.inventory_path = Path(inventory_path)
        self.devices: List[Device] = []

    def load(self) -> List[Device]:
        """Load devices from the YAML inventory file."""

        if not self.inventory_path.exists():
            raise FileNotFoundError(
                f"Inventory file not found: {self.inventory_path}"
            )

        with self.inventory_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        self.devices = [
            Device(**device)
            for device in data.get("devices", [])
        ]

        return self.devices

    def get_device(self, hostname: str) -> Device:
        """Return a device by hostname."""

        for device in self.devices:
            if device.hostname == hostname:
                return device

        raise ValueError(
            f"Device not found in inventory: {hostname}"
        )

    def list_devices(self) -> List[Device]:
        """Return all loaded devices."""

        return self.devices
