# Trabalho I

- `impl`: Código fonte do projeto;
- `latex`: Arquivos referentes a elaboração do relatório prático;

## Execução do projeto

No diretório `impl`:

- Para executar **todos** (💀) os testes:

```bash
# pwd: INE5633-2025.02/trabalho_1/impl

make
```

***

- Para filtrar os testes de acordo com dimensão/uso de heurística:

```bash
# pwd: INE5633-2025.02/trabalho_1/impl
# Dimensão e nível de heurística indicados pelo prefixo N_LEVEL; ex.:

make run POSTFIX=8_L1
```

***
- Para executar um teste em específico:

```bash
# pwd: INE5633-2025.02/trabalho_1/impl

make run TEST=<TEST_CASE>.txt
```

Onde `<TEST_CASE>` refere-se a um cenário de teste elaborado em `impl/resources/`.

### Formato dos dados de entrada do programa

Caso deseje executar o programa com um conjunto de dados diferente dos arquivos que estão presentes no diretório de recursos, basta executar o comando inicial:

```bash
# Pode ser necessário registrar o script via
# `poetry install`

poetry run py_8pzzl
```

E em seguida digitar os dados no seguinte formato:

```
M
E1..EN
LEVEL
```

Onde:

- _M_ refere-se ao tamanho (do lado) do tabuleiro (ex.: 3 para _8Puzzle_, 4 para _15Puzzle_, etc...);
- _E1..EN_ referem-se aos números de _(N = M^2)_ de 0 até _N_ (em qualquer ordem) que expressam o estado inicial do tabuleiro;
- _LEVEL_ é um valor dentre:
    - _**L0:**_ Para execução de _A*_ com heurística _nula_ (custo uniforme);
    - _**L1:**_ Para execução de _A*_ com heurística não admissível;
    - _**L2:**_ Para execução de _A*_ com heurística _Manhattan_;
    - _**L3:**_ Para execução de _A*_ com heurística tunada;

