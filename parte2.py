def tabela_frequencias(dados):
    """Retorna lista de (xi, fi, Fi) ordenada por xi."""
    contagem = {}
    for x in dados:
        contagem[x] = contagem.get(x, 0) + 1
    tabela, acumulada = [], 0
    for xi in sorted(contagem):
        acumulada += contagem[xi]
        tabela.append((xi, contagem[xi], acumulada))
    return tabela


def _valor_na_posicao(tabela, posicao):
    for xi, _, Fi in tabela:
        if Fi >= posicao:
            return xi
    raise ValueError("posição fora da tabela")


def media(tabela):
    n = tabela[-1][2]
    return sum(xi * fi for xi, fi, _ in tabela) / n


def mediana(tabela):
    n = tabela[-1][2]
    if n % 2 == 1:
        return float(_valor_na_posicao(tabela, (n + 1) // 2))
    return (_valor_na_posicao(tabela, n // 2) + _valor_na_posicao(tabela, n // 2 + 1)) / 2


def modas(tabela):
    maior = max(fi for _, fi, _ in tabela)
    return [xi for xi, fi, _ in tabela if fi == maior]


def calcular(tabela):
    return {"media": media(tabela), "mediana": mediana(tabela), "modas": modas(tabela)}
