import sys


def rotate_quad(current_quad: str, degrees: int):
    """
    # rotate:
    #  q2 | q1
    #  ---+---
    #  q3 | q4
    """

    # how to move from one q to another with minimal code?
    quads = ['q1', 'q2', 'q3', 'q4']
    current_offset = quads.index(current_quad)
    quad_advance = divmod(degrees, 90)[0]  # 1, 2, 3 | -1, -2, -3

    print(quad_advance)
    new_quad = -99

    # if Right rotation
    if quad_advance < 0:
        if current_offset - abs(quad_advance) < 0:
            new_quad = len(quads) - abs(current_offset - quad_advance)
        else:
            new_quad = current_offset - quad_advance
    else:
        # if left rotation
        if current_offset + quad_advance >= len(quads):
            new_quad = len(quads) - abs(current_offset + quad_advance)
        else:
            new_quad = current_offset + quad_advance
    return quads[new_quad]


if __name__ == "__main__":
    print(rotate_quad(sys.argv[1], int(sys.argv[2])))
