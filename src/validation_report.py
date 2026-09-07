import logging

logger = logging.getLogger(__name__)

class ValidationReport:
    """
    A class to hold the validation results, while validating records.

    """

    def __init__(self) -> None:
        self._valid_count = 0
        self._errors: list[str] = []

    def record_success(self) -> None:
        """Records one successful validation."""
        self._valid_count += 1

    def record_failure(self, reason: str) -> None:
        """Records an error that failed validation, inkl reason."""
        self._errors.append(reason)
        logger.debug("Validation failure recorded: %s", reason)

    # Using @property to protect valid_count from being overwritten by mistake
    @property
    def valid_count(self) -> int:
        """Number of records that passed validation."""
        return self._valid_count

    @property
    def failure_count(self) -> int:
        """Number of records that failed validation."""
        return len(self._errors)

    @property
    def errors(self) -> list[str]:
        """The list of reasons validation failed, in order."""
        return list(self._errors)

    def summary(self) -> str:
        """A short summary of the batch's outcome, for me to check."""
        return f"{self._valid_count} valid, {self.failure_count} rejected"

if __name__ == "__main__":
    # Quick manual check with a mix of fake successes and failures.
    logging.basicConfig(level=logging.DEBUG)

    report = ValidationReport()
    report.record_success()
    report.record_success()
    report.record_failure("DayAheadPriceEUR was null")
    report.record_success()

    print(report.summary())
    print(report.errors)    