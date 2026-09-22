"""
Network pre-change and post-change validation.

Provides reusable validation checks for network operations
before and after configuration changes.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ValidationResult:
    """Represents the result of a validation check."""

    device: str
    check: str
    status: str
    message: str


class ValidationEngine:
    """Perform operational validation checks."""

    def __init__(self, device_name: str):
        self.device_name = device_name

    def check_reachability(
        self,
        reachable: bool,
    ) -> ValidationResult:
        """Validate device reachability."""

        if reachable:
            return ValidationResult(
                device=self.device_name,
                check="reachability",
                status="PASS",
                message="Device is reachable.",
            )

        return ValidationResult(
            device=self.device_name,
            check="reachability",
            status="FAIL",
            message="Device is not reachable.",
        )

    def check_interface_state(
        self,
        interface: str,
        state: str,
        expected_state: str = "up",
    ) -> ValidationResult:
        """Validate an interface operational state."""

        if state.lower() == expected_state.lower():
            return ValidationResult(
                device=self.device_name,
                check=f"interface:{interface}",
                status="PASS",
                message=(
                    f"{interface} is {state}; "
                    f"expected {expected_state}."
                ),
            )

        return ValidationResult(
            device=self.device_name,
            check=f"interface:{interface}",
            status="FAIL",
            message=(
                f"{interface} is {state}; "
                f"expected {expected_state}."
            ),
        )

    def check_required_configuration(
        self,
        configuration: str,
        required_lines: List[str],
    ) -> List[ValidationResult]:
        """Validate required configuration statements."""

        results = []

        for line in required_lines:
            if line in configuration:
                results.append(
                    ValidationResult(
                        device=self.device_name,
                        check="configuration",
                        status="PASS",
                        message=f"Required configuration found: {line}",
                    )
                )
            else:
                results.append(
                    ValidationResult(
                        device=self.device_name,
                        check="configuration",
                        status="FAIL",
                        message=f"Required configuration missing: {line}",
                    )
                )

        return results

    def check_forbidden_configuration(
        self,
        configuration: str,
        forbidden_lines: List[str],
    ) -> List[ValidationResult]:
        """Validate that forbidden configuration is absent."""

        results = []

        for line in forbidden_lines:
            if line in configuration:
                results.append(
                    ValidationResult(
                        device=self.device_name,
                        check="configuration",
                        status="FAIL",
                        message=f"Forbidden configuration found: {line}",
                    )
                )
            else:
                results.append(
                    ValidationResult(
                        device=self.device_name,
                        check="configuration",
                        status="PASS",
                        message=f"Forbidden configuration absent: {line}",
                    )
                )

        return results

    def summarize(
        self,
        results: List[ValidationResult],
    ) -> dict:
        """Return a summary of validation results."""

        passed = sum(
            1 for result in results
            if result.status == "PASS"
        )

        failed = sum(
            1 for result in results
            if result.status == "FAIL"
        )

        return {
            "device": self.device_name,
            "total_checks": len(results),
            "passed": passed,
            "failed": failed,
            "overall_status": "PASS" if failed == 0 else "FAIL",
        }
