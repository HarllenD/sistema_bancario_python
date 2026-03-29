from banco import *

criar_tabela()

while True:
    print("\n=== SISTEMA BANCÁRIO ===")
    print("1 - Criar conta") 
    print("2 - Listar contas")
    print("3 - Depositar")
    print("4 - Sacar")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input("Nome: ")
        criar_conta(nome)

    elif opcao == "2":
        contas = listar_contas()
        for conta in contas:
            print(f"ID: {conta[0]} | Nome: {conta[1]} | Saldo: R${conta[2]:.2f}")

    elif opcao == "3":  
        id = int(input("ID da conta: "))
        valor = float(input("Valor: "))
        depositar(id, valor)    

    elif opcao == "4":
        id = int(input("ID da conta: "))
        valor = float(input("Valor: "))
        sacar(id,valor)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida!")