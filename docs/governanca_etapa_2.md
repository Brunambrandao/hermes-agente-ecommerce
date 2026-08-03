# Relatório de Governança, Processamento e Chunking — Etapa 2

**Versão:** 1.0  
**Última Atualização:** 03/08/2026  
**Responsável:** Bruna Brandão

## 1. Estratégia de Extração e Limpeza
* **Formato de Origem:** Arquivos Markdown (`.md`) e JSON de manifesto (`manifesto_documentos.json`).
* **Regras de Limpeza:** Remoção de marcações de formatação gráfica (sintaxes de negrito `**`, itálico `*`, códigos inline `` ` `` e hiperlinks Markdown), preservando a integridade textual e a pontuação para inferência dos modelos.

## 2. Estratégia de Chunking
* **Critério de Divisão:** Chunking Lógico por Seção e Título (baseado em marcações de cabeçalhos `##` e blocos de Perguntas/Respostas `Q1:`).
* **Granularidade:** Cada chunk representa uma unidade temática completa e autocontida (política específica, regra de envio ou resposta de FAQ).
* **Total de Chunks Gerados:** 45 chunks.

## 3. Esquema dos Metadados do Chunk
Cada chunk processado contém os seguintes campos obrigatórios:
* `chunk_id`: Identificador único do trecho (ex: `DOC-LOJA-001-CHK-01`).
* `documento_id`: Código de controle do documento de origem.
* `titulo_documento`: Nome oficial do documento.
* `secao`: Nome da seção ou item correspondente.
* `categoria`: Categoria organizacional (`loja` ou `logistica`).
* `organizacao`: Entidade responsável (`Aurora Commerce` ou `RotaLog`).
* `responsavel`: Área técnica dona do conteúdo.
* `conteudo`: Texto limpo pronto para vetorização.

## 4. Arquivos Gerados
* `scripts/processar_documentos.py`: Pipeline Python de limpeza e ingestão.
* `data/docs/chunks_processados.json`: Base de conhecimento fragmentada e enriquecida.