import random
from typing import List, Tuple


class ZobristHasher:
    """
    Implementa Zobrist Hashing para o N-Puzzle.
    Gera uma tabela de números aleatórios por (posição, peça).
    O hash de um estado é a XOR de todos os números de acordo com
    a posição das peças no tabuleiro.
    """

    def __init__(self, n: int, seed: int = 42) -> None:
        """
        n: tamanho do puzzle (3 para 8-puzzle, 4 para 15-puzzle, 5 para 24-puzzle)
        seed: semente para gerar números aleatórios consistentes
        """
        self.n = n
        self.size = n * n
        random.seed(seed)

       
        self.table: List[List[int]] = [
            [random.getrandbits(64) for _ in range(self.size)]
            for _ in range(self.size)
        ]

    def hash_state(self, state: Tuple[int, ...]) -> int:
        """
        Calcula o hash Zobrist para um estado do puzzle.
        """
        h = 0
        for pos, val in enumerate(state):
            h ^= self.table[pos][val]
        return h

    def update_hash(self, old_hash: int, pos1: int, pos2: int, val1: int, val2: int) -> int:
        """
        Atualiza o hash quando duas peças são trocadas (pos1 <-> pos2).
        Isso evita recalcular o hash inteiro do estado.
        """
        h = old_hash
        
        h ^= self.table[pos1][val1]
        h ^= self.table[pos2][val2]
        h ^= self.table[pos1][val2]
        h ^= self.table[pos2][val1]
        return h
