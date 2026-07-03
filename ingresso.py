class Evento:
    def __init__(self, nome, preco, local, idade_minima, data):
        self.nome = nome
        self.preco = preco
        self.local = local
        self.idade_minima = idade_minima
        self.data = data

    def mostrar_evento(self):
        return f"""
Show: {self.nome}
Local: {self.local}
Data: {self.data}
Preço: R$ {self.preco}
Idade mínima: {self.idade_minima}
"""


class Usuario:
    def __init__(self, nome, email, idade):
        self.nome = nome
        self.email = email
        self.idade = idade

    def apresentar(self):
        return f"Usuário: {self.nome} ({self.idade} anos)"


class Ingresso:
    def __init__(self, usuario, evento):
        self.usuario = usuario
        self.evento = evento

    def verificar_entrada(self, autorizacao_responsavel=False):
        if self.usuario.idade >= self.evento.idade_minima:
            return "Compra autorizada"

        if autorizacao_responsavel:
            return "Compra autorizada com responsável"

        return "Menor de idade: precisa de autorização do responsável"


Eventos = [
    Evento("Matuê", 220, "Allianz Parque", 16, "15/09/2026"),
    Evento("Teto", 180, "Espaço Unimed", 16, "22/10/2026"),
    Evento("WIU", 150, "Vibra São Paulo", 16, "05/11/2026"),
    Evento("Veigh", 200, "Arena São Paulo", 18, "18/11/2026"),
    Evento("MC Ryan SP", 120, "Baile Arena", 18, "25/11/2026"),
    Evento("MC Cabelinho", 160, "Espaço Hall", 16, "02/12/2026"),
    Evento("Orochi", 170, "Audio Club", 18, "10/12/2026"),
    Evento("Djonga", 190, "Arena Hall", 16, "20/12/2026"),
    Evento("BK'", 175, "Qualistage", 16, "15/01/2027"),
    Evento("L7NNON", 140, "Vivo Rio", 16, "28/01/2027"),
    Evento("Caetano Veloso", 300, "Teatro Bradesco", 12, "10/02/2027"),
    Evento("Gilberto Gil", 320, "Tokio Marine Hall", 12, "18/02/2027"),
    Evento("The Weeknd", 350, "Allianz Parque", 16, "15/03/2027"),
    Evento("Seu Jorge", 250, "Citibank Hall", 14, "20/03/2027"),
    Evento("Ludmilla", 280, "Jeunesse Arena", 16, "25/03/2027"),
    Evento("MC Hariel", 130, "Arena Funk", 18, "02/04/2027"),
    Evento("KayBlack", 190, "Audio Club", 16, "12/04/2027"),
    Evento("Filipe Ret", 210, "Via Music Hall", 18, "25/04/2027"),
    Evento("Poze do Rodo", 150, "Baile do RJ", 18, "08/05/2027"),
    Evento("Festival Trap", 350, "Interlagos", 18, "20/05/2027"),
    Evento("Supernova Ent (Veigh, G.A, Niink, GHard)", 72, "Terra SP - São Paulo", 16, "24/04/2026"),
    Evento("Niink - Show Solo", 120, "Audio Club - São Paulo", 16, "15/05/2026"),
    Evento("G.A - Trap Experience", 110, "Espaço Unimed - São Paulo", 16, "22/05/2026"),
    Evento("GHARD Live", 100, "Vibra São Paulo", 16, "30/05/2026"),
    Evento("Ajuliacosta", 90, "Virada Cultural - São Paulo", 14, "24/05/2026"),
    Evento("Duquesa", 95, "Palco M'Boi Mirim - São Paulo", 14, "24/05/2026"),
    Evento("Tasha & Tracie", 130, "Grajaú Festival - São Paulo", 16, "24/05/2026"),
    Evento("Don Juan", 120, "Baile do Funk - RJ", 16, "10/06/2026"),
    Evento("Vulgo FK", 150, "Espaço LIV - São Paulo", 16, "20/03/2026"),
    Evento("MC Paiva", 110, "Komplexo Tempo - São Paulo", 16, "11/04/2026"),
    Evento("BTS (K-Pop World Tour)", 400, "Allianz Parque - São Paulo", 16, "15/08/2026"),
    Evento("Gaab", 140, "Vivo Rio - Rio de Janeiro", 14, "05/07/2026"),
    Evento("MC Don Juan", 120, "Baile Funk Arena - São Paulo", 16, "18/07/2026"),
    Evento("MC Ryan SP", 130, "Baile Arena - São Paulo", 16, "25/07/2026"),
    Evento("MC Hariel", 130, "Interlagos Festival - São Paulo", 16, "02/08/2026"),
    Evento("Veigh (Eu Venci o Mundo Tour)", 200, "Allianz Parque - São Paulo", 16, "15/09/2026"),
    Evento("Filipe Ret", 210, "Via Music Hall - RJ", 18, "25/04/2026"),
    Evento("KayBlack", 190, "Audio Club - SP", 16, "12/04/2026"),
    Evento("Poze do Rodo", 150, "Baile do RJ", 18, "08/05/2026"),
    Evento("Festival Trap 2026", 350, "Interlagos - SP", 18, "20/05/2026")
]


usuario = None
ingressos_comprados = []


def menu():
    global usuario

    while True:
        print("\n==== SISTEMA DE COMPRAS ====")
        print("1 - Cadastrar Usuário")
        print("2 - Comprar Ingresso")
        print("3 - Listar Shows")
        print("4 - Listar Ingressos Comprados")
        print("5 - Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            nome = input("Nome: ")
            email = input("Email: ")
            idade = int(input("Idade: "))

            usuario = Usuario(nome, email, idade)
            print(usuario.apresentar())

        elif opcao == 2:
            if usuario is None:
                print("Você precisa se cadastrar primeiro!")
                continue

            for i, evento in enumerate(Eventos):
                print(f"[{i+1}] {evento.nome}")

            escolha = int(input("Escolha o show: "))
            evento_escolhido = Eventos[escolha - 1]

            print(f"\nVocê escolheu: {evento_escolhido.nome}")
            print(f"Preço: R$ {evento_escolhido.preco}")

            print("\nForma de pagamento:")
            print("1 - PIX")
            print("2 - Cartão")

            forma = int(input("Escolha: "))

            if forma == 1:
                input("Chave PIX: ")
                print("Pagamento via PIX aprovado!")

            elif forma == 2:
                input("Número do cartão: ")
                input("Senha: ")
                print("Pagamento no cartão aprovado!")

            else:
                print("Forma de pagamento inválida!")
                continue

            autorizacao = False

            if usuario.idade < evento_escolhido.idade_minima:
                resp = input("Menor de idade. Responsável autoriza? (s/n): ")
                autorizacao = resp.lower() == "s"

            ingresso = Ingresso(usuario, evento_escolhido)
            resultado = ingresso.verificar_entrada(autorizacao)

            print(resultado)

            if "autorizada" in resultado:
                ingressos_comprados.append(ingresso)

        elif opcao == 3:
            for evento in Eventos:
                print(evento.mostrar_evento())

        elif opcao == 4:
            if not ingressos_comprados:
                print("Nenhum ingresso comprado!")
            else:
                for ing in ingressos_comprados:
                    print(f"{ing.usuario.nome} - {ing.evento.nome}")
                    

        elif opcao == 5:
            print("Obrigada pela sua compra! Volte sempre!")
            break

        else:
            print("Opção inválida!")
            class Usuario(UserMixin):
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ingressos = []


menu()