import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
from game_logic import TicTacToe
from ai_player import AIPlayer

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        pygame.mixer.init()

        self.game = TicTacToe()
        self.ai = None
        self.is_vs_ai = tk.BooleanVar(value=False)
        self.ai_difficulty = tk.StringVar(value="easy")
        self.current_theme = tk.StringVar(value="light")

        self.auto_restart = tk.BooleanVar(value=True)

        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "board_bg": "#ffffff",
                "button_bg": "#e0e0e0",
                "x_color": "#3498db",
                "o_color": "#e74c3c",
                "text_color": "#333333",
                "line_color": "#2c3e50"
            },
            "dark": {
                "bg": "#2c3e50",
                "board_bg": "#34495e",
                "button_bg": "#2c3e50",
                "x_color": "#3498db",
                "o_color": "#e74c3c",
                "text_color": "#ecf0f1",
                "line_color": "#ecf0f1"
            },
            "pastel": {
                "bg": "#D7BDE2",
                "board_bg": "#F5EEF8",
                "button_bg": "#D7BDE2",
                "x_color": "#85C1E9",
                "o_color": "#F8C471",
                "text_color": "#5D6D7E",
                "line_color": "#5D6D7E"
            }
        }

        self.scores = {"X": 0, "O": 0, "Draw": 0}

        self.sounds = {
            "click": None,
            "win": None,
            "draw": None
        }

        self._create_widgets()
        self._load_sounds()
        self.apply_theme()

    def _load_sounds(self):
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        sound_files = {
            "click": os.path.join(assets_dir, "click.wav"),
            "win": os.path.join(assets_dir, "win.wav"),
            "draw": os.path.join(assets_dir, "draw.wav")
        }

        for sound_name, file_path in sound_files.items():
            if os.path.exists(file_path):
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)

    def _create_widgets(self):
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.score_frame = ttk.Frame(self.root)
        self.score_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.settings_frame = ttk.Frame(self.root)
        self.settings_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Button(self.menu_frame, text="New Game", command=self.reset_game).pack(side=tk.LEFT, padx=5)

        self.score_labels = {}
        for player in ["X", "O", "Draw"]:
            frame = ttk.Frame(self.score_frame)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

            ttk.Label(frame, text=f"Player {player}:").pack(side=tk.LEFT, padx=5)
            self.score_labels[player] = ttk.Label(frame, text="0")
            self.score_labels[player].pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.game_frame, width=300, height=300, highlightthickness=0)
        self.canvas.pack(expand=True)

        ttk.Label(self.settings_frame, text="Game Mode:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.settings_frame, text="Player vs Player", variable=self.is_vs_ai, value=False, 
                    command=self.update_game_mode).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.settings_frame, text="Player vs AI", variable=self.is_vs_ai, value=True,
                    command=self.update_game_mode).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.settings_frame, text="AI Difficulty:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.settings_frame, text="Easy", variable=self.ai_difficulty, value="easy",
                    command=self.update_ai_difficulty).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.settings_frame, text="Hard", variable=self.ai_difficulty, value="hard",
                    command=self.update_ai_difficulty).grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.settings_frame, text="Theme:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        theme_combobox = ttk.Combobox(self.settings_frame, textvariable=self.current_theme, 
                                  values=list(self.themes.keys()), state="readonly")
        theme_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        theme_combobox.bind("<<ComboboxSelected>>", lambda e: self.apply_theme())

        ttk.Checkbutton(self.settings_frame, text="Auto-restart game after finish", 
                     variable=self.auto_restart).grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()
        self.update_ai_difficulty()

    def update_game_mode(self):
        """Update game mode based on player selection."""
        self.reset_game()

    def update_ai_difficulty(self):
        """Update AI difficulty based on player selection."""
        self.ai = AIPlayer(difficulty=self.ai_difficulty.get())

    def apply_theme(self):
        """Apply the selected theme to the game."""
        theme = self.themes[self.current_theme.get()]

        self.root.configure(bg=theme["bg"])
        for frame in [self.menu_frame, self.score_frame, self.game_frame, self.settings_frame]:
            try :
                frame.configure(style='TFrame')
            except :
                pass

        self.draw_board()

    def draw_board(self):
        """Draw the game board with current theme."""
        theme = self.themes[self.current_theme.get()]
        self.canvas.delete("all")
        self.canvas.configure(bg=theme["board_bg"])

        for i in range(1, 3):
            self.canvas.create_line(
                i * 100, 0, i * 100, 300,
                fill=theme["line_color"], width=2
            )
            self.canvas.create_line(
                0, i * 100, 300, i * 100,
                fill=theme["line_color"], width=2
            )

        for row in range(3):
            for col in range(3):
                x = col * 100 + 50
                y = row * 100 + 50

                if self.game.board[row][col] == 'X':
                    self.draw_x(x, y, theme["x_color"])
                elif self.game.board[row][col] == 'O':
                    self.draw_o(x, y, theme["o_color"])

        self.root.title(f"Tic-Tac-Toe - Player {self.game.current_player}'s Turn")

    def draw_x(self, x, y, color):
        """Draw an X symbol at the specified position."""
        offset = 30
        self.canvas.create_line(
            x - offset, y - offset, x + offset, y + offset,
            fill=color, width=3, capstyle=tk.ROUND
        )
        self.canvas.create_line(
            x - offset, y + offset, x + offset, y - offset,
            fill=color, width=3, capstyle=tk.ROUND
        )

    def draw_o(self, x, y, color):
        """Draw an O symbol at the specified position."""
        offset = 30
        self.canvas.create_oval(
            x - offset, y - offset, x + offset, y + offset,
            outline=color, width=3
        )

    def handle_click(self, event):
        """Handle mouse click events on the game board."""
        if self.game.game_over:
            return
        
        col = event.x // 100
        row = event.y // 100

        if self.game.make_move(row, col):
            if self.sounds["click"]:
                self.sounds["click"].play()

            self.draw_board()

            if self.game.game_over:
                self.handle_game_over()

            if self.is_vs_ai.get() and self.game.current_player == 'O' and not self.game.game_over:
                self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        """Make an AI move."""
        if self.ai and not self.game.game_over:
            row, col = self.ai.make_move(self.game)
            if row is not None and col is not None:
                self.game.make_move(row, col)

                if self.sounds["click"]:
                    self.sounds["click"].play()

                self.draw_board()

                if self.game.game_over:
                    self.handle_game_over()

    def handle_game_over(self):
        """Handle game over state."""
        if self.game.winner:
            self.scores[self.game.winner] += 1
            message = f"Player {self.game.winner} wins!"

            if self.sounds["win"]:
                self.sounds["win"].play()
        else :
            self.scores["Draw"] += 1
            message = "It's a draw!"
            if self.sounds["draw"]:
                self.sounds["draw"].play()

        for player, score in self.scores.items():
            self.score_labels[player].config(text=str(score))

        self.root.title("Tic-Tac-Toe - Game Over")
        messagebox.showinfo("Game Over", message)

        if self.auto_restart.get():
            self.root.after(1000, self.reset_game)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.game.reset_game()
        self.draw_board()

        if self.is_vs_ai.get() and self.game.current_player == 'O':
            self.root.after(500, self.make_ai_move)


