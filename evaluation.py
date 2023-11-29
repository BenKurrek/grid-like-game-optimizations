import json

file_path = 'evaluations.json'

# Read the JSON data from the file
with open(file_path, 'r') as json_file:
    evaluations = json.load(json_file)
    
    sum_fitness = 0
    sum_rank_score = 0 
    for evaluation in evaluations:
        fitness_score, best_move, index, num_moves = evaluation
        
        sum_fitness += fitness_score
        sum_rank_score += index/num_moves
        
    fitness_mean = sum_fitness/len(evaluations)
    rank_score_mean = sum_rank_score/len(evaluations)
    
    std_dev_fitness = 0
    std_dev_rank_score = 0
    for evaluation in evaluations:
        fitness_score, best_move, index, num_moves = evaluation
        
        std_dev_fitness += (fitness_score-fitness_mean)**2/len(evaluations)
        std_dev_rank_score += (index/num_moves-rank_score_mean)**2/len(evaluations)
        
    std_dev_fitness = std_dev_fitness**(1/2)
    std_dev_rank_score =std_dev_rank_score**(1/2) 
        
    
    print(f"Fitness mean: {fitness_mean} std dev: {std_dev_fitness}\nRank score mean: {rank_score_mean} std dev: {std_dev_rank_score}")