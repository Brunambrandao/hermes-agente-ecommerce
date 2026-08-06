# 🏛️ Hermes — Agente Inteligente de E-commerce

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hermes-agente-ecommerce.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Hermes** é um assistente virtual baseado em Inteligência Artificial Generativa e **RAG (Retrieval-Augmented Generation)** desenvolvido para automatizar o atendimento ao cliente em e-commerces, fornecendo respostas precisas e fundamentadas sobre políticas de devolução, termos de uso e suporte institucional.

---

## 📌 Links do Projeto

* 🌐 **Aplicação Online:** [hermes-agente-ecommerce.streamlit.app](https://hermes-agente-ecommerce.streamlit.app/)
* 📦 **Repositório GitHub:** [github.com/Brunambrandao/hermes-agente-ecommerce](https://github.com/Brunambrandao/hermes-agente-ecommerce)

---

## 🎯 Objetivo do Projeto

Reduzir a sobrecarga dos canais de suporte humano através de um agente conversacional capaz de:
1. Consultar diretamente a base de conhecimento e políticas oficiais da loja em tempo real.
2. Evitar alucinações de modelos de linguagem limitando as respostas estritamente ao contexto indexado.
3. Direcionar o cliente para canais humanos de fallback (como Ouvidoria e suporte via e-mail) quando a informação solicitada não constar nos documentos oficiais.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Web:** Streamlit
* **Provedor de LLM:** Groq API (Modelo Llama-3)
* **Banco de Dados Vetorial:** ChromaDB
* **Embeddings:** HuggingFace / Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Containerização:** Docker & Docker Compose
* **Hospedagem & Deploy:** Streamlit Community Cloud

---

## 🧱 Arquitetura e Fluxo RAG

```text
[Usuário] ──> (Interface Streamlit)
                     │
                     ▼
          [Busca Vetorial no ChromaDB] ──> (Recupera Trechos Relevantes)
                     │
                     ▼
            [Prompt de Contexto + LLM Groq]
                     │
                     ▼
  [Resposta Fundamentada com Citação de Fontes / Fallback]

## Estrutura do Repositório
  hermes-agente-ecommerce/
├── .devcontainer/          # Configuração de ambiente de desenvolvimento
├── dados/                  # Base de conhecimento e banco vetorial ChromaDB
├── documentos/             # Relatórios de governança e documentação de IA
├── registros_execucao/     # Capturas de tela e evidências de execução na nuvem
├── roteiros/               # Roteiros de testes e casos de uso
├── .dockerignore           # Arquivos ignorados no build da imagem
├── .gitignore              # Proteção de credenciais e arquivos locais
├── app.py                  # Aplicação principal Streamlit
├── Dockerfile              # Receita para build do container Docker
├── docker-compose.yml      # Execução orquestrada do container
├── LICENÇA                 # Licença MIT do repositório
├── README.md               # Documentação principal do projeto
└── requisitos.txt          # Dependências do ecossistema Python

## Como Executar o Projeto Localmente
* Opção 1: Com Python e Ambiente Virtual

1 - Clone o repositório:
git clone [https://github.com/Brunambrandao/hermes-agente-ecommerce.git](https://github.com/Brunambrandao/hermes-agente-ecommerce.git)
cd hermes-agente-ecommerce
2 - Crie e ative um ambiente virtual:
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
3 - Instale as dependências:
pip install -r requisitos.txt
4 - Configure a variável de ambiente:
Crie um arquivo .env na raiz do projeto contendo sua chave da Groq:
GROQ_API_KEY=sua_chave_aqui
5 - Execute a aplicação:
streamlit run app.py
** Opção 2: Com Docker e Docker Compose
1 - Certifique-se de ter o Docker instalado e rode:
docker-compose up --build
2 - Acesse a aplicação em http://localhost:8501.

## 🔒 Governança e Segurança de Dados
* Alinhamento LGPD: O agente não coleta e nem armazena dados pessoais identificáveis (PII) durante as interações.

* Segurança de Credenciais: As chaves de API são gerenciadas via Secrets da plataforma de nuvem e variáveis de ambiente locais, nunca ficando expostas no código público.

* Transparência: O assistente identifica claramente suas limitações e orienta o usuário quanto aos canais de suporte oficiais quando necessário.

## 👩‍💻 Autora
Desenvolvido por Bruna Brandão

💼 LinkedIn

🐙 GitHub
