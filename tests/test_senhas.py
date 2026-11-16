"""
Testes automáticos do projeto.

Testes são pequenos programas que conferem se o código faz o que deveria.
Se um dia você mudar algo e quebrar sem querer, os testes avisam.

Para rodar (na pasta do projeto):  python -m unittest -v
"""

import string
import unittest

from analisador import analisar_senha, calcular_entropia, tem_repeticao, tem_sequencia
from gerador import gerar_senha
from vazamentos import contar_ocorrencias, gerar_hash_sha1


class TestAnalisador(unittest.TestCase):
    def test_senha_comum_e_muito_fraca(self):
        resultado = analisar_senha("123456")
        self.assertTrue(resultado["senha_comum"])
        self.assertEqual(resultado["nivel"], "Muito fraca")

    def test_senha_comum_ignora_maiusculas(self):
        self.assertTrue(analisar_senha("PASSWORD")["senha_comum"])

    def test_senha_longa_e_variada_e_muito_forte(self):
        resultado = analisar_senha("Tr0ub4dor&3xQ!zP")
        self.assertEqual(resultado["nivel"], "Muito forte")
        self.assertEqual(resultado["problemas"], [])

    def test_senha_vazia(self):
        resultado = analisar_senha("")
        self.assertEqual(resultado["entropia"], 0)
        self.assertEqual(resultado["nivel"], "Muito fraca")

    def test_entropia_de_uma_letra(self):
        # 1 letra minúscula = log2(26) ≈ 4,7 bits
        self.assertAlmostEqual(calcular_entropia("a"), 4.7, places=1)

    def test_detecta_sequencias(self):
        self.assertTrue(tem_sequencia("xabcx"))
        self.assertTrue(tem_sequencia("senha321"))
        self.assertFalse(tem_sequencia("acegi"))

    def test_detecta_repeticao(self):
        self.assertTrue(tem_repeticao("caaasa"))
        self.assertFalse(tem_repeticao("aabbcc"))


class TestGerador(unittest.TestCase):
    def test_tamanho_correto(self):
        self.assertEqual(len(gerar_senha(20)), 20)

    def test_contem_todos_os_tipos(self):
        senha = gerar_senha(12)
        self.assertTrue(any(c in string.ascii_lowercase for c in senha))
        self.assertTrue(any(c in string.ascii_uppercase for c in senha))
        self.assertTrue(any(c in string.digits for c in senha))
        self.assertTrue(any(c in string.punctuation for c in senha))

    def test_sem_simbolos(self):
        senha = gerar_senha(30, usar_simbolos=False)
        self.assertFalse(any(c in string.punctuation for c in senha))

    def test_senhas_diferentes(self):
        self.assertNotEqual(gerar_senha(), gerar_senha())

    def test_tamanho_minimo(self):
        with self.assertRaises(ValueError):
            gerar_senha(3)


class TestVazamentos(unittest.TestCase):
    def test_hash_sha1_conhecido(self):
        self.assertEqual(
            gerar_hash_sha1("password"),
            "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8",
        )

    def test_contar_ocorrencias(self):
        # Simula uma resposta da API (sem precisar de internet)
        resposta = "AAAAA:3\r\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:9545824\r\nBBBBB:0"
        self.assertEqual(contar_ocorrencias("1E4C9B93F3F0682250B6CF8331B7EE68FD8", resposta), 9545824)
        self.assertEqual(contar_ocorrencias("NAOEXISTE", resposta), 0)


if __name__ == "__main__":
    unittest.main()
