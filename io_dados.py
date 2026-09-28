import csv
import math


class ErroDeDados(Exception):
    """Dados de entrada inválidos (mensagem já pronta para o usuário)."""


def converter_numero(texto):
    """Converte texto em float. Aceita vírgula decimal ('24,5'). Levanta ValueError."""
    t = texto.strip()
    if "," in t and "." not in t:
        t = t.replace(",", ".")
    valor = float(t)
    if not math.isfinite(valor):
        raise ValueError(texto)
    return valor


def parse_entrada_manual(texto):
    tokens = [t.strip() for t in texto.replace(";", ",").split(",")]
    while tokens and tokens[-1] == "":
        tokens.pop()  # tolera vírgula final
    if not tokens:
        raise ErroDeDados("Nenhum valor informado.")
    dados = []
    for i, t in enumerate(tokens, start=1):
        try:
            dados.append(converter_numero(t))
        except ValueError:
            raise ErroDeDados(f"Valor inválido na posição {i}: '{t}' não é um número.")
    return dados


def _ler_linhas(caminho):
    try:
        with open(caminho, newline="", encoding="utf-8-sig") as f:
            texto = f.read()
    except FileNotFoundError:
        raise ErroDeDados(f"Arquivo não encontrado: {caminho}")
    except (OSError, UnicodeDecodeError) as e:
        raise ErroDeDados(f"Não foi possível ler '{caminho}': {e}")
    linhas = texto.splitlines()
    if not any(l.strip() for l in linhas):
        raise ErroDeDados("O arquivo está vazio.")
    primeira = next(l for l in linhas if l.strip())
    delim = ";" if ";" in primeira else ("\t" if "\t" in primeira else ",")
    rows = [(n, r) for n, r in enumerate(csv.reader(linhas, delimiter=delim), start=1)
            if any(c.strip() for c in r)]
    return rows


def numero_colunas_csv(caminho):
    return max(len(r) for _, r in _ler_linhas(caminho))


def carregar_csv(caminho, coluna=0):
    rows = _ler_linhas(caminho)
    dados = []
    for pos, (n_linha, r) in enumerate(rows):
        if coluna >= len(r):
            raise ErroDeDados(f"Linha {n_linha}: a coluna {coluna + 1} não existe.")
        celula = r[coluna]
        try:
            dados.append(converter_numero(celula))
        except ValueError:
            if pos == 0:
                continue  # cabeçalho
            raise ErroDeDados(f"Linha {n_linha}: '{celula.strip()}' não é um número.")
    if not dados:
        raise ErroDeDados("Nenhum valor numérico encontrado na coluna escolhida.")
    return dados
