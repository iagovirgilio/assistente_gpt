# Assistente de Suporte ao Cliente

Este é um assistente de suporte ao cliente que utiliza a linguagem de modelagem de linguagem (LLM) para responder às perguntas dos usuários com base em um documento de referência fornecido.

## Visão Geral

Este projeto consiste em um assistente virtual desenvolvido em Python que utiliza a API da OpenAI para interagir com os usuários e fornecer respostas às suas perguntas. O assistente é treinado em um modelo de linguagem específico para responder a consultas com base em um documento de referência fornecido.

## Funcionalidades

- Responde perguntas dos usuários com base no conteúdo do documento de referência.
- Fácil integração com a plataforma Streamlit para criar uma interface de usuário interativa.

## Pré-requisitos

- Python 3.x
- Conta na OpenAI com acesso à API
- Documento de referência no formato Excel (`.xlsx`)

## Como Usar

1. Clone este repositório:

```bash
    git clone https://github.com/iagovirgilio/assistente_gpt.git
    cd assistente_gpt
```

2. Instale as dependências:

```bash
  pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

   Antes de executar o projeto, defina a variável de ambiente `OPENAI_API_KEY` com sua chave de API da OpenAI.

4. Execute o projeto:

```bash
  streamlit run assistente.py
```

5. Insira sua pergunta na interface do Streamlit e aguarde a resposta do assistente.

## Contribuições

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Autor

[Iago Virgílio](https://github.com/iagovirgilio)

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
