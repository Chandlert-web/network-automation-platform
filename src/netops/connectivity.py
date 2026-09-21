"""
Network device connectivity layer.

Provides a controlled interface for establishing connections to
managed network devices using Netmiko.
"""

from typing import Any, Dict

from netmiko import ConnectHandler


class NetworkConnection:
    """Manage connections to network devices."""

    def __init__(
        self,
        hostname: str,
        device_type: str,
        host: str,
        username: str,
        password: str,
        port: int = 22,
    ):
        self.hostname = hostname
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self) -> None:
        """Establish an SSH connection to the device."""

        device = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "port": self.port,
        }

        self.connection = ConnectHandler(**device)

    def disconnect(self) -> None:
        """Close the active device connection."""

        if self.connection:
            self.connection.disconnect()
            self.connection = None

    def send_command(self, command: str) -> str:
        """Execute a read-only command on the connected device."""

        if not self.connection:
            raise RuntimeError(
                f"No active connection to {self.hostname}"
            )

        return self.connection.send_command(command)

    def get_device_info(self) -> Dict[str, Any]:
        """Retrieve basic operational information from a device."""

        commands = {
            "hostname": "show running-config | include hostname",
            "interfaces": "show ip interface brief",
            "version": "show version",
        }

        results = {}

        for name, command in commands.items():
            results[name] = self.send_command(command)

        return results
