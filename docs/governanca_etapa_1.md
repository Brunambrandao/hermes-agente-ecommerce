# Relatório de Governança e Organização — Etapa 1

## 1. Mapeamento das Fontes
O projeto **Hermes** utiliza duas fontes complementares de informação:
1. **Dados Transacionais (Estruturados):** Dataset público da Olist (Kaggle), simulando o histórico de pedidos, status e entregas do e-commerce.
2. **Base de Conhecimento Institucional (Não Estruturada):** Conjunto de 10 documentos em formato Markdown (`.md`), criados para subsidiar as respostas do agente sobre políticas, procedimentos e dúvidas frequentes.

Para garantir responsabilidade institucional e clareza de atribuição:
* **Aurora Commerce:** Marca fictícia utilizada para representar a loja online (e-commerce).
* **RotaLog:** Marca fictícia utilizada para representar a empresa parceira de logística e entregas.

## 2. Definição de Categorias
Os documentos não estruturados foram divididos em duas categorias operacionais primárias (`categoria-mãe`):
* `loja`: Documentos focados nas regras de negócio da Aurora Commerce (vendas, devoluções, privacidade e termos).
* `logistica`: Documentos focados no fluxo operacional da RotaLog (transporte, rastreamento, sinistros e avarias).

Essas categorias funcionam como metadados no arquivo `manifesto_documentos.json`, permitindo filtragem nas etapas posteriores do pipeline do agente.

## 3. Curadoria de Qualidade
* Apenas documentos em versão vigente (`v1.0`) compõem a base ativa.
* Não há arquivos duplicados ou rascunhos. Alterações futuras exigirão incremento de versão no manifesto (`v1.1`, `v2.0`).

## 4. Definição de Responsáveis (Ownership)
Embora os documentos sejam mantidos pela equipe do projeto, simulou-se a matriz de responsabilidade por departamento:
* **Jurídico & Compliance:** Política de Privacidade, Termos e Condições.
* **Atendimento ao Cliente / SAC:** FAQs e Políticas de Devolução/Reclamação.
* **Operações Logísticas:** Políticas de Envio, Rastreamento e Sinistros.

## 5. Acesso e Permissões
No escopo deste projeto, o agente tem acesso de leitura direta ao repositório local na pasta `data/docs/`. Em ambiente de produção, esta estrutura equivale à integração via leitura de API com repositórios de arquivos corporativos (SharePoint, Google Drive).

## 6. Processo de Ingestão Inicial
1. Criação manual e versionada dos documentos Markdown.
2. Mapeamento centralizado no arquivo `data/docs/manifesto_documentos.json`.
3. Leitura direta dos arquivos pelo pipeline de busca/RAG do agente nas etapas posteriores.