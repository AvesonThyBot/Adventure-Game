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