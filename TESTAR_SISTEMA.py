"""Diagnóstico local sem acessar a internet ou alterar os arquivos JSON."""
import sys
from unittest.mock import patch


def executar():
    import app
    from modelos import Usuario
    from werkzeug.security import generate_password_hash
    from pathlib import Path
    import ast

    arquivo = Path(app.__file__).resolve()
    ast.parse(arquivo.read_text(encoding="utf-8"))
    assert app.login_required.__code__.co_firstlineno < app.pagar.__code__.co_firstlineno, (
        "A rota /pagar precisa ficar depois da função login_required")
    print("app.py em uso:", arquivo)

    pagina = app.app
    pagina.config["TESTING"] = True
    id_cliente = max([u.id for u in app.usuarios], default=0) + 100
    id_admin = id_cliente + 1
    cliente = Usuario(id_cliente, "Teste comum", "teste-comum@exemplo.invalid",
                      generate_password_hash("senha_teste_123"), "usuario")
    admin = Usuario(id_admin, "Teste admin", "teste-admin@exemplo.invalid",
                    generate_password_hash("senha_teste_456"), "admin")
    app.usuarios.extend([cliente, admin])
    try:
        with pagina.test_client() as navegador:
            for caminho in ("/login", "/cadastro_usuario"):
                assert navegador.get(caminho).status_code == 200, caminho
            assert navegador.get("/admin").status_code == 302
            assert navegador.post("/autenticar", data={"email": cliente.email,
                       "senha": "senha_teste_123"}).status_code == 302
            assert navegador.get("/").status_code == 200
            assert navegador.get("/perfil").status_code == 200
            assert navegador.get("/consultar-cep").status_code == 200
            assert navegador.get("/admin").status_code == 403
            assert navegador.get("/api/cep/123").status_code == 400
            with patch.object(app, "buscar_clima", return_value={
                    "cidade": "Campos do Jordão", "temperatura": 18.2,
                    "vento": 10.0, "descricao": "Nublado"}):
                assert navegador.get("/api/clima").status_code == 200
            with patch.object(app, "buscar_clima", return_value=None):
                assert navegador.get("/api/clima").status_code == 503
            with patch.object(app, "buscar_cep", return_value=({
                    "cep": "01001-000", "logradouro": "Praça da Sé",
                    "bairro": "Sé", "cidade": "São Paulo", "uf": "SP"}, 200)):
                assert navegador.get("/api/cep/01001000").status_code == 200
            # Fluxos demonstrativos: PIX e cartão, sem cobrar nem marcar como pago.
            show_id = app.SHOWS[0]["id"]
            prev = app.SHOWS[0]["ingressos_vendidos"]
            for forma in ("PIX", "CARTAO"):
                pagina_compra = navegador.get(f"/comprar/{show_id}")
                assert pagina_compra.status_code == 200
                assert b"Checkout" in pagina_compra.data or b"pedido" in pagina_compra.data
                escolha = navegador.post("/finalizar_compra", data={"show_id": show_id, "pagamento": forma})
                assert escolha.status_code == 200, (forma, escolha.status_code)
                assert b"Nenhum pagamento" in escolha.data
                with navegador.session_transaction() as sess:
                    token = sess["checkout_demo"]["nonce"]
                conclusao = navegador.post("/concluir_demo", data={"token":token})
                assert conclusao.status_code == 200, (forma, conclusao.status_code)
                assert b"DEMO-" in conclusao.data
                assert app.SHOWS[0]["ingressos_vendidos"] == prev
                assert navegador.post("/concluir_demo", data={"token":token}).status_code == 400
                # remove os dados de teste para não escrever ingressos fictícios no projeto
                pedido = app.ingressos[-1]
                app.ingressos.remove(pedido)
                app.salvar_ingressos_json()
            assert navegador.get("/meus_ingressos").status_code == 200
            navegador.get("/logout")
            assert navegador.post("/autenticar", data={"email": admin.email,
                       "senha": "senha_teste_456"}).status_code == 302
            assert navegador.get("/admin").status_code == 200
            assert navegador.get("/meus_shows").status_code == 200
            print("OK: Flask, usuario, ADM, permissoes, clima, CEP e checkout de demonstracao")
    finally:
        app.usuarios[:] = [u for u in app.usuarios if u not in (cliente, admin)]


if __name__ == "__main__":
    try:
        executar()
    except Exception as erro:
        import traceback
        traceback.print_exc()
        print("FALHOU:", erro)
        sys.exit(1)
