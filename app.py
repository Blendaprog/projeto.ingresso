import json
import os
import uuid
import random
import secrets
import hmac
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import abort, flash

import mercadopago
import qrcode

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from modelos import Usuario, Ingresso
from clima import buscar_clima
from cep import buscar_cep

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-local-apenas-para-desenvolvimento")
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT", "ticketshow-reset-local")

# =========================
# MERCADO PAGO
# =========================
sdk = mercadopago.SDK(os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_DE_TESTE"))  # Depois troque pelo seu Access Token

# =========================
# FLASK-MAIL
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME", "noreply@ticketshow.local")

mail = Mail(app)

# =========================
# DADOS
# =========================
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
    with open(os.path.join(os.path.dirname(__file__), "usuarios.json"), "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        usuarios = [Usuario(**usuario) for usuario in dados]
except FileNotFoundError:
    pass


# Restaurar shows e ingressos salvos; não perder alterações após reiniciar.
for nome_arquivo, destino in (("shows.json", "shows"), ("ingressos.json", "ingressos")):
    try:
        with open(os.path.join(os.path.dirname(__file__), nome_arquivo), encoding="utf-8") as arquivo:
            dados_salvos = json.load(arquivo)
        if isinstance(dados_salvos, list):
            if destino == "shows":
                SHOWS = dados_salvos
            else:
                ingressos = [Ingresso(**item) for item in dados_salvos]
    except (OSError, ValueError, TypeError):
        pass

corrigir_shows()

# Evita colisões de login entre cadastros antigos duplicados.
# Um administrador com e-mail repetido não será escolhido automaticamente.
# Para criar ou redefinir uma conta administrativa, rode: flask --app app criar-admin.
normalizados = []
emails_vistos = set()
for usuario in sorted(usuarios, key=lambda u: (u.email.strip().lower(), u.tipo == "admin", u.id)):
    email_normalizado = usuario.email.strip().lower()
    if email_normalizado and email_normalizado not in emails_vistos:
        usuario.email = email_normalizado
        emails_vistos.add(email_normalizado)
        normalizados.append(usuario)
usuarios = normalizados

# Migração automática de senhas antigas em texto para hashes.
senhas_migradas = False
for usuario in usuarios:
    if not usuario.senha.startswith(("scrypt:", "pbkdf2:")):
        usuario.senha = generate_password_hash(usuario.senha)
        senhas_migradas = True

def _to_dict(obj):
    """Converte um objeto Usuario/Ingresso em dict para salvar em JSON."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return vars(obj)


def salvar_usuarios_json():
    with open(os.path.join(os.path.dirname(__file__), "usuarios.json"), "w", encoding="utf-8") as arquivo:
        json.dump([_to_dict(u) for u in usuarios], arquivo, ensure_ascii=False, indent=2)
# Normalização dos cadastros é persistida no primeiro carregamento.
salvar_usuarios_json()

def salvar_shows_json():
    with open(os.path.join(os.path.dirname(__file__), "shows.json"), "w", encoding="utf-8") as arquivo:
        json.dump(SHOWS, arquivo, ensure_ascii=False, indent=2)

def salvar_ingressos_json():
    with open(os.path.join(os.path.dirname(__file__), "ingressos.json"), "w", encoding="utf-8") as arquivo:
        json.dump([_to_dict(i) for i in ingressos], arquivo, ensure_ascii=False, indent=2)


def atualizar_shows():
    for show in SHOWS:
        if "ingressos_total" not in show:
            show["ingressos_total"] = 100

        if "ingressos_vendidos" not in show:
            show["ingressos_vendidos"] = 0

        show.setdefault("nome", "Evento")
        show.setdefault("preco", 0)
        show.setdefault("local", "A confirmar")
        show.setdefault("data", "")
        show.setdefault("categoria", "Outros")
        show.setdefault("lotes", [])
        show["esgotado"] = show["ingressos_vendidos"] >= show["ingressos_total"]


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session or not any(u.id == session.get("usuario_id") and u.email == session.get("usuario") for u in usuarios):
            session.clear()
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        usuario = next((u for u in usuarios
                        if u.id == session.get("usuario_id")
                        and u.email == session.get("usuario")), None)
        if usuario is None or usuario.tipo != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@app.route("/pagar", methods=["POST"])
@login_required
def pagar():
    # Compatibilidade com formulários antigos: sempre apresenta o checkout.
    return finalizar_compra()


# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------
def autenticar_credenciais(email, senha):
    email = (email or "").strip().lower()
    for usuario in usuarios:
        if usuario.email.strip().lower() != email:
            continue
        try:
            valido = check_password_hash(usuario.senha, senha or "")
        except (ValueError, TypeError):
            valido = False
        if valido:
            session.clear()
            session["usuario"] = usuario.email
            session["usuario_id"] = usuario.id
            session["nome_usuario"] = usuario.nome
            session["tipo"] = usuario.tipo
            return True
    return False


def gerar_token_redefinicao(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def validar_token_redefinicao(token, validade=900):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        return serializer.loads(
            token,
            salt=app.config["SECURITY_PASSWORD_SALT"],
            max_age=validade,
        )
    except (BadSignature, SignatureExpired):
        return None


@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    mensagem = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        usuario = next((u for u in usuarios if u.email.lower() == email), None)
        # A mesma resposta é exibida exista ou não a conta, evitando revelar cadastros.
        if usuario:
            token = gerar_token_redefinicao(usuario.email)
            link = url_for("redefinir_senha", token=token, _external=True)
            try:
                mensagem_email = Message(
                    subject="TicketShow | Recuperação de senha",
                    recipients=[usuario.email],
                    body=(
                        f"Olá, {usuario.nome}!\n\n"
                        "Recebemos um pedido para redefinir sua senha. "
                        "Acesse o link abaixo em até 15 minutos:\n\n"
                        f"{link}\n\n"
                        "Se você não solicitou, ignore este e-mail."
                    ),
                )
                mail.send(mensagem_email)
            except Exception:
                app.logger.exception("Não foi possível enviar o e-mail de recuperação.")
                flash("Não foi possível enviar o e-mail agora. Confira a configuração de e-mail.", "erro")
                return render_template("esqueci_senha.html", mensagem=None), 503
        mensagem = "Se o e-mail estiver cadastrado, você receberá um link de recuperação."
    return render_template("esqueci_senha.html", mensagem=mensagem)


@app.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    email = validar_token_redefinicao(token)
    if not email:
        return render_template(
            "redefinir_senha.html", token=None, expirado=True
        ), 400
    usuario = next((u for u in usuarios if u.email.lower() == email.lower()), None)
    if usuario is None:
        abort(404)
    if request.method == "POST":
        senha = request.form.get("senha") or ""
        confirmacao = request.form.get("confirmacao") or ""
        if len(senha) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "erro")
        elif senha != confirmacao:
            flash("As senhas não coincidem.", "erro")
        else:
            usuario.senha = generate_password_hash(senha)
            salvar_usuarios_json()
            flash("Senha alterada! Entre com sua nova senha.", "sucesso")
            return redirect(url_for("login"))
    return render_template("redefinir_senha.html", token=token, expirado=False)


@app.route("/clima")
@login_required
def pagina_clima():
    dados = buscar_clima()
    return render_template("clima.html", clima=dados)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if autenticar_credenciais(request.form.get("email"), request.form.get("senha")):
            return redirect(url_for("admin" if session.get("tipo") == "admin" else "home"))
        return render_template("login.html", resultado="falha"), 401
    return render_template("login.html", resultado=None)

@app.route("/admin")
@login_required
@admin_required
def admin():
    atualizar_shows()
    return render_template("admin.html", **montar_painel("painel"))

def montar_painel(aba):
    from collections import Counter
    atualizar_shows()
    return {
        "aba": aba,
        "shows": SHOWS,
        "ingressos": ingressos,
        "usuarios": usuarios,
        "categorias": sorted({s.get("categoria", "Outros") for s in SHOWS}),
        "categorias_contagem": dict(Counter(s.get("categoria", "Outros") for s in SHOWS)),
    }


@app.route("/admin/<secao>")
@login_required
@admin_required
def admin_secao(secao):
    if secao not in {"eventos", "ingressos", "categorias", "relatorios", "usuarios", "configuracoes"}:
        abort(404)
    return render_template("admin.html", **montar_painel(secao))


@app.route("/editar_ingressos/<int:id>", methods=["POST"])
@login_required
@admin_required
def editar_ingressos(id):

    for show in SHOWS:
        if show["id"] == id:
            try:
                total = int(request.form["total"])
                vendidos = int(request.form["vendidos"])
            except (ValueError, KeyError):
                return "Quantidade inválida.", 400
            if total < 0 or vendidos < 0 or vendidos > total:
                return "O total deve ser maior ou igual aos ingressos vendidos.", 400
            show["ingressos_total"] = total
            show["ingressos_vendidos"] = vendidos
            break

    salvar_shows_json()
    return redirect(url_for("admin"))


    


@app.route("/autenticar", methods=["POST"])
def autenticar():
    if autenticar_credenciais(request.form.get("email"), request.form.get("senha")):
        return redirect(url_for("admin" if session.get("tipo") == "admin" else "home"))
    return render_template("login.html", resultado="falha"), 401


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

    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    if not nome or "@" not in email or len(senha or "") < 8:
        return "Informe nome, e-mail válido e senha com pelo menos 8 caracteres.", 400
    if any(u.email.lower() == email for u in usuarios):
        return "E-mail já cadastrado.", 409
    nome_arquivo = "sem_foto.png"
    if adicionar_foto == "sim":
        foto = request.files.get("foto")
        if foto and foto.filename != "":
            extensao = os.path.splitext(foto.filename)[-1].lower()
            if extensao not in (".png", ".jpg", ".jpeg", ".webp"):
                return "Envie uma imagem PNG, JPG ou WEBP.", 400
            nome_arquivo = secrets.token_hex(8) + extensao
            foto.save(os.path.join(app.static_folder, "img", nome_arquivo))

    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    if not nome or "@" not in email or not senha or len(senha) < 8:
        return "Informe nome, e-mail válido e senha com pelo menos 8 caracteres.", 400
    if any(u.email.lower() == email for u in usuarios):
        return "E-mail já cadastrado.", 409
    usuarios.append(
        Usuario(
            max([u.id for u in usuarios], default=0) + 1,
            nome,
            email,
            generate_password_hash(senha),
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

@app.route("/cancelar_ingresso/<int:id>", methods=["POST"])
@login_required
def cancelar_ingresso(id):

    global ingressos

    alvo = next((i for i in ingressos if i.id == id
                 and i.usuario_id == session["usuario_id"]), None)
    if alvo is None:
        abort(404)
    ingressos = [i for i in ingressos if i.id != alvo.id]
    show = next((s for s in SHOWS if s.get("nome") == alvo.show), None)
    if show and "DEMONSTRAÇÃO" not in alvo.pagamento and "DEMONSTRACAO" not in alvo.pagamento and show.get("ingressos_vendidos", 0) > 0:
        show["ingressos_vendidos"] -= 1
        salvar_shows_json()
    salvar_ingressos_json()
    return redirect(url_for("meus_ingressos"))

@app.route("/meu_ingresso/<codigo>")
@login_required
def meu_ingresso(codigo):

    ingresso = next((i for i in ingressos if i.codigo == codigo), None)

    if ingresso is None or ingresso.usuario_id != session["usuario_id"]:
        abort(404)

    return render_template("ingresso.html", ingresso=ingresso)

@app.route("/cadastro_adm")
@login_required
@admin_required
def cadastro_adm():
    return render_template("cadastro_adm.html")


@app.route("/salvar_adm", methods=["POST"])
@login_required
@admin_required
def salvar_adm():
    nome = (request.form.get("nome") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    senha = request.form.get("senha") or ""
    if not nome or "@" not in email or len(senha) < 8:
        return "Informe nome, e-mail válido e senha com pelo menos 8 caracteres.", 400
    if any(u.email.lower() == email for u in usuarios):
        return "E-mail já cadastrado.", 409
    usuarios.append(Usuario(max([u.id for u in usuarios], default=0) + 1,
                            nome, email, generate_password_hash(senha), "admin",
                            request.form.get("data_nascimento", ""), request.form.get("genero", "")))
    salvar_usuarios_json()
    return redirect(url_for("admin"))


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
        extensao = os.path.splitext(foto.filename)[-1].lower()
        if extensao not in (".png", ".jpg", ".jpeg", ".webp"):
            return "Envie uma imagem PNG, JPG ou WEBP.", 400
        nome_arquivo = secrets.token_hex(8) + extensao
        foto.save(os.path.join(app.static_folder, "img", nome_arquivo))

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
    meus = [s for s in SHOWS if s.get("admin") in (None, "", session["usuario"])]
    return render_template("meus_shows.html", shows=meus)

@app.route("/definir_destaque/<int:id>", methods=["POST"])
@login_required
@admin_required
def definir_destaque(id):

    for show in SHOWS:
        if show["id"] == id:
            for outro in SHOWS:
                outro["destaque"] = False

            show["destaque"] = True

            break

    salvar_shows_json()
    return redirect(url_for("meus_shows"))

@app.route("/excluir_show/<int:id>", methods=["POST"])
@login_required
@admin_required
def excluir_show(id):

    global SHOWS

    SHOWS = [
        show for show in SHOWS
        if not (
            show["id"] == id and
            show.get("admin") in (None, "", session["usuario"])
        )
    ]

    salvar_shows_json()

    return redirect(url_for("meus_shows"))

@app.route("/editar_show/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_show(id):

    show = next((s for s in SHOWS if s["id"] == id and s.get("admin") in (None, "", session["usuario"])), None)

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
            "id": max([sh["id"] for sh in SHOWS], default=0) + 1,
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

        for i, lote in enumerate(show.get("lotes", [])):

            lote["quantidade"] = int(
                request.form[f"quantidade_{i}"]
            )

            lote["preco"] = float(
                request.form[f"preco_{i}"]
            )

        if show.get("lotes"):
            show["ingressos_total"] = sum(lote["quantidade"] for lote in show["lotes"])

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
    """Checkout de demonstração. Não solicita dados financeiros."""
    forma = (request.form.get("pagamento") or "").upper()
    if forma not in {"PIX", "CARTAO"}:
        return render_template("erro.html", codigo=400, mensagem="Escolha PIX ou cartão para continuar."), 400

    try:
        show_id = int(request.form.get("show_id", ""))
    except ValueError:
        return render_template("erro.html", codigo=400, mensagem="Selecione um evento válido."), 400

    show = next((s for s in SHOWS if s.get("id") == show_id), None)
    if show is None:
        abort(404)
    if show.get("ingressos_vendidos", 0) >= show.get("ingressos_total", 0):
        return render_template("erro.html", codigo=409, mensagem="Os ingressos deste evento estão esgotados."), 409

    # Os dados do evento e o valor são sempre obtidos no servidor.
    nonce = secrets.token_urlsafe(24)
    session["checkout_demo"] = {"nonce": nonce, "show_id": show_id, "forma": forma}
    return render_template("checkout_demo.html", show=show, forma=forma, nonce=nonce)


@app.route("/concluir_demo", methods=["POST"])
@login_required
def concluir_demo():
    """Registra um pedido de teste, nunca um pagamento confirmado."""
    demo = session.get("checkout_demo")
    token = request.form.get("token", "")
    if not isinstance(demo, dict) or not isinstance(token, str) or not secrets.compare_digest(token, demo.get("nonce", "")):
        return render_template("erro.html", codigo=400, mensagem="A sessão de checkout expirou. Volte ao evento e tente novamente."), 400

    # Descartar token antes de registrar impede compras repetidas ao atualizar.
    session.pop("checkout_demo", None)
    show = next((s for s in SHOWS if s.get("id") == demo["show_id"]), None)
    if show is None:
        abort(404)
    if show.get("ingressos_vendidos", 0) >= show.get("ingressos_total", 0):
        return render_template("erro.html", codigo=409, mensagem="Os ingressos deste evento estão esgotados."), 409

    forma = demo.get("forma")
    if forma not in {"PIX", "CARTAO"}:
        abort(400)
    descricao = "Cartão" if forma == "CARTAO" else "PIX"
    codigo = "DEMO-" + secrets.token_hex(5).upper()
    ingresso = Ingresso(
        id=max((item.id for item in ingressos), default=0) + 1,
        show=show["nome"],
        preco=show["preco"],
        local=show["local"],
        data=show["data"],
        pagamento=f"DEMONSTRAÇÃO - {descricao} (NÃO PAGO)",
        usuario_id=session["usuario_id"],
        codigo=codigo,
    )
    ingressos.append(ingresso)
    salvar_ingressos_json()
    # Não alterar ingressos_vendidos: nenhuma transação financeira aconteceu.
    return render_template("confirmacao_demo.html", ingresso=ingresso, forma=forma)


@app.route("/pagar_cartao", methods=["POST"])
@login_required
def pagar_cartao():
    """Compatibilidade: formulários antigos não coletam cartão no servidor."""
    return redirect(url_for("home"), code=303)


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


# -------------------------------------------------------------
# Integrações externas: mantidas separadas das compras/ingressos
# -------------------------------------------------------------
@app.route("/api/clima")
@login_required
def api_clima():
    dados = buscar_clima()
    if dados is None:
        return jsonify(erro="Não foi possível consultar o clima agora."), 503
    return jsonify(dados)


@app.route("/api/cep/<cep>")
@login_required
def api_cep(cep):
    dados, status = buscar_cep(cep)
    if status == 400:
        return jsonify(erro="O CEP deve conter exatamente 8 dígitos."), 400
    if status == 404:
        return jsonify(erro="CEP não encontrado."), 404
    if status == 503:
        return jsonify(erro="Serviço de CEP indisponível no momento."), 503
    return jsonify(dados)


@app.route("/consultar-cep")
@login_required
def consultar_cep():
    return render_template("consultar_cep.html")


@app.cli.command("criar-admin")
def criar_admin():
    """Cria ou redefine administrador pelo terminal, sem cadastro público."""
    import getpass
    email = input("E-mail do administrador: ").strip().lower()
    nome = input("Nome: ").strip() or "Administrador"
    senha = getpass.getpass("Nova senha (mínimo 8 caracteres): ")
    if "@" not in email or len(senha) < 8:
        raise SystemExit("E-mail inválido ou senha curta.")
    usuario = next((u for u in usuarios if u.email.lower() == email), None)
    if usuario is None:
        usuario = Usuario(max([u.id for u in usuarios], default=0) + 1,
                          nome, email, generate_password_hash(senha), "admin")
        usuarios.append(usuario)
    else:
        usuario.nome = nome
        usuario.senha = generate_password_hash(senha)
        usuario.tipo = "admin"
    salvar_usuarios_json()
    print("Administrador configurado com sucesso.")


@app.errorhandler(403)
def erro_proibido(e):
    return render_template("erro.html", codigo=403, mensagem="Você não tem permissão para acessar esta área."), 403


@app.errorhandler(404)
def erro_nao_encontrado(e):
    return render_template("erro.html", codigo=404, mensagem="Página não encontrada."), 404


if __name__ == "__main__":
    print("TicketShow verificado | app.py:", os.path.abspath(__file__))
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
