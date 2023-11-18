def create_base_game(game_name, game_meta): 
    if game_name == "chess":
        from src.game.chess.chess_game import ChessGame
        from src.game.base_game import BaseGame
        game = ChessGame(game_meta)
        return BaseGame(game) # Pass the game_name argument
    # elif self.game_name == "othello":
    #     self.game = Othello()  # Replace with actual Othello initialization
    # elif self.game_name == "go":
    #     self.game = Go()  # Replace with actual Go initialization
    else:
        raise ValueError("Invalid game name. Supported options: chess, othello, go")