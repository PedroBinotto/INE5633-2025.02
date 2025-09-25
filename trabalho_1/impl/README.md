# py_8pzzl

Implementação do Trabalho I da disciplina de Sistemas Inteligentes

## Execução do projeto

**Requisitos:**

- [Python](https://www.python.org/) >=3.12;
- [Poetry](https://python-poetry.org/) (para gerenciamento de ambiente virtual e versão do intérprete Python);
- [Make](https://www.gnu.org/software/make/);

**Recomendações:**

- Executar projeto em ambiente _UNIX-like_;

***

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

make run TEST=<TESTCASE>.txt
```

Onde _TESTCASE_ refere-se a um cenário de teste elaborado em `impl/resources/`.

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
E0..EN
LEVEL
```

Onde:

- _M_ refere-se ao tamanho (do lado) do tabuleiro (ex.: 3 para _8Puzzle_, 4 para _15Puzzle_, etc...);
- _E0..EN_ referem-se aos números de _(N = M^2)_ de 0 até _N_ (em qualquer ordem) que expressam o estado inicial do tabuleiro;
- _LEVEL_ é um valor dentre:
    - _**L0:**_ Para execução de _A*_ com heurística _nula_ (custo uniforme);
    - _**L1:**_ Para execução de _A*_ com heurística não admissível;
    - _**L2:**_ Para execução de _A*_ com heurística _Manhattan_;
    - _**L3:**_ Para execução de _A*_ com heurística tunada;

### Formato dos dados de saída do programa

Para cada execução do algoritmo sobre um conjunto de dados de entrada, um arquivo com os dados de saída do programa será gerado no diretório `/output`, de acordo com o seguinte padrão de nomenclatura:

```
<TIMESTAMP>_<STATE>_<LEVEL>.json
```

Onde:

- _TIMESTAMP_ refere-se ao _UNIX timestamp_ (_epoch_) associada à execução do algoritmo;
- _STATE_ refere-se ao estado inicial informado ao programa (_E0..EN_);
- _LEVEL_ refere-se ao nível de heurística escolhido para a execução do algoritmo;

Cada arquivo apresentará os dados referentes à execução de acordo com o seguinte esquema de organização de conteúdos:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "start_time": {
      "type": "number"
    },
    "end_time": {
      "type": "number"
    },
    "elapsed_time": {
      "type": "number"
    },
    "h_level": {
      "type": "string"
    },
    "size": {
      "type": "number"
    },
    "nodes_open": {
      "type": "number"
    },
    "nodes_open_upper_bound": {
      "type": "number"
    },
    "nodes_visited": {
      "type": "number"
    },
    "path_size": {
      "type": "number"
    },
    "path": {
      "type": "array",
      "items": {
        "type": "array",
        "items": {
          "type": "number"
        }
      }
    }
  },
  "required": [
    "start_time",
    "end_time",
    "elapsed_time",
    "h_level",
    "size",
    "nodes_open",
    "nodes_open_upper_bound",
    "nodes_visited",
    "path_size",
    "path"
  ]
}

```
