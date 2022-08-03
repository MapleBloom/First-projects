"""          Guess number game.
Computer pick a number and guess it by itself.
"""

import numpy as np


def guess(number:int, a:int, b:int, count:int=1)-> int:
    """Algorithm culculates number

    Args:
        number (int): number to guess
        a (int): lower border of interval to consider
        b (int): upper border of interval to consider inclusive
        count (int, optional): counter of iterations. Defaults to 1.

    Returns:
        int: number of iterations
    """
    prediction = int((a + b) / 2)   # makes prediction at the center of the interval
    return count if prediction == number else \
           guess(number, *(a, prediction) if prediction > number else (prediction, b), count + 1)
    

def score_game(guess, min_n:int=1, max_n:int=100, games_number:int=1000)-> list[int]:
    """Receive number of iterations in every game with random int and summarise it

    Args:
        guess (_type_): function to guess
        min_n (int, optional): lower border of interval to consider. Defaults to 1.
        max_n (int, optional): upper border of interval to consider inclusive. Defaults to 100.
        games_number (int, optional): number of games to call. Defaults to 1000.

    Returns:
        list[int]: mean number of iterations, maximum number of iterations
    """
    count_it = [''] * games_number  # list of iterations in every game
    np.random.seed(1)
     
    for i in range(games_number):   # start the game games_number times with random number
        count_it[i] = guess(np.random.randint(min_n, max_n + 1), min_n, max_n + 1)
    score_max = int(max(count_it))
    score_mean = int(np.mean(count_it))
    
    print(f'Your algorithm needs about {score_mean} iterations, maximum {score_max} iterations,')
    print(f'to guess the number in {min_n} to {max_n} interval.')
    print(f'Checked at {games_number} games \n\n')
    return score_mean, score_max


if __name__ == '__main__':
   # RUN
    score_game(guess, min_n=1, max_n=100, games_number=1000)
