import json
import asyncio

from dotenv import load_dotenv

from src.application.dto.SpamEmailValidator import SpamEmailValidator
from src.llm.openai_response_generator import OpenAIResponseGenerator
from src.application.use_case.system_prompt_loader import SystemPromptLoader
from src.application.use_case.response_input_assembler import ResponseInputAssembler

from src.config.logger_config import setup_logger
logger = setup_logger(name="APP")


async def check_spam(email: str) -> SpamEmailValidator:
    user_prompt = f"E-mail Content: <email>{email}</email>"

    logger.info("Validando se o e-mail é spam...")

    try:
        system_prompt_loader = SystemPromptLoader()
        response_input_assembler = ResponseInputAssembler(
            system_prompt_loader=system_prompt_loader)
        input_data = response_input_assembler.assemble(user_prompt)

        response_generator = OpenAIResponseGenerator()
        response = await response_generator.generate(
            input_data=input_data,
            response_model=SpamEmailValidator,
            model_name="gpt-5-mini",
            # temperature=None,
            max_output_tokens=500
        )

        logger.info('E-mail validado com sucesso!')
        return response
    except Exception:
        logger.exception("Falha ao gerar resposta do validador de e-mail.")
        raise


async def main() -> None:
    emails = [
        "hi how are you i have a million dollar deal just sign here",
        "Congratulations! You've won a free iPhone, click the link to claim.",
        "Urgent: Your account will be suspended, verify your password now.",
        "Limited time offer!!! Get rich fast with this simple trick.",
        "Can we reschedule our meeting to Thursday at 10am?",
        "Attached is the invoice for last month's services. Please review.",
        "Hey, just checking in about the proposal we discussed yesterday.",
        "Reminder: Your appointment is confirmed for 3pm tomorrow.",
    ]

    for email in emails:
        try:
            spam_email_validator = await check_spam(email)
        except Exception:
            logger.exception(
                f"Validação de e-mail spam falhou para o e-mail: {email}")
            continue

        if spam_email_validator:
            print(f"E-mail: {email}")
            print(json.dumps(spam_email_validator.model_dump(), indent=2))
            print()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
