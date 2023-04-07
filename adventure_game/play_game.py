import pandas as pd, random, time

equipment = pd.read_csv('adventure_game/data/equipments.csv')
u_details = pd.read_csv('adventure_game/data/user_details.csv')

spacing = "---------"

#loads data
from adventure_game.login import login_data
username,password = login_data()
user_data = u_details[(u_details['username'] == username) & (u_details['password'] == password)]

#main functions 

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


def monster_room():
  room_count = room_counter()#updates room counter
  print("monster")

def empty_room():
  room_count = room_counter()#updates room counter
  print("This room is empty!")
def chest_room():
  room_count = room_counter()#updates room counter
  print("You have entered the chest room")
  print("You open the chest")
  r_open = random.randint(0, 3)
  if r_open == 1:
    random_row_index()


def profession_info():
  time.sleep(0.5)
  print(f"\n{spacing}{spacing}{spacing}{spacing}\n1) Knight\n{spacing}Knight Information{spacing}\n• Knight starts with 'Training Sword' and 'Training Shield'.\n• Training Sword stats: \n Attack: 10\n Magic Attack: 0\n• Training Shield:\n Defense: 1\n• Other Stats:\n Health: 200\n Mana: 100\n{spacing}Knight Leveling Perks{spacing}\n• Knight's base attack and defense increases by 10!\n• Knight's health increases by 200 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(0.5)
  print(f"2) Magician\n{spacing}Magician Information{spacing}\n• Magician starts with 'Training Wand' with stats:\n Attack: 0\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 200\n Beginner Spell: 'Wind Strike' (10 mana per cast)\n{spacing}Magician Leveling Perks{spacing}\n• Magician's base magic attack increases by 10!\n• Magician's health increases by 100 and mana increases by 200!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(0.5)
  print(f"3) Archer\n{spacing}Archer Information{spacing}\n• Archer starts with 'Training Bow' and 'Training Arrows' with stats:\n Attack: 10\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 100\n Basic Arrow Shot (uses 1 arrow)\n Magic Arrow Shot (uses 1 arrow and 10 mana)\n{spacing}Archer Leveling Perks{spacing}\n• Archer's base attack and magic increase by 10!\n• Archer's health increases by 100 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(1)
def profession():
  while True:
    profession_info()
    profession_choice = input("Pick an Option. ").strip()
    # line to fetch their info
    if profession_choice in ['1', "Magician", "one", "magician"]:
      u_details.loc[u_details['username'] == username, 'profession'] = 'Magician'
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    elif profession_choice in ['2', "Archer", "two", "archer"]:
      u_details.loc[u_details['username'] == username, 'profession'] = 'Archer'
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    elif profession_choice in ['3', "Knight", "three", "knight"]:
      u_details.loc[u_details['username'] == username, 'profession'] = 'Knight'
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    else:
      print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
      continue

def room_counter(increment=1):# only write room_counter() to increase the room by 1, write room_counter(x) (x being number above 1) to add more than 1 room
    global room_count
    if 'room_count' not in globals():
        room_count = 0
    room_count += increment
    u_details.loc[u_details['username'] == username, 'room'] = room_count
    u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
    return room_count
def game():
  print("Welcome To Adventure Game.\nTo start, pick a profession you will like to be.")
  profession()
  print(f"{spacing}\nYou will be going through 3 tutorial rooms.\nIn this game there can only be empty room, room containing Chest or room containing monsters!\n{spacing}") #better if we force them into a certain room order, empty -> chest -> fight
  time.sleep(0.5)
  empty_room()
  time.sleep(0.5)
  chest_room()
  time.sleep(0.5)
  monster_room()

game()

