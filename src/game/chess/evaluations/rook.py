import chess
import random
from chess import Square, Piece

rook_weight_labels = [
    "Rook Material Weight",
    "Rook Attacking Weight",
    "Rook Defending Weight",
    "Rook number of free spaces",
    "7th Rank Rook Weight",
    "Open File Rook Weight",
    "Semi-Open File Rook Weight",
    "Closed File Rook Weight",
    "Connected Rook Weight",
]
rook_weight_bounds = [
    (400, 600), # how much the rook is worth
    (0, 1000), # how much rooks that attack the enemy king are worth
    (0, 1000), # how much rooks that defend your king are worth
    (0, 1000), # how much the mobility of rook is worth
    (0, 1000), # how much rooks on the 7th rank are worth
    (0, 1000), # how much rooks on open files are worth
    (0, 1000), # how much rooks on semi-open files are worth
    (0, 1000), # how much rooks on closed files are penalized
    (0, 1000), # how much connected rooks are worth
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class RookEvaluator:    
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(rook_weight_bounds))]
        self.board = board
        
        self.adjacent_white_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.WHITE)))]
        self.adjacent_black_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.BLACK)))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece, attack_squares):
        if piece.piece_type == chess.ROOK:
            open_file, semi_open_file, closed_file = self.check_file_data(square, piece)
            is_connected = self.is_rook_connected(attack_squares)

            self.material_evaluation(piece)
            self.king_attacking_defending_evalutation(attack_squares, square, piece)
            self.free_squares_evaluation(attack_squares, piece)

            # Check for rooks on the seventh rank
            rank = chess.square_rank(square) + 1
            if piece.color == chess.WHITE and rank == 7:
                self.rook_on_seventh_evaluation(piece)
            if piece.color == chess.BLACK and rank == 2:
                self.rook_on_seventh_evaluation(piece)

            if open_file:
                self.open_file_evaluation(piece)
            
            if semi_open_file:
                self.semi_open_file_evaluation(piece)

            if closed_file:
                self.closed_file_evaluation(piece)

            if is_connected:
                self.connected_rooks_evaluation(piece)
                
    def material_evaluation(self, piece):
        rook_material_idx = 0
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[rook_material_idx][color_idx] += 1
            
    def king_attacking_defending_evalutation(self, rook_attack_squares: list[str], square: chess.Square, piece: chess.Piece):
        attacking_pawn_idx = 1
        defending_pawn_idx = 2
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
    
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        # TODO correct color calculations
        for rook_attack_square in rook_attack_squares:
            # Attacking
            if rook_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_pawn_idx][color_idx] += 1
            
            # Defending   
            if rook_attack_square in defending_king_squares:
                self.scores_for_weights[defending_pawn_idx][color_idx] += 1
                
    def free_squares_evaluation(self, rook_attack_squares, piece: chess.Piece):
        free_square_idx = 3
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[free_square_idx][color_idx] += len(rook_attack_squares)
        
    def rook_on_seventh_evaluation(self, piece: chess.Piece):
        rook_on_seventh_idx = 4
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[rook_on_seventh_idx][color_idx] += 1

    def open_file_evaluation(self, piece: chess.Piece):
        open_file_idx = 5
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[open_file_idx][color_idx] += 1
    
    def semi_open_file_evaluation(self, piece: chess.Piece):
        semi_open_file_idx = 6
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[semi_open_file_idx][color_idx] += 1

    def closed_file_evaluation(self, piece: chess.Piece):
        closed_file_idx = 7
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[closed_file_idx][color_idx] -= 1

    def connected_rooks_evaluation(self, piece: chess.Piece):
        connected_rook_idx = 8
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[connected_rook_idx][color_idx] += 1


    # UTILITY
    def check_file_data(self, square, piece):
        # Assume no pawns on the file
        open_file = True
        semi_open_file = True
        closed_file = False 

        ally_pawn_seen = False
        enemy_pawn_seen = False
        
        file = chess.square_file(square)
        # go through other squares in the same file
        for rank in range(8):
            cur_file_square = chess.square(file, rank)
            cur_file_piece = self.board.piece_at(int(cur_file_square))

            # If there is a pawn of any color
            if cur_file_piece is not None and cur_file_piece.piece_type == chess.PAWN:
                open_file = False

                # If there is a pawn of the same color we're no longer on a semi-open file
                if cur_file_piece.color == piece.color:
                    semi_open_file = False
                    ally_pawn_seen = True
                else:
                    enemy_pawn_seen = True

                # If we've seen both an ally and enemy pawn we're on a closed file
                if ally_pawn_seen and enemy_pawn_seen:
                    closed_file = True

        return open_file, semi_open_file, closed_file


    def is_rook_connected(self, attack_squares: list[str]):
        for square in attack_squares:
            piece_at_square = self.board.piece_at(square)

            # Check if there is another rook of the same color in the attacked squares
            if piece_at_square and piece_at_square.piece_type == chess.ROOK and piece_at_square.color == rook.color:
                return True

        return False