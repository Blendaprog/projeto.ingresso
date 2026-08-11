import json
import os
import uuid
import random
from datetime import datetime
from functools import wraps

import mercadopago
import qrcode

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message

from modelos import Usuario, Ingresso

app = Flask(__name__)
app.secret_key = "segredo"

# =========================
# MERCADO PAGO
# =========================
sdk = mercadopago.SDK("SEU_ACCESS_TOKEN_DE_TESTE")  # Depois troque pelo seu Access Token

# =========================
# FLASK-MAIL
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "ticketshows26@gmail.com"
app.config["MAIL_PASSWORD"] = "SUA_SENHA_DE_APP"

mail = Mail(app)

# =========================
# DADOS
# =========================
usuarios = [
    Usuario(1, "Admin", "admin@gmail.com", "123", "admin", "2000-01-01", "M")
]

ingressos = []
@app.route("/pagar", methods=["POST"])
def pagar():

    pagamento = {
        "transaction_amount": float(request.form["valor"]),
        "description": "Compra de ingresso",
        "payment_method_id": "pix",
        "payer": {
            "email": "teste@email.com"
        }
    }

    resultado = sdk.payment().create(pagamento)

    qr_code = resultado["response"]["point_of_interaction"]["transaction_data"]["qr_code"]

    return render_template("pix.html", qr_code=qr_code)


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
        "preco": 250,
        "local": "A definir!",
        "data": "A definir!",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "BRANDAO.png"
    },
    {
        "id": 18,
        "nome": "Kyan",
        "preco": 220,
        "local": "A definir!",
        "data": "A definir!",
        "idade_minima": 18,
        "categoria": "Trap",
        "imagem": "kyan.png"
    },
    {
        "id": 19,
        "nome": "Marina Sena",
        "preco": 220,
        "local": "Parque Ibirapuera!",
        "data": "2026-06-13",
        "idade_minima": 16,
        "categoria": "Trap",
        "imagem": "marinasena.png"
    },
    {
        "id": 20,
        "nome": "Mc paiva",
        "preco": 180,
        "local": "Vigor On Stage",
        "data": "2026-07-18",
        "idade_minima": 18,
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

def corrigir_shows():
    for s in SHOWS:
        s.setdefault("ingressos_total", 100)
        s.setdefault("ingressos_vendidos", 0)

corrigir_shows()

# ---------------------------------------------------------------------------
# Carrega usuarios salvos em disco (se existir o arquivo)
# ---------------------------------------------------------------------------
try:
    with open("usuarios.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        usuarios = [Usuario(**usuario) for usuario in dados]
except FileNotFoundError:
    pass


def _to_dict(obj):
    """Converte um objeto Usuario/Ingresso em dict para salvar em JSON."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj)


def salvar_usuarios_json():
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        json.dump([_to_dict(u) for u in usuarios], arquivo, ensure_ascii=False, indent=2)
def salvar_shows_json():
    with open("shows.json", "w", encoding="utf-8") as arquivo:
        json.dump(SHOWS, arquivo, ensure_ascii=False, indent=2)

def salvar_ingressos_json():
    with open("ingressos.json", "w", encoding="utf-8") as arquivo:
        json.dump([_to_dict(i) for i in ingressos], arquivo, ensure_ascii=False, indent=2)


def atualizar_shows():
    for show in SHOWS:
        if "ingressos_total" not in show:
            show["ingressos_total"] = 100

        if "ingressos_vendidos" not in show:
            show["ingressos_vendidos"] = 0

        show["esgotado"] = show["ingressos_vendidos"] >= show["ingressos_total"]


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        for u in usuarios:
            if u.email == email and u.senha == senha:
                session["usuario"] = u.email
                session["usuario_id"] = u.id
                session["nome_usuario"] = u.nome
                session["tipo"] = u.tipo

                return redirect(url_for("home"))

        return render_template("login.html", resultado="falha")

    return render_template("login.html", resultado=None)

@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("admin.html", shows=SHOWS)

@app.route("/editar_ingressos/<int:id>", methods=["POST"])
@login_required
@admin_required
def editar_ingressos(id):

    for show in SHOWS:
        if show["id"] == id:
            show["ingressos_total"] = int(request.form["total"])
            show["ingressos_vendidos"] = int(request.form["vendidos"])
            break

    salvar_shows_json()

    return redirect(url_for("admin"))


    


@app.route("/autenticar", methods=["POST"])
def autenticar():

    email = request.form.get("email")
    senha = request.form.get("senha")

    for usuario in usuarios:
        if usuario.email == email and usuario.senha == senha:
            session["usuario"] = usuario.email
            session["usuario_id"] = usuario.id
            session["nome_usuario"] = usuario.nome
            session["tipo"] = usuario.tipo

            return redirect(url_for("home"))

    return render_template("login.html", resultado="falha")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/cadastro_usuario")
def cadastro_usuario():
    return render_template("cadastro_usuario.html", resultado=None)




@app.route("/salvar_usuario", methods=["POST"])
def salvar_usuario():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    data_nascimento = request.form.get("data_nascimento")
    genero = request.form.get("genero")

    adicionar_foto = request.form.get("adicionar_foto")

    nome_arquivo = "sem_foto.png"
    if adicionar_foto == "sim":
        foto = request.files.get("foto")
        if foto and foto.filename != "":
            nome_arquivo = foto.filename
            foto.save(os.path.join("static", "img", nome_arquivo))

    usuarios.append(
        Usuario(
            len(usuarios) + 1,
            nome,
            email,
            senha,
            "usuario",
            data_nascimento,
            genero,
            nome_arquivo
        )
    )

    salvar_usuarios_json()

    return redirect(url_for("login"))

@app.route("/meus_ingressos")
@login_required
def meus_ingressos():

    meus = [
        ingresso for ingresso in ingressos
        if ingresso.usuario_id == session["usuario_id"]
    ]

    return render_template(
        "meus_ingressos.html",
        ingressos=meus
    )

@app.route("/cancelar_ingresso/<int:id>")
@login_required
def cancelar_ingresso(id):

    global ingressos

    ingressos = [
        ingresso for ingresso in ingressos
        if not (
            ingresso.id == id and
            ingresso.usuario_id == session["usuario_id"]
        )
    ]

    salvar_ingressos_json()

    return redirect(url_for("meus_ingressos"))

@app.route("/meu_ingresso/<codigo>")
@login_required
def meu_ingresso(codigo):

    ingresso = next((i for i in ingressos if i.codigo == codigo), None)

    if ingresso is None:
        return redirect(url_for("home"))

    return render_template("ingresso.html", ingresso=ingresso)

@app.route("/cadastro_adm")
def cadastro_adm():
    return render_template("cadastro_adm.html")


@app.route("/salvar_adm", methods=["POST"])
def salvar_adm():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    data_nascimento = request.form.get("data_nascimento")
    genero = request.form.get("genero")

    codigo = str(random.randint(100000, 999999))
    session["codigo_verificacao"] = codigo




    novo = Usuario(
        len(usuarios) + 1,
        nome,
        email,
        senha,
        "admin",
        data_nascimento,
        genero
    )

    usuarios.append(novo)
    salvar_usuarios_json()

    return redirect(url_for("login"))

@app.route("/perfil")
@login_required
def perfil():

    usuario_atual = next(
        (u for u in usuarios if u.id == session["usuario_id"]),
        None
    )

    return render_template("perfil.html", usuario=usuario_atual)


@app.route("/atualizar_foto", methods=["POST"])
@login_required
def atualizar_foto():

    foto = request.files.get("foto")

    if foto and foto.filename != "":
        nome_arquivo = foto.filename
        foto.save(os.path.join("static", "img", nome_arquivo))

        for usuario in usuarios:
            if usuario.id == session["usuario_id"]:
                usuario.foto = nome_arquivo
                break

        salvar_usuarios_json()

    return redirect(url_for("perfil"))

@app.route("/verificar", methods=["GET", "POST"])
def verificar():

    if request.method == "POST":
        codigo_digitado = request.form["codigo"]

        if codigo_digitado == session.get("codigo_verificacao"):
            return redirect(url_for("login"))
        else:
            return "Código inválido"

    return render_template("verificar.html")




# ---------------------------------------------------------------------------
# Shows
# ---------------------------------------------------------------------------
@app.route("/")
@login_required
def home():

    atualizar_shows()

    shows_disponiveis = [show for show in SHOWS if not show["esgotado"]]

    destaque = next(
    (show for show in shows_disponiveis if show.get("destaque")),
    shows_disponiveis[0] if shows_disponiveis else None
)
    return render_template(
        "index.html",
        shows=shows_disponiveis,
        destaque=destaque,
        nome=session.get("nome_usuario")
    )

@app.route("/categorias")
@login_required
def categorias():
    return render_template("categorias.html")

@app.route("/categoria/<categoria>")
@login_required
def filtrar_categoria(categoria):

    atualizar_shows()

    categoria = categoria.lower()

    shows_filtrados = [
        show for show in SHOWS
        if show.get("categoria", "").lower() == categoria
        and not show.get("esgotado", False)
    ]

    # 🔥 AQUI VOCÊ COLOCA O CÓDIGO
    if not shows_filtrados:
        return render_template(
            "index.html",
            shows=[],
            nome=session.get("nome_usuario"),
            mensagem="Nenhum show encontrado nessa categoria."
        )

    return render_template(
        "index.html",
        shows=shows_filtrados,
        nome=session.get("nome_usuario"),
        categoria=categoria
    )



@app.route("/meus_shows")
@login_required
@admin_required
def meus_shows():
    meus = [s for s in SHOWS if s.get("admin") == session["usuario"]]
    return render_template("meus_shows.html", shows=meus)

@app.route("/definir_destaque/<int:id>")
@login_required
@admin_required
def definir_destaque(id):

    for show in SHOWS:
        if show["id"] == id:
            for outro in SHOWS:
                outro["destaque"] = False

            show["destaque"] = True

            break

    return redirect(url_for("meus_shows"))

@app.route("/excluir_show/<int:id>")
@login_required
@admin_required
def excluir_show(id):

    global SHOWS

    SHOWS = [
        show for show in SHOWS
        if not (
            show["id"] == id and
            show["admin"] == session["usuario"]
        )
    ]

    salvar_shows_json()

    return redirect(url_for("meus_shows"))

@app.route("/editar_show/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_show(id):

    show = next((s for s in SHOWS if s["id"] == id and s["admin"] == session["usuario"]), None)

    if show is None:
        return redirect(url_for("meus_shows"))

    if request.method == "POST":

        show["nome"] = request.form["nome"]
        show["categoria"] = request.form["categoria"]
        show["local"] = request.form["local"]
        show["data"] = request.form["data"]
        show["preco"] = float(request.form["preco"])
        show["idade_minima"] = int(request.form["idade_minima"])
        show["ingressos_total"] = int(request.form["ingressos_total"])

        salvar_shows_json()

        return redirect(url_for("meus_shows"))

    return render_template("editar_show.html", show=show)


@app.route("/cadastrar_show", methods=["GET", "POST"])
@login_required
@admin_required
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
            "ingressos_vendidos": 0,

            "lotes": [
                {
                    "nome": "Lote 1",
                    "quantidade": 50,
                    "vendidos": 0,
                    "preco": float(request.form["preco"])
                },
                {
                    "nome": "Lote 2",
                    "quantidade": 30,
                    "vendidos": 0,
                    "preco": float(request.form["preco"]) + 20
                },
                {
                    "nome": "Lote 3",
                    "quantidade": 20,
                    "vendidos": 0,
                    "preco": float(request.form["preco"]) + 40
                }
            ],

            "admin": session["usuario"]
        }

        SHOWS.append(novo_show)

        salvar_shows_json()

        return redirect(url_for("meus_shows"))

    return render_template("cadastrar_show.html")



@app.route("/gerenciar_lotes/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def gerenciar_lotes(id):

    show = next((s for s in SHOWS if s["id"] == id), None)

    if show is None:
        return "Show não encontrado", 404

    if request.method == "POST":

        for i, lote in enumerate(show["lotes"]):

            lote["quantidade"] = int(
                request.form[f"quantidade_{i}"]
            )

            lote["preco"] = float(
                request.form[f"preco_{i}"]
            )

        show["ingressos_total"] = sum(
            lote["quantidade"]
            for lote in show["lotes"]
        )

        salvar_shows_json()

        return redirect(url_for("meus_shows"))

    return render_template(
        "gerenciar_lotes.html",
        show=show
    )

# ---------------------------------------------------------------------------
# Compra de ingressos
# ---------------------------------------------------------------------------
@app.route("/comprar/<int:id>")
@login_required
def comprar(id):

    show = next((s for s in SHOWS if s["id"] == id), None)

    if show is None:
        return redirect(url_for("home"))

    return render_template("comprar.html", show=show)

@app.route("/finalizar_compra", methods=["POST"])
@login_required
def finalizar_compra():

    show = request.form.get("show")
    local = request.form.get("local")
    data = request.form.get("data")
    pagamento = request.form.get("pagamento")

    codigo = str(uuid.uuid4())[:8]

    # pega o show real
    show_obj = next((s for s in SHOWS if s["nome"] == show), None)

    if show_obj is None:
        return redirect(url_for("home"))

    # preço do show
    preco = show_obj["preco"]

    # PIX
    if pagamento == "PIX":

        ingresso = Ingresso(
            id=len(ingressos) + 1,
            show=show,
            preco=preco,
            local=local,
            data=data,
            pagamento="PIX",
            usuario_id=session["usuario_id"],
            codigo=codigo
        )

        ingressos.append(ingresso)

        # atualiza vendas
        show_obj["ingressos_vendidos"] = show_obj.get("ingressos_vendidos", 0) + 1

        salvar_ingressos_json()

        texto_pix = (
            f"PIX\n"
            f"Show: {show}\n"
            f"Valor: R$ {preco}\n"
            f"Código: {codigo}"
        )

        img = qrcode.make(texto_pix)

        caminho = os.path.join(
            "static",
            "img",
            f"{codigo}.png"
        )

        img.save(caminho)

        return render_template(
            "pix.html",
            show=show,
            preco=preco,
            codigo=codigo,
            qr_code=f"img/{codigo}.png"
        )

    # CARTÃO
    elif pagamento == "CARTAO":

        return render_template(
            "cartao.html",
            show=show,
            preco=preco,
            codigo=codigo,
            local=local,
            data=data
        )

        data_formatada = datetime.strptime(data, "%Y-%m-%d")
    return redirect(url_for("home"))

@app.route("/pagar_cartao", methods=["POST"])
@login_required
def pagar_cartao():

    show = request.form.get("show")
    local = request.form.get("local")
    data = request.form.get("data")
    preco = float(request.form.get("preco"))
    codigo = request.form.get("codigo")

    tipo_cartao = request.form.get("tipo_cartao")
    numero = request.form.get("numero")
    nome = request.form.get("nome")
    validade = request.form.get("validade")
    cvv = request.form.get("cvv")
    parcelas = request.form.get("parcelas")

    # verifica se os campos foram preenchidos
    if not tipo_cartao or not numero or not nome or not validade or not cvv:
        return "Preencha todos os dados do cartão."

    # forma de pagamento
    pagamento = f"Cartão - {tipo_cartao}"

    if tipo_cartao == "Crédito":
        pagamento += f" - {parcelas}x"

    # cria ingresso somente depois do pagamento
    ingresso = Ingresso(
        id=len(ingressos) + 1,
        show=show,
        preco=preco,
        local=local,
        data=data,
        pagamento=pagamento,
        usuario_id=session["usuario_id"],
        codigo=codigo
    )

    ingressos.append(ingresso)

    # atualiza vendas
    show_obj = next((s for s in SHOWS if s["nome"] == show), None)

    if show_obj:
        show_obj["ingressos_vendidos"] = show_obj.get(
            "ingressos_vendidos", 0
        ) + 1

    salvar_ingressos_json()

    return render_template(
        "confirmacao.html",
        ingresso=ingresso,
        show=show,
        preco=preco,
        local=local,
        data=data,
        pagamento=pagamento,
        codigo=codigo
    )


@app.route("/esgotados")
@login_required
def esgotados():

    shows_esgotados = [
        show for show in SHOWS
        if show.get("ingressos_vendidos", 0)
        >= show.get("ingressos_total", 0)
    ]

    return render_template(
        "esgotados.html",
        shows=shows_esgotados
    )


if __name__ == "__main__":
    print("Flask iniciando...")
    app.run(debug=True)
