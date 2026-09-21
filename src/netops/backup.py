"""
Network configuration backup functionality.

Provides configuration backup workflows for managed network devices.
"""

from datetime import datetime
from pathlib import Path

from .connectivity import NetworkConnection


class ConfigurationBackup:
    """Create timestamped configuration backups."""

    def __init__(self, backup_directory: str = "backups"):
        self.backup_directory = Path(backup_directory)

    def backup_device(
        self,
        connection: NetworkConnection,
    ) -> Path:
        """Retrieve and save the running configuration."""

        self.backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"{connection.hostname}_{timestamp}.cfg"
        )

        backup_path = self.backup_directory / filename

        configuration = connection.send_command(
            "show running-config"
        )

        backup_path.write_text(
            configuration,
            encoding="utf-8",
        )

        return backup_path
