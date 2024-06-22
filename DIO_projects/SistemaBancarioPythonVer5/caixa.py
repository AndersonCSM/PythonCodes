import textwrap
from datetime import datetime, timezone
from pathlib import Path

from cliente import ContaCorrente, PessoaFisica
from operacoes import Deposito, Saque

ROOT_PATH = Path(__file__).parent

# Desafio futuro: log de usuários e contas


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        # with -> gerenciador de contexto
        with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as file:
            file.write(
                f"[{data_hora} Função '{func.__name__}' executada com argumentos {args} e {kwargs}]"
                f"Retornou {resultado}\n"
            )

        print(f"{data_hora}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu(cliente=None):
    menu_txt = """\n
    ================ MENU ================
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tAcessar Conta
    [0]\tSair
    => """ if not cliente else """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tAcessar Conta
    [0]\tSair
    => """
    return int(input(textwrap.dedent(menu_txt)))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n=== Cliente não possui conta! ===")
        return

    return cliente.select


@log_transacao
def depositar(cliente):
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(cliente):
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(cliente):
    if not cliente:
        print("\n=== Cliente não encontrado! ===")
        return

    conta = recuperar_conta_cliente(cliente)
    print(conta)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    # transacoes = conta.historico.transacoes

    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n=== Já existe cliente com esse CPF! ===")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    print("\n=== Cliente criado com sucesso! ===")

    return cliente


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n=== Cliente não encontrado, fluxo de criação de conta encerrado! ===")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def login(clientes):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_cliente(cpf, clientes)
    # ADD ME: forma de autenticação

    if usuario:  # se usuario existe
        # print(usuario.__dict__)
        if usuario.contas:  # se usuario possui conta
            for k, v in enumerate(usuario.contas):
                print("=" * 100)
                print(f"Opção - [{k+1}]\n", textwrap.dedent(str(v)))
            while True:
                opc = int(input("\nSelecione uma conta\n Sair - [0]\n=>"))
                opcs = len(usuario.contas)

                if 1 <= opc <= opcs:
                    usuario.select = opc - 1
                    print("\nConta Selecionada")
                    return usuario

                elif opc == 0:
                    break

                else:
                    print("Opção inválida")
        else:
            print("Usuario não possui conta cadastrada")
    else:
        print("CPF informando não cadastrado")

    return None
