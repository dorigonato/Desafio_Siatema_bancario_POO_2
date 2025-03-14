from abc import ABC, abstractmethod
from datetime import datetime

# Classe Cliente: Representa um cliente do banco com informações básicas e uma lista de contas
class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome  # Nome completo do cliente
        self.data_nascimento = data_nascimento  # Data de nascimento no formato dd/mm/aaaa
        self.cpf = cpf  # CPF do cliente (único)
        self.endereco = endereco  # Endereço completo do cliente
        self.contas = []  # Lista de contas associadas ao cliente

    # Realiza uma transação (saque ou depósito) em uma conta específica
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Adiciona uma nova conta à lista de contas do cliente
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe Conta: Classe base para contas bancárias com atributos e métodos básicos
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0  # Saldo inicial da conta (protegido)
        self._numero = numero  # Número da conta (protegido)
        self._agencia = "0001"  # Agência fixa (protegida)
        self._cliente = cliente  # Cliente associado à conta (protegido)
        self._historico = Historico()  # Histórico de transações da conta

    # Método de classe para criar uma nova conta e associá-la ao cliente
    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(numero, cliente)  # Cria uma nova instância da conta
        cliente.adicionar_conta(conta)  # Adiciona a conta ao cliente
        return conta

    @property
    def saldo(self):  # Propriedade para acessar o saldo
        return self._saldo

    @property
    def numero(self):  # Propriedade para acessar o número da conta
        return self._numero

    @property
    def agencia(self):  # Propriedade para acessar a agência
        return self._agencia

    @property
    def cliente(self):  # Propriedade para acessar o cliente
        return self._cliente

    @property
    def historico(self):  # Propriedade para acessar o histórico
        return self._historico

    # Realiza um saque na conta, verificando saldo e valor válido
    def sacar(self, valor):
        if valor > self._saldo:
            print("@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("=== Saque realizado com sucesso! ===")
            return True
        else:
            print("@@@ Operação falhou! Valor inválido. @@@")
            return False

    # Realiza um depósito na conta, verificando valor válido
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("@@@ Operação falhou! Valor inválido. @@@")
            return False

# Classe ContaCorrente: Herda de Conta, adicionando limite e limite de saques
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite  # Limite máximo por saque
        self.limite_saques = limite_saques  # Limite de saques diários

    # Sobrescreve o método sacar para adicionar regras específicas de ContaCorrente
    def sacar(self, valor):
        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if transacao["tipo"] == "Saque"
        ])  # Conta o número de saques no histórico

        if valor > self.limite:
            print("@@@ Operação falhou! Limite de saque excedido. @@@")
        elif numero_saques >= self.limite_saques:
            print("@@@ Operação falhou! Limite diário de saques atingido. @@@")
        else:
            return super().sacar(valor)  # Chama o método sacar da classe pai
        return False

# Classe Historico: Armazena as transações realizadas em uma conta
class Historico:
    def __init__(self):
        self._transacoes = []  # Lista privada de transações

    @property
    def transacoes(self):  # Propriedade para acessar as transações
        return self._transacoes

    # Adiciona uma transação ao histórico com tipo, valor e data
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,  # Nome da classe (Saque ou Deposito)
            "valor": transacao.valor,  # Valor da transação
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Data atual formatada
        })

# Classe Abstrata Transacao: Define a interface para transações (saque e depósito)
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):  # Propriedade abstrata para o valor da transação
        pass

    @abstractmethod
    def registrar(self, conta):  # Método abstrato para registrar a transação
        pass

# Classe Saque: Implementa a transação de saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor  # Valor do saque (protegido)

    @property
    def valor(self):  # Propriedade para acessar o valor
        return self._valor

    # Registra o saque na conta, adicionando ao histórico se bem-sucedido
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# Classe Deposito: Implementa a transação de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor  # Valor do depósito (protegido)

    @property
    def valor(self):  # Propriedade para acessar o valor
        return self._valor

    # Registra o depósito na conta, adicionando ao histórico se bem-sucedido
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# Função auxiliar: Filtra um cliente na lista pelo CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None  # Retorna o cliente ou None

# Função auxiliar: Recupera a primeira conta do cliente (simplificação)
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]  # Retorna a primeira conta da lista

# Função para realizar um depósito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)  # Cria uma transação de depósito
    conta = recuperar_conta_cliente(cliente)  # Recupera a conta do cliente

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)  # Executa a transação

# Função para realizar um saque
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)  # Cria uma transação de saque
    conta = recuperar_conta_cliente(cliente)  # Recupera a conta do cliente

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)  # Executa a transação

# Função para exibir o extrato de uma conta
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("========================================")

# Função para criar um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_cliente(cpf, clientes):
        print("@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço: ")
    cliente = Cliente(nome, data_nascimento, cpf, endereco)  # Cria um novo cliente
    clientes.append(cliente)  # Adiciona à lista de clientes
    print("=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta corrente
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)  # Cria uma nova conta corrente
    contas.append(conta)  # Adiciona à lista global de contas
    print("=== Conta criada com sucesso! ===")

# Função para listar todas as contas correntes
def listar_contas(contas):
    if not contas:
        print("Nenhuma conta corrente cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome}")

# Sistema Bancário Completo: Menu principal e lógica do programa
clientes = []  # Lista global de clientes
contas = []  # Lista global de contas

menu = """
[u] Criar Usuário
[c] Criar Conta Corrente
[l] Listar Clientes
[lc] Listar Contas Correntes
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Função principal: Executa o loop do menu
def main():
    while True:
        opcao = input(menu)

        if opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            criar_conta(len(contas) + 1, clientes, contas)  # Gera número da conta incremental

        elif opcao == "l":
            for cliente in clientes:
                print(f"Nome: {cliente.nome} | CPF: {cliente.cpf}")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "q":
            print("Saindo do sistema. Obrigado por usar nossos serviços!")
            break

        else:
            print("Operação inválida! Por favor, selecione uma opção válida.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()