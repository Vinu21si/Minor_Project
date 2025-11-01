# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random
import math

# =====================================================
# TIC TAC TOE ENGINE
# =====================================================

def available_moves(board):
    return [i for i, x in enumerate(board) if x == ""]

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "draw"
    return None

def minimax(board, player):
    winner = check_winner(board)
    if winner == "X":
        return {"score": -1}
    elif winner == "O":
        return {"score": 1}
    elif winner == "draw":
        return {"score": 0}

    moves = []
    for idx in available_moves(board):
        move = {}
        move["index"] = idx
        board[idx] = player
        if player == "O":
            result = minimax(board, "X")
            move["score"] = result["score"]
        else:
            result = minimax(board, "O")
            move["score"] = result["score"]
        board[idx] = ""
        moves.append(move)

    if player == "O":
        best_score = -math.inf
        best_move = None
        for m in moves:
            if m["score"] > best_score:
                best_score = m["score"]
                best_move = m
        return best_move
    else:
        best_score = math.inf
        best_move = None
        for m in moves:
            if m["score"] < best_score:
                best_score = m["score"]
                best_move = m
        return best_move

# =====================================================
# TIC TAC TOE SCREEN
# =====================================================

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = [""]*9
        self.current = "X"
        self.game_over = False

        root = BoxLayout(orientation='vertical', spacing=8, padding=12)
        
        with root.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_rect, size=self._update_rect)

        self.status = Label(
            text="Your turn (X)", 
            size_hint=(1, 0.1), 
            font_size=20,
            color=(1, 1, 1, 1)
        )
        root.add_widget(self.status)

        grid = GridLayout(cols=3, spacing=4, size_hint=(1, 0.75))
        self.buttons = []
        for i in range(9):
            b = Button(
                text="", 
                font_size=48,
                background_color=(0.2, 0.3, 0.4, 1),
                background_normal=''
            )
            b.bind(on_release=lambda inst, idx=i: self.on_click(idx))
            self.buttons.append(b)
            grid.add_widget(b)
        root.add_widget(grid)

        ctrl = BoxLayout(size_hint=(1, 0.15), spacing=8)
        reset = Button(
            text="Reset",
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        reset.bind(on_release=lambda x: self.reset())
        back = Button(
            text="← Back",
            background_color=(0.6, 0.2, 0.2, 1),
            background_normal=''
        )
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        ctrl.add_widget(reset)
        ctrl.add_widget(back)
        root.add_widget(ctrl)

        self.add_widget(root)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_click(self, idx):
        if self.board[idx] != "" or self.game_over:
            return
        
        self.board[idx] = "X"
        self.buttons[idx].text = "X"
        self.buttons[idx].color = (0.3, 0.6, 1, 1)

        winner = check_winner(self.board)
        if winner:
            self.status.text = f"Game over: {winner} wins!" if winner != "draw" else "Draw!"
            self.game_over = True
            return

        result = minimax(self.board.copy(), "O")
        if result is None:
            self.status.text = "Draw!"
            self.game_over = True
            return
        
        ai_index = result.get("index")
        if ai_index is not None:
            self.board[ai_index] = "O"
            self.buttons[ai_index].text = "O"
            self.buttons[ai_index].color = (1, 0.3, 0.3, 1)

            winner = check_winner(self.board)
            if winner:
                self.status.text = f"Game over: {winner} wins!" if winner != "draw" else "Draw!"
                self.game_over = True
                return

        self.status.text = "Your turn (X)"

    def reset(self):
        self.board = [""]*9
        for b in self.buttons:
            b.text = ""
            b.color = (1, 1, 1, 1)
        self.status.text = "Your turn (X)"
        self.game_over = False

# =====================================================
# CHESS SCREEN
# =====================================================

from kivy.uix.image import Image
import os

class ChessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = self.create_initial_board()
        self.selected = None
        self.white_turn = True
        
        # Image mappings for chess pieces
        self.piece_images = {
            '♔': 'images/white_king.png',
            '♕': 'images/white_queen.png',
            '♖': 'images/white_rook.png',
            '♗': 'images/white_bishop.png',
            '♘': 'images/white_knight.png',
            'a': 'D:/VS Code/Minor_Project2/frontend/images/white_pawn.png',
            '♚': 'images/black_king.png',
            '♛': 'images/black_queen.png',
            '♜': 'images/black_rook.png',
            '♝': 'images/black_bishop.png',
            '♞': 'images/black_knight.png',
            '1': 'images/black_pawn.png',
        }
        
        # Check if images directory exists
        self.use_images = os.path.exists('images')

        root = BoxLayout(orientation='vertical', spacing=6, padding=8)
        
        with root.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_rect, size=self._update_rect)

        self.status = Label(
            text="White's turn - Select a piece", 
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1),
            font_size=18
        )
        root.add_widget(self.status)

        self.grid = GridLayout(cols=8, spacing=1, size_hint=(1, 0.84))
        self.buttons = []
        self.draw_board()
        root.add_widget(self.grid)

        ctrl = BoxLayout(size_hint=(1, 0.08), spacing=6)
        back = Button(
            text="← Back",
            background_color=(0.6, 0.2, 0.2, 1),
            background_normal=''
        )
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        reset = Button(
            text="Reset Board",
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        reset.bind(on_release=lambda x: self.reset_board())
        ctrl.add_widget(reset)
        ctrl.add_widget(back)
        root.add_widget(ctrl)
        self.add_widget(root)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def create_initial_board(self):
        return [
            ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
            ['1', '1', '1', '1', '1', '1', '1', '1'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        ]

    def draw_board(self):
        self.grid.clear_widgets()
        self.buttons = []
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                is_light = (row_idx + col_idx) % 2 == 0
                bg_color = (0.9, 0.8, 0.6, 1) if is_light else (0.6, 0.4, 0.2, 1)
                
                # Create button with image or text
                if self.use_images and cell in self.piece_images:
                    # Use image if available
                    btn_layout = BoxLayout()
                    b = Button(
                        background_color=bg_color,
                        background_normal='',
                    )
                    
                    if os.path.exists(self.piece_images[cell]):
                        img = Image(source=self.piece_images[cell], 
                                  allow_stretch=True,
                                  keep_ratio=True)
                        b.add_widget(img)
                    else:
                        # Fallback to text if image not found
                        b.text = cell
                        b.font_size = 32
                        b.color = (0, 0, 0, 1)
                else:
                    # Use Unicode text
                    b = Button(
                        text=cell, 
                        font_size=32,
                        background_color=bg_color,
                        background_normal='',
                        color=(0, 0, 0, 1)
                    )
                
                b.row = row_idx
                b.col = col_idx
                b.bind(on_release=self.cell_pressed)
                self.buttons.append(b)
                self.grid.add_widget(b)

    def is_white_piece(self, piece):
        return piece in ['f', 'e', 'd', 'c', 'b', 'a']

    def is_black_piece(self, piece):
        return piece in ['6', '5', '4', '3', '2', '1']

    def cell_pressed(self, btn):
        row = btn.row
        col = btn.col
        
        if self.selected is None:
            piece = self.board[row][col]
            if piece != "":
                if (self.white_turn and self.is_white_piece(piece)) or \
                   (not self.white_turn and self.is_black_piece(piece)):
                    self.selected = (row, col)
                    btn.background_color = (0.3, 0.8, 0.3, 1)
                    self.status.text = f"Selected {piece} - Choose destination"
        else:
            src_row, src_col = self.selected
            piece = self.board[src_row][src_col]
            dest_piece = self.board[row][col]
            
            can_move = True
            if dest_piece != "":
                if (self.white_turn and self.is_white_piece(dest_piece)) or \
                   (not self.white_turn and self.is_black_piece(dest_piece)):
                    can_move = False
            
            if can_move:
                self.board[row][col] = piece
                self.board[src_row][src_col] = ''
                self.white_turn = not self.white_turn
                self.status.text = f"{'White' if self.white_turn else 'Black'}'s turn"
            else:
                self.status.text = "Invalid move - try again"
            
            self.selected = None
            self.draw_board()

    def reset_board(self):
        self.board = self.create_initial_board()
        self.selected = None
        self.white_turn = True
        self.status.text = "White's turn - Select a piece"
        self.draw_board()

# =====================================================
# SNAKE GAME
# =====================================================

class SnakeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = 20
        self.snake = [(10, 10)]
        self.direction = (0, 0)
        self.apple = (15, 15)
        self.score = 0
        self.game_over = False
        
        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.draw()

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.draw()

    def get_cell_size(self):
        return min(self.width, self.height) / 30

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            cell_size = self.get_cell_size()
            offset_x = self.x + (self.width - 30 * cell_size) / 2
            offset_y = self.y + (self.height - 30 * cell_size) / 2
            
            Color(0, 1, 0, 1)
            for segment in self.snake:
                Rectangle(
                    pos=(offset_x + segment[0] * cell_size, 
                         offset_y + segment[1] * cell_size),
                    size=(cell_size - 1, cell_size - 1)
                )
            
            Color(1, 0, 0, 1)
            Rectangle(
                pos=(offset_x + self.apple[0] * cell_size, 
                     offset_y + self.apple[1] * cell_size),
                size=(cell_size - 1, cell_size - 1)
            )

    def move(self):
        if self.game_over or self.direction == (0, 0):
            return
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        new_head = (new_head[0] % 30, new_head[1] % 30)
        
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.apple:
            self.score += 1
            self.apple = (random.randint(0, 29), random.randint(0, 29))
            while self.apple in self.snake:
                self.apple = (random.randint(0, 29), random.randint(0, 29))
        else:
            self.snake.pop()
        
        self.draw()

    def reset(self):
        self.snake = [(10, 10)]
        self.direction = (0, 0)
        self.apple = (15, 15)
        self.score = 0
        self.game_over = False
        self.draw()


class SnakeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        root = BoxLayout(orientation='vertical', spacing=8, padding=12)
        
        with root.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_rect, size=self._update_rect)

        self.status = Label(
            text="Score: 0 | Use Arrow Keys", 
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1),
            font_size=20
        )
        root.add_widget(self.status)

        self.snake_widget = SnakeWidget(size_hint=(1, 0.75))
        root.add_widget(self.snake_widget)

        ctrl = BoxLayout(size_hint=(1, 0.15), spacing=8)
        reset = Button(
            text="Reset",
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        reset.bind(on_release=lambda x: self.reset_game())
        back = Button(
            text="← Back",
            background_color=(0.6, 0.2, 0.2, 1),
            background_normal=''
        )
        back.bind(on_release=self.go_back)
        ctrl.add_widget(reset)
        ctrl.add_widget(back)
        root.add_widget(ctrl)

        self.add_widget(root)
        
        self.game_event = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        dx, dy = self.snake_widget.direction
        
        if key == 'up' and dy == 0:
            self.snake_widget.direction = (0, 1)
        elif key == 'down' and dy == 0:
            self.snake_widget.direction = (0, -1)
        elif key == 'left' and dx == 0:
            self.snake_widget.direction = (-1, 0)
        elif key == 'right' and dx == 0:
            self.snake_widget.direction = (1, 0)
        
        return True

    def on_enter(self):
        if self.game_event:
            self.game_event.cancel()
        self.game_event = Clock.schedule_interval(self.update_game, 0.15)

    def on_leave(self):
        if self.game_event:
            self.game_event.cancel()
            self.game_event = None

    def update_game(self, dt):
        self.snake_widget.move()
        if self.snake_widget.game_over:
            self.status.text = f"Game Over! Final Score: {self.snake_widget.score}"
            if self.game_event:
                self.game_event.cancel()
        else:
            self.status.text = f"Score: {self.snake_widget.score} | Use Arrow Keys"

    def reset_game(self):
        self.snake_widget.reset()
        self.status.text = "Score: 0 | Use Arrow Keys"
        if self.game_event:
            self.game_event.cancel()
        self.game_event = Clock.schedule_interval(self.update_game, 0.15)

    def go_back(self, instance):
        if self.game_event:
            self.game_event.cancel()
            self.game_event = None
        self.manager.current = 'dashboard'

# =====================================================
# DASHBOARD
# =====================================================

Builder.load_string('''
<Dashboard>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.2, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: 'Gaming Platform'
            font_size: '32sp'
            size_hint: (1, 0.15)
            color: 1, 1, 1, 1
            bold: True
        
        Label:
            text: 'Choose Your Game'
            font_size: '18sp'
            size_hint: (1, 0.1)
            color: 0.8, 0.8, 1, 1
        
        GridLayout:
            cols: 1
            spacing: 10
            size_hint: (1, 0.75)
            
            Button:
                text: 'Tic Tac Toe'
                font_size: '24sp'
                background_color: 0.2, 0.6, 0.8, 1
                on_release: root.manager.current = 'tic_tac_toe'
            
            Button:
                text: 'Chess'
                font_size: '24sp'
                background_color: 0.8, 0.6, 0.2, 1
                on_release: root.manager.current = 'chess'
            
            Button:
                text: 'Snake Game'
                font_size: '24sp'
                background_color: 0.2, 0.8, 0.4, 1
                on_release: root.manager.current = 'snake'
''')

class Dashboard(Screen):
    pass

class GameManager(ScreenManager):
    pass

# =====================================================
# MAIN APPLICATION
# =====================================================

class MiniGamesApp(App):
    def build(self):
        sm = GameManager()
        sm.add_widget(Dashboard(name="dashboard"))
        sm.add_widget(TicTacToeScreen(name="tic_tac_toe"))
        sm.add_widget(ChessScreen(name="chess"))
        sm.add_widget(SnakeScreen(name="snake"))
        return sm

if __name__ == "__main__":
    MiniGamesApp().run()