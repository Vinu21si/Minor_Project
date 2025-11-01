# tic_tac_toe.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from tictactoe_engine import minimax, check_winner

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = [""]*9
        self.current = "X"  # human is X, AI is O
        self.game_over = False

        root = BoxLayout(orientation='vertical', spacing=8, padding=12)
        
        # Add background
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
        
        # Player's move
        self.board[idx] = "X"
        self.buttons[idx].text = "X"
        self.buttons[idx].color = (0.3, 0.6, 1, 1)

        # Check if player won
        winner = check_winner(self.board)
        if winner:
            self.status.text = f"Game over: {winner} wins!" if winner != "draw" else "Draw!"
            self.game_over = True
            return

        # AI's turn
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

            # Check if AI won
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