import pandas as pd

user_info = pd.read_csv("user_details.csv")
# this is getting the level column specifically
player_level = user_info["level"]
# this is getting the experience column specifically
player_xp = user_info["experience"]

xp_per_level = 100

# if they are max level already then they won't be able to level up
if player_level >= 100:
  print("You are at max level.")
else:
  # this will see if they need to level up after reaching the level requirements for a level
  while player_xp >= xp_per_level:
    # adding one to their level
    player_level += 1
    # taking away their xp so its back to 0
    player_xp -= xp_per_level
    # this will increase each level. level 1 will need 100xp, level 2 will need 200xp etc.
    xp_per_level += 100
    print("You have levelled up! You are now level", player_level)
    if player_level == 100:
      print("You have reached max level!")
      break





# leave this here for now
def row_to_dict(row):
    monster_dict = {
        'Name': row['Name'],
        'HP': row['HP'],
        'Attack': row['Attack'],
        'Defence': row['Defence'],
        'Magic Attack': row['Magic Attack'],
        'Magic Defence': row['Magic Defence']
    }
    return monster_dict

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('monsters.csv')

# Apply the row_to_dict function to each row in the DataFrame
monster_dicts = df.apply(row_to_dict, axis=1).tolist()

# Print the list of dictionaries
#print(monster_dicts[0])

def monster_exp():
  import pandas as pd 
  monster = pd.read_csv("monsters.csv")
  exp_gained = monster["HP"] * 4