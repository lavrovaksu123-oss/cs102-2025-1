import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)  # Преобразуем путь в объект Path
    with path.open() as f:
        puzzle = f.read()  # Читаем содержимое файла
    return create_grid(puzzle)  # Преобразуем в сетку


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Преобразовать строку в сетку 9x9"""
    digits = [c for c in puzzle if c in "123456789."]  # Оставляем только цифры и точки
    grid = group(digits, 9)  # Группируем в 9 строк по 9 элементов
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2  # Ширина ячейки
    line = "+".join(["-" * (width * 3)] * 3)  # Горизонтальная линия-разделитель
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":  # После 3-й и 6-й строки
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i * n : (i + 1) * n] for i in range(n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, _ = pos  # Извлекаем номер строки
    return grid[row]  # Возвращаем строку


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, col = pos  # Извлекаем номер столбца
    return [row[col] for row in grid]  # Собираем элементы столбца


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    # Находим начальную позицию блока 3x3
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3
    # Собираем все значения из блока
    return [grid[block_row + i][block_col + j] for i in range(3) for j in range(3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    # Проходим по всем клеткам сетки
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":  # Нашли пустую клетку
                return (row, col)
    return None  # Пустых клеток нет


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    all_values = set("123456789")  # Все возможные цифры
    row_values = set(get_row(grid, pos))  # Цифры в строке
    col_values = set(get_col(grid, pos))  # Цифры в столбце
    block_values = set(get_block(grid, pos))  # Цифры в блоке
    return all_values - row_values - col_values - block_values  # Разность множеств


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # 1. Найти свободную позицию
    pos = find_empty_positions(grid)

    # Базовый случай: если нет свободных позиций, пазл решён
    if pos is None:
        return grid

    row, col = pos

    # 2. Найти все возможные значения для этой позиции
    possible_values = find_possible_values(grid, pos)

    # Если нет возможных значений — тупик, нужен откат
    if not possible_values:
        return None

    # 3. Для каждого возможного значения
    for value in possible_values:
        # 3.1. Поместить это значение на эту позицию
        grid[row][col] = value

        # 3.2. Продолжить решать оставшуюся часть пазла
        result = solve(grid)

        # Если решение найдено — вернуть его
        if result is not None:
            return result

        # Откат: если решение не найдено, вернуть пустое значение
        grid[row][col] = "."

    # Если ни одно значение не подошло — тупик
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    expected = set("123456789")  # Эталон: все цифры от 1 до 9

    # Проверка всех строк
    for row in range(9):
        if set(get_row(solution, (row, 0))) != expected:
            return False

    # Проверка всех столбцов
    for col in range(9):
        if set(get_col(solution, (0, col))) != expected:
            return False

    # Проверка всех блоков 3x3
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            if set(get_block(solution, (block_row, block_col))) != expected:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    # Создаём пустую сетку и решаем её
    grid = [["." for _ in range(9)] for _ in range(9)]
    solved = solve(grid)
    
    if solved is None:
        # Fallback: создаём простое решённое судоку
        solved = [list("123456789"[(i+j)%9] for i in range(9)) for j in range(9)]
    
    grid = solved

    # Ограничиваем N до допустимого диапазона
    N = max(0, min(N, 81))
    
    # Сколько клеток нужно очистить
    cells_to_clear = 81 - N
    
    # Создаём список всех позиций и перемешиваем
    positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(positions)
    
    # Очищаем нужное количество клеток
    for i in range(cells_to_clear):
        row, col = positions[i]
        grid[row][col] = "."
    
    return grid


if __name__ == "__main__":
    # Решаем все пазлы из файлов
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)  # Читаем пазл
        display(grid)  # Показываем исходный пазл
        solution = solve(grid)  # Решаем
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)  # Показываем решение
