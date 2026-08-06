import os
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import streamlit as st

# 1. Configurações da Página
st.set_page_config(page_title="Hermes - Assistente E-commerce", page_icon="🤖", layout="centered")
load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

# 2. Função de Busca no ChromaDB
def recuperar_contexto(pergunta: str, top_k: int = 3):
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    collection = client.get_collection(
        name="hermes_base_conhecimento",
        embedding_function=sentence_transformer_ef
    )

    resultados = collection.query(query_texts=[pergunta], n_results=top_k)

    bloco_contexto = []
    for i in range(len(resultados["ids"][0])):
        chunk_id = resultados["ids"][0][i]
        texto = resultados["documents"][0][i]
        categoria = resultados["metadatas"][0][i].get("categoria", "N/A")
        bloco_contexto.append(
            f"[DOCUMENTO {i+1}]\nID: {chunk_id}\nCategoria: {categoria}\nConteúdo:\n{texto}\n---"
        )
    return "\n\n".join(bloco_contexto)

# 3. Função de Geração de Resposta via Groq
def gerar_resposta_rag(pergunta: str):
    contexto = recuperar_contexto(pergunta, top_k=3)
    
    system_instruction = (
    "Você é o Hermes, o assistente virtual oficial de atendimento da loja Aurora Commerce.\n"
    "Sua tarefa é responder às perguntas dos clientes utilizando EXCLUSIVAMENTE as informações da base de conhecimento da loja.\n\n"
    "Regras de Ouro de Comunicação:\n"
    "1. Mantenha um tom profissional, amigável e focado em resolver o problema do cliente.\n"
    "2. NUNCA use termos técnicos como 'CONTEXTO', 'prompt', 'documentos recuperados' ou 'RAG' na sua resposta final. Refira-se apenas às 'nossas políticas' ou 'nossos registros'.\n"
    "3. Baseie-se apenas em fatos confirmados. Não invente ou presuma informações.\n"
    "4. REGRA DE FALLBACK: Se a informação pedida não constar nas políticas, informe polidamente e indique o canal adequado:\n"
    "   - Suporte Geral: suporte@auroracommerce.com.br\n"
    "   - Financeiro: financeiro@auroracommerce.com.br\n"
    "   - Logística: logistica@auroracommerce.com.br\n"
    "5. Sempre finalize citando a fonte de referência ao final da resposta (ex: Fonte: [DOCUMENTO 1] - Política de Devolução)."
)

    prompt_usuario = f"--- CONTEXTO RECUPERADO ---\n{contexto}\n---------------------------\n\nPERGUNTA: {pergunta}"

    # Tenta obter primeiro dos Secrets do Streamlit Cloud; se não achar, lê do .env local
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ Erro: Variável GROQ_API_KEY não configurada no arquivo .env."

    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt_usuario}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )
    return chat_completion.choices[0].message.content

# 4. Interface Web (Streamlit)
st.title("🤖 Hermes - Assistente de E-commerce")
st.caption("Aviso: Esta é uma inteligência artificial especialista na base de conhecimento da loja.")

# Inicializar histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de pergunta
if prompt := st.chat_input("Digite sua dúvida sobre reembolsos, entregas ou produtos..."):
    # Exibir pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processar e exibir resposta do Hermes
    with st.chat_message("assistant"):
        with st.spinner("Hermes está consultando os documentos..."):
            resposta = gerar_resposta_rag(prompt)
            st.markdown(resposta)
            
            # Botões de feedback simples
            col1, col2 = st.columns([1, 10])
            with col1:
                st.button("👍", key=f"up_{len(st.session_state.messages)}")
            with col2:
                st.button("👎", key=f"down_{len(st.session_state.messages)}")

    st.session_state.messages.append({"role": "assistant", "content": resposta})