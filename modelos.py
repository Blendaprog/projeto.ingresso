from datetime import datetime


class Usuario:
    def __init__(
        self,
        id,
        nome,
        email,
        senha,
        tipo="usuario",
        data_nascimento="",
        genero="",
        foto="sem_foto.png",
        ingressos=None
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.foto = foto
        self.ingressos = ingressos if ingressos else []

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "tipo": self.tipo,
            "data_nascimento": self.data_nascimento,
            "genero": self.genero,
            "foto": self.foto,
            "ingressos": self.ingressos
        }


class Ingresso:
    def __init__(
        self,
        id,
        show,
        preco,
        local,
        data,
        pagamento,
        usuario_id,
        codigo=None
    ):
        self.id = id
        self.show = show
        self.preco = float(preco)
        self.local = local
        self.data = data
        self.pagamento = pagamento
        self.usuario_id = usuario_id
        self.codigo = codigo

    def to_dict(self):
        return {
            "id": self.id,
            "show": self.show,
            "preco": self.preco,
            "local": self.local,
            "data": self.data,
            "pagamento": self.pagamento,
            "usuario_id": self.usuario_id,
            "codigo": self.codigo
        }