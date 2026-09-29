# Analisador Estatístico (CLI)

Aplicação de linha de comando em Python que calcula estatística descritiva a partir de dados digitados ou de um arquivo `.csv`, em três níveis de abstração:

| Parte | Tipo de dado | Restrição |
|---|---|---|
| 1 | Não agrupado | Somente o módulo `statistics` |
| 2 | Agrupado sem intervalo de classe | Cálculos feitos a partir da tabela de frequências |
| 3 | Agrupado com intervalo de classe | Python puro: nenhuma biblioteca estatística |

Não há dependências externas.

## 👥 Autores

- **Bianca Caetano Oliveira** — [GitHub ](https://github.com/BiancaaCaetano)
- **Kaio Oliveira** — [GitHub](https://github.com/KaioOliveiradS)
- **João Guilherme Schirm Couto** — [GitHub](https://github.com/aoocjeta)
- **João Guilherme de Oliveira Miranda** — [GitHub](https://github.com/jguilhermemiranda)
- **Nicolas de Souza** — [GitHub](https://github.com/NicolasLdeSouza)
## Requisitos e execução

- Python 3.8 ou superior.

```bash
python main.py                         # executa o programa
python -m unittest discover -s tests -v # executa os testes
```

## Uso

O programa oferece duas formas de entrada:

```text
[1] Inserir dados via terminal (separados por vírgula)
[2] Carregar arquivo .csv
```

**Opção 1:** digite números separados por vírgula (ou `;`). Exemplo:

```text
18, 19, 22.5, 24
```

**Opção 2:** informe o caminho do arquivo.

- O separador (`,`, `;` ou tab) é detectado na primeira linha.
- Se a primeira linha da coluna escolhida não for numérica, ela é tratada como cabeçalho.
- Se houver mais de uma coluna, o programa pergunta qual usar.
- Vírgula decimal é aceita. Em CSV separado por vírgula, o valor precisa estar entre aspas (`"19,5"`), senão a vírgula é lida como separador de colunas.
- Qualquer valor não numérico interrompe a leitura e informa a linha, por exemplo `Linha 3: 'xx' não é um número.`

### Exemplo de saída (19 valores digitados)

```text
PARTE 1: DADOS NÃO AGRUPADOS (Módulo Statistics)
Média: 24.68
Mediana: 24.00
Moda: 22.00

PARTE 3: DISTRIBUIÇÃO DE FREQUÊNCIA (COM INTERVALO)
n = 19 | k (Sturges) = 5 | h = 3.2000
Classe               |    fi |    Fi
[18.00 - 21.20)      |     5 |     5
[21.20 - 24.40)      |     5 |    10
[24.40 - 27.60)      |     4 |    14
[27.60 - 30.80)      |     2 |    16
[30.80 - 34.00]      |     3 |    19

Calculados via Fórmulas de Interpolação:
-> Média: 24.82 | Mediana: 24.08
-> Moda (Czuber): 21.20 | Moda (King): 21.20
-> Quartis: Q1 = 21.04 | Q3 = 28.00
-> Decis: D2 = 20.43 | D7 = 27.04
-> Percentis: P15 = 19.82 | P22 = 20.68 | P63 = 25.98 | P70 = 27.04
```

A Parte 2 também é exibida, com a tabela `xi | fi | Fi`.

## Arquitetura

```text
main.py           Menu e orquestração (apenas entrada/saída)
io_dados.py       Entrada manual e CSV, validação, exceção ErroDeDados
parte1.py         Média, mediana e moda via statistics
parte2.py         Tabela (xi, fi, Fi) e cálculos baseados nela
parte3.py         Classes, Sturges e fórmulas de interpolação
formatacao.py     Formatação das tabelas e números
tests/            Testes unitários (unittest)
```

### Princípios adotados

- **Separação de responsabilidades:** só `main.py` interage com o usuário; os módulos de cálculo não fazem `print` nem `input`.
- **Restrições isoladas por módulo:** `statistics` só é importado em `parte1.py`; `parte3.py` importa apenas `math` (para `log10`).
- **Erros tratados na fronteira:** `io_dados.py` levanta `ErroDeDados` com mensagem pronta para o usuário; `main.py` a exibe e pede a entrada novamente.

## Como as fórmulas viraram código

### Parte 2: tabela discreta (`parte2.py`)

| Medida | Fórmula | Implementação |
|---|---|---|
| Média | `Σ(xi·fi) / n` | `media()` |
| Mediana | valor cuja `Fi` alcança a posição `(n+1)/2` (n ímpar) ou a média das posições `n/2` e `n/2+1` (n par) | `mediana()`, `_valor_na_posicao()` |
| Moda | `xi` de maior `fi` | `modas()` (devolve todas em caso de empate) |

### Parte 3: classes (`parte3.py`)

#### Quantidade de classes e amplitude (Sturges)

```text
k = 1 + 3,322 · log10(n)   -> arredondado ao inteiro mais próximo
h = (máximo − mínimo) / k  -> sem arredondar
```

As classes são `[li, ls)`; somente a última é fechada, `[li, ls]`, para que o valor máximo seja contado.

**Média:**

`x̄ = Σ(PMi · fi) / n`

onde `PMi = (li + ls) / 2` é o ponto médio da classe.

**Separatrizes:** todas usam uma única função, `separatriz(classes, p)`:

```text
posição = p · n / 100
Pp = li + ((posição − F_anterior) / fi) · h
```

onde `li`, `fi` e `h` pertencem à primeira classe cuja `Fi ≥ posição`, e `F_anterior` é a frequência acumulada da classe anterior.

| Medida | Chamada |
|---|---|
| Mediana | `separatriz(classes, 50)` |
| Quartil Qi | `separatriz(classes, 25·i)` |
| Decil Di | `separatriz(classes, 10·i)` |
| Percentil Pp | `separatriz(classes, p)` |

### Moda

A classe modal é a primeira classe de maior `fi`. Nas bordas, `f_ant` e `f_post` valem `0`.

```text
Czuber: Mo = li + d1/(d1+d2) · h
d1 = fi − f_ant
d2 = fi − f_post

King: Mo = li + f_post/(f_ant+f_post) · h
```

Se o denominador for zero, o resultado é exibido como `indefinida`.

## Decisões de projeto

O enunciado deixa alguns pontos em aberto. Escolhas adotadas:

- **k de Sturges:** arredondado ao inteiro mais próximo, não `ceil`.
- **Amplitude `h`:** exata, sem arredondamento.
- **Moda da Parte 3:** Czuber como principal; King exibida em conjunto.
- **Separatrizes exibidas:** Q1, Q3, D2, D7, P15, P22, P63 e P70, inferidas do exemplo do enunciado. Estão em constantes no topo de `main.py` e podem ser alteradas.
- **Moda multimodal:** na Parte 1, `statistics.mode` retorna o primeiro valor mais frequente; na Parte 2, todas as modas são listadas.
- **Dados constantes ou n < 2:** a Parte 3 é pulada com mensagem explicativa; as Partes 1 e 2 continuam normalmente.

## Testes

`tests/test_estatistica.py` cobre:

- consistência entre as Partes 1 e 2;
- mediana com n ímpar e par, e moda multimodal;
- fórmulas de interpolação da Parte 3, com valores calculados manualmente;
- Sturges (n = 100 e n = 120 resultam em 8 classes);
- inclusão do valor máximo na última classe;
- entradas inválidas (texto, arquivo inexistente, CSV com linha inválida).

## Limitações conhecidas

- A atribuição de valores às classes usa `float`. Dados com muitas casas decimais exatamente sobre o limite entre duas classes podem, raramente, cair na classe vizinha por erro de arredondamento.
- Os números do exemplo de saída do enunciado não são reproduzíveis a partir da própria tabela dele (por exemplo, a média da tabela é 24,87, e não 24,16; e Sturges com n = 120 resulta em 8 classes, não 4). Por isso os testes usam valores calculados à mão sobre a mesma tabela.