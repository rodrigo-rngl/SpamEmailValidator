import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Evita adicionar handlers duplicados
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
