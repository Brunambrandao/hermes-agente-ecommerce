import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

def buscar_e_montar_contexto(pergunta: str, top_k: int = 3, filtro_categoria: str = None):
    print(f"\n Realizando Busca Semântica RAG para: '{pergunta}'")

    # 1. Conectar ao ChromaDB
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    collection = client.get_collection(
        name="hermes_base_conhecimento",
        embedding_function=sentence_transformer_ef
    )

    # 2. Configurar filtro de metadados se informado (Fase 3 da Etapa 4)
    where_clause = {"categoria": filtro_categoria} if filtro_categoria else None

    # 3. Executar busca vetorial (Fases 1 e 2 da Etapa 4)
    resultados = collection.query(
        query_texts=[pergunta],
        n_results=top_k,
        where=where_clause
    )

    # 4. Montagem do Contexto Unificado com Metadados (Fase 5 da Etapa 4)
    bloco_contexto = []
    
    print("\n--- TRECHOS RECUPERADOS (TOP K) ---")
    for i in range(len(resultados["ids"][0])):
        chunk_id = resultados["ids"][0][i]
        texto = resultados["documents"][0][i]
        metadado = resultados["metadatas"][0][i]
        distancia = resultados["distances"][0][i]

        categoria = metadado.get("categoria", "N/A")
        arquivo = metadado.get("arquivo_origem", "N/A")

        print(f"  [{i+1}] ID: {chunk_id} | Categoria: {categoria} | Distância: {distancia:.4f}")

        # Formatação do bloco individual de contexto para o Prompt do LLM
        item_contexto = (
            f"[DOCUMENTO {i+1}]\n"
            f"ID: {chunk_id}\n"
            f"Categoria: {categoria}\n"
            f"Conteúdo:\n{texto}\n"
            f"---"
        )
        bloco_contexto.append(item_contexto)

    # Junta todos os trechos recuperados em uma única string estruturada
    contexto_final = "\n\n".join(bloco_contexto)

    print("\n=== CONTEXTO FINAL MONTADO PARA O LLM ===")
    print(contexto_final)

    return contexto_final

if __name__ == "__main__":
    pergunta_teste = "Qual é a política de troca e devolução de produtos?"
    contexto = buscar_e_montar_contexto(pergunta_teste, top_k=3)