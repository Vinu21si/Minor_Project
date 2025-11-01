# chess_game.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class ChessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = self.create_initial_board()
        self.selected = None
        self.white_turn = True

        root = BoxLayout(orientation='vertical', spacing=6, padding=8)
        
        # Add background
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
            ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        ]

    def draw_board(self):
        self.grid.clear_widgets()
        self.buttons = []
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                is_light = (row_idx + col_idx) % 2 == 0
                bg_color = (0.9, 0.8, 0.6, 1) if is_light else (0.6, 0.4, 0.2, 1)
                
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
        return piece in ['♔', '♕', '♖', '♗', '♘', '♙']

    def is_black_piece(self, piece):
        return piece in ['♚', '♛', '♜', '♝', '♞', '♟']

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
            
            # Simple validation: can't capture your own piece
            can_move = True
            if dest_piece != "":
                if (self.white_turn and self.is_white_piece(dest_piece)) or \
                   (not self.white_turn and self.is_black_piece(dest_piece)):
                    can_move = False
            
            if can_move:
                # Make the move
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