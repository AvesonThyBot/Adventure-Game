import pandas as pd, time

print("3")

leaderboard = pd.read_csv("adventure_game/data/user_details.csv")
leaderboard = leaderboard.sort_values(by='levels')
leaderboard = leaderboard.head(10)
print(leaderboard)
