from random import randint, triangular
from math import floor

def roll(dice):
    """Takes arguments in the format "{#}d{#}", e.g. 2d6 returns the total"""
    try:
        num, die = dice.split('d')
        total = 0
        for i in range(0,int(num)):
            roll = randint(1,int(die))
            total += roll
        return total
    except Exception as e:
        print("Error: " + str(e))
        return "Something went wrong! Check your input."

def tri_int(low, high, mode):
    """Returns an integer in a triangular distribution."""
    return floor(triangular(low, high, mode))

def tri_sample(population, k, mode=0):
    """
    Mimics the functionality of random.sample() but with a triangular
    distribution over the length of the sequence.

    Mode defaults to 0, which favors lower indices.
    """
    psize = len(population)
    if k > psize:
        raise ValueError("k must be less than the number of items in population.")
    if mode > psize:
        raise ValueError("mode must be less than the number of items in population.")
    indices_chosen = []
    sample = []
    for i in range(k):
        while True:
            choice = tri_int(0, psize, mode)
            if choice not in indices_chosen:
                break
        indices_chosen.append(choice)
        sample.append(population[choice])
    return sample