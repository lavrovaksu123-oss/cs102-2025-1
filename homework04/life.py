import pathlib
import random
import typing as tp


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[int] = None,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Код из предыдущего задания.
        grid: Grid = []
        for _ in range(self.rows):
            if randomize:
                row = [random.randint(0, 1) for _ in range(self.cols)]
            else:
                row = [0] * self.cols
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Код из предыдущего задания.
        row, col = cell
        neighbours: Cells = []
        for row_shift in (-1, 0, 1):
            for col_shift in (-1, 0, 1):
                if row_shift == 0 and col_shift == 0:
                    continue
                neighbour_row = row + row_shift
                neighbour_col = col + col_shift
                if 0 <= neighbour_row < self.rows and 0 <= neighbour_col < self.cols:
                    neighbours.append(self.curr_generation[neighbour_row][neighbour_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Код из предыдущего задания.
        next_generation: Grid = []
        for row in range(self.rows):
            next_row: Cells = []
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                alive_neighbours = sum(neighbours)
                cell = self.curr_generation[row][col]
                if cell == 1:
                    next_cell = 1 if alive_neighbours in (2, 3) else 0
                else:
                    next_cell = 1 if alive_neighbours == 3 else 0
                next_row.append(next_cell)
            next_generation.append(next_row)
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        next_generation = self.get_next_generation()
        self.prev_generation = self.curr_generation
        self.curr_generation = next_generation
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as handle:
            lines = [line.strip() for line in handle if line.strip()]

        rows = len(lines)
        cols = len(lines[0]) if rows else 0
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = [[int(value) for value in line] for line in lines]
        game.prev_generation = game.create_grid(randomize=False)
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as handle:
            for row in self.curr_generation:
                handle.write("".join(str(value) for value in row) + "\n")
