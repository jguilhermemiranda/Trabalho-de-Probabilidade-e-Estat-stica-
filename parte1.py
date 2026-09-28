import statistics


def tendencia_central(dados):
    return {
        "media": statistics.mean(dados),
        "mediana": statistics.median(dados),
        "moda": statistics.mode(dados),  # multimodal: retorna o 1º valor mais frequente
    }
