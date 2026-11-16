"""
main.py
-------
Menu do programa no terminal. Aqui fica só a "conversa" com o usuário;
a lógica de verdade está em analisador.py, gerador.py e vazamentos.py.
Separar assim deixa o código mais organizado e fácil de testar.

Para rodar:  python main.py
"""

from getpass import getpass

from analisador import analisar_senha
from gerador import gerar_senha
from vazamentos import verificar_vazamento


def ler_inteiro(mensagem, padrao):
    """Lê um número do teclado. Se a pessoa só apertar Enter, usa o padrão."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            return padrao
        if texto.isdigit():
            return int(texto)
        print("Digite apenas números.")


def ler_sim_nao(mensagem, padrao=True):
    """Pergunta sim/não. Enter usa o padrão."""
    texto = input(mensagem).strip().lower()
    if texto == "":
        return padrao
    return texto in ("s", "sim", "y", "yes")


def opcao_analisar():
    # getpass esconde o que é digitado, como num campo de senha.
    senha = getpass("Digite a senha (ela não aparece na tela): ")
    if not senha:
        print("Nenhuma senha digitada.")
        return

    resultado = analisar_senha(senha)
    print(f"\nNível:     {resultado['nivel']}")
    print(f"Entropia:  {resultado['entropia']} bits")
    print(f"Pontuação: {resultado['pontuacao']} (após descontar padrões fracos)")

    if resultado["problemas"]:
        print("\nPontos a melhorar:")
        for problema in resultado["problemas"]:
            print(f"  - {problema}")
    else:
        print("\nNenhum problema encontrado. Ótima senha!")


def opcao_gerar():
    tamanho = ler_inteiro("Tamanho da senha [16]: ", padrao=16)
    if tamanho < 4:
        print("O tamanho mínimo é 4.")
        return
    maiusculas = ler_sim_nao("Usar letras maiúsculas? [S/n]: ")
    numeros = ler_sim_nao("Usar números? [S/n]: ")
    simbolos = ler_sim_nao("Usar símbolos? [S/n]: ")

    senha = gerar_senha(tamanho, maiusculas, numeros, simbolos)
    resultado = analisar_senha(senha)
    print(f"\nSenha gerada: {senha}")
    print(f"Nível: {resultado['nivel']} ({resultado['entropia']} bits)")


def opcao_vazamento():
    senha = getpass("Digite a senha (ela não aparece na tela): ")
    if not senha:
        print("Nenhuma senha digitada.")
        return

    print("Consultando... (só os 5 primeiros caracteres do hash saem do computador)")
    vezes = verificar_vazamento(senha)

    if vezes is None:
        print("Não foi possível consultar. Verifique sua conexão com a internet.")
    elif vezes == 0:
        print("Boa notícia: essa senha não aparece em vazamentos conhecidos.")
    else:
        print(f"ATENÇÃO: essa senha apareceu {vezes:,} vezes em vazamentos!".replace(",", "."))
        print("Não use essa senha. Se você usa, troque o quanto antes.")


def main():
    opcoes = {
        "1": opcao_analisar,
        "2": opcao_gerar,
        "3": opcao_vazamento,
    }

    while True:
        print("\n===== VERIFICADOR DE SENHAS =====")
        print("1 - Analisar a força de uma senha")
        print("2 - Gerar uma senha segura")
        print("3 - Verificar se uma senha já vazou")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Até mais!")
            break
        if escolha in opcoes:
            opcoes[escolha]()  # chama a função correspondente
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
