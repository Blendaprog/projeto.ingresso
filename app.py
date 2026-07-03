import json
import qrcode
import os
import uuid

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from modelos import Usuario, Ingresso
from functools import wraps

app = Flask(__name__)
app.secret_key = "segredo"

usuarios = [
    Usuario(1, "Admin", "admin@gmail.com", "123", "admin", "2000-01-01", "M")
]

shows = []
ingressos = []

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("tipo") != "admin":
            return "Acesso negado"
        return f(*args, **kwargs)
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        for u in usuarios:
            if u.email == email and u.senha == senha:
                session["usuario"] = u.email
                session["tipo"] = u.tipo
                return redirect(url_for("home"))

        return "Login inválido"

    return render_template("login.html")

@app.route("/")
@login_required
def home():
    return render_template("home.html", tipo=session["tipo"])

@app.route("/cadastrar_show", methods=["GET", "POST"])
@login_required
@admin_required
def cadastrar_show():
    if request.method == "POST":
        show = {
            "id": len(shows) + 1,
            "nome": request.form["nome"],
            "preco": request.form["preco"],
            "admin": session["usuario"]
        }

        shows.append(show)
        return redirect(url_for("meus_shows"))

    return render_template("cadastrar_show.html")

@app.route("/meus_shows")
@login_required
@admin_required
def meus_shows():
    meus = [s for s in shows if s["admin"] == session["usuario"]]
    return render_template("meus_shows.html", shows=meus)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function

usuarios = []
ingressos = []

SHOWS = [
    {
        "id": 1,
        "nome": "Veigh",
        "preco": 200,
        "local": "Allianz Parque - São Paulo",
        "data": "2026-09-15",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "veigh.png"
    },
    {
        "id": 2,
        "nome": "Matuê",
        "preco": 220,
        "local": "Allianz Parque - São Paulo",
        "data": "2026-10-10",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "matue.png"
    },
    {
        "id": 3,
        "nome": "KayBlack",
        "preco": 190,
        "local": "Audio Club - São Paulo",
        "data": "2026-11-12",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "kayblack.png"
    },
    {
        "id": 4,
        "nome": "Teto",
        "preco": 180,
        "local": "Espaço Unimed - São Paulo",
        "data": "2026-12-05",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "teto.png"
    },
    {
        "id": 5,
        "nome": "Supernova Ent",
        "preco": 72,
        "local": "Terra SP",
        "data": "2026-04-24",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "supernovaent.png"
    },
    {
        "id": 6,
        "nome": "Niink",
        "preco": 120,
        "local": "Audio Club",
        "data": "2026-05-15",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "niink.png"
    },
    {
        "id": 7,
        "nome": "G.A",
        "preco": 110,
        "local": "Espaço Unimed",
        "data": "2026-05-22",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "G.A.png"
    },
    {
        "id": 8,
        "nome": "GHARD",
        "preco": 100,
        "local": "Vibra São Paulo",
        "data": "2026-05-30",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "ghard.png"

    },
    {
        "id": 9,
        "nome": "Ajuliacosta",
        "preco": 90,
        "local": "São Paulo",
        "data": "2026-05-24",
        "idade_minima": 14,
        "categoria": "Rap",
        "imagem": "ajuliacosta.png"
    },
    {
        "id": 10,
        "nome": "Duquesa",
        "preco": 95,
        "local": "São Paulo",
        "data": "2026-05-24",
        "idade_minima": 14,
        "categoria": "Rap",
        "imagem": "duquesa.png"
    },
    {
        "id": 11,
        "nome": "Tasha & Tracie",
        "preco": 130,
        "local": "Grajaú Festival",
        "data": "2026-05-24",
        "idade_minima": 16,
        "categoria": "Rap",
        "imagem": "tashaetracie.png"
    },
    {
        "id": 12,
        "nome": "MC Don Juan",
        "preco": 120,
        "local": "Baile Funk Arena",
        "data": "2026-07-18",
        "idade_minima": 16,
        "categoria": "Funk",
        "imagem": "mcdonjuan.png"
    },
    {
        "id": 13,
        "nome": "MC Ryan SP",
        "preco": 130,
        "local": "Baile Arena",
        "data": "2026-07-25",
        "idade_minima": 16,
        "categoria": "Funk",
        "imagem": "ryansp.png"
    },
    {
        "id": 14,
        "nome": "MC Hariel",
        "preco": 130,
        "local": "Interlagos Festival",
        "data": "2026-08-02",
        "idade_minima": 16,
        "categoria": "Funk",
        "imagem": "hariel.png"
    },
    {
        "id": 15,
        "nome": "BTS",
        "preco": 400,
        "local": "Allianz Parque",
        "data": "2026-08-15",
        "idade_minima": 14,
        "categoria": "K-Pop",
        "imagem": "bts.png"
    },
    {
        "id": 16,
        "nome": "Gaab",
        "preco": 140,
        "local": "Vivo Rio",
        "data": "2026-07-05",
        "idade_minima": 14,
        "categoria": "R&B",
        "imagem": "gaab.png"

    },
    {
        "id": 17,
        "nome": "Brandão",
        "preco": "250",
        "local": "A definir!",
        "data": "A definir!",
        "idade_minima": "16",
        "categoria": "Trap",
        "imagem": "BRANDAO.png"


    },
    {
         "id": 18,
        "nome": "Kyan",
        "preco": "220",
        "local": "A definir!",
        "data": " A definir! ",
        "idade_minima": "18 ",
        "categoria": "Trap",
        "imagem": "kyan.png"
    },
    {
        "id": 19,
        "nome": "Marina Sena",
        "preco": "220",
        "local": "Parque Ibirapuera!",
        "data": "2026-06-13",
        "idade_minima": "16 ",
        "categoria": "Trap",
        "imagem": "marinasena.png"
    },
    {
        "id": 20,
        "nome": " Mc paiva",
        "preco": "180",
        "local": " Vigor On Stage",
        "data": "2026-07-18",
        "idade_minima": "18 ",
        "categoria": "Funk",
        "imagem": "paiva.png"
    },
    {
        "id": 21,
        "nome": "Mc Tuto",
        "preco": 240,
        "local": "Evento Bday Surf Scream",
        "data": "2026-08-15",
        "idade_minima": 16,
        "categoria": "Funk",
        "imagem": "tuto.png"
    },
    {
        "id": 22,
        "nome": "Vulgo FK",
        "preco": 240,
        "local": "Tokio Marine Hall",
        "data": "2026-04-14",
        "idade_minima": 16,
            "categoria": "Trap",
        "imagem": "vulgofk.png"
    },
    {
        "id": 23,
        "nome": "Orochi",
        "preco": 240,
        "local": "Audio Club",
        "data": "2026-08-29",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "orochi.png"
    },
    {
        "id": 24,
        "nome": "Alee",
        "preco": 240,
        "local": "Audio Club",
        "data": "2026-03-10",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "alee.png"
    },
    {
        "id": 25,
        "nome": "WIU",
        "preco": 150,
        "local": "Vibra São Paulo",
        "data": "2026-11-05",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "wiu.png"
    },
    {
        "id": 26,
        "nome": "MC Cabelinho",
        "preco": 160,
        "local": "Espaço Hall",
        "data": "2026-12-02",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "mccabelinho.png"
    },
    {
        "id": 27,
        "nome": "Djonga",
        "preco": 190,
        "local": "Arena Hall",
        "data": "2026-12-20",
        "idade_minima": 16,
        "categoria": "Rap",
        "imagem": "djonga.png"
    },
    {
        "id": 28,
        "nome": "BK'",
        "preco": 175,
        "local": "Qualistage",
        "data": "2027-01-15",
        "idade_minima": 16,
        "categoria": "Rap",
        "imagem": "bk.png"
    },
    {
        "id": 29,
        "nome": "L7NNON",
        "preco": 140,
        "local": "Vivo Rio",
        "data": "2027-01-28",
        "idade_minima": 16,
        "categoria": "Rap",
        "imagem": "l7nnon.png"
    },
    {
        "id": 30,
        "nome": "Caetano Veloso",
        "preco": 300,
        "local": "Teatro Bradesco",
        "data": "2027-02-10",
        "idade_minima": 12,
        "categoria": "MPB",
        "imagem": "caetano.png"
    },
    {
        "id": 31,
        "nome": "Gilberto Gil",
        "preco": 320,
        "local": "Tokio Marine Hall",
        "data": "2027-02-18",
        "idade_minima": 12,
        "categoria": "MPB",
        "imagem": "gilbertogil.png"
    },
    {
        "id": 32,
        "nome": "The Weeknd",
        "preco": 350,
        "local": "Allianz Parque",
        "data": "2027-03-15",
        "idade_minima": 16,
        "categoria": "Pop",
        "imagem": "theweeknd.png",
        "ingressos_total": 100,
        "ingressos_vendidos": 100
    },
    {
        "id": 33,
        "nome": "Seu Jorge",
        "preco": 250,
        "local": "Citibank Hall",
        "data": "2027-03-20",
        "idade_minima": 14,
        "categoria": "MPB",
        "imagem": "seujorge.png"
    },
    {
        "id": 34,
        "nome": "Ludmilla",
        "preco": 280,
        "local": "Jeunesse Arena",
        "data": "2027-03-25",
        "idade_minima": 16,
        "categoria": "Funk",
        "imagem": "ludmilla.png"
    },
    {
        "id": 35,
        "nome": "BLACKPINK",
        "preco": 450,
        "local": "Allianz Parque - São Paulo",
        "data": "2027-04-10",
        "idade_minima": 14,
        "categoria": "K-Pop",
        "imagem": "blackpink.png"
    },
    {
        "id": 36,
        "nome": "TWICE",
        "preco": 380,
        "local": "Espaço Unimed - São Paulo",
        "data": "2027-04-24",
        "idade_minima": 14,
        "categoria": "K-Pop",
        "imagem": "twice.png"
    },
    {
        "id": 37,
        "nome": "Stray Kids",
        "preco": 420,
        "local": "Allianz Parque - São Paulo",
        "data": "2027-05-08",
        "idade_minima": 14,
        "categoria": "K-Pop",
        "imagem": "straykids.png"
    },
    {
        "id": 38,
        "nome": "SEVENTEEN",
        "preco": 390,
        "local": "Vibra São Paulo",
        "data": "2027-05-22",
        "idade_minima": 14,
        "categoria": "K-Pop",
        "imagem": "seventeen.png"
    },
    {
        "id": 39,
        "nome": "NewJeans",
        "preco": 350,
        "local": "Espaço Unimed - São Paulo",
        "data": "2027-06-05",
        "idade_minima": 12,
        "categoria": "K-Pop",
        "imagem": "newjeans.png"
    },
    {
        "id": 40,
        "nome": "IVE",
        "preco": 320,
        "local": "Vibra São Paulo",
        "data": "2027-06-19",
        "idade_minima": 12,
        "categoria": "K-Pop",
        "imagem": "ive.png"
    },
    {
        "id": 41,
        "nome": "JAY PARK",
        "preco": 360,
        "local": "Vibra São Paulo - São Paulo",
        "data": "2027-07-10",
        "idade_minima": 16,
        "categoria": "K-Pop",
        "imagem": "jaypark.png"
    },
    {
        "id": 42,
        "nome": "ARIANA GRANDE",
        "preco": 500,
        "local": "Allianz Parque - São Paulo",
        "data": "2027-08-15",
        "idade_minima": 14,
        "categoria": "Pop",
        "imagem": "arianagrande.png"
    }
]

from datetime import datetime

hoje = datetime.now().date()

def atualizar_shows():
    for show in SHOWS:

        if "ingressos_total" not in show:
            show["ingressos_total"] = 100

        if "ingressos_vendidos" not in show:
            show["ingressos_vendidos"] = 0

        show["esgotado"] = (
            show["ingressos_vendidos"] >= show["ingressos_total"]
        )
@app.route("/cadastrar_show", methods=["GET", "POST"])
@login_required
def cadastrar_show():

    if request.method == "POST":

        novo_show = {
            "id": len(SHOWS) + 1,
            "nome": request.form["nome"],
            "categoria": request.form["categoria"],
            "local": request.form["local"],
            "data": request.form["data"],
            "idade_minima": int(request.form["idade_minima"]),
            "preco": float(request.form["preco"]),
            "imagem": request.form["imagem"],
            "ingressos_total": 100,
            "ingressos_vendidos": 0
        }

        SHOWS.append(novo_show)

        return redirect(url_for("home"))

    return render_template("cadastrar_show.html")

try:
    with open("usuarios.json", "r") as arquivo:
        dados = json.load(arquivo)
        usuarios = [Usuario(**usuario) for usuario in dados]
except:
    pass

@app.route("/")
@login_required
def home():

    atualizar_shows()

    shows_disponiveis = [
        show for show in SHOWS
        if not show["esgotado"]
    ]

    return render_template(
        "index.html",
        shows=shows_disponiveis,
        nome=session["nome_usuario"]
    )
@app.route("/esgotados")
@login_required
def shows_esgotados():

    atualizar_shows()

    lista = [
        show for show in SHOWS
        if show["esgotado"]
    ]

    return render_template(
        "esgotados.html",
        shows=lista,
        nome=session["nome_usuario"]
    )

@app.route("/categoria/<categoria>")
@login_required
def filtrar_categoria(categoria):

    shows_filtrados = [
        show for show in SHOWS
        if show["categoria"] == categoria
    ]

    return render_template(
        "index.html",
        shows=shows_filtrados,
        nome=session["nome_usuario"]
    )


@app.route("/login")
def login():
    return render_template("login.html", resultado=None)




@app.route("/autenticar", methods=["POST"])
def autenticar():

    email = request.form.get("email")
    senha = request.form.get("senha")

    for usuario in usuarios:

        if usuario.email == email and usuario.senha == senha:

            session["usuario"] = usuario.email
            session["usuario_id"] = usuario.id
            session["nome_usuario"] = usuario.nome

            return redirect(url_for("home"))

    return render_template(
        "login.html",
        resultado="falha"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/cadastro_usuario")
def cadastro_usuario():
    return render_template(
        "cadastro_usuario.html",
        resultado=None
    )
@app.route("/atualizar_foto", methods=["POST"])
@login_required
def atualizar_foto():

    foto = request.files.get("foto")

    if foto and foto.filename != "":

        nome_arquivo = foto.filename
        foto.save(f"static/img/{nome_arquivo}")

        for usuario in usuarios:
            if usuario.id == session["usuario_id"]:
                usuario.foto = nome_arquivo
                break

        salvar_usuarios_json()

    return redirect(url_for("perfil"))


@app.route("/salvar_usuario", methods=["POST"])
def salvar_usuario():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    data_nascimento = request.form.get("data_nascimento")
    genero = request.form.get("genero")

    adicionar_foto = request.form.get("adicionar_foto")

    if adicionar_foto == "sim":
        foto = request.files.get("foto")

        if foto and foto.filename != "":
            nome_arquivo = foto.filename
            foto.save(f"static/img/{nome_arquivo}")
        else:
            nome_arquivo = "sem_foto.png"
    else:
        nome_arquivo = "sem_foto.png"

    usuarios.append(
    Usuario(
    len(usuarios) + 1,
    nome,
    email,
    senha,
    data_nascimento,
    genero,
    nome_arquivo
)
    )

    salvar_usuarios_json()

    return redirect(url_for("login"))



@app.route("/comprar/<int:id>")
@login_required
def comprar(id):

    show = None

    for s in SHOWS:
        if s["id"] == id:
            show = s
            break

    return render_template(
        "comprar.html",
        show=show
    )

@app.route("/finalizar_compra", methods=["POST"])
@login_required
def finalizar_compra():

    show = request.form.get("show")
    preco = request.form.get("preco")
    local = request.form.get("local")
    data = request.form.get("data")
    pagamento = request.form.get("pagamento")

    codigo = str(uuid.uuid4())[:8]

    if pagamento == "PIX":

        texto_pix = (
            f"PIX\n"
            f"Show: {show}\n"
            f"Valor: R$ {preco}\n"
            f"Código: {codigo}"
        )

        img = qrcode.make(texto_pix)

        caminho = os.path.join("static", "img", f"{codigo}.png")
        img.save(caminho)

        return render_template(
            "pix.html",
            show=show,
            preco=preco,
            codigo=codigo
        )

    ingresso = Ingresso(
        id=len(ingressos) + 1,
        show=show,
        preco=preco,
        local=local,
        data=data,
        pagamento=pagamento,
        usuario_id=session["usuario"]
    )

    ingressos.append(ingresso)

    for s in shows:
        if s["nome"] == show:
            s["ingressos_vendidos"] += 1
            break

    salvar_ingressos_json()

    return redirect(url_for("home"))