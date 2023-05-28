import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QSlider, QAction
from PyQt5.QtCore import Qt

from instruction import InstructionWindow


class SettingsWindow(QMainWindow):
    def __init__(self, game_window):
        super().__init__()
        self.game_window = game_window
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(100, 100, 200, 50)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(self.game_window.max_moves)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Настройки')

        # Метка с количеством шагов
        self.moves_label = QLabel(f'Макс. шагов: {self.game_window.max_moves}', self)
        self.moves_label.setGeometry(200, 150, 200, 50)

    def closeEvent(self, event):
        self.game_window.settings_window = None
        super().closeEvent(event)

    def slider_value_changed(self, value):
        self.game_window.max_moves = value
        self.moves_label.setText(f'Макс. шагов: {self.game_window.max_moves}')


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board_size = 12
        self.colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
        self.board = np.random.choice(self.colors, (self.board_size, self.board_size))
        self.buttons = []
        self.move_count = 0
        self.max_moves = 22
        self.best_score = 22
        self.row_indent = 50
        self.move_in_progress = False
        self.settings_window = None
        self.init_ui()
        self.init_menu()

        self.update_ui()

    def init_ui(self):
        self.setWindowTitle('Перекрась')
        self.setGeometry(100, 100, 800, 800)  # изменяем ширину окна
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = QPushButton('', self)
                btn.setStyleSheet(f'background-color: {self.board[i, j]}')
                btn.setGeometry(j * 50, self.row_indent + i * 50, 50, 50)
                row.append(btn)
            self.buttons.append(row)

        for i, color in enumerate(self.colors):
            btn = QPushButton('', self)
            btn.setStyleSheet(f'background-color: {color}')
            btn.clicked.connect(self.make_move(color))
            btn.setGeometry(600, self.row_indent + i * 100, 100, 100)  # перемещаем кнопки в сторону

        self.best_label = QLabel(f'ЛУЧШИЙ: {self.best_score}', self)
        self.best_label.setGeometry(540, 660, 100, 50)

        self.curr_label = QLabel(f' {self.move_count} / {self.max_moves}', self)
        self.curr_label.setGeometry(340, 660, 200, 50)

        # Кнопка перегенерации
        self.regen_btn = QPushButton('Новая игра', self)
        self.regen_btn.setGeometry(300, 710, 150, 50)  # перемещаем кнопку в сторону
        self.regen_btn.clicked.connect(self.regenerate_board)

        self.show()

    def regenerate_board(self):
        self.board = np.random.choice(self.colors, (self.board_size, self.board_size))
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].setStyleSheet(f'background-color: {self.board[i, j]}')
        self.move_count = 0
        if self.settings_window is not None:  # Проверяем наличие окна настроек
            self.settings_window.moves_label.setText(
                f'Макс. шагов: {self.max_moves}') # Обновляем метку в окне настроек

    def init_menu(self):
        settings_action = QAction('Настройки', self)
        settings_action.triggered.connect(self.open_settings)
        instruction_action = QAction('Инструкция', self)
        instruction_action.triggered.connect(self.open_instruction)

        menu = self.menuBar()
        settings_menu = menu.addMenu('Меню')
        settings_menu.addAction(settings_action)
        settings_menu.addAction(instruction_action)

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self)
            self.settings_window.setAttribute(Qt.WA_DeleteOnClose)  # Добавленная строка
        self.settings_window.show()

    def open_instruction(self):
        self.instruction_window = InstructionWindow()  # Сохраняем ссылку на объект в переменной класса
        self.instruction_window.show()

    def make_move(self, color):
        def action():
            if self.move_in_progress:
                return

            self.move_in_progress = True
            self.move_count += 1
            if self.settings_window is not None:  # Проверяем наличие окна настроек
                self.settings_window.moves_label.setText(
                    f'Макс. шагов: {self.max_moves}')  # Обновляем метку в окне настроек
            self.curr_label.setText(f'{self.move_count} / {self.max_moves}')

            self.fill(0, 0, self.board[0, 0], color)
            self.update_ui()
            if (self.board == color).all():
                self.best_score = min(self.best_score, self.move_count)
                self.best_label.setText(f'BEST: {self.best_score}')
                self.board = np.random.choice(self.colors, (self.board_size, self.board_size))
                self.move_count = 0
                if self.settings_window is not None:  # Проверяем наличие окна настроек
                    self.settings_window.moves_label.setText(
                        f'Макс. шагов: {self.max_moves}')  # Обновляем метку в окне настроек
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        self.buttons[i][j].setStyleSheet(f'background-color: {self.board[i, j]}')

                QMessageBox.information(self, "Победа!", "Вы выиграли!")
                self.close()
            elif self.move_count == self.max_moves:
                QMessageBox.information(self, "Поражение", "Вы проиграли!")
                self.close()

            self.move_in_progress = False

        return action

    def update_ui(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].setStyleSheet(f'background-color: {self.board[i, j]}')

    def fill(self, i, j, old_color, new_color):
        stack = [(i, j)]
        if old_color != new_color:
            while stack:
                i, j = stack.pop()
                if i < 0 or j < 0 or i >= self.board_size or j >= self.board_size:
                    continue
                if self.board[i, j] != old_color:
                    continue
                self.board[i, j] = new_color
                stack.append((i - 1, j))
                stack.append((i + 1, j))
                stack.append((i, j - 1))
                stack.append((i, j + 1))


if __name__ == '__main__':
    app = QApplication([])
    game = GameWindow()
    app.exec()