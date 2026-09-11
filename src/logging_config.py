import logging


LOGGER_NAME = "dk2_pipeline"


def configure_logging() -> None:
    """
    Set up logging for the whole pipeline: INFO and above to the
    console, everything else (DEBUG) saved to a log file.
    """
    package_logger = logging.getLogger(LOGGER_NAME)

    if package_logger.handlers:
        return

    package_logger.setLevel(logging.DEBUG)
    package_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("dk2_pipeline.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    package_logger.addHandler(console_handler)
    package_logger.addHandler(file_handler)