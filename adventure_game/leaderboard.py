# -------------------- Imports and read_csv --------------------
import pandas as pd, random, time
equipment = pd.read_csv('adventure_game/data/equipments.csv')
u_details = pd.read_csv('adventure_game/data/user_details.csv')
spacing = "---------"
# --------------------  Loads data --------------------
from adventure_game.login import login_data
global username,password
username,password = login_data()
user_data = u_details[(u_details['username'] == username) & (u_details['password'] == password)]
# -------------------- All functions under --------------------
leaderboard_choice = input("Which profession would you like to view the high score for?\n1.Archer\n2.Magician\n3.Knight")
leaderboard = pd.read_csv("adventure_game/data/user_details.csv")
leaderboard = leaderboard.sort_values(by='levels')
leaderboard = leaderboard.head(10)
print(leaderboard)