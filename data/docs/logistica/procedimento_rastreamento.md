# Procedimento de Rastreamento de Pedidos — RotaLog

**Versão:** 1.0  
**Última Atualização:** 03/08/2026  
**Responsável:** Tecnologia & Rastreio

## 1. Código de Rastreio
Assim que o pedido é coletado no remetente, um código alfanumérico único (ex: `RL123456789BR`) é gerado e associado ao CPF/CNPJ do destinatário.

## 2. Atualização de Status
O sistema de rastreamento é atualizado em tempo real nas seguintes etapas:
* **Objeto Coletado:** Pacote recebido pela RotaLog.
* **Em Trânsito:** Pacote em deslocamento entre hubs.
* **Saiu para Entrega:** O motorista iniciou a rota final até o endereço informado.
* **Entregue:** Encomenda entregue ao destinatário final.

## 3. Dificuldades na Localização
Se o rastreio indicar "Endereço Não Localizado" ou "Ausente", o destinatário pode solicitar o reagendamento diretamente no portal da RotaLog em até 48 horas.