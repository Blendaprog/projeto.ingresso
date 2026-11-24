"""Consulta ao Open-Meteo para Campos do Jordão, com falha segura."""
import requests

URL_OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
CIDADE = "Campos do Jordão"
LATITUDE = -22.7394
LONGITUDE = -45.5914
DESCRICOES = {
    0: "Céu limpo", 1: "Predomínio de sol", 2: "Parcialmente nublado",
    3: "Nublado", 45: "Neblina", 48: "Neblina",
    51: "Garoa fraca", 53: "Garoa", 55: "Garoa forte",
    61: "Chuva fraca", 63: "Chuva", 65: "Chuva forte",
    80: "Pancadas de chuva", 81: "Pancadas de chuva",
    82: "Pancadas fortes de chuva", 95: "Trovoada",
    96: "Trovoada com granizo", 99: "Trovoada com granizo",
}

def buscar_clima():
    parametros = {
        "latitude": LATITUDE, "longitude": LONGITUDE,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "timezone": "America/Sao_Paulo",
    }
    try:
        resposta = requests.get(URL_OPEN_METEO, params=parametros, timeout=5)
        resposta.raise_for_status()
        atual = resposta.json()["current"]
        return {
            "cidade": CIDADE,
            "temperatura": float(atual["temperature_2m"]),
            "vento": float(atual["wind_speed_10m"]),
            "descricao": DESCRICOES.get(int(atual["weather_code"]), "Tempo instável"),
        }
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return None
