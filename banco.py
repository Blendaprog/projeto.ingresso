import sqlite3


class Banco:
    def __init__(self, nome_banco="ticketshow.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.conexao.row_factory = sqlite3.Row
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()

        # ==========================
        # TABELA DE USUÁRIOS
        # ==========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL DEFAULT 'usuario',
                data_nascimento TEXT,
                genero TEXT,
                foto TEXT DEFAULT 'sem_foto.png'
            )
        """)

        # ==========================
        # TABELA DE SHOWS
        # ==========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                local TEXT NOT NULL,
                data TEXT NOT NULL,
                idade_minima INTEGER NOT NULL,
                categoria TEXT NOT NULL,
                imagem TEXT,
                ingressos_total INTEGER DEFAULT 100,
                ingressos_vendidos INTEGER DEFAULT 0,
                destaque INTEGER DEFAULT 0,
                admin TEXT
            )
        """)

        # ==========================
        # TABELA DE LOTES
        # ==========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                vendidos INTEGER DEFAULT 0,
                preco REAL NOT NULL,

                FOREIGN KEY (show_id)
                REFERENCES shows(id)
                ON DELETE CASCADE
            )
        """)

        # ==========================
        # TABELA DE INGRESSOS
        # ==========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingressos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show TEXT NOT NULL,
                preco REAL NOT NULL,
                local TEXT NOT NULL,
                data TEXT NOT NULL,
                pagamento TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                codigo TEXT NOT NULL UNIQUE,

                FOREIGN KEY (usuario_id)
                REFERENCES usuarios(id)
            )
        """)

        self.conexao.commit()

    # ==================================================
    # USUÁRIOS
    # ==================================================

    def adicionar_usuario(
        self,
        nome,
        email,
        senha,
        tipo="usuario",
        data_nascimento=None,
        genero=None,
        foto="sem_foto.png"
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (nome, email, senha, tipo, data_nascimento, genero, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nome,
            email,
            senha,
            tipo,
            data_nascimento,
            genero,
            foto
        ))

        self.conexao.commit()

        return cursor.lastrowid

    def buscar_usuario_por_email(self, email):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE email = ?
        """, (email,))

        return cursor.fetchone()

    def buscar_usuario_por_id(self, usuario_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE id = ?
        """, (usuario_id,))

        return cursor.fetchone()

    def listar_usuarios(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            ORDER BY id
        """)

        return cursor.fetchall()

    def atualizar_foto_usuario(self, usuario_id, foto):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET foto = ?
            WHERE id = ?
        """, (foto, usuario_id))

        self.conexao.commit()

    # ==================================================
    # SHOWS
    # ==================================================

    def adicionar_show(
        self,
        nome,
        preco,
        local,
        data,
        idade_minima,
        categoria,
        imagem,
        admin=None,
        ingressos_total=100
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO shows
            (
                nome,
                preco,
                local,
                data,
                idade_minima,
                categoria,
                imagem,
                ingressos_total,
                ingressos_vendidos,
                destaque,
                admin
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?)
        """, (
            nome,
            preco,
            local,
            data,
            idade_minima,
            categoria,
            imagem,
            ingressos_total,
            admin
        ))

        self.conexao.commit()

        return cursor.lastrowid

    def buscar_show(self, show_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM shows
            WHERE id = ?
        """, (show_id,))

        return cursor.fetchone()

    def listar_shows(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM shows
            ORDER BY id
        """)

        return cursor.fetchall()

    def listar_shows_disponiveis(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM shows
            WHERE ingressos_vendidos < ingressos_total
            ORDER BY id
        """)

        return cursor.fetchall()

    def listar_shows_por_categoria(self, categoria):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM shows
            WHERE LOWER(categoria) = LOWER(?)
            AND ingressos_vendidos < ingressos_total
            ORDER BY id
        """, (categoria,))

        return cursor.fetchall()

    def atualizar_show(
        self,
        show_id,
        nome,
        categoria,
        local,
        data,
        idade_minima,
        preco,
        ingressos_total
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE shows
            SET
                nome = ?,
                categoria = ?,
                local = ?,
                data = ?,
                idade_minima = ?,
                preco = ?,
                ingressos_total = ?
            WHERE id = ?
        """, (
            nome,
            categoria,
            local,
            data,
            idade_minima,
            preco,
            ingressos_total,
            show_id
        ))

        self.conexao.commit()

    def atualizar_ingressos_show(
        self,
        show_id,
        ingressos_total,
        ingressos_vendidos
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE shows
            SET
                ingressos_total = ?,
                ingressos_vendidos = ?
            WHERE id = ?
        """, (
            ingressos_total,
            ingressos_vendidos,
            show_id
        ))

        self.conexao.commit()

    def definir_destaque(self, show_id):
        cursor = self.conexao.cursor()

        # Retira o destaque dos outros shows
        cursor.execute("""
            UPDATE shows
            SET destaque = 0
        """)

        # Coloca destaque no show escolhido
        cursor.execute("""
            UPDATE shows
            SET destaque = 1
            WHERE id = ?
        """, (show_id,))

        self.conexao.commit()

    def excluir_show(self, show_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            DELETE FROM shows
            WHERE id = ?
        """, (show_id,))

        self.conexao.commit()

    # ==================================================
    # LOTES
    # ==================================================

    def adicionar_lote(
        self,
        show_id,
        nome,
        quantidade,
        preco
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO lotes
            (
                show_id,
                nome,
                quantidade,
                vendidos,
                preco
            )
            VALUES (?, ?, ?, 0, ?)
        """, (
            show_id,
            nome,
            quantidade,
            preco
        ))

        self.conexao.commit()

        self.atualizar_total_ingressos(show_id)

        return cursor.lastrowid

    def listar_lotes(self, show_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM lotes
            WHERE show_id = ?
            ORDER BY id
        """, (show_id,))

        return cursor.fetchall()

    def atualizar_lote(
        self,
        lote_id,
        quantidade,
        preco
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE lotes
            SET
                quantidade = ?,
                preco = ?
            WHERE id = ?
        """, (
            quantidade,
            preco,
            lote_id
        ))

        self.conexao.commit()

    def excluir_lote(self, lote_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT show_id
            FROM lotes
            WHERE id = ?
        """, (lote_id,))

        lote = cursor.fetchone()

        if lote is None:
            return

        show_id = lote["show_id"]

        cursor.execute("""
            DELETE FROM lotes
            WHERE id = ?
        """, (lote_id,))

        self.conexao.commit()

        self.atualizar_total_ingressos(show_id)

    def atualizar_total_ingressos(self, show_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(quantidade), 0) AS total
            FROM lotes
            WHERE show_id = ?
        """, (show_id,))

        resultado = cursor.fetchone()

        total = resultado["total"]

        cursor.execute("""
            UPDATE shows
            SET ingressos_total = ?
            WHERE id = ?
        """, (
            total,
            show_id
        ))

        self.conexao.commit()

    # ==================================================
    # INGRESSOS
    # ==================================================

    def adicionar_ingresso(
        self,
        show,
        preco,
        local,
        data,
        pagamento,
        usuario_id,
        codigo
    ):
        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO ingressos
            (
                show,
                preco,
                local,
                data,
                pagamento,
                usuario_id,
                codigo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            show,
            preco,
            local,
            data,
            pagamento,
            usuario_id,
            codigo
        ))

        self.conexao.commit()

        return cursor.lastrowid

    def listar_ingressos_usuario(self, usuario_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM ingressos
            WHERE usuario_id = ?
            ORDER BY id DESC
        """, (usuario_id,))

        return cursor.fetchall()

    def buscar_ingresso_por_codigo(self, codigo):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM ingressos
            WHERE codigo = ?
        """, (codigo,))

        return cursor.fetchone()

    def excluir_ingresso(self, ingresso_id, usuario_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            DELETE FROM ingressos
            WHERE id = ?
            AND usuario_id = ?
        """, (
            ingresso_id,
            usuario_id
        ))

        self.conexao.commit()

    # ==================================================
    # VENDA
    # ==================================================

    def registrar_venda(self, show_id):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE shows
            SET ingressos_vendidos = ingressos_vendidos + 1
            WHERE id = ?
            AND ingressos_vendidos < ingressos_total
        """, (show_id,))

        self.conexao.commit()

        return cursor.rowcount > 0

    # ==================================================
    # FECHAR BANCO
    # ==================================================

    def fechar(self):
        self.conexao.close()


# ======================================================
# TESTE DO BANCO
# ======================================================

if __name__ == "__main__":
    banco = Banco()

    print("Banco de dados conectado com sucesso!")
    print("Tabelas criadas:")
    print("- usuarios")
    print("- shows")
    print("- lotes")
    print("- ingressos")

    banco.fechar()