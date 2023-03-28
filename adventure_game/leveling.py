import pandas as pd

user_info = pd.read_csv("user_details.csv")
# this is getting the level column specifically
player_level = user_info["level"]
player_xp = user_info["experience"]

# if they are max level already then they won't be able to level up
if player_level >= 100:
  print("You are already max level")

# this is for level 1. if they get 100 xp then they level up to level 1
if player_xp > 100:
  # adding one onto the csv file so that is saves their level (although it may be incorrect as it as right now)
  player_level + 1
  # telling them their level
  print("You have levelled up! You are now level ", player_level)
