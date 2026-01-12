from pathlib import Path

from src.config.logger_config import setup_logger
logger = setup_logger(name="SystemPromptLoader")


class SystemPromptLoader:
    def __init__(self) -> None:
        self.system_prompt_path = "src/prompt/spam_email_validator.txt"

    def load(self) -> str:
        try:
            return Path(self.system_prompt_path).read_text(encoding="utf-8")

        except FileNotFoundError:
            logger.error(
                f"O arquivo do system prompt não existe: {self.system_prompt_path}")
            raise
        except Exception:
            logger.exception("Exceção ao importar o prompt do sistema.")
            raise
