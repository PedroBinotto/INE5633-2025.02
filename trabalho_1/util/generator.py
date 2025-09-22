#!/usr/bin/python3
#
# Util script used to generate valid states for test files
# Adapted from https://stackoverflow.com/a/62149931

from itertools import permutations
import json
import sys


def inversion_count(tiles):
    """Count inversions in the tile sequence (ignoring 0 = blank)."""
    count = 0
    seq = [t for t in tiles if t != 0]
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                count += 1
    return count


def solvable(tiles, N):
    """
    Check solvability of an N-puzzle.
    - For odd N: solvable if inversions even
    - For even N: solvable if (inversions + row_of_blank_from_bottom) even
    """
    inv_count = inversion_count(tiles)

    if N % 2 == 1:
        is_solvable = inv_count % 2 == 0
    else:
        blank_index = tiles.index(0)
        row_from_top = blank_index // N
        row_from_bottom = N - row_from_top
        is_solvable = (inv_count + row_from_bottom) % 2 == 0

    if is_solvable:
        difficulties = {0: "trivial", 2: "easy", 4: "medium", 6: "hard"}
        difficulty = difficulties.get(inv_count, "very hard")
        return [difficulty, inv_count, is_solvable]

    return [inv_count, is_solvable]


def generate_tiles(N, limit=None):
    """Generate solvable tiles for the NxN puzzle.
    Optionally limit the number of generated states."""
    tile_candidates = permutations(range(N * N))
    good_tiles = []
    for idx, tile_candidate in enumerate(tile_candidates):
        if solvable(tile_candidate, N)[-1]:
            good_tiles.append(tile_candidate)
        if limit and len(good_tiles) >= limit:
            break
    return good_tiles


def choose_difficulty(tiles, N, level=2):
    """Choose tiles of given difficulty level (measured by inversion count)."""
    labelled_tiles = []
    for tile in tiles:
        labelled_tiles.append({"tile": tile, "label": solvable(tile, N)})
    return [tile for tile in labelled_tiles if tile["label"][1] == level]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    else:
        exit(1)

    tiles = generate_tiles(N, limit=50)
    print(json.dumps(choose_difficulty(tiles, N, level=2)))
