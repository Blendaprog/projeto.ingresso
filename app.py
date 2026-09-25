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
from banco import Banco

app = Flask(__name__)
banco = Banco()
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
    Usuario(
        1,
        "Administrador",
        "admin@ticketshow.com",
        "Admin123",
        "admin",
        "2000-01-01",
        "M"
    )
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
        if (
            session.get("tipo") != "admin"
            or session.get("usuario") != ADMIN_EMAIL
        ):
            return "Acesso negado", 403

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

        if u.email == email and u.senha == senha:
            session["usuario"] = u.email
            session["usuario_id"] = u.id
            session["nome_usuario"] = u.nome
            session["tipo"] = u.tipo

            if u.tipo == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("home"))

        return render_template("login.html", resultado="falha")

    return render_template("login.html", resultado=None)

@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("admin.html", shows=SHOWS)

@app.route("/admin_vendas")
@login_required
@admin_required
def admin_vendas():

    vendas = []

    for ingresso in ingressos:

        usuario = next(
            (u for u in usuarios if u.id == ingresso.usuario_id),
            None
        )

        vendas.append({
            "codigo": ingresso.codigo,
            "show": ingresso.show,
            "preco": ingresso.preco,
            "local": ingresso.local,
            "data": ingresso.data,
            "pagamento": ingresso.pagamento,
            "usuario": usuario.nome if usuario else "Usuário"
        })

    faturamento = sum(v["preco"] for v in vendas)

    return render_template(
        "admin_vendas.html",
        vendas=vendas,
        faturamento=faturamento
    )

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

    print("EMAIL DIGITADO:", email)
    print("SENHA DIGITADA:", senha)

    for usuario in usuarios:
        print("USUARIO CADASTRADO:", usuario.email, usuario.senha)

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

    total_gasto = sum(
        float(ingresso.preco)
        for ingresso in meus
    )

    return render_template(
        "meus_ingressos.html",
        ingressos=meus,
        total_gasto=total_gasto
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

    if email.lower() != ADMIN_EMAIL:
        return "Somente o administrador principal pode utilizar esta conta.", 403

    if senha != ADMIN_SENHA:
        return "Senha de administrador inválida.", 403

    novo = Usuario(
        len(usuarios) + 1,
        "Administrador",
        ADMIN_EMAIL,
        ADMIN_SENHA,
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

    if session.get("tipo") == "admin":
        return redirect(url_for("admin"))

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
# =========================
# FILTRAR SHOWS POR LOCAL
# =========================

@app.route("/local/<path:local>")
@login_required
def filtrar_local(local):

    atualizar_shows()

    local_pesquisado = local.lower().strip()

    shows_filtrados = []

    for show in SHOWS:

        if show.get("esgotado", False):
            continue

        local_show = show.get("local", "").lower().strip()

        # Aceita variações como:
        # Allianz Parque
        # Allianz Parque - São Paulo

        if (
            local_show == local_pesquisado
            or local_show.startswith(local_pesquisado + " -")
            or local_show.startswith(local_pesquisado + ",")
        ):
            shows_filtrados.append(show)

    if not shows_filtrados:

        return render_template(
            "index.html",
            shows=[],
            nome=session.get("nome_usuario"),
            mensagem="Nenhum show encontrado nesse local."
        )

    return render_template(
        "index.html",
        shows=shows_filtrados,
        nome=session.get("nome_usuario"),
        local=local
    )


@app.route("/meus_shows")
@login_required
@admin_required
def meus_shows():

    meus = [
        s for s in SHOWS
        if s.get("admin", ADMIN_EMAIL) == session["usuario"]
    ]

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
           show.get("admin", ADMIN_EMAIL) == session["usuario"]
        )
    ]

    salvar_shows_json()

    return redirect(url_for("meus_shows"))

@app.route("/editar_show/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_show(id):

    show = next(
        (
            s for s in SHOWS
            if s["id"] == id
            and s.get("admin", ADMIN_EMAIL) == session["usuario"]
        ),
        None
    )

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

        # Garante que shows antigos também tenham um administrador
        show.setdefault("admin", session["usuario"])

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

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado", 404

    # Cria lotes para shows antigos que ainda não possuem
    if not show.get("lotes"):
        preco_base = float(show.get("preco", 0))

        show["lotes"] = [
            {
                "nome": "Lote 1",
                "quantidade": 50,
                "vendidos": 0,
                "preco": preco_base
            },
            {
                "nome": "Lote 2",
                "quantidade": 30,
                "vendidos": 0,
                "preco": preco_base + 20
            },
            {
                "nome": "Lote 3",
                "quantidade": 20,
                "vendidos": 0,
                "preco": preco_base + 40
            }
        ]

        show["ingressos_total"] = sum(
            lote["quantidade"]
            for lote in show["lotes"]
        )

        salvar_shows_json()

    if request.method == "POST":

        for i, lote in enumerate(show["lotes"]):

            quantidade = request.form.get(f"quantidade_{i}")
            preco = request.form.get(f"preco_{i}")

            # Só altera se o campo realmente veio do formulário
            if quantidade is not None:
                lote["quantidade"] = int(quantidade)

            if preco is not None:
                lote["preco"] = float(preco)

        show["ingressos_total"] = sum(
            lote.get("quantidade", 0)
            for lote in show["lotes"]
        )

        salvar_shows_json()

        return redirect(url_for("admin"))

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

    if session.get("tipo") == "admin":
        return redirect(url_for("admin"))

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
# =========================================================
# NOVAS FUNCIONALIDADES
# BANCO DO CARTÃO + ADMIN PRINCIPAL + NOVOS LOTES
# =========================================================

# ---------------------------------------------------------
# ADMINISTRADOR PRINCIPAL
# ---------------------------------------------------------

ADMIN_EMAIL_PRINCIPAL = "admin@ticketshow.com"
ADMIN_SENHA_PRINCIPAL = "Admin123"


# ---------------------------------------------------------
# VERIFICAÇÃO DO ADMIN PRINCIPAL
# ---------------------------------------------------------

def verificar_admin_principal():
    return (
        session.get("tipo") == "admin"
        and session.get("usuario") == ADMIN_EMAIL_PRINCIPAL
    )


# ---------------------------------------------------------
# LOGIN EXCLUSIVO DO ADMIN
# ---------------------------------------------------------

@app.route("/login_admin", methods=["GET", "POST"])
def login_admin_novo():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if (
            email == ADMIN_EMAIL_PRINCIPAL
            and senha == ADMIN_SENHA_PRINCIPAL
        ):
            session["usuario"] = ADMIN_EMAIL_PRINCIPAL
            session["usuario_id"] = 0
            session["nome_usuario"] = "Administrador"
            session["tipo"] = "admin"

            return redirect(url_for("painel_admin_novo"))

        return render_template(
            "login_admin.html",
            erro="E-mail ou senha incorretos."
        )

    return render_template("login_admin.html")


# ---------------------------------------------------------
# PAINEL EXCLUSIVO DO ADMIN
# ---------------------------------------------------------

@app.route("/painel_admin")
@login_required
def painel_admin_novo():

    if not verificar_admin_principal():
        return "Acesso permitido somente ao administrador principal.", 403

    atualizar_shows()

    return render_template(
        "admin.html",
        shows=SHOWS
    )


# ---------------------------------------------------------
# ADICIONAR NOVO LOTE
# ---------------------------------------------------------

@app.route("/adicionar_lote_novo/<int:id>", methods=["POST"])
@login_required
def adicionar_lote_novo(id):

    if not verificar_admin_principal():
        return "Acesso permitido somente ao administrador principal.", 403

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    if "lotes" not in show:
        show["lotes"] = []

    nome_lote = request.form.get("nome_lote", "").strip()
    quantidade = request.form.get("quantidade")
    preco = request.form.get("preco")

    if not nome_lote or not quantidade or not preco:
        return "Preencha todos os campos do lote."

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        return "Quantidade ou preço inválido."

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero."

    if preco <= 0:
        return "O preço deve ser maior que zero."

    novo_lote = {
        "nome": nome_lote,
        "quantidade": quantidade,
        "vendidos": 0,
        "preco": preco
    }

    show["lotes"].append(novo_lote)

    # Recalcula o total de ingressos
    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for(
            "gerenciar_lotes",
            id=id
        )
    )


# ---------------------------------------------------------
# EDITAR LOTES PELO NOVO PAINEL
# ---------------------------------------------------------

@app.route("/salvar_lotes_novo/<int:id>", methods=["POST"])
@login_required
def salvar_lotes_novo(id):

    if not verificar_admin_principal():
        return "Acesso permitido somente ao administrador principal.", 403

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    if "lotes" not in show:
        show["lotes"] = []

    for i, lote in enumerate(show["lotes"]):

        quantidade = request.form.get(
            f"quantidade_{i}"
        )

        preco = request.form.get(
            f"preco_{i}"
        )

        if quantidade is not None:
            try:
                lote["quantidade"] = int(quantidade)
            except ValueError:
                return "Quantidade inválida."

        if preco is not None:
            try:
                lote["preco"] = float(preco)
            except ValueError:
                return "Preço inválido."

    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for(
            "gerenciar_lotes",
            id=id
        )
    )


# ---------------------------------------------------------
# PAGAMENTO COM CARTÃO — NOVA VERSÃO
# ---------------------------------------------------------

@app.route("/pagar_cartao_novo", methods=["POST"])
@login_required
def pagar_cartao_novo():

    show = request.form.get("show")
    local = request.form.get("local")
    data = request.form.get("data")
    codigo = request.form.get("codigo")

    tipo_cartao = request.form.get("tipo_cartao")
    banco = request.form.get("banco")

    numero = request.form.get("numero")
    nome = request.form.get("nome")
    validade = request.form.get("validade")
    cvv = request.form.get("cvv")
    parcelas = request.form.get("parcelas")

    # -----------------------------------------------------
    # VALIDAÇÃO
    # -----------------------------------------------------

    if not tipo_cartao:
        return "Selecione o tipo do cartão."

    if not banco:
        return "Selecione o banco."

    if not numero:
        return "Informe o número do cartão."

    if not nome:
        return "Informe o nome do titular."

    if not validade:
        return "Informe a validade do cartão."

    if not cvv:
        return "Informe o CVV."

    # -----------------------------------------------------
    # LOCALIZA O SHOW
    # -----------------------------------------------------

    show_obj = next(
        (s for s in SHOWS if s["nome"] == show),
        None
    )

    if show_obj is None:
        return redirect(url_for("home"))

    # -----------------------------------------------------
    # PREÇO
    # -----------------------------------------------------

    preco = float(show_obj.get("preco", 0))

    # -----------------------------------------------------
    # FORMA DE PAGAMENTO
    # -----------------------------------------------------

    pagamento = f"Cartão - {tipo_cartao} - {banco}"

    if tipo_cartao == "Crédito":

        if not parcelas:
            parcelas = "1"

        pagamento += f" - {parcelas}x"

    # -----------------------------------------------------
    # CRIA INGRESSO
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # ATUALIZA VENDAS
    # -----------------------------------------------------

    show_obj["ingressos_vendidos"] = (
        show_obj.get("ingressos_vendidos", 0) + 1
    )

    salvar_ingressos_json()
    salvar_shows_json()

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


# ---------------------------------------------------------
# DESLOGAR DO ADMIN
# ---------------------------------------------------------

@app.route("/logout_admin")
def logout_admin_novo():

    session.clear()

    return redirect(
        url_for("login_admin_novo")
    )


# =========================================================
# FIM DAS NOVAS FUNCIONALIDADES
# =========================================================
# ============================================================
# 👑 CONTROLE DO ADMINISTRADOR PRINCIPAL - TICKETSHOW
# ============================================================

# ------------------------------------------------------------
# DADOS DO ADMIN PRINCIPAL
# ------------------------------------------------------------
# ALTERE AQUI PARA O E-MAIL E SENHA QUE VOCÊ QUISER

ADMIN_EMAIL = "admin@ticketshow.com"
ADMIN_SENHA = "Admin123"


# ------------------------------------------------------------
# VERIFICA SE O USUÁRIO LOGADO É O ADMIN PRINCIPAL
# ------------------------------------------------------------

def eh_admin_principal():
    return (
        session.get("usuario") == ADMIN_EMAIL
        and session.get("tipo") == "admin"
    )


# ------------------------------------------------------------
# PROTEÇÃO DO PAINEL ADMINISTRATIVO
# ------------------------------------------------------------

@app.route("/acesso_admin")
def acesso_admin():

    if eh_admin_principal():
        return redirect(url_for("admin"))

    return render_template("login_admin.html")


# ------------------------------------------------------------
# LOGIN EXCLUSIVO DO ADMIN
# ------------------------------------------------------------

@app.route("/entrar_admin", methods=["POST"])
def entrar_admin():

    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")

    if email == ADMIN_EMAIL.lower() and senha == ADMIN_SENHA:

        session.clear()

        session["usuario"] = ADMIN_EMAIL
        session["usuario_id"] = 0
        session["nome_usuario"] = "Administrador"
        session["tipo"] = "admin"

        return redirect(url_for("admin"))

    return render_template(
        "login_admin.html",
        erro="E-mail ou senha incorretos."
    )


# ------------------------------------------------------------
# SAÍDA DO ADMIN
# ------------------------------------------------------------

@app.route("/sair_admin")
def sair_admin():

    session.clear()

    return redirect(url_for("acesso_admin"))


# ============================================================
# 🔒 FUNÇÃO PARA GARANTIR QUE SOMENTE O ADMIN ALTERE O SITE
# ============================================================

def somente_admin():

    if not eh_admin_principal():
        return False

    return True


# ============================================================
# 🎟️ ADICIONAR LOTE
# ============================================================

@app.route("/novo_lote/<int:id>", methods=["POST"])
@login_required
def novo_lote(id):

    if not somente_admin():
        return "Acesso negado. Somente o administrador pode alterar os lotes.", 403

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    if "lotes" not in show:
        show["lotes"] = []

    nome = request.form.get("nome_lote", "").strip()
    quantidade = request.form.get("quantidade")
    preco = request.form.get("preco")

    if not nome or not quantidade or not preco:
        return "Preencha todos os campos do lote."

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        return "Quantidade ou preço inválido."

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero."

    if preco <= 0:
        return "O preço deve ser maior que zero."

    show["lotes"].append({
        "nome": nome,
        "quantidade": quantidade,
        "vendidos": 0,
        "preco": preco
    })

    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for("gerenciar_lotes", id=id)
    )


# ============================================================
# 💰 ATUALIZAR LOTES
# ============================================================

@app.route("/atualizar_lotes_admin/<int:id>", methods=["POST"])
@login_required
def atualizar_lotes_admin(id):

    if not somente_admin():
        return "Acesso negado. Somente o administrador pode alterar os lotes.", 403

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    if "lotes" not in show:
        show["lotes"] = []

    for i, lote in enumerate(show["lotes"]):

        quantidade = request.form.get(
            f"quantidade_{i}"
        )

        preco = request.form.get(
            f"preco_{i}"
        )

        if quantidade:
            try:
                lote["quantidade"] = int(quantidade)
            except ValueError:
                return "Quantidade inválida."

        if preco:
            try:
                lote["preco"] = float(preco)
            except ValueError:
                return "Preço inválido."

    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for("gerenciar_lotes", id=id)
    )


# ============================================================
# ➕ CADASTRAR SHOW PELO ADMIN
# ============================================================

@app.route("/admin_novo_show", methods=["POST"])
@login_required
def admin_novo_show():

    if not somente_admin():
        return "Acesso negado.", 403

    try:

        novo_show = {
            "id": max(
                [s["id"] for s in SHOWS],
                default=0
            ) + 1,

            "nome": request.form["nome"],

            "categoria": request.form["categoria"],

            "local": request.form["local"],

            "data": request.form["data"],

            "idade_minima": int(
                request.form["idade_minima"]
            ),

            "preco": float(
                request.form["preco"]
            ),

            "imagem": request.form.get(
                "imagem",
                "sem_imagem.png"
            ),

            "ingressos_total": 0,

            "ingressos_vendidos": 0,

            "lotes": [],

            "admin": ADMIN_EMAIL
        }

    except (ValueError, KeyError):

        return "Dados inválidos para cadastrar o show.", 400

    SHOWS.append(novo_show)

    salvar_shows_json()

    return redirect(url_for("meus_shows"))


# ============================================================
# ✏️ EDITAR SHOW PELO ADMIN
# ============================================================

@app.route("/admin_editar_show/<int:id>", methods=["POST"])
@login_required
def admin_editar_show(id):

    if not somente_admin():
        return "Acesso negado.", 403

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    try:

        show["nome"] = request.form["nome"]

        show["categoria"] = request.form["categoria"]

        show["local"] = request.form["local"]

        show["data"] = request.form["data"]

        show["idade_minima"] = int(
            request.form["idade_minima"]
        )

        show["preco"] = float(
            request.form["preco"]
        )

    except (ValueError, KeyError):

        return "Dados inválidos.", 400

    salvar_shows_json()

    return redirect(url_for("meus_shows"))


# ============================================================
# 🗑️ EXCLUIR SHOW PELO ADMIN
# ============================================================

@app.route("/admin_excluir_show/<int:id>")
@login_required
def admin_excluir_show(id):

    if not somente_admin():
        return "Acesso negado.", 403

    global SHOWS

    SHOWS = [
        show
        for show in SHOWS
        if show["id"] != id
    ]

    salvar_shows_json()

    return redirect(url_for("meus_shows"))


# ============================================================
# ⭐ DEFINIR SHOW COMO DESTAQUE
# ============================================================

@app.route("/admin_destaque/<int:id>")
@login_required
def admin_destaque(id):

    if not somente_admin():
        return "Acesso negado.", 403

    for show in SHOWS:

        show["destaque"] = (
            show["id"] == id
        )

    salvar_shows_json()

    return redirect(url_for("meus_shows"))


# ============================================================
# 🔐 BLOQUEIO EXTRA
# ============================================================
# Se alguém tentar acessar funções administrativas
# sem ser o administrador principal, será bloqueado.

@app.before_request
def proteger_area_administrativa():

    rotas_admin = [

        "admin",
        "meus_shows",
        "cadastrar_show",
        "editar_show",
        "excluir_show",
        "definir_destaque",
        "gerenciar_lotes",
        "editar_ingressos"

    ]

    if request.endpoint in rotas_admin:

        if not eh_admin_principal():

            if "usuario" not in session:
                return redirect(url_for("login"))

            return "Acesso negado. Área exclusiva do administrador.", 403


# ============================================================
# FIM DO CONTROLE ADMINISTRATIVO
# ============================================================
# =========================================================
# CONTROLE DO ADMINISTRADOR
# =========================================================

# COLOQUE AQUI O E-MAIL DA SUA CONTA DE ADMIN
EMAIL_ADMIN = "SEU_EMAIL_DE_ADMIN@gmail.com"


# =========================================================
# ÁREA EXCLUSIVA DO ADMIN
# =========================================================

@app.route("/area_admin")
@login_required
@admin_required
def area_admin():

    atualizar_shows()

    return render_template(
        "admin.html",
        shows=SHOWS,
        nome=session.get("nome_usuario")
    )


# =========================================================
# ADICIONAR NOVO LOTE
# =========================================================

@app.route("/adicionar_lote/<int:id>", methods=["POST"])
@login_required
@admin_required
def adicionar_lote(id):

    show = next(
        (s for s in SHOWS if s["id"] == id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    nome_lote = request.form.get("nome_lote")
    quantidade = request.form.get("quantidade")
    preco = request.form.get("preco")

    if not nome_lote or not quantidade or not preco:
        return "Preencha todos os campos.", 400

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        return "Quantidade ou preço inválido.", 400

    if quantidade <= 0 or preco <= 0:
        return "Digite valores maiores que zero.", 400

    if "lotes" not in show:
        show["lotes"] = []

    novo_lote = {
        "nome": nome_lote,
        "quantidade": quantidade,
        "vendidos": 0,
        "preco": preco
    }

    show["lotes"].append(novo_lote)

    # Atualiza a quantidade total de ingressos
    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for("gerenciar_lotes", id=id)
    )


# =========================================================
# EXCLUIR LOTE
# =========================================================

@app.route("/excluir_lote/<int:show_id>/<int:lote_id>")
@login_required
@admin_required
def excluir_lote(show_id, lote_id):

    show = next(
        (s for s in SHOWS if s["id"] == show_id),
        None
    )

    if show is None:
        return "Show não encontrado.", 404

    if "lotes" not in show:
        return redirect(
            url_for("gerenciar_lotes", id=show_id)
        )

    if lote_id < 0 or lote_id >= len(show["lotes"]):
        return "Lote não encontrado.", 404

    lote = show["lotes"][lote_id]

    # Não deixa apagar lote que já vendeu ingresso
    if lote.get("vendidos", 0) > 0:
        return (
            "Não é possível excluir um lote "
            "que já possui ingressos vendidos."
        ), 400

    show["lotes"].pop(lote_id)

    # Atualiza o total
    show["ingressos_total"] = sum(
        lote.get("quantidade", 0)
        for lote in show["lotes"]
    )

    salvar_shows_json()

    return redirect(
        url_for("gerenciar_lotes", id=show_id)
    )


# =========================================================
# DISPONIBILIZA A INFORMAÇÃO DE ADMIN PARA OS HTMLS
# =========================================================

@app.context_processor
def verificar_usuario_admin():

    eh_admin = (
        session.get("usuario") == EMAIL_ADMIN
    )

    return {
        "eh_admin": eh_admin
    }

if __name__ == "__main__":
    print("Flask iniciando...")
    app.run(debug=True)
