
from openai.types.responses import ResponseInputParam


from src.application.use_case.system_prompt_loader import SystemPromptLoader
from src.config.logger_config import setup_logger
logger = setup_logger(name="ResponseInputAssembler")


class ResponseInputAssembler:
    def __init__(self, system_prompt_loader: SystemPromptLoader) -> None:
        self.system_prompt_loader = system_prompt_loader

    def assemble(self, user_prompt: str) -> ResponseInputParam:
        system_prompt = self.system_prompt_loader.load()
        
        input_data: ResponseInputParam = [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}]
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}]
            }
        ]

        return input_data