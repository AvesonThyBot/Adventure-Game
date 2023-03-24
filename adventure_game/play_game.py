import pandas as pd, random, time

equipment = pd.read_csv('adventure_game/data/equipments.csv')
u_details_df = pd.read_csv('adventure_game/data/user_details.csv')
#print(equipment.Class.loc[equipment['Class'].str.contains("Archer")])
#randomised_attack = ( attack * 10)

spacing = "---------"


#working on it under
def login_menu_choice():
  from adventure_game.login import login_menu


def login_stats():
  from adventure_game.login.login import username, password
  data = pd.read_csv('user_details.csv')
  user_data = data[(data['username'] == username)
                   & (data['password'] == password)]
  global user_stats
  user_stats = user_data.copy()
  return user_stats


def create_stats():
  from adventure_game.login.create_account import username, password
  username_val = username
  password_val = password
  data = pd.read_csv('user_details.csv')
  user_data = data[(data['username'] == username_val)
                   & (data['password'] == password_val)]
  global user_stats
  user_stats = user_data.copy()
  return user_stats


menu_choice = login_menu_choice().choice
if menu_choice == 1:
  stats = login_stats()
elif menu_choice == 2:
  stats = create_stats()


def profession():

  while True:
    profession_choice = input(
      f"Magician\n{spacing}\nArcher\n{spacing}\nKnight\n{spacing}\nEnter your choice: "
    ).strip()

    login_info = create_stats() or login_stats()

    if profession_choice in ['1', "Magician", "one", "magician"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details_df.append(new_user, ignore_index=True)
      merged_df.to_csv("u_details", index=False)
      #global Class = profession_choice

    elif profession_choice in ['2', "Archer", "two", "archer"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details_df.append(new_user, ignore_index=True)
      merged_df.to_csv("u_details", index=False)
      break
    elif profession_choice in ['3', "Knight", "three", "knight"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details_df.append(new_user, ignore_index=True)
      merged_df.to_csv("u_details", index=False)
      break
    else:
      print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
      continue


def return_menu():
  #leave this for now (needs to be changed for this part of code)
  while True:
    from adventure_game.login import login_menu
    choice = login_menu()
    if choice is None:
      continue
    choice = int(choice)
    if choice == 3:
      menu()
    elif choice in (1, 2):
      break
    else:
      continue


def random_row_index(Class, level):
  filtered_equipment = equipment[(equipment['Class'] == Class)
                                 & (equipment['Level'] == level)]
  num_rows = len(filtered_equipment)
  random_row = random.randint(0, num_rows - 1)
  selected_row = filtered_equipment.iloc[random_row]
  selected_row_2 = random_row_index(Class, Level)
  inventory_list = u_details_df['inventory'].tolist()

  print(selected_row)


def chest_roomT():
  print("T")
  print("You have entered the chest room")
  print("You open the chest")
  r_open = random.randint(0, 3)
  if r_open == 1:
    random_row_index()


def game():
  print("Welcome To W")
  print(
    "we will first be putting you through a tutorial"
  )  #better if we force them into a certain room order, empty -> chest -> fight
  user_choice = input("Please choose between the 3 rooms , 1,2,3")
  if user_choice == "1":
    chest_roomT()
  #elif user_choice == "2":
  #monster_roomT()
  #else :
  #empty_room()


profession()

# import pandas as pd
# import random

# def random_row_index(Class, level):
#     equipment = pd.read_csv("equipment.csv")
#     filtered_equipment = equipment[(equipment['Class'] == Class) & (equipment['Level'] == level)]
#     num_rows = len(filtered_equipment)
#     random_row = random.randint(0, num_rows-1)
#     selected_row = filtered_equipment.iloc[random_row]
#     return selected_row

# # Read the existing CSV file with the 'inventory' column
# inventory_df = pd.read_csv("inventory.csv")

# # Get the random row based on Class and level
# selected_row = random_row_index("Class_Name", level_number)

# # Append the selected row value to the inventory list
# inventory_list = inventory_df['inventory'].tolist()
# inventory_list.append(selected_row.to_dict())

# # Update the 'inventory' column with the new list
# inventory_df['inventory'] = inventory_list

# # Save the updated DataFrame to the CSV file
# inventory_df.to_csv("inventory.csv", index=False)
