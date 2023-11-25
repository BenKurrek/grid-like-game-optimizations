from itertools import product

def check_conditions(combo):
    # Count occurrences of "X" and "O"
    count_x = combo.count("X")
    count_o = combo.count("O")

    # Check conditions for X and O
    x_conditions = [
        not (combo[0] == combo[1] == combo[2] == "X"),
        not (combo[3] == combo[4] == combo[5] == "X"),
        not (combo[6] == combo[7] == combo[8] == "X"),
        not (combo[0] == combo[3] == combo[6] == "X"),
        not (combo[1] == combo[4] == combo[7] == "X"),
        not (combo[2] == combo[5] == combo[8] == "X"),
        not (combo[0] == combo[4] == combo[8] == "X"),
        not (combo[2] == combo[4] == combo[6] == "X"),
    ]

    o_conditions = [
        not (combo[0] == combo[1] == combo[2] == "O"),
        not (combo[3] == combo[4] == combo[5] == "O"),
        not (combo[6] == combo[7] == combo[8] == "O"),
        not (combo[0] == combo[3] == combo[6] == "O"),
        not (combo[1] == combo[4] == combo[7] == "O"),
        not (combo[2] == combo[5] == combo[8] == "O"),
        not (combo[0] == combo[4] == combo[8] == "O"),
        not (combo[2] == combo[4] == combo[6] == "O"),
    ]

    # Number of X and O equal, so that X is next move
    return all(x_conditions) and all(o_conditions) and count_x == count_o

# Define the possible values for each space
options = [" ", "X", "O"]

# Generate all combinations
combinations = list(product(options, repeat=9))

# Filter combinations based on conditions
filtered_combinations = [combo for combo in combinations if check_conditions(combo)]

# Print debug information
print(f"Total combinations: {len(combinations)}")
print(f"Filtered combinations: {len(filtered_combinations)}")

# Write filtered combinations to a text file with comma as delimiter
with open("./src/utility/ttt_all_incomplete_board_states.csv", "w") as file:
    for combo in filtered_combinations:
        file.write(",".join(combo) + "\n")

print("Filtered combinations have been written to ./src/utility/ttt_all_incomplete_board_states.csv")