# -------------------- Imports and read_csv --------------------
try:
  import pandas as pd, random, time
  equipment = pd.read_csv('adventure_game/data/equipments.csv')
  u_details = pd.read_csv('adventure_game/data/user_details.csv')
  spacing = "---------"
except Exception as error:
  print(f"There was an {error}. Stopping program.")
  time.sleep(3)
  print("Exiting...")
  exit()
# --------------------  Loads data --------------------
from adventure_game.login import login_data
global username
username = login_data()
username = u_details[(u_details['username'] == username)]
# -------------------- All functions under --------------------
def exit_menu(room): #menu to show if they want to exit.
  pass
def return_menu(room): #menu to show if they want to return to menu
  #leave this for now (needs to be changed for this part of code)
  while True:
    from adventure_game.login import login_menu
    choice = login_menu()
    if choice is None:
      continue
    choice = int(choice)
    if choice == 3:
      from adventure_game.login import menu
    elif choice in (1, 2):
      break
    else:
      continue
def random_row_index(Class, level): #random chest drop
    level = int(level)
    filtered_equipment = equipment[(equipment['Class'] == Class) & (equipment['Level'] <= level + 3)]
    num_rows = len(filtered_equipment)

    if num_rows == 0:
        return None

    random_row = random.randint(0, num_rows - 1)
    selected_row = filtered_equipment.iloc[random_row]

    name = selected_row['Name']
    inventory_list_str = u_details.loc[u_details['username'] == username, 'inventory'].tolist()[0]
    inventory_list = [item.strip() for item in inventory_list_str.split(',')]
    inventory_list.append(name)
    u_details.loc[u_details['username'] == username, 'inventory'] = [', '.join(inventory_list)]
    u_details.to_csv('user_details.csv', index=False)

    print(selected_row)
# -------------------- Inventory & Equipped Item function --------------------
inventory = [] #stores the inventory temporarily 
def inventory_updater(): #updates inventory on csv
  formatted_inventory = ','.join(str(item) for item in inventory)
  formatted_inventory = formatted_inventory
  u_details.loc[u_details['username'] == username, ['inventory']] = formatted_inventory
  u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
def equipped(x): #currently equipped item
  return inventory[x]
# -------------------- Room options function --------------------
def empty_options(): #option list for empty rooms.
  option_choice = input(f"""\
------- Empty Room Options -------
1) Proceed to room {room_count + 1}.
2) Check Inventory.
3) Back to menu.
4) Save & Quit Game.
----------------------------------
""")
  try:
    option_choice = int(option_choice)
    if option_choice == 1:
      return
    elif option_choice == 2:
      print(inventory)
    elif option_choice == 3:
      return_menu("empty")
      return
    elif option_choice == 4:
      exit_menu("empty")
      return
    else:
      print(f"{spacing*4}\nInvalid option. Must be 1-4.")
      empty_options()
  except ValueError:
    print("Invalid Value Type. Input must be integer between 1-4.")
    empty_options()
  except Exception:
    print("Input must be integer between 1-4.")
    empty_options()
def chest_options(): #option list for chest rooms.
  print(f"""\
------- Chest Room Options -------
1) Open chest
2) Check Inventory.
3) Proceed to room {room_count+1}
4) Back to menu.
5) Save & Quit Game.
----------------------------------""")
def monster_options(): #option list for monster rooms.
  print(f"""\
------- Monster Room Options -------
1) Fight monster.
2) Check Inventory.
3) Back to menu.
4) Save & Quit Game.
----------------------------------""")
# -------------------- Monster gameplay function --------------------
def monster_fight(): #monster fight options
  pass
# -------------------- Rooms function --------------------
def room_counter(increment=1):# only write room_counter() to increase the room by 1, write room_counter(x) (x being number above 1) to add more than 1 room
    global room_count
    if 'room_count' not in globals():
        room_count = 0
    room_count += increment
    u_details.loc[u_details['username'] == username, 'room'] = room_count
    u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
    return room_count
def empty_room(): #main controlling function for empty rooms
  room_count = room_counter()#updates room counter
  if room_count in [1.0,1,"1","1.0"]: #tutorial stage
    print(f"{spacing}\nThis room has nothing at all. Just a empty room...")
    empty_options()
  elif room_count > 3 or room_count> 3.0: #normal stages
    print(f"{spacing}\nThis room is empty! Room number: {room_count}.")
    empty_options()
def chest_room(): #main controlling function for chest rooms
  room_count = room_counter()#updates room counter
  print(f"{spacing}\nThis is a chest room! Room number: {room_count}.")
  if room_count in [2.0,2,"2","2.0"]: #tutorial stage
    print("chest tutorial")
    chest_options()
  elif room_count> 2 or room_count > 1.0:#normal room stages
    print("You open the chest")
    r_open = random.randint(0, 3)
    if r_open == 1:
      profession = u_details.loc[u_details['username']==username, 'profession'].values[0]
      level = u_details.loc[u_details['username']==username, 'level'].values[0]
      random_row_index(f"{profession}",f"{level}")
    chest_options()
def monster_room(): #main controlling function for monster rooms
  room_count = room_counter()#updates room counter
  print(f"{spacing}\nThis is a monster room! Room number: {room_count}.")
  if room_count in [3.0,3,"3","3.0"]: #tutorial stage
    print("monster tutorial")
    monster_options()
  elif room_count> 3 or room_count > 3.0:#normal room stages
    print("normal")
    monster_options()
def random_room(): #function to call a random room from the 3
  room_num = random.randint(1, 3)
  if room_num == 1:
    empty_room() 
  elif room_num == 2:
    chest_room()
  else:
    monster_room()
# -------------------- Profession function --------------------
def profession_info(): #gives them information of professions
  time.sleep(1)
  print(f"{spacing}{spacing}{spacing}{spacing}\n1) Magician\n{spacing}Magician Information{spacing}\n• Magician starts with 'Training Wand' with stats:\n Attack: 0\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 200\n Beginner Spell: 'Wind Strike' (10 mana per cast)\n{spacing}Magician Leveling Perks{spacing}\n• Magician's base magic attack increases by 10!\n• Magician's health increases by 100 and mana increases by 200!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(1)
  print(f"2) Archer\n{spacing}Archer Information{spacing}\n• Archer starts with 'Training Bow' and 'Training Arrows' with stats:\n Attack: 10\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 100\n Basic Arrow Shot (uses 1 arrow)\n Magic Arrow Shot (uses 1 arrow and 10 mana)\n{spacing}Archer Leveling Perks{spacing}\n• Archer's base attack and magic increase by 10!\n• Archer's health increases by 100 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(1)
  print(f"3) Knight\n{spacing}Knight Information{spacing}\n• Knight starts with 'Training Sword' and 'Training Shield'.\n• Training Sword stats: \n Attack: 10\n Magic Attack: 0\n• Training Shield:\n Defense: 1\n• Other Stats:\n Health: 200\n Mana: 100\n{spacing}Knight Leveling Perks{spacing}\n• Knight's base attack and defense increases by 10!\n• Knight's health increases by 200 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  time.sleep(1)
def profession(): #main professional handling function
  while True:
    profession_info_choice = input(f"{spacing}\nDo you want to check profession information and perks? (Yes or No): ").strip()
    if profession_info_choice.lower() in [1,"yes","yea","one","sure","ye","y"]:
      profession_info()
      break
    elif profession_info_choice.lower() in [2,"no","nah","two","na","n"]:
      print(spacing)
      break
    else:
      profession()
  while True:
    profession_choice = input(f"Pick an Option.\n• Magician (1)\n• Archer (2)\n• Knight (3)\n{spacing}\nEnter your choice: ").strip()
    #Needs to add inventory items to the list.
    if profession_choice in ['1', "Magician", "one", "magician","1.0",1,1.0]:
      print("Congrats! You have chosen the profession Magician!")
      u_details.loc[u_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Magician',0, 0, 10, 0,100,200]
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    elif profession_choice in ['2', "Archer", "two", "archer","2.0",2,2.0]:
      print("Congrats! You have chosen the profession Archer!")
      u_details.loc[u_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Archer',0, 10, 0, 1,200,100]
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    elif profession_choice in ['3', "Knight", "three", "knight","3.0",3,3.0]:
      print("Congrats! You have chosen the profession Knight!")
      u_details.loc[u_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Knight',0, 10, 10, 0,100,100]
      u_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      break
    else:
      print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
      continue  
# -------------------- Main Game function --------------------
def game(): #main game controlling function
  print("Welcome To Adventure Game.\nTo start, pick a profession you will like to be.")
  profession()
  print(f"{spacing}\nYou will be going through 3 tutorial rooms.\nIn this game there 3 types of rooms:\n• Empty Room\n• Chest Room\n• Monster Room")
  time.sleep(1)
  print(f"{spacing}\nFirst Tutorial room.")
  time.sleep(1)
  empty_room() #sends player to empty room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  time.sleep(1)
  print(f"{spacing}\nSecond Tutorial room.")
  time.sleep(1)
  chest_room() #sends player to chest room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  time.sleep(1)
  print(f"{spacing}\nThird Tutorial room.")
  time.sleep(1)
  monster_room() #sends player to monster room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  time.sleep(1)
  print(f"{spacing}\nThis is the end of the tutorial. You now have the ability to exit the game moving forward.")
  while True: #infinitvely goes on until there is a breaking point
    time.sleep(1)
    random_room()
    inventory_updater() #updates inventory to csv after room is complete.
game() #Run the game
# -------------------- Extra things --------------------
""" 
TO DO:
create room_menu
do design for room_menu
fix room_menu for each room type
fix random_row_indexer
"""

""" Room menu option template
Empty:
------- Empty Room Options -------
1) Proceed to room {room_count+1}.
2) Check Inventory.
3) Back to menu.
4) Save & Quit Game.
----------------------------------
Chest:
------- Chest Room Options -------
1) Open chest
2) Check Inventory.
3) Proceed to room {room_count+1}
4) Back to menu.
5) Save & Quit Game.
----------------------------------
Monster:
------- Monster Room Options -------
1) Fight monster.
2) Check Inventory.
3) Back to menu.
4) Save & Quit Game.
----------------------------------
"""