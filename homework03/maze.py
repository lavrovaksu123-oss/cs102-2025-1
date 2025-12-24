from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    direction = choice(("up", "right"))
    if direction == "up":
        next_x, next_y = x - 2, y
        if next_x < 0:
            next_x, next_y = x, y + 2
    else:
        next_x, next_y = x, y + 2
        if next_y >= cols:
            next_x, next_y = x - 2, y

    if not (0 <= next_x < rows and 0 <= next_y < cols):
        return grid

    wall_x = x - 1 if next_x < x else x
    wall_y = y + 1 if next_y > y else y
    grid[wall_x][wall_y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for coord in empty_cells:
        remove_wall(grid, coord)

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_x, next_y = i + dx, j + dy
                    if 0 <= next_x < rows and 0 <= next_y < cols and grid[next_x][next_y] == 0:
                        grid[next_x][next_y] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    x, y = exit_coord
    if not isinstance(grid[x][y], int) or grid[x][y] == 0:
        return None

    k = grid[x][y]
    path = [(x, y)]
    while int(k) > 1:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < rows and 0 <= next_y < cols and grid[next_x][next_y] == int(k) - 1:
                x, y = next_x, next_y
                k = int(k) - 1 
                path.append((x, y))
                break
        else:
            return None
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])
    if x not in (0, rows - 1) and y not in (0, cols - 1):
        return False

    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_x, next_y = x + dx, y + dy
        if 0 <= next_x < rows and 0 <= next_y < cols:
            if grid[next_x][next_y] != "■":
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    maze = deepcopy(grid)
    exits = get_exits(maze)
    if len(exits) < 2:
        return maze, None

    if any(encircled_exit(maze, coord) for coord in exits):
        return maze, None

    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell in (" ", "X"):
                maze[i][j] = 0

    start, finish = exits[0], exits[1]
    maze[start[0]][start[1]] = 1

    k = 1
    while maze[finish[0]][finish[1]] == 0:
        prev = deepcopy(maze)
        make_step(maze, k)
        if maze == prev:
            break
        k += 1

    if maze[finish[0]][finish[1]] == 0:
        return maze, None
    return maze, shortest_path(maze, finish)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


def print_grid(grid: List[List[Union[str, int]]]) -> None:
    for row in grid:
        print(" ".join(str(cell) for cell in row))


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print_grid(GRID)
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print_grid(MAZE)
