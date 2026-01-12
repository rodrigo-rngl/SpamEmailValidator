from src.application.use_case.response_input_assembler import ResponseInputAssembler


def test_assemble(mocker) -> None:
    loader = mocker.Mock()
    loader.load.return_value = "System Prompt String Content"

    assembler = ResponseInputAssembler(system_prompt_loader=loader)

    user_prompt = "User Prompt String Content"
    input_data = assembler.assemble(user_prompt)

    loader.load.assert_called_once_with()
    assert input_data == [
        {
            "role": "system",
            "content": [{"type": "input_text", "text": "System Prompt String Content"}],
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": "User Prompt String Content"}],
        },
    ]
