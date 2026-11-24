"""Consulta de CEP com validação e tratamento de indisponibilidade."""
import re
import requests

def buscar_cep(cep):
    if not re.fullmatch(r"\d{8}", str(cep)):
        return None, 400
    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("erro"):
            return None, 404
        return {
            "cep": dados.get("cep", ""),
            "logradouro": dados.get("logradouro", ""),
            "bairro": dados.get("bairro", ""),
            "cidade": dados.get("localidade", ""),
            "uf": dados.get("uf", ""),
        }, 200
    except (requests.RequestException, ValueError, TypeError, KeyError):
        return None, 503
