"""
analisador.py
-------------
Funções que avaliam a força de uma senha.

Ideia principal: uma senha forte é uma senha DIFÍCIL DE ADIVINHAR.
Medimos isso com a ENTROPIA, em bits. Cada bit a mais DOBRA o número de
tentativas que um atacante precisaria fazer para descobrir a senha por
força bruta (testando todas as combinações possíveis).
"""

import math
import string
from pathlib import Path

# Arquivo com senhas muito usadas. Fica na mesma pasta deste arquivo.
ARQUIVO_SENHAS_COMUNS = Path(__file__).parent / "senhas_comuns.txt"

# Todos os caracteres "conhecidos": letras, números e símbolos do teclado.
CARACTERES_CONHECIDOS = (
    string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
)


def carregar_senhas_comuns(caminho=ARQUIVO_SENHAS_COMUNS):
    """Lê o arquivo de senhas comuns e devolve um conjunto (set) com elas.

    Usamos set em vez de lista porque procurar um item num set é muito
    rápido: o Python não precisa olhar item por item.
    """
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return {linha.strip().lower() for linha in arquivo if linha.strip()}
    except FileNotFoundError:
        return set()


SENHAS_COMUNS = carregar_senhas_comuns()


def tamanho_do_alfabeto(senha):
    """Quantos símbolos diferentes um atacante teria que testar em CADA
    posição da senha, de acordo com os tipos de caractere que ela usa."""
    tamanho = 0
    if any(c in string.ascii_lowercase for c in senha):
        tamanho += 26  # a-z
    if any(c in string.ascii_uppercase for c in senha):
        tamanho += 26  # A-Z
    if any(c in string.digits for c in senha):
        tamanho += 10  # 0-9
    if any(c in string.punctuation for c in senha):
        tamanho += len(string.punctuation)  # !@#$%... (32 símbolos)
    if any(c not in CARACTERES_CONHECIDOS for c in senha):
        tamanho += 32  # espaço, acentos (é, ç, ã...) e outros
    return tamanho


def calcular_entropia(senha):
    """Entropia = tamanho da senha x log2(tamanho do alfabeto).

    Exemplo: uma senha de 8 letras minúsculas tem 8 x log2(26) = 37,6 bits,
    ou seja, cerca de 2^37,6 (uns 200 bilhões) de combinações possíveis.
    """
    alfabeto = tamanho_do_alfabeto(senha)
    if alfabeto == 0:
        return 0.0
    return len(senha) * math.log2(alfabeto)


def tem_sequencia(senha, tamanho=3):
    """Detecta sequências óbvias como 'abc', '123', 'cba' ou '321'.

    ord() devolve o código numérico de um caractere: ord('a') = 97,
    ord('b') = 98... Se a diferença entre vizinhos é sempre +1 ou -1,
    é uma sequência.
    """
    texto = senha.lower()
    for i in range(len(texto) - tamanho + 1):
        trecho = texto[i:i + tamanho]
        diferencas = {ord(trecho[j + 1]) - ord(trecho[j]) for j in range(tamanho - 1)}
        if diferencas == {1} or diferencas == {-1}:
            return True
    return False


def tem_repeticao(senha, tamanho=3):
    """Detecta o mesmo caractere repetido em seguida, como 'aaa' ou '111'."""
    for i in range(len(senha) - tamanho + 1):
        if len(set(senha[i:i + tamanho])) == 1:
            return True
    return False


def classificar(pontuacao):
    """Transforma a pontuação (em bits) num nível fácil de entender."""
    if pontuacao < 28:
        return "Muito fraca"
    if pontuacao < 40:
        return "Fraca"
    if pontuacao < 60:
        return "Média"
    if pontuacao < 80:
        return "Forte"
    return "Muito forte"


def analisar_senha(senha):
    """Analisa a senha e devolve um dicionário com o resultado.

    A pontuação começa igual à entropia e perde pontos por padrões que
    facilitam a vida de um atacante (sequências, repetições, senha comum).
    """
    problemas = []

    if len(senha) < 8:
        problemas.append("Tem menos de 8 caracteres (o ideal é 12 ou mais).")
    elif len(senha) < 12:
        problemas.append("Tem menos de 12 caracteres. Aumentar o tamanho é o jeito mais fácil de fortalecer.")

    if not any(c.islower() for c in senha):
        problemas.append("Não tem letras minúsculas.")
    if not any(c.isupper() for c in senha):
        problemas.append("Não tem letras maiúsculas.")
    if not any(c.isdigit() for c in senha):
        problemas.append("Não tem números.")
    if not any(c in string.punctuation for c in senha):
        problemas.append("Não tem símbolos (!@#$%...).")

    entropia = calcular_entropia(senha)
    pontuacao = entropia

    if tem_sequencia(senha):
        problemas.append("Tem uma sequência óbvia (ex: abc, 123).")
        pontuacao -= 10
    if tem_repeticao(senha):
        problemas.append("Repete o mesmo caractere várias vezes seguidas (ex: aaa).")
        pontuacao -= 10

    senha_comum = senha.lower() in SENHAS_COMUNS
    if senha_comum:
        # Atacantes testam essas senhas PRIMEIRO, então ela cai em segundos.
        problemas.insert(0, "Está na lista de senhas mais usadas. Seria descoberta em segundos!")
        pontuacao = 0

    pontuacao = max(pontuacao, 0)

    return {
        "nivel": classificar(pontuacao),
        "entropia": round(entropia, 1),
        "pontuacao": round(pontuacao, 1),
        "senha_comum": senha_comum,
        "problemas": problemas,
    }
