import pandas as pd, time

#variable
spacing = "---------"

print("3")

leaderboard_choice = input("Which profession would you like to view the high score for?\n1.Archer\n2.Magician\n3.Knight")
leaderboard = pd.read_csv("adventure_game/data/user_details.csv")
leaderboard = leaderboard.sort_values(by='levels')
leaderboard = leaderboard.head(10)
print(leaderboard)
