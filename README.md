<h1 align="center"><b>Spam Email Validator - LLM</b></h1>

<p align="center">Projeto de avaliação técnica para a vaga de Data Scientist (IA) na Omie.</p>

> **Status**: *Em desenvolvimento*

## Objetivo do Projeto

Avaliar a base de código dada e propor melhoria na sua estrutura, respondendo as seguintes questões:

1. What problems do you see with this code?
2. What ideas do you have to make it better? 

Código:
```
def check_spam(email: str) -> str | None: 
   prompt = f"""\ 
      Determine if the email is spam. 
      Return a valid JSON object with the format: 
      {{ 
      "is_spam": is the email spam? // bool 
      "reason": think step by step, why is it spam or not spam? // str 
      }} 

      Email: {email}""" 

   completion = openai.chat.completions.create( 
   model="gpt-4o-mini", 
   messages=[{"role": "user", "content": prompt}], 
   temperature=1.0, 
   max_tokens=100)

   return completion.choices[0].message.content

email = "hi how are you i have a million dollar deal just sign here" 

res = check_spam(email) 
if res: 
   print(json.dumps(json.loads(res), indent=2))
```

### Repostas

#### 1. What problems do you see with this code?
   - **Potencial para prompt injection**: O conteúdo do e-mail é inserido diretamente no prompt sem isolamento ou reforço de instruções.
   - **Ausência de system prompt**: O código utiliza apenas a permissão de usuário (user) para passar o prompt, então a política de segurança se torna fraca.
   - **Dependência frágil de `chat.completions` e ausência de controle rígido da saída**: A validação depende do modelo “obedecer” ao formato passado por prompt, sem schema ou contrato forte. O modelo pode retornar texto fora do JSON, quebrando json.loads().
   - **Uso de “think step by step”**: Pode incentivar o raciocínio explícito na saída, aumentando o risco de saída não estruturada.
   - **'temperature' inadequada (1.0)**: Alta variabilidade para uma tarefa determinística de classificação.
   - **'max_tokens' insuficiente**: Pode interromper a resposta e gerar JSON incompleto.
   - **Falta de tratamento de exceções**: Erros de API ou falhas no parse de JSON não são tratados.

#### 2. What ideas do you have to make it better? 

Construir um validador de e-mails de spam usando a API Responses da OpenAI, com foco em robustez de prompt, saída estruturada e validação por DTO Pydantic. Exatamento o que este projeto faz!

## O que este projeto melhora em relação ao código original?

- Proteção contra *prompt injection* com políticas explícitas no system prompt.
- Saída obrigatoriamente em DTO Pydantic e validação via `responses.parse`.
- Remoção de "think step by step" para reduzir vazamento de raciocínio e saídas fora do formato.
- Separação em camadas (loader, assembler, generator) para facilitar testes e manutenção.
- Logging básico para diagnóstico de falhas.

## Arquitetura e Fluxo

1) **SystemPromptLoader** carrega o prompt do sistema em `src/prompt/spam_email_validator.txt`.
2) **ResponseInputAssembler** monta o payload de entrada no formato esperado pela API Responses.
3) **OpenAIResponseGenerator** chama `responses.parse` e valida a saida contra `SpamEmailValidator`.
4) **app.py** executa o fluxo e imprime a resposta validada.

## Estrutura de Pastas

```
.
├── app.py
├── src/
│   ├── application/
│   │   ├── dto/SpamEmailValidator.py
│   │   └── use_case/
│   │       ├── response_input_assembler.py
│   │       └── system_prompt_loader.py
│   ├── config/logger_config.py
│   ├── llm/
│   │   ├── openai_response_generator.py
│   │   └── setting/openai_api_connection_handler.py
│   └── prompt/spam_email_validator.txt
└── test/
    └── application/use_case/response_input_assembler_test.py
```

## Como rodar localmente?

1. Requisitos: Python 3.11+ e acesso a API da OpenAI.
2. (Opcional) Crie e ative um ambiente virtual.
3. Instale as dependências:
   ```bash
   pip install openai python-dotenv pydantic
   ```
4. Crie um arquivo `.env` na raiz do projeto com sua chave:
   ```env
   OPENAI_API_KEY=coloque_sua_chave_aqui
   ```
5. Execute:
   ```bash
   python app.py
   ```

## Prompts

- Prompt principal: `src/prompt/spam_email_validator.txt`
