from argparse import ArgumentParser
from consts import (REGULAR_TRIANGLE, ISOSCELES_TRIANGLE, EQUILATERAL_TRIANGLE,
    NOT_TRIANGLE, UNKNOWN_ERROR, ERROR_ARGUMENTS)


class NotEnoughArguments(Exception):
    pass


def is_triangle(edges: list):
    a, b, c = sorted(edges)
    return a + b > c


def is_equilateral_triangle(edges: list) -> bool:
    a, b, c = edges
    return a == b == c


def is_isosceles_triangle(edges: list) -> bool:
    a, b, c = sorted(edges)
    return a == b or b == c


def is_digits(edges: list):
    try:
        return all([float(i) for i in edges])
    except ValueError:
        return False


def get_triangle_edges() -> list:
    parser = ArgumentParser()
    parser.add_argument('edges', nargs='*')
    try:
        args = parser.parse_args()
        if len(args.edges) != 3:
            raise NotEnoughArguments

        if not is_digits(args.edges):
            raise ValueError
        return [float(value) for value in args.edges]
    except ValueError:
        raise ValueError(UNKNOWN_ERROR)
    except NotEnoughArguments:
        raise ValueError(ERROR_ARGUMENTS)
    except Exception:
        raise Exception


def classify_triangle(edges: list) -> str:
    if not is_triangle(edges):
        raise Exception(NOT_TRIANGLE)
    elif is_equilateral_triangle(edges):
        return EQUILATERAL_TRIANGLE
    elif is_isosceles_triangle(edges):
        return ISOSCELES_TRIANGLE
    else:
        return REGULAR_TRIANGLE


def main():
    try:
        triangle_edges = get_triangle_edges()
        print(classify_triangle(triangle_edges))
    except BaseException as error:
        print(error)


if __name__ == "__main__":
    main()
