from random import randint

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