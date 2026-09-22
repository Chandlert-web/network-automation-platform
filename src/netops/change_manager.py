"""
Controlled network change management.

Provides a structured workflow for proposing, validating,
executing, and rolling back network configuration changes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ChangeRequest:
    """Represents a proposed network change."""

    change_id: str
    device: str
    description: str
    configuration: str
    status: str = "PENDING"
    created_at: str = ""


class ChangeManager:
    """Manage controlled network configuration changes."""

    def __init__(self):
        self.changes = {}

    def create_change(
        self,
        change_id: str,
        device: str,
        description: str,
        configuration: str,
    ) -> ChangeRequest:
        """Create a new change request."""

        if change_id in self.changes:
            raise ValueError(
                f"Change already exists: {change_id}"
            )

        change = ChangeRequest(
            change_id=change_id,
            device=device,
            description=description,
            configuration=configuration,
            created_at=datetime.now().isoformat(),
        )

        self.changes[change_id] = change

        return change

    def get_change(
        self,
        change_id: str,
    ) -> ChangeRequest:
        """Retrieve a change request."""

        if change_id not in self.changes:
            raise ValueError(
                f"Change not found: {change_id}"
            )

        return self.changes[change_id]

    def approve_change(
        self,
        change_id: str,
    ) -> ChangeRequest:
        """Approve a pending change."""

        change = self.get_change(change_id)

        if change.status != "PENDING":
            raise ValueError(
                "Only pending changes can be approved."
            )

        change.status = "APPROVED"

        return change

    def dry_run(
        self,
        change_id: str,
    ) -> dict:
        """Generate a dry-run representation of a change."""

        change = self.get_change(change_id)

        return {
            "change_id": change.change_id,
            "device": change.device,
            "mode": "DRY-RUN",
            "configuration": change.configuration,
            "would_execute": change.status == "APPROVED",
        }

    def execute_change(
        self,
        change_id: str,
    ) -> ChangeRequest:
        """Mark an approved change for execution."""

        change = self.get_change(change_id)

        if change.status != "APPROVED":
            raise ValueError(
                "Change must be approved before execution."
            )

        change.status = "EXECUTED"

        return change

    def rollback_change(
        self,
        change_id: str,
        rollback_configuration: Optional[str] = None,
    ) -> ChangeRequest:
        """Rollback an executed change."""

        change = self.get_change(change_id)

        if change.status != "EXECUTED":
            raise ValueError(
                "Only executed changes can be rolled back."
            )

        change.status = "ROLLED_BACK"

        if rollback_configuration:
            change.configuration = rollback_configuration

        return change
