from typing import Optional, Type, TypeVar

from openai.types.responses import ResponseInputParam
from pydantic import BaseModel

from src.llm.setting.openai_api_connection_handler import OpenAIAPIConnectionHandler
from src.config.logger_config import setup_logger

logger = setup_logger(name="OpenAIResponseGenerator")


BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class OpenAIResponseGenerator:
    async def generate(self,
                       input_data: str | ResponseInputParam,
                       response_model: Type[BaseModelType],
                       model_name: str = "gpt-5-mini",
                       temperature: Optional[float] = None,
                       max_output_tokens: int = 500
                       ) -> BaseModelType:
        async with OpenAIAPIConnectionHandler() as openai:
            try:
                logger.info(
                    "Enviando requisição para API da OpenAI...")

                response_params = {
                    "model": model_name,
                    "input": input_data,
                    "text_format": response_model,
                    "temperature": temperature,
                    "max_output_tokens": max_output_tokens
                }

                if temperature is not None:
                    response_params['temperature'] = temperature

                response = await openai.client.responses.parse(
                    **response_params  # type: ignore
                )

                assistant_response = response.output_parsed

                if assistant_response is None:
                    raise ValueError(
                        "A resposta do assitente não pode estar vazia!")

                logger.info("Resposta obtida com sucesso.")
                return assistant_response

            except Exception:
                logger.exception(
                    "Exceção ao obter resposta da API da OpenAI."
                )
                raise
