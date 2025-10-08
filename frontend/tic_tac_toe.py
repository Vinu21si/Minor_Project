# tic_tac_toe.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

BACKEND = "http://127.0.0.1:5000"

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = [""]*9
        self.current = "X"  # human is X, server AI is O

        root = BoxLayout(orientation='vertical', spacing=8, padding=12)
        self.status = Label(text="Your turn (X)", size_hint=(1,0.1), font_size=20)
        root.add_widget(self.status)

        grid = GridLayout(cols=3, spacing=4, size_hint=(1,0.75))
        self.buttons = []
        for i in range(9):
            b = Button(text="", font_size=32)
            b.bind(on_release=lambda inst, idx=i: self.on_click(idx))
            self.buttons.append(b)
            grid.add_widget(b)
        root.add_widget(grid)

        ctrl = BoxLayout(size_hint=(1,0.15), spacing=8)
        reset = Button(text="Reset")
        reset.bind(on_release=lambda x: self.reset())
        back = Button(text="⬅ Back")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        ctrl.add_widget(reset)
        ctrl.add_widget(back)
        root.add_widget(ctrl)

        self.add_widget(root)

    def on_click(self, idx):
        if self.board[idx] != "":
            return
        self.board[idx] = "X"
        self.buttons[idx].text = "X"

        # Check if someone already won locally
        resp = requests.post(BACKEND + "/tictactoe/ai_move", json={"board": self.board})
        if resp.status_code != 200:
            self.status.text = "Server error"
            return
        data = resp.json()
        if data.get("winner"):
            self.status.text = f"Game over: {data.get('winner')}"
            return
        ai_index = data.get("ai_index")
        if ai_index is None:
            self.status.text = "Draw"
            return
        self.board[ai_index] = "O"
        self.buttons[ai_index].text = "O"

        # update status
        self.status.text = "Your turn (X)"

    def reset(self):
        self.board = [""]*9
        for b in self.buttons:
            b.text = ""
        self.status.text = "Your turn (X)"
