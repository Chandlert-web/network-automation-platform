"""
Network configuration compliance engine.

Evaluates network device configuration against defined
engineering standards and produces structured findings.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ComplianceFinding:
    """Represents a single compliance finding."""

    device: str
    rule: str
    status: str
    message: str


class ComplianceEngine:
    """Evaluate device configurations against compliance rules."""

    def __init__(self, rules: dict):
        self.rules = rules

    def evaluate(
        self,
        device: str,
        configuration: str,
    ) -> List[ComplianceFinding]:
        """Evaluate configuration against all defined rules."""

        findings = []

        for rule_name, rule in self.rules.items():
            required = rule.get("required")
            forbidden = rule.get("forbidden")

            if required:
                for command in required:
                    if command in configuration:
                        findings.append(
                            ComplianceFinding(
                                device=device,
                                rule=rule_name,
                                status="PASS",
                                message=(
                                    f"Required configuration found: "
                                    f"{command}"
                                ),
                            )
                        )
                    else:
                        findings.append(
                            ComplianceFinding(
                                device=device,
                                rule=rule_name,
                                status="FAIL",
                                message=(
                                    f"Required configuration missing: "
                                    f"{command}"
                                ),
                            )
                        )

            if forbidden:
                for command in forbidden:
                    if command in configuration:
                        findings.append(
                            ComplianceFinding(
                                device=device,
                                rule=rule_name,
                                status="FAIL",
                                message=(
                                    f"Forbidden configuration found: "
                                    f"{command}"
                                ),
                            )
                        )
                    else:
                        findings.append(
                            ComplianceFinding(
                                device=device,
                                rule=rule_name,
                                status="PASS",
                                message=(
                                    f"Forbidden configuration absent: "
                                    f"{command}"
                                ),
                            )
                        )

        return findings
