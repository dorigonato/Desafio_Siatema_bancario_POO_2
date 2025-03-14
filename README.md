# 🏦 Sistema Bancário com Programação Orientada a Objetos

Este projeto implementa um Sistema Bancário em Python utilizando os princípios de Programação Orientada a Objetos (POO). O objetivo é simular operações bancárias básicas, como criação de clientes, abertura de contas correntes, depósitos, saques e consulta de extrato, tudo gerenciado por meio de um menu interativo no terminal.

## 🥬 O desenvolvimento foi dividido em duas fases:

- Fase 1: Modelagem das classes seguindo um diagrama UML, com foco em herança, polimorfismo e classes abstratas.

- Fase 2: Atualização do menu para integrar as operações com as classes modeladas, tornando o sistema funcional.

## 🥬 Funcionalidades

- Criar Usuário: Cadastro de clientes com nome, data de nascimento, CPF e endereço.
- Criar Conta Corrente: Associação de uma conta corrente a um cliente existente, com número incremental e agência fixa ("0001").
- Listar Clientes: Exibe todos os clientes cadastrados.
- Listar Contas Correntes: Mostra as contas existentes com agência, número e titular.
- Depositar: Permite adicionar valores a uma conta, com validação de valor positivo.
- Sacar: Realiza saques com verificação de saldo, limite por saque (R$ 500) e limite diário de saques (3).
- Extrato: Exibe o histórico de transações (data, tipo e valor) e o saldo atual da conta.

## 🥬 Estrutura do Código
O projeto utiliza as seguintes classes principais:

- Cliente: Armazena informações do cliente e gerencia suas contas.
- Conta: Classe base para contas bancárias, com atributos como saldo, número, agência e histórico.
- ContaCorrente: Herda de Conta, adicionando limite de saque e limite de saques diários.
- Historico: Registra as transações realizadas em uma conta.
- Transacao: Classe abstrata que define a interface para saques e depósitos.
- Saque e Deposito: Implementam a lógica específica de cada tipo de transação.

Além disso, funções auxiliares como filtrar_cliente e recuperar_conta_cliente suportam a interação entre o menu e as classes.

## 🥬 Pré-requisitos

- Python 3.x: Certifique-se de ter o Python instalado em sua máquina.

## 🥬 Como Usar

1. Clone o repositório:
    - git clone https://github.com/seu-usuario/sistema-bancario-poo.git
    - cd sistema-bancario-poo

2. Execute o programa:
    - python sistema_bancario_poo.py

3. Interaja com o menu:
    - Use as opções [u], [c], [l], [lc], [d], [s], [e] ou [q] para navegar.
    - Siga as instruções no terminal para fornecer os dados solicitados (CPF, valores, etc.).

4. Exemplo de Uso

    - [u] Criar Usuário
    - [c] Criar Conta Corrente
    - [l] Listar Clientes
    - [lc] Listar Contas Correntes
    - [d] Depositar
    - [s] Sacar
    - [e] Extrato
    - [q] Sair

- => u
    - Informe o CPF (somente números): 12345678900
    - Nome: João Silva
    - Data de Nascimento (dd/mm/aaaa): 15/05/1990
    - Endereço: Rua Exemplo, 123 - Centro - SP
    - === Cliente criado com sucesso! ===

5. Detalhes da Implementação
- POO: Uso de herança (ContaCorrente herda de Conta), polimorfismo (método sacar) e encapsulamento (atributos protegidos com '_').
- Histórico: As transações são armazenadas com data, tipo e valor, permitindo um extrato detalhado.
- Simplificações:
    - Cada cliente tem apenas uma conta acessada automaticamente (primeira da lista).
    - Agência fixa como "0001" para todas as contas.
- Validações: Verificação de saldo insuficiente, valor inválido e limites de saque.
