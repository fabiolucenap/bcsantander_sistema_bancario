# Sistema Bancário v2 (modularizado)

AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500.00

# ---------------------- Funções de negócio ----------------------

def depositar(saldo, valor, extrato):
    """Depósito: retorna (novo_saldo, novo_extrato)."""
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito realizado: R$ {valor:.2f}")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Saque (args keyword-only). 
    Retorna (novo_saldo, novo_extrato, novo_numero_saques).
    """
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite por operação.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato += f"Saque:    R$ {valor:.2f}\n"
    numero_saques += 1
    print(f"Saque realizado: R$ {valor:.2f}")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Extrato: saldo é posicional-only, extrato é keyword-only."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato, end="")
    print(f"\nSaldo:   R$ {saldo:.2f}")
    print("=========================================\n")


# ---------------------- Funções de cadastro ----------------------

def _somente_digitos(texto):
    return "".join(ch for ch in texto if ch.isdigit())

def encontrar_usuario_por_cpf(usuarios, cpf):
    cpf = _somente_digitos(cpf)
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_usuario(usuarios):
    print("\n=== Novo Usuário ===")
    cpf = _somente_digitos(input("CPF (somente números): ").strip())
    if not cpf:
        print("CPF inválido.")
        return

    existente = encontrar_usuario_por_cpf(usuarios, cpf)
    if existente:
        print("Já existe usuário com este CPF.")
        return

    nome = input("Nome completo: ").strip()
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    usuarios.append({
        "nome": nome,
        "data_nasc": data_nasc,
        "cpf": cpf,
        "endereco": endereco,
    })
    print(f"Usuário criado: {nome}")

def criar_conta_corrente(contas, usuarios):
    print("\n=== Nova Conta Corrente ===")
    cpf = _somente_digitos(input("CPF do titular (somente números): ").strip())
    usuario = encontrar_usuario_por_cpf(usuarios, cpf)

    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário antes.")
        return

    numero_conta = len(contas) + 1  # sequencial iniciando em 1
    conta = {
        "agencia": AGENCIA_PADRAO,
        "numero": numero_conta,
        "titular": usuario,      # vínculo direto ao dicionário do usuário
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência {AGENCIA_PADRAO} Conta {numero_conta:04d} - Titular: {usuario['nome']}")

def listar_contas(contas):
    print("\n=== Contas Cadastradas ===")
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for c in contas:
        print(f"Agência: {c['agencia']} | Conta: {c['numero']:04d} | Titular: {c['titular']['nome']} | CPF: {c['titular']['cpf']}")
    print()

def selecionar_conta(contas):
    """Retorna referência à conta escolhida pelo número informando na entrada."""
    if not contas:
        print("Não há contas cadastradas.")
        return None
    try:
        numero = int(input("Informe o número da conta: ").strip())
    except ValueError:
        print("Número de conta inválido.")
        return None
    conta = next((c for c in contas if c["numero"] == numero), None)
    if not conta:
        print("Conta não encontrada.")
    return conta

# ---------------------- Interface de menu ----------------------

def menu_principal():
    return """
========= Bootcamp Santander ===============
=================== MENU ===================
[u] Criar usuário
[c] Criar conta corrente
[l] Listar contas

[d] Depositar
[s] Sacar
[e] Extrato

[q] Sair
=> """

def main():
    usuarios = []
    contas = []

    while True:
        opcao = input(menu_principal()).strip().lower()

        if opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta_corrente(contas, usuarios)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "d":
            conta = selecionar_conta(contas)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do depósito: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

        elif opcao == "s":
            conta = selecionar_conta(contas)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do saque: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue

            novo_saldo, novo_extrato, novo_num_saques = sacar(
                saldo=conta["saldo"],
                valor=valor,
                extrato=conta["extrato"],
                limite=LIMITE_VALOR_SAQUE,
                numero_saques=conta["numero_saques"],
                limite_saques=LIMITE_SAQUES,
            )
            conta["saldo"], conta["extrato"], conta["numero_saques"] = novo_saldo, novo_extrato, novo_num_saques

        elif opcao == "e":
            conta = selecionar_conta(contas)
            if not conta:
                continue
            exibir_extrato(conta["saldo"], extrato=conta["extrato"])

        elif opcao == "q":
            print("Até logo!")
            break

        else:
            print("Operação inválida, tente novamente.")

# Execução
if __name__ == "__main__":
    main()
