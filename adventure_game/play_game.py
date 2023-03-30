import pandas as pd, random, time

equipment = pd.read_csv('adventure_game/data/equipments.csv')
u_details = pd.read_csv('adventure_game/data/user_details.csv')
#print(equipment.Class.loc[equipment['Class'].str.contains("Archer")])
#randomised_attack = ( attack * 10)

spacing = "---------"

#loads data
from adventure_game.login import login_data
username,password = login_data()
user_data = u_details[(u_details['username'] == username) & (u_details['password'] == password)]



def profession():

  while True:
    profession_choice = input(
      f"Magician\n{spacing}\nArcher\n{spacing}\nKnight\n{spacing}\nEnter your choice: "
    ).strip()

    # line to fetch their info

    if profession_choice in ['1', "Magician", "one", "magician"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details.append(new_user, ignore_index=True)
      merged_df.to_csv("u_details", index=False)
      #global Class = profession_choice

    elif profession_choice in ['2', "Archer", "two", "archer"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details.append(new_user, ignore_index=True)
      merged_df.to_csv("u_details", index=False)
      break
    elif profession_choice in ['3', "Knight", "three", "knight"]:
      new_user = pd.DataFrame({'profession': [profession_choice]})
      merged_df = u_details.append(new_user, ignore_index=True)
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
    level = int(level)
    equipment = pd.read_csv('equipments.csv')
    u_details = pd.read_csv('user_details.csv')

    filtered_equipment = equipment[(equipment['Class'] == Class) & (equipment['Level'] == level)]
    num_rows = len(filtered_equipment)

    # Base condition
    if num_rows == 0:
        return None

    random_row = random.randint(0, num_rows - 1)
    selected_row = equipment.iloc[random_row]

    # Append the name of the selected equipment to the CSV file
    name = selected_row['Name']

    # Get the current inventory list for the user
    inventory_list_str = u_details.loc[u_details['username'] == user_data, 'inventory'].tolist()[0]

    # Convert inventory_list_str to a list of equipment names
    inventory_list = [item.strip() for item in inventory_list_str.split(',')]

    # Add the selected equipment to the inventory list
    inventory_list.append(name)

    # Update the inventory list in the DataFrame
    u_details.loc[u_details['username'] == user_data, 'inventory'] = [', '.join(inventory_list)]

    # Write the updated DataFrame back to the u_details CSV file
    u_details.to_csv('user_details.csv', index=False)

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


