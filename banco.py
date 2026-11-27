"""Camada de banco de dados SQLite do TicketShow."""

import json
import os
import sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(BASE_DIR, "ticketshow.db")


@contextmanager
def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def _json(dados):
    return json.dumps(dados, ensure_ascii=False)


def inicializar_banco():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT,
                tipo TEXT NOT NULL DEFAULT 'usuario',
                data_nascimento TEXT,
                genero TEXT,
                foto TEXT,
                ingressos TEXT NOT NULL DEFAULT '[]'
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                preco REAL,
                local TEXT,
                data TEXT,
                idade_minima INTEGER,
                categoria TEXT,
                imagem TEXT,
                ingressos_total INTEGER DEFAULT 100,
                ingressos_vendidos INTEGER DEFAULT 0,
                destaque INTEGER DEFAULT 0,
                admin TEXT
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_id INTEGER NOT NULL,
                nome TEXT,
                quantidade INTEGER,
                vendidos INTEGER DEFAULT 0,
                preco REAL,
                FOREIGN KEY(show_id) REFERENCES shows(id)
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS ingressos (
                id INTEGER PRIMARY KEY,
                show TEXT NOT NULL,
                preco REAL,
                local TEXT,
                data TEXT,
                pagamento TEXT,
                usuario_id INTEGER NOT NULL,
                codigo TEXT UNIQUE,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)

        colunas = [
            coluna["name"]
            for coluna in db.execute("PRAGMA table_info(usuarios)")
        ]

        if "ingressos" not in colunas:
            db.execute("""
                ALTER TABLE usuarios
                ADD COLUMN ingressos TEXT NOT NULL DEFAULT '[]'
            """)


def listar_usuarios():
    with conectar() as db:
        registros = db.execute(
            "SELECT * FROM usuarios ORDER BY id"
        ).fetchall()

        resultado = []

        for registro in registros:
            usuario = dict(registro)
            usuario["ingressos"] = json.loads(
                usuario.get("ingressos") or "[]"
            )
            resultado.append(usuario)

        return resultado


def salvar_usuarios(lista):
    with conectar() as db:
        ids = []

        for item in lista:
            d = item.to_dict() if hasattr(item, "to_dict") else dict(item)

            ids.append(d["id"])

            db.execute("""
                INSERT INTO usuarios (
                    id, nome, email, senha, tipo,
                    data_nascimento, genero, foto, ingressos
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    nome=excluded.nome,
                    email=excluded.email,
                    senha=excluded.senha,
                    tipo=excluded.tipo,
                    data_nascimento=excluded.data_nascimento,
                    genero=excluded.genero,
                    foto=excluded.foto,
                    ingressos=excluded.ingressos
            """, (
                d["id"],
                d.get("nome", ""),
                d["email"].strip().lower(),
                d.get("senha", ""),
                d.get("tipo", "usuario"),
                d.get("data_nascimento", ""),
                d.get("genero", ""),
                d.get("foto", "sem_foto.png"),
                _json(d.get("ingressos", []))
            ))

        if ids:
            marcadores = ",".join("?" for _ in ids)
            db.execute(
                f"DELETE FROM usuarios WHERE id NOT IN ({marcadores})",
                ids
            )
        else:
            db.execute("DELETE FROM usuarios")


def listar_shows():
    with conectar() as db:
        registros = db.execute(
            "SELECT * FROM shows ORDER BY id"
        ).fetchall()

        resultado = []

        for registro in registros:
            show = dict(registro)

            lotes = db.execute(
                "SELECT * FROM lotes WHERE show_id = ? ORDER BY id",
                (show["id"],)
            ).fetchall()

            show["lotes"] = [dict(lote) for lote in lotes]

            total = show.get("ingressos_total") or 0
            vendidos = show.get("ingressos_vendidos") or 0

            show["esgotado"] = (
                total > 0 and vendidos >= total
            )

            show["destaque"] = bool(show.get("destaque", 0))

            resultado.append(show)

        return resultado


def salvar_shows(lista):
    with conectar() as db:
        ids = []

        for d in lista:
            show_id = d["id"]
            ids.append(show_id)

            db.execute("""
                INSERT INTO shows (
                    id, nome, preco, local, data, idade_minima,
                    categoria, imagem, ingressos_total,
                    ingressos_vendidos, destaque, admin
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    nome=excluded.nome,
                    preco=excluded.preco,
                    local=excluded.local,
                    data=excluded.data,
                    idade_minima=excluded.idade_minima,
                    categoria=excluded.categoria,
                    imagem=excluded.imagem,
                    ingressos_total=excluded.ingressos_total,
                    ingressos_vendidos=excluded.ingressos_vendidos,
                    destaque=excluded.destaque,
                    admin=excluded.admin
            """, (
                show_id,
                d.get("nome", "Evento"),
                d.get("preco", 0),
                d.get("local", ""),
                d.get("data", ""),
                d.get("idade_minima", 0),
                d.get("categoria", ""),
                d.get("imagem", ""),
                d.get("ingressos_total", 100),
                d.get("ingressos_vendidos", 0),
                int(bool(d.get("destaque", False))),
                d.get("admin", "")
            ))

            db.execute(
                "DELETE FROM lotes WHERE show_id = ?",
                (show_id,)
            )

            for lote in d.get("lotes", []) or []:
                lote_id = lote.get("id")

                if lote_id is not None:
                    db.execute("""
                        INSERT INTO lotes (
                            id, show_id, nome, quantidade, vendidos, preco
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        lote_id,
                        show_id,
                        lote.get("nome", "Lote"),
                        lote.get("quantidade", 0),
                        lote.get("vendidos", 0),
                        lote.get("preco", 0)
                    ))
                else:
                    db.execute("""
                        INSERT INTO lotes (
                            show_id, nome, quantidade, vendidos, preco
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        show_id,
                        lote.get("nome", "Lote"),
                        lote.get("quantidade", 0),
                        lote.get("vendidos", 0),
                        lote.get("preco", 0)
                    ))

        if ids:
            marcadores = ",".join("?" for _ in ids)
            db.execute(
                f"DELETE FROM shows WHERE id NOT IN ({marcadores})",
                ids
            )
            db.execute(
                f"DELETE FROM lotes WHERE show_id NOT IN ({marcadores})",
                ids
            )
        else:
            db.execute("DELETE FROM lotes")
            db.execute("DELETE FROM shows")


def listar_ingressos():
    with conectar() as db:
        registros = db.execute(
            "SELECT * FROM ingressos ORDER BY id"
        ).fetchall()

        return [dict(registro) for registro in registros]


def salvar_ingressos(lista):
    with conectar() as db:
        ids = []

        for item in lista:
            d = item.to_dict() if hasattr(item, "to_dict") else dict(item)

            ids.append(d["id"])

            db.execute("""
                INSERT INTO ingressos (
                    id, show, preco, local, data,
                    pagamento, usuario_id, codigo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    show=excluded.show,
                    preco=excluded.preco,
                    local=excluded.local,
                    data=excluded.data,
                    pagamento=excluded.pagamento,
                    usuario_id=excluded.usuario_id,
                    codigo=excluded.codigo
            """, (
                d["id"],
                d.get("show", "Evento"),
                d.get("preco", 0),
                d.get("local", ""),
                d.get("data", ""),
                d.get("pagamento", ""),
                d["usuario_id"],
                d.get("codigo")
            ))

        if ids:
            marcadores = ",".join("?" for _ in ids)
            db.execute(
                f"DELETE FROM ingressos WHERE id NOT IN ({marcadores})",
                ids
            )
        else:
            db.execute("DELETE FROM ingressos")


def migrar_json_se_necessario():
    arquivos = {
        "usuarios": os.path.join(BASE_DIR, "usuarios.json"),
        "shows": os.path.join(BASE_DIR, "shows.json"),
        "ingressos": os.path.join(BASE_DIR, "ingressos.json")
    }

    with conectar() as db:
        totais = [
            db.execute(
                f"SELECT COUNT(*) FROM {tabela}"
            ).fetchone()[0]
            for tabela in ("usuarios", "shows", "ingressos")
        ]

    if any(totais):
        return False

    dados = {}

    for chave, caminho in arquivos.items():
        try:
            with open(caminho, encoding="utf-8") as arquivo:
                conteudo = json.load(arquivo)

            dados[chave] = (
                conteudo if isinstance(conteudo, list) else []
            )
        except (OSError, ValueError):
            dados[chave] = []

    salvar_usuarios(dados["usuarios"])
    salvar_shows(dados["shows"])
    salvar_ingressos(dados["ingressos"])

    return True


inicializar_banco()