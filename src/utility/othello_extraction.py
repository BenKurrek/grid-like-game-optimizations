import csv
import random

from src.game.othello.othello_game import OthelloGame

data_file = "./src/utility/othello_world_championship_2022.csv"
train_data = []
test_data = []


def initialize_train_test_data(train_ratio=0.6, randomize=True) -> None:
    """
    Initializes the train and test data for Othello.

    :param train_ratio: Ratio of training positions to test positions.
    :param randomize: If True, the positions are shuffled.
    """
    with open(data_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        raw_data = []  # Each row in the CSV file
        for row in reader:
            raw_data.append(row)
    raw_data = raw_data[1:]  # Remove header row

    board_data: dict[str, str] = {}
    for row in raw_data:
        _, _, _, move = row
        for i in range(len(move) // 2 - 1):
            board_tmp = OthelloGame(move[: 2 * i + 2])
            board_str = str(board_tmp)
            if board_str not in board_data:
                board_data[board_str] = move[: 2 * i + 2]

    board_moves = list(board_data.values())
    if randomize:
        random.shuffle(board_moves)

    split = int(len(board_data) * train_ratio)
    train_data.extend(board_moves[:split])
    test_data.extend(board_moves[split:])
    return


def extract_random_othello_positions(
    num_positions=1, dataset="train", randomize=True, train_ratio=0.6
) -> list[str]:
    """
    Extracts random Othello positions from the dataset.
    Note: The dataset is only loaded once and then cached. `randomize` and
    `train_ratio` are only used the first time this function is called.

    :param num_positions: Number of random positions to extract.
    :param dataset: Dataset to extract from. Either "train" or "test".
    :param randomize: If True, the positions are shuffled.
    :param train_ratio: Ratio of training positions to test positions.
    """
    if not train_data:
        initialize_train_test_data(train_ratio=train_ratio, randomize=randomize)
    if dataset == "train":
        return random.choices(train_data, k=num_positions)
    else:
        return random.choices(test_data, k=num_positions)
