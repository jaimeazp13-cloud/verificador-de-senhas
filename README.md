# 🔐 Verificador de Senhas

Ferramenta de linha de comando em Python que **analisa a força de senhas**, **gera senhas seguras** e **verifica se uma senha já apareceu em vazamentos de dados**. A verificação acontece sem a senha sair do seu computador.

Projeto feito para estudar conceitos de **segurança da informação** durante o curso de Sistemas de Informação.

## Funcionalidades

- **Análise de força**: calcula a entropia (em bits), detecta sequências (`abc`, `123`), repetições (`aaa`) e senhas comuns, e dá dicas de melhoria.
- **Gerador de senhas**: cria senhas aleatórias com o módulo `secrets`, que é criptograficamente seguro.
- **Verificação de vazamentos**: consulta a API [Pwned Passwords](https://haveibeenpwned.com/Passwords) usando **k-anonimato**, ou seja, só os 5 primeiros caracteres do hash SHA-1 são enviados.

## Exemplo de uso

```
===== VERIFICADOR DE SENHAS =====
1 - Analisar a força de uma senha
2 - Gerar uma senha segura
3 - Verificar se uma senha já vazou
0 - Sair
Escolha uma opção: 1
Digite a senha (ela não aparece na tela):

Nível:     Fraca
Entropia:  41.4 bits
Pontuação: 31.4 (após descontar padrões fracos)

Pontos a melhorar:
  - Tem menos de 12 caracteres. Aumentar o tamanho é o jeito mais fácil de fortalecer.
  - Não tem letras maiúsculas.
  - Não tem símbolos (!@#$%...).
  - Tem uma sequência óbvia (ex: abc, 123).
```

## Como rodar

Precisa do [Python 3.8+](https://www.python.org/downloads/). Não usa nenhuma biblioteca externa.

```bash
git clone https://github.com/SEU-USUARIO/verificador-de-senhas.git
cd verificador-de-senhas
python main.py
```

## Testes

```bash
python -m unittest -v
```

## Conceitos de segurança aplicados

| Conceito | Onde aparece |
|---|---|
| **Entropia**: quanto mais bits, mais tentativas um ataque de força bruta precisa | `analisador.py` |
| **Ataque de dicionário**: atacantes testam senhas comuns primeiro | `senhas_comuns.txt` |
| **Aleatoriedade segura**: `secrets` em vez de `random`, que é previsível | `gerador.py` |
| **Hash (SHA-1)**: "impressão digital" de mão única da senha | `vazamentos.py` |
| **k-anonimato**: consultar uma base sem revelar o dado consultado | `vazamentos.py` |

## Estrutura

```
verificador-de-senhas/
├── main.py              # menu no terminal
├── analisador.py        # cálculo de força e detecção de padrões
├── gerador.py           # geração de senhas seguras
├── vazamentos.py        # consulta à API Pwned Passwords
├── senhas_comuns.txt    # lista de senhas mais usadas
└── tests/               # testes automáticos
```

## Próximos passos

- [ ] Gerar frases-senha (ex: `cavalo-bateria-grampo-correto`)
- [ ] Transformar em API web com Flask ou FastAPI
- [ ] Usar uma lista maior de senhas comuns

## Autor

Feito por **Jaime Augusto**, estudante de Sistemas de Informação.
