import csv
import random

from src.game.othello.othello_game import OthelloGame

def extract_random_othello_positions(num_positions=1):
    with open('./src/utility/othello_world_championship_2022.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
    data = data[1:]  # Remove header row
    metadata = []    
    for i in range(num_positions):
        _, _, _, board_data = random.choice(data)
        num_moves = len(board_data)//2
        move_index = random.randint(0, num_moves-1)
        metadata.append(board_data[0:move_index*2+2])
    return metadata