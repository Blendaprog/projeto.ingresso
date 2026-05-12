from flask import Flask, render_template 

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
    
class evento:
    def__init__(self, nome, preco, local, idade_minima, data):
        self.nome = nome
        self.preco = preco
        self.local = local 
        self.idade_minima
        self.data = data

    def mostrar_evento(self):
        return f"""
Show: (self.nome)
Local: {self.local}
Data: {self.data}
Preço: {self.preco}
Idade mínima: {self.idade_minima}
"""
show1 = Evento(
    "Matuê",
    220,
    "Allianz Parque",
    16,
    "15/09/2026"
)

show2 = Evento(
    "Teto",
    180,
    "Espaço Unimed",
    16,
    "22/10/2026"
)

show3 = Evento(
    "WIU",
    150,
    "Vibra São Paulo",
    16,
    "05/11/2026"
)

show4 = Evento(
    "Veigh",
    200,
    "Arena São Paulo",
    18,
    "18/11/2026"
)

show5 = Evento(
    "MC Ryan SP",
    120,
    "Baile Arena",
    18,
    "25/11/2026"
)

show6 = Evento(
    "MC Cabelinho",
    160,
    "Espaço Hall",
    16,
    "02/12/2026"
)

show7 = Evento(
    "Orochi",
    170,
    "Audio Club",
    18,
    "10/12/2026"
)

show8 = Evento(
    "Djonga",
    190,
    "Arena Hall",
    16,
    "20/12/2026"
)

show9 = Evento(
    "BK'",
    175,
    "Qualistage",
    16,
    "15/01/2027"
)

show10 = Evento(
    "L7NNON",
    140,
    "Vivo Rio",
    16,
    "28/01/2027"
)

show11 = Evento(
    "Caetano Veloso",
    300,
    "Teatro Bradesco",
    12,
    "10/02/2027"
)

show12 = Evento(
    "Gilberto Gil",
    320,
    "Tokio Marine Hall",
    12,
    "18/02/2027"
)

show13 = Evento(
    "the weeknd",
    350,
    "Alliians Parque",
    16,
    "15/09/2026"
)

show14 = Evento(
    "Seu Jorge",
    250,
    "Citibank Hall",
    14,
    "14/03/2027"
)

show15 = Evento(
    "Ludmilla",
    280,
    "Jeunesse Arena",
    16,
    "20/03/2027"
)

show16 = Evento(
    "MC Hariel",
    130,
    "Arena Funk",
    18,
    "02/04/2027"
)

show17 = Evento(
    "KayBlack",
    190,
    "Audio Club",
    16,
    "12/04/2027"
)

show18 = Evento(
    "Filipe Ret",
    210,
    "Via Music Hall",
    18,
    "25/04/2027"
)

show19 = Evento(
    "Poze do Rodo",
    150,
    "Baile do RJ",
    18,
    "08/05/2027"
)

show20 = Evento(
    "Cabelinho e Orochi Festival",
    350,
    "Autódromo de Interlagos",
    18,
    "20/05/2027"
)
eventos = [show1, show2, show3, show4, show5, show6, show7, show8, show9, show10, show11, show12, show13, show14, show15, show16, show17, show18, show19, sow20]


for evento in eventos:
    print(evento.mostrar_evento())

class usuario:
    def __init__(self, nome, email, idade):
        self.nome = nome
        self.email = email
        self.idade = idade 

    def apresentar(self):
        return f"Usuario: {self.nome} ({self.idade} anos)"

class ingresso:
    def__init__(self, usuario, evento)
       self.usuario  usuario
       self.evento = evento

    def verificar_entrada(self):

        if self.usuario.idade >=self.evento.idade_minima:
            return "Compra autorizada"

        else:
            return "A entrada nao é permitida para menores!."



