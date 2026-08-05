# 🏛️ Hermes — Agente Inteligente de E-commerce & Logística

**Hermes** é um agente inteligente baseado em IA desenvolvido para responder a dúvidas de clientes e colaboradores sobre pedidos, entregas, políticas de devolução e procedimentos de e-commerce e logística.

---

## 💡 Sobre o Projeto
O nome remete ao deus grego do comércio, das estradas e dos mensageiros. O projeto integra duas bases centrais:
1. **Aurora Commerce (E-commerce Fictício):** Consultas transacionais baseadas no dataset da Olist e documentação oficial da loja.
2. **RotaLog (Logística Fictícia):** Regras de envio, prazos, rastreamento e sinistros da transportadora parceira.

---

## 📁 Estrutura do Repositório

```text
hermes-agente-ecommerce/
├── docs/                       # Documentação de governança do projeto
├── data/
│   ├── docs/                   # Base de conhecimento (.md) e manifesto
│   └── raw/                    # Dados transacionais brutos (Olist CSVs)
└── scripts/                    # Scripts do pipeline do agente