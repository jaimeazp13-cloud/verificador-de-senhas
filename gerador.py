"""
gerador.py
----------
Gera senhas aleatórias e seguras.

Ponto importante de segurança: usamos o módulo `secrets`, e NÃO o `random`.
O `random` é previsível: se alguém descobrir o estado interno dele, consegue
prever os próximos números. O `secrets` usa a fonte de aleatoriedade do
sistema operacional, feita justamente para senhas e chaves.
"""

import secrets
import string


def gerar_senha(tamanho=16, usar_maiusculas=True, usar_numeros=True, usar_simbolos=True):
    """Gera uma senha aleatória com pelo menos um caractere de cada tipo escolhido."""
    if tamanho < 4:
        raise ValueError("O tamanho mínimo é 4 caracteres.")

    grupos = [string.ascii_lowercase]
    if usar_maiusculas:
        grupos.append(string.ascii_uppercase)
    if usar_numeros:
        grupos.append(string.digits)
    if usar_simbolos:
        grupos.append(string.punctuation)

    # 1) Garante pelo menos um caractere de cada grupo escolhido.
    caracteres = [secrets.choice(grupo) for grupo in grupos]

    # 2) Completa o resto com caracteres de qualquer grupo.
    todos = "".join(grupos)
    caracteres += [secrets.choice(todos) for _ in range(tamanho - len(caracteres))]

    # 3) Embaralha, para os caracteres "garantidos" não ficarem sempre no começo.
    secrets.SystemRandom().shuffle(caracteres)

    return "".join(caracteres)
