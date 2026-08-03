import json
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = BASE_DIR / "data" / "docs" / "chunks_processados.json"
# Pasta onde o ChromaDB vai salvar os dados localmente
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

def executar_indexacao():
    print(" Iniciando Etapa 3: Indexação Vetorial no ChromaDB...")

    # 1. Verificar se o arquivo de chunks existe (insumo da Etapa 2)
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"Arquivo de chunks não encontrado em: {CHUNKS_PATH}. Execute a Etapa 2 primeiro.")

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f" Carregados {len(chunks)} chunks para indexação.")

    # 2. Configurar o Banco de Vetores (ChromaDB)
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

    # 3. Definir o Modelo de Embedding (all-MiniLM-L6-v2)
    print("⏳ Carregando modelo de embedding (all-MiniLM-L6-v2)...")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # 4. Criar ou Obter a Coleção no ChromaDB
    try:
        client.delete_collection(name="hermes_base_conhecimento")
        print("♻️ Coleção antiga removida para re-indexação limpa.")
    except Exception:
        pass

    collection = client.create_collection(
        name="hermes_base_conhecimento",
        embedding_function=sentence_transformer_ef,
        metadata={"hnsw:space": "cosine"}
    )

    # 5. Preparar os dados para o ChromaDB
    ids = []
    documents = []
    metadados_lista = []

    print(f" Gerando embeddings e indexando {len(chunks)} chunks...")

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["conteudo"])
        
        meta = chunk.copy()
        del meta["conteudo"]
        metadados_lista.append(meta)

    # 6. Adicionar os dados à coleção
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadados_lista
    )

    print(f" Indexação concluída com sucesso!")
    print(f" Banco de vetores salvo na pasta: {VECTOR_DB_DIR}")
    print(f" Total de itens indexados: {collection.count()}")

if __name__ == "__main__":
    executar_indexacao()