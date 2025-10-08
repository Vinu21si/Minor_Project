# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from tic_tac_toe import TicTacToeScreen
from chess_game import ChessScreen

Builder.load_file("dashboard.kv")

class Dashboard(Screen):
    pass

class GameManager(ScreenManager):
    pass

class MiniGamesApp(App):
    def build(self):
        sm = GameManager()
        sm.add_widget(Dashboard(name="dashboard"))
        sm.add_widget(TicTacToeScreen(name="tic_tac_toe"))
        sm.add_widget(ChessScreen(name="chess"))
        return sm

if __name__ == "__main__":
    MiniGamesApp().run()
