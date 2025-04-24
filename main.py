import tkinter as tk
import os
from gui import TicTacToeGUI

def create_assets_directory():
    """Create assets directory and sample sound files if they don't exist."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

def main():
    """Main function to run the Tic-Tac-Toe game."""
    create_assets_directory()
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()