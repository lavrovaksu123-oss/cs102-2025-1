import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Код из предыдущего задания.
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Код из предыдущего задания.
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = (
                    pygame.Color("green")
                    if self.life.curr_generation[row][col]
                    else pygame.Color("white")
                )
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        # Код из предыдущего задания.
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        paused = False  # Флаг паузы симуляции.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    # Переключаем паузу клавишей пробел.
                    paused = not paused
                elif event.type == MOUSEBUTTONDOWN and paused:
                    # Меняем состояние клетки на паузе.
                    x_pos, y_pos = event.pos
                    col = x_pos // self.cell_size
                    row = y_pos // self.cell_size
                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        self.life.curr_generation[row][col] = (
                            0 if self.life.curr_generation[row][col] else 1
                        )
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            if (
                not paused
                and self.life.is_changing
                and not self.life.is_max_generations_exceeded
            ):
                # Делаем шаг только если можно продолжать.
                self.life.step()
            clock.tick(self.speed)
        pygame.quit()
