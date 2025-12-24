import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row_index, row in enumerate(self.life.curr_generation):
            line = "".join("O" if cell else " " for cell in row)
            screen.addstr(row_index + 1, 1, line)

    def run(self) -> None:
        screen = curses.initscr()
        # Настраиваем терминал для неблокирующего ввода без эха.
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        screen.nodelay(True)
        try:
            running = True
            while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
                key = screen.getch()
                if key in (ord("q"), ord("Q")):
                    # Выходим по клавишам Q/q.
                    running = False
                    continue
                screen.erase()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                # Делаем шаг симуляции.
                self.life.step()
                curses.napms(100)
        finally:
            # Возвращаем настройки терминала.
            curses.nocbreak()
            curses.echo()
            curses.endwin()
