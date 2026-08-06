import os
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq

# Carrega as variáveis do arquivo .env sobrescrevendo a memória antiga
load_dotenv(override=True)

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

def recuperar_contexto(pergunta: str, top_k: int = 3):
    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

        collection = client.get_collection(
            name="hermes_base_conhecimento",
            embedding_function=sentence_transformer_ef
        )

        resultados = collection.query(
            query_texts=[pergunta],
            n_results=top_k
        )
    except Exception as e:
        # Encapsula qualquer erro do ChromaDB (banco ausente, coleção não criada,
        # caminho incorreto, etc.) em uma mensagem amigável e re-lança para quem chamou.
        raise RuntimeError(
            "Não foi possível consultar a base de conhecimento (ChromaDB). "
            "Verifique se o banco vetorial foi gerado corretamente em 'data/vector_db'."
        ) from e

    bloco_contexto = []
    for i in range(len(resultados["ids"][0])):
        chunk_id = resultados["ids"][0][i]
        texto = resultados["documents"][0][i]
        categoria = resultados["metadatas"][0][i].get("categoria", "N/A")

        bloco_contexto.append(
            f"[DOCUMENTO {i+1}]\nID: {chunk_id}\nCategoria: {categoria}\nConteúdo:\n{texto}\n---"
        )

    return "\n\n".join(bloco_contexto)

def gerar_resposta_rag(pergunta: str):
    print(f"\n💬 Processando pergunta: '{pergunta}'")

    # 1. Recuperar contexto da Etapa 4
    try:
        contexto = recuperar_contexto(pergunta, top_k=3)
    except RuntimeError as e:
        # Mensagem já formatada de forma amigável em recuperar_contexto
        print(f"\n⚠️ {e}")
        return

    # 2. System Instruction (Guardrails & Fallback)
    system_instruction = (
        "Você é o Hermes, um assistente virtual especialista em e-commerce.\n"
        "Sua tarefa é responder às perguntas dos clientes utilizando EXCLUSIVAMENTE as informações fornecidas no CONTEXTO abaixo.\n\n"
        "Regras obrigatórias:\n"
        "1. Seja cortês, claro, objetivo e profissional.\n"
        "2. Baseie-se apenas nos fatos presentes no CONTEXTO. Não invente ou presuma informações.\n"
        "3. REGRA DE FALLBACK (Ausência de Informação): Se a resposta para a dúvida do cliente NÃO estiver presente ou coberta no CONTEXTO recuperado, responda de forma polida informando que não possui essa informação específica nos documentos atuais e oriente o cliente a entrar em contato com a equipe responsável através dos canais de suporte:\n"
        "   - Atendimento Geral / Dúvidas: suporte@auroracommerce.com.br\n"
        "   - Financeiro / Reembolsos: financeiro@auroracommerce.com.br\n"
        "   - Logística / Rastreio: logistica@auroracommerce.com.br\n"
        "4. Cite as fontes/documentos de referência ao final da resposta (ex: Fonte: [DOCUMENTO 1]). Não inclua fontes se a informação não foi encontrada."
    )

    # 3. Montar prompt
    prompt_usuario = (
        f"--- CONTEXTO RECUPERADO ---\n"
        f"{contexto}\n"
        f"---------------------------\n\n"
        f"PERGUNTA DO CLIENTE: {pergunta}"
    )

    # 4. Validar e executar API do Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n⚠️ ATENÇÃO: Variável de ambiente GROQ_API_KEY não encontrada!")
        print("Defina no arquivo .env a variável: GROQ_API_KEY=\"gsk_...\"")
        return

    try:
        client = Groq(api_key=api_key)

        print("⏳ Solicitando resposta ao LLM (Groq)...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

        resposta = chat_completion.choices[0].message.content
    except Exception as e:
        # Captura falhas da API da Groq (instabilidade, limite de uso, chave inválida, etc.)
        print("\n⚠️ Não foi possível obter uma resposta do modelo agora.")
        print("Isso pode acontecer por instabilidade temporária ou limite de uso da API Groq.")
        print("Tente novamente em instantes.")
        return

    print("\n🤖 RESPOSTA DO HERMES:")
    print("=" * 60)
    print(resposta)
    print("=" * 60)

if __name__ == "__main__":
    # Teste de Fallback com uma pergunta fora da base
    pergunta_teste = "Qual é o horário de atendimento por telefone da loja?"
    gerar_resposta_rag(pergunta_teste)