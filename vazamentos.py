"""
vazamentos.py
-------------
Verifica se uma senha já apareceu em vazamentos de dados, usando a API
pública e gratuita "Pwned Passwords" (do site Have I Been Pwned).

COMO ISSO É FEITO SEM ENVIAR SUA SENHA? (técnica chamada k-anonimato)

1. Calculamos o hash SHA-1 da senha. Um hash é uma "impressão digital":
   "password" vira 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8.
   Não dá para voltar do hash para a senha.
2. Enviamos à API só os 5 PRIMEIROS caracteres do hash (ex: 5BAA6).
3. A API devolve TODOS os hashes vazados que começam com 5BAA6 (centenas).
4. Nós mesmos procuramos, aqui no computador, se o resto do nosso hash
   está nessa lista.

Assim, nem a senha nem o hash completo saem do seu computador.
"""

import hashlib
import urllib.request

URL_API = "https://api.pwnedpasswords.com/range/"


def gerar_hash_sha1(senha):
    """Devolve o hash SHA-1 da senha em letras maiúsculas (formato da API)."""
    return hashlib.sha1(senha.encode("utf-8")).hexdigest().upper()


def contar_ocorrencias(sufixo, resposta):
    """Procura o sufixo do hash na resposta da API.

    A resposta tem uma linha por hash, no formato  SUFIXO:QUANTIDADE
    Devolve quantas vezes a senha apareceu em vazamentos (0 se nenhuma).
    """
    for linha in resposta.splitlines():
        sufixo_da_linha, _, quantidade = linha.partition(":")
        if sufixo_da_linha.strip() == sufixo:
            return int(quantidade)
    return 0


def verificar_vazamento(senha, timeout=10):
    """Devolve quantas vezes a senha apareceu em vazamentos,
    ou None se não foi possível consultar (sem internet, por exemplo)."""
    hash_completo = gerar_hash_sha1(senha)
    prefixo, sufixo = hash_completo[:5], hash_completo[5:]

    requisicao = urllib.request.Request(
        URL_API + prefixo,
        headers={
            "User-Agent": "verificador-de-senhas-estudo",
            # Pede à API para misturar respostas falsas, deixando a consulta
            # ainda mais difícil de ser analisada por quem estiver olhando a rede.
            "Add-Padding": "true",
        },
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=timeout) as resposta:
            texto = resposta.read().decode("utf-8")
    except OSError:
        # Erros de rede (sem internet, tempo esgotado, site fora do ar...)
        return None

    return contar_ocorrencias(sufixo, texto)
