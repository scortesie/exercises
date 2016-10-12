import sys
from earthmatrix import EarthMatrix


def main():
    photograph = [
        [9, 2, 2, 2, 3, 5],
        [9, 8, 3, 2, 4, 5],
        [9, 7, 2, 2, 4, 3],
        [9, 9, 2, 4, 4, 3],
        [9, 2, 3, 4, 3, 5]]
    matrix = EarthMatrix(photograph)
    assert(matrix.detect_borders() == [
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 0, 1],
        [0, 1, 0, 0, 1, 0]])
    return 0

if __name__ == '__main__':
    sys.exit(main())
