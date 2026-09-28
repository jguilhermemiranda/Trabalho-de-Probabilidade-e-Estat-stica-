import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Classe:
    inferior: float
    superior: float
    fi: int
    Fi: int
    fechada_direita: bool = False  # True apenas na última classe

    @property
    def amplitude(self):
        return self.superior - self.inferior

    @property
    def ponto_medio(self):
        return (self.inferior + self.superior) / 2


def numero_classes(n):
    return max(1, int(1 + 3.322 * math.log10(n) + 0.5))


def montar_classes(dados):
    n = len(dados)
    minimo, maximo = min(dados), max(dados)
    if n < 2 or maximo == minimo:
        raise ValueError("São necessários ao menos 2 valores distintos para agrupar em classes.")
    k = numero_classes(n)
    h = (maximo - minimo) / k
    limites = [minimo + i * h for i in range(k)] + [maximo]  # último = máx exato
    freq = [0] * k
    for x in dados:
        i = min(int((x - minimo) / h), k - 1)
        while i < k - 1 and x >= limites[i + 1]:
            i += 1
        while i > 0 and x < limites[i]:
            i -= 1
        freq[i] += 1
    classes, acumulada = [], 0
    for i in range(k):
        acumulada += freq[i]
        classes.append(Classe(limites[i], limites[i + 1], freq[i], acumulada, i == k - 1))
    return classes


def media(classes):
    n = classes[-1].Fi
    return sum(c.ponto_medio * c.fi for c in classes) / n


def separatriz(classes, p):
    if not 0 < p < 100:
        raise ValueError("p deve estar entre 0 e 100 (exclusivo)")
    posicao = p * classes[-1].Fi / 100
    f_ant = 0
    for c in classes:
        if c.Fi >= posicao:
            return c.inferior + ((posicao - f_ant) / c.fi) * c.amplitude
        f_ant = c.Fi
    raise ValueError("posição fora da tabela")


def mediana(classes):
    return separatriz(classes, 50)


def quartil(classes, i):
    return separatriz(classes, 25 * i)


def decil(classes, i):
    return separatriz(classes, 10 * i)


def _classe_modal(classes):
    idx = max(range(len(classes)), key=lambda i: classes[i].fi)  # 1ª em empate
    ant = classes[idx - 1].fi if idx > 0 else 0
    post = classes[idx + 1].fi if idx < len(classes) - 1 else 0
    return idx, ant, post


def moda_czuber(classes):
    idx, ant, post = _classe_modal(classes)
    c = classes[idx]
    d1, d2 = c.fi - ant, c.fi - post
    if d1 + d2 == 0:
        return None
    return c.inferior + d1 / (d1 + d2) * c.amplitude


def moda_king(classes):
    idx, ant, post = _classe_modal(classes)
    c = classes[idx]
    if ant + post == 0:
        return None
    return c.inferior + post / (ant + post) * c.amplitude
