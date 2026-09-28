import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import io_dados, parte1, parte2, parte3
from parte3 import Classe

# Tabela do exemplo do enunciado: n=120, h=4
CLASSES = [Classe(18, 22, 32, 32), Classe(22, 26, 45, 77),
           Classe(26, 30, 28, 105), Classe(30, 34, 15, 120, True)]


class Testes(unittest.TestCase):
    def test_parte1_e_parte2_concordam(self):
        d = [1, 2, 2, 3, 4, 4, 4, 5]
        p1 = parte1.tendencia_central(d)
        p2 = parte2.calcular(parte2.tabela_frequencias(d))
        self.assertAlmostEqual(p1["media"], p2["media"])
        self.assertAlmostEqual(p1["mediana"], p2["mediana"])
        self.assertEqual(p2["modas"], [4])
        self.assertEqual(p1["mediana"], 3.5)

    def test_mediana_impar_e_multimodal(self):
        t = parte2.tabela_frequencias([1, 1, 2, 2, 3])
        self.assertEqual(parte2.mediana(t), 2.0)
        self.assertEqual(parte2.modas(t), [1, 2])

    def test_interpolacao(self):
        c = CLASSES
        self.assertAlmostEqual(parte3.media(c), 2984 / 120)
        self.assertAlmostEqual(parte3.mediana(c), 22 + 28 / 45 * 4)
        self.assertAlmostEqual(parte3.quartil(c, 1), 18 + 30 / 32 * 4)   # 21.75
        self.assertAlmostEqual(parte3.moda_czuber(c), 22 + 13 / 30 * 4)  # 23.7333
        self.assertAlmostEqual(parte3.moda_king(c), 22 + 28 / 60 * 4)    # 23.8667
        self.assertAlmostEqual(parte3.decil(c, 2), 18 + 24 / 32 * 4)     # 21.0

    def test_sturges(self):
        self.assertEqual(parte3.numero_classes(120), 8)
        self.assertEqual(parte3.numero_classes(100), 8)

    def test_montar_classes_inclui_maximo(self):
        d = list(range(1, 41))
        cl = parte3.montar_classes(d)
        self.assertEqual(cl[-1].Fi, 40)
        self.assertEqual(cl[-1].superior, 40)
        self.assertTrue(cl[-1].fechada_direita)

    def test_dados_constantes(self):
        with self.assertRaises(ValueError):
            parte3.montar_classes([5, 5, 5])

    def test_entrada_invalida(self):
        with self.assertRaises(io_dados.ErroDeDados):
            io_dados.parse_entrada_manual("1, abc, 3")
        with self.assertRaises(io_dados.ErroDeDados):
            io_dados.carregar_csv("/nao/existe.csv")

    def test_csv(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write('idade\n18\n"19,5"\n20\n')
            nome = f.name
        self.assertEqual(io_dados.carregar_csv(nome), [18.0, 19.5, 20.0])
        with open(nome, "w") as f:
            f.write("idade\n18\nxx\n")
        with self.assertRaises(io_dados.ErroDeDados):
            io_dados.carregar_csv(nome)
        os.remove(nome)


if __name__ == "__main__":
    unittest.main()
