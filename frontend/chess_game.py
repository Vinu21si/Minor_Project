# chess_game.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

BACKEND = "http://127.0.0.1:5000"

class ChessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.selected = None

        root = BoxLayout(orientation='vertical', spacing=6, padding=8)
        self.status = Label(text="Select a piece to move", size_hint=(1,0.08))
        root.add_widget(self.status)

        self.grid = GridLayout(cols=8, spacing=2, size_hint=(1,0.84))
        self.buttons = []
        self.draw_board()
        root.add_widget(self.grid)

        ctrl = BoxLayout(size_hint=(1,0.08), spacing=6)
        back = Button(text="⬅ Back")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        reset = Button(text="Reset Board")
        reset.bind(on_release=lambda x: self.reset_board())
        ctrl.add_widget(reset)
        ctrl.add_widget(back)
        root.add_widget(ctrl)
        self.add_widget(root)

    def draw_board(self):
        # Fetch pieces from fen and show unicode or images
        self.grid.clear_widgets()
        board_matrix = self.fen_to_matrix(self.fen)
        for r in board_matrix:
            for cell in r:
                b = Button(text=cell, font_size=24)
                b.bind(on_release=lambda inst, text=cell, btn=b: self.cell_pressed(btn))
                self.grid.add_widget(b)

    def fen_to_matrix(self, fen):
        piece_map = {
            'r':'♜','n':'♞','b':'♝','q':'♛','k':'♚','p':'♟',
            'R':'♖','N':'♘','B':'♗','Q':'♕','K':'♔','P':'♙'
        }
        parts = fen.split()
        rows = parts[0].split('/')
        matrix = []
        for row in rows:
            mat_row = []
            for ch in row:
                if ch.isdigit():
                    mat_row.extend([""]*int(ch))
                else:
                    mat_row.append(piece_map.get(ch, ch))
            matrix.append(mat_row)
        return matrix

    def cell_pressed(self, btn):
        idx = list(self.grid.children).index(btn)
        # convert idx to row,col:
        # grid.children is reversed; handle by computing positions
        total = len(self.grid.children)
        pos = total - 1 - idx
        row = pos // 8
        col = pos % 8
        if self.selected is None:
            # select if piece present
            board_matrix = self.fen_to_matrix(self.fen)
            if board_matrix[row][col] != "":
                self.selected = (row, col)
                self.status.text = f"Selected {board_matrix[row][col]} at {row},{col}"
        else:
            src_row, src_col = self.selected
            # convert coordinates to UCI: rows 0..7 -> ranks 8..1, files a..h
            def to_sq(r,c):
                file = chr(ord('a') + c)
                rank = 8 - r
                return f"{file}{rank}"
            uci = to_sq(src_row, src_col) + to_sq(row, col)
            # Ask backend if move is legal and apply
            resp = requests.post(BACKEND + "/chess/apply_move", json={"fen": self.fen, "move": uci})
            if resp.status_code == 200:
                self.fen = resp.json().get("fen")
                self.draw_board()
                # notify backend move count if you want:
                requests.get(BACKEND + "/scores")  # optional
            else:
                self.status.text = "Illegal move or server error"
            self.selected = None
