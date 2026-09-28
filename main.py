import formatacao as fmt
import io_dados
import parte1
import parte2
import parte3

# Separatrizes exibidas (inferidas do exemplo do enunciado). Ajuste aqui se necessário.
QUARTIS = (1, 3)
DECIS = (2, 7)
PERCENTIS = (15, 22, 63, 70)


def obter_dados():
    print("[1] Inserir dados via terminal (separados por vírgula)")
    print("[2] Carregar arquivo .csv\n")
    while True:
        op = input("Escolha a opção: ").strip()
        try:
            if op == "1":
                dados = io_dados.parse_entrada_manual(input("Dados: "))
                print(f"Dados recebidos! (n = {len(dados)} elementos)")
                return dados
            if op == "2":
                caminho = input("Caminho do arquivo .csv: ").strip().strip('"')
                coluna = 0
                ncols = io_dados.numero_colunas_csv(caminho)
                if ncols > 1:
                    resp = input(f"O arquivo tem {ncols} colunas. Qual usar (1-{ncols})? [1]: ").strip()
                    if resp:
                        if not resp.isdigit() or not 1 <= int(resp) <= ncols:
                            raise io_dados.ErroDeDados("Coluna inválida.")
                        coluna = int(resp) - 1
                dados = io_dados.carregar_csv(caminho, coluna)
                print(f"Arquivo carregado com sucesso! (n = {len(dados)} elementos)")
                return dados
            print("Opção inválida. Digite 1 ou 2.")
        except io_dados.ErroDeDados as e:
            print(f"ERRO: {e}\n")


def mostrar_parte1(dados):
    r = parte1.tendencia_central(dados)
    print(fmt.secao("PARTE 1: DADOS NÃO AGRUPADOS (Módulo Statistics)"))
    print(f"Média: {fmt.num(r['media'])}\nMediana: {fmt.num(r['mediana'])}\nModa: {fmt.num(r['moda'])}")


def mostrar_parte2(dados):
    tabela = parte2.tabela_frequencias(dados)
    r = parte2.calcular(tabela)
    print(fmt.secao("PARTE 2: DISTRIBUIÇÃO DE FREQUÊNCIA (SEM INTERVALO)"))
    print(fmt.tabela_discreta(tabela))
    modas = ", ".join(fmt.num(m) for m in r["modas"])
    rotulo = "Moda" if len(r["modas"]) == 1 else "Modas"
    print(f"Calculados via tabela: Média = {fmt.num(r['media'])} | "
          f"Mediana = {fmt.num(r['mediana'])} | {rotulo} = {modas}")


def mostrar_parte3(dados):
    print(fmt.secao("PARTE 3: DISTRIBUIÇÃO DE FREQUÊNCIA (COM INTERVALO)"))
    try:
        classes = parte3.montar_classes(dados)
    except ValueError as e:
        print(f"Não foi possível montar as classes: {e}")
        return
    n = len(dados)
    print(f"n = {n} | k (Sturges) = {len(classes)} | h = {classes[0].amplitude:.4f}")
    print(fmt.tabela_classes(classes))
    print("Calculados via Fórmulas de Interpolação:")
    print(f"-> Média: {fmt.num(parte3.media(classes))} | Mediana: {fmt.num(parte3.mediana(classes))}")
    print(f"-> Moda (Czuber): {fmt.num(parte3.moda_czuber(classes))} | "
          f"Moda (King): {fmt.num(parte3.moda_king(classes))}")
    print("-> Quartis: " + " | ".join(f"Q{i} = {fmt.num(parte3.quartil(classes, i))}" for i in QUARTIS))
    print("-> Decis: " + " | ".join(f"D{i} = {fmt.num(parte3.decil(classes, i))}" for i in DECIS))
    print("-> Percentis: " + " | ".join(f"P{p} = {fmt.num(parte3.separatriz(classes, p))}" for p in PERCENTIS))


def main():
    print(fmt.cabecalho("ANALISADOR ESTATÍSTICO - ENGENHARIA DE SOFTWARE"))
    try:
        dados = obter_dados()
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrado.")
        return
    mostrar_parte1(dados)
    mostrar_parte2(dados)
    mostrar_parte3(dados)


if __name__ == "__main__":
    main()
