LARGURA = 53
SEP = "-" * LARGURA


def num(x):
    return "indefinida" if x is None else f"{x:.2f}"


def valor(x):
    return str(int(x)) if float(x).is_integer() else f"{x:g}"


def cabecalho(titulo):
    return f"{'=' * LARGURA}\n   {titulo}\n{'=' * LARGURA}"


def secao(titulo):
    return f"{SEP}\n{titulo}\n{SEP}"


def tabela_discreta(tabela):
    linhas = ["Valor (xi) | Freq. Absoluta (fi) | Freq. Acumulada (Fi)"]
    for xi, fi, Fi in tabela:
        linhas.append(f"{valor(xi):>9}  | {fi:>19} | {Fi:>20}")
    return "\n".join(linhas)


def tabela_classes(classes):
    linhas = [f"{'Classe':<20}| {'fi':>5} | {'Fi':>5}"]
    for c in classes:
        fecho = "]" if c.fechada_direita else ")"
        rot = f"[{c.inferior:.2f} - {c.superior:.2f}{fecho}"
        linhas.append(f"{rot:<20}| {c.fi:>5} | {c.Fi:>5}")
    return "\n".join(linhas)
