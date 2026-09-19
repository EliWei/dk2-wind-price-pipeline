import logging

logger = logging.getLogger(f"dk2_pipeline.{__name__}")

# Honestly, having ValidationReport as functions, rather than a separate class,
# would be easier for me to read. But to be able to scale this project in 
# the future, I am doing it as a Class now. 

# And summary() is the only function that is actually used by the pipeline

class ValidationReport:
    """
    A class to track the results of validating records.
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

        """The list of reasons validation failed."""
        return list(self._errors)

    def summary(self) -> str:
        
        """A short summary of the batch's outcome, for me to check."""
        return f"{self._valid_count} valid, {self.failure_count} rejected"

  