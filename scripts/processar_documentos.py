import json
import re
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
MANIFESTO_PATH = BASE_DIR / "data" / "docs" / "manifesto_documentos.json"
OUTPUT_CHUNKS_PATH = BASE_DIR / "data" / "docs" / "chunks_processados.json"

def limpar_markdown(texto: str) -> str:
    """Remove marcações visuais do Markdown mantendo apenas o texto limpo."""
    texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)  # Remove negrito
    texto = re.sub(r'\*(.*?)\*', r'\1', texto)      # Remove itálico
    texto = re.sub(r'`(.*?)`', r'\1', texto)        # Remove código inline
    texto = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', texto) # Remove links
    return texto.strip()

def extrair_chunks_por_secao(conteudo_md: str, doc_info: dict) -> list:
    """Divide o documento em chunks baseados em cabeçalhos (## ou Q1:)."""
    # Separa por títulos de nível 2 (##) ou por perguntas (## Q)
    secoes = re.split(r'\n(?=## )', conteudo_md)
    chunks = []
    
    for idx, secao in enumerate(secoes):
        secao_limpa = secao.strip()
        if not secao_limpa:
            continue
            
        # Extrai o título da seção se houver
        linhas = secao_limpa.split('\n')
        titulo_secao = "Introdução"
        if linhas[0].startswith("## "):
            titulo_secao = linhas[0].replace("## ", "").strip()
            
        texto_processado = limpar_markdown(secao_limpa)
        
        # Estrutura do chunk enriquecido com metadados
        chunk = {
            "chunk_id": f"{doc_info['id']}-CHK-{idx+1:02d}",
            "documento_id": doc_info["id"],
            "titulo_documento": doc_info["titulo"],
            "secao": titulo_secao,
            "categoria": doc_info["categoria"],
            "organizacao": doc_info["organizacao"],
            "responsavel": doc_info["responsavel"],
            "conteudo": texto_processado
        }
        chunks.append(chunk)
        
    return chunks

def executar_ingestao():
    print("Iniciando Etapa 2: Processamento e Chunking de Documentos...")
    
    if not MANIFESTO_PATH.exists():
        raise FileNotFoundError(f"Manifesto não encontrado em: {MANIFESTO_PATH}")
        
    with open(MANIFESTO_PATH, "r", encoding="utf-8") as f:
        manifesto = json.load(f)
        
    todos_chunks = []
    
    for doc in manifesto.get("documentos", []):
        caminho_arquivo = BASE_DIR / doc["caminho"]
        if not caminho_arquivo.exists():
            print(f"AVISO: Arquivo não encontrado: {caminho_arquivo}")
            continue
            
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            
        chunks_doc = extrair_chunks_por_secao(conteudo, doc)
        todos_chunks.extend(chunks_doc)
        print(f" Processado: {doc['titulo']} ({len(chunks_doc)} chunks gerados)")
        
    # Salva a base final de chunks
    with open(OUTPUT_CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=2)
        
    print(f"\n Processamento concluído! Total de {len(todos_chunks)} chunks salvos em: {OUTPUT_CHUNKS_PATH}")

if __name__ == "__main__":
    executar_ingestao()