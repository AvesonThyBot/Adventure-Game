# -------------------- Imports and read_csv --------------------
try: #checks imports
  import pandas as pd, random, time
  user_details = pd.read_csv('adventure_game/data/user_details.csv')
  user_inventory = pd.read_csv('adventure_game/data/user_inventory.csv')
  equipment = pd.read_csv('adventure_game/data/equipments.csv')
  spells = pd.read_csv('adventure_game/data/spells.csv')
  potions =pd.read_csv('adventure_game/data/potions.csv')
  spacing = "---------"
  global options 
  options = {'sleep':True,'skipEmpty':False}
except Exception as error: #error message
  print(f"There was an {error}. Stopping program.")
  time.sleep(3)
  print("Exiting...")
  exit()
# --------------------  Options function --------------------
def sleep(x): #function that lets user bypass time.sleep
  if options['sleep'] == True:
    time.sleep(x)
def proceedEmpty(): #function to proceed empty room automatically
  if options['skipEmpty'] == True:
    return "skip"
def options_menu(): #options menu
  return_toggle = True
  while return_toggle:
    print(f"{spacing} Options {spacing}\nSelect the option you want to change or type 'return'.")
    choice = input(f"1) Keep Slowdown: {options['sleep']}\n2) Skip Empty Rooms: {options['skipEmpty']}\n{spacing*3}\n")
    try:
      if choice.lower() == "return":
        return_toggle = False
      else:
          choice = int(choice)
          if choice == 1:
            print(f"{spacing*3}\nKeep Slowdown is set to {not options['sleep']}")
            options['sleep'] = not options['sleep']
          elif choice == 2:
            print(f"{spacing*3}\nSkip Empty Rooms is set to {not options['skipEmpty']}")
            options['skipEmpty'] = not options['skipEmpty']
          else:
            print(f"{spacing*3}\nInvalid choice. Please choose 1 or 2.")
    except ValueError:
      print(f"{spacing*3}\nInput must be an Integer between 1-2 or 'return'.")
    except Exception as error:
      print(f"{spacing}\nThere was an {error}.")
      time.sleep(1)
      print(f"{spacing}\nQuitting...\n{spacing}")
      exit()
# --------------------  Loads data --------------------
with open("adventure_game/data/player.txt", "r") as file: #fetching username
  global username
  username = file.read().strip().split()[0]
userdata = user_details[(user_details['username'] == username)] #assigns the players data to userdata
def update_details(): #updates profession_type and level
    profession_type = user_details.loc[user_details['username'] == username, 'profession'].values[0]
    level = user_details.loc[user_details['username'] == username, 'level'].values[0]
    return profession_type, level
# -------------------- Extra Functions --------------------
def exit_menu(): #menu to show if they want to exit.
  while True:
      choice = input(f"{spacing}\nDo you want to save and exit the game? (Yes or No): \n{spacing}\n")
      try:
          choice = str(choice)
          if choice.lower().strip() in ["yes","ye","yea","y"]:
              print("Exiting...")
              sleep(1) #Slows down the program to give better UX
              exit()
          elif choice.lower().strip() in ["no","nah","n"]:
              return
          else:
              print("Enter either 'Yes' or 'No'.")
      except ValueError:
          print("Enter either 'Yes' or 'No'.")
          continue
      except Exception:
          print("There has been an unexpected error. Try again")
def chest_drop(profession_type, level): #random chest drop
  # ---------- Sorting drop options ----------
  if profession_type == "Magician":
    filtered_spells = spells[spells['Level'] <= level + 10]#gets all spells that is within 10 level or same level
    drop_data = random.randint(1,3)
    inventory_spells = user_inventory.loc[user_inventory["username"] == username, "spells"].values
  else:
    drop_data = random.randint(1,2)
  filtered_equipment = equipment[(equipment['Class'] == profession_type) & (equipment['Level'] <= level + 3)] #gets all equipments for that profession & same equipment level or 3 above 
  if drop_data == 1: #equipments
    drop_type = "Equipments"
    drop_data = filtered_equipment
    num_rows = len(filtered_equipment)
  elif drop_data == 2: #potions
    drop_type = "Potions"
    drop_data = potions
    num_rows = len(potions)
  else: #spells
    drop_type = "Spells"
    drop_data = filtered_spells
    num_rows = len(filtered_spells)

  # ---------- Updating Inventory ----------
  global inventory
  inventory = inventory_assigner() #updates inventory

  # ---------- Giving a valid drop ----------
  while True:#while loop to give them a drop that they don't have.
    # ---------- Gets Item ----------
    random_row = random.randint(0,num_rows-1) #gets a random row
    selected_row = drop_data.iloc[random_row] #random drop
    
    # ---------- Coverting data types ----------
    try: #tries to make Name it
      item_name = selected_row["Name"]
    except KeyError: #if its a spell it will use spell not name
      if "Name" in selected_row.index:
        item_name = selected_row.loc["Name"]
      elif "Spells" in selected_row.index:
        item_name = selected_row.loc["Spells"]
      elif "name" in selected_row.index:
        item_name = selected_row.loc["name"]
      else:
        print("There was an Error with chest drop. ID: Item_name")
    
    # ---------- Iteration for item and amount of item ----------
    # ---------- Equipment not stackable ----------
    print(item_name,drop_type)
    if drop_type == "Equipments" and item_name != "Trainer Arrows":
      if item_name not in inventory: #checks if the item is not in inventory
        inventory[item_name] = 1 #adds 1 of the item to inventory
        print(f"Added {inventory[item_name]} {item_name} to inventory.")
        break
    # ---------- Spells not stackable and stored in spells ----------
    elif drop_type == "Spells":
      if item_name not in inventory_spells:
        existing_spells = user_inventory.loc[user_inventory['username'] == username, 'spells'].values[0]
        updated_spells = existing_spells + ',' + item_name
        user_inventory.loc[user_inventory['username'] == username, 'spells'] = updated_spells
        user_inventory.to_csv('adventure_game/data/user_inventory.csv', index=False)
        break
    # ---------- Stackable Potion amount ----------
    elif drop_type == "Potions":
      if item_name not in inventory:
        inventory[item_name] = 1 #adds 1 of the item to inventory
        print(f"Added {inventory[item_name]} {item_name} to inventory.")
        break
      else:
        inventory[item_name] += 1
        print(f"Added {inventory[item_name]} {item_name} to inventory.")
        break
    # ---------- Multiple arrows awarded and stackable ----------
    elif drop_type=="Equipments" and item_name == "Trainer Arrows":
        if item_name not in inventory:
          inventory[item_name] = 8 #8 arrows per drop
          print(f"Added {inventory[item_name]} {item_name} to inventory.")
          break
        else:
          inventory[item_name] += 8 #8 arrows per drop
          print(f"Added {inventory[item_name]} more {item_name} to inventory.")
          break
    # ---------- Additional error handling, should not occur ----------
    else:
      print("There was an error.")
      print("Exiting...")
      exit()
# -------------------- Inventory & Equipped Item function --------------------
def inventory_assigner(): #updates inventory variable when this function is called.
  inventory_data = user_inventory[user_inventory['username'] == username]['items'].values[0]
  inventory_data = inventory_data.replace("'", "").replace(":", ": ").replace(",", ",")
  inventory_dict = dict(item.split(": ") for item in inventory_data.split(","))
  return inventory_dict #stores the inventory temporarily 
def inventory_updater(): #updates inventory on csv
    formatted_inventory = ','.join(f"'{key}':{value}" for key, value in inventory.items())
    user_inventory.loc[user_inventory['username'] == username, ['items']] = formatted_inventory
    user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
def inventory_UI(): #currently equipped item
  pass
# -------------------- Room options function --------------------
def empty_options(): #option list for empty rooms.
  option_choice = input(f"""\
------- Empty Room Options -------
1) Proceed to room {room_count + 1}.
2) Check Inventory.
3) Save & Quit Game.
4) Check options
----------------------------------
""")
  try:
    option_choice = int(option_choice)
    if option_choice == 1:
      return
    elif option_choice == 2:
      print(inventory)
      empty_options()
    elif option_choice == 3:
      exit_menu()
      return
    elif option_choice == 4:
      options_menu()
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
  option_choice = input(f"""\
------- Chest Room Options -------
1) Open chest
2) Check Inventory.
3) Proceed to room {room_count+1}
4) Save & Quit Game.
5) Check options
----------------------------------
""")
  try:
    option_choice = int(option_choice)
    if option_choice == 1:
      return "open"
    elif option_choice == 2:
      print(inventory)
      chest_options()
    elif option_choice == 3:
      return "proceed"
    elif option_choice == 4:
      exit_menu()
      return
    elif option_choice == 5:
      options_menu()
      return
    else:
      print(f"{spacing*4}\nInvalid option. Must be 1-4.")
      chest_options()
  except ValueError:
    print("Invalid Value Type. Input must be integer between 1-4.")
    chest_options()
  except Exception:
    print("Input must be integer between 1-4.")
    chest_options()
def monster_options(): #option list for monster rooms.
  option_choice = input(f"""\
------- Monster Room Options -------
1) Fight monster.
2) Check Inventory.
3) Save & Quit Game.
4) Check options
----------------------------------
""")
  try:
    option_choice = int(option_choice)
    if option_choice == 1:
      return
    elif option_choice == 2:
      print(inventory)
      monster_options()
    elif option_choice == 3:
      exit_menu()
      return
    elif option_choice == 4:
      options_menu()
      return
    else:
      print(f"{spacing*4}\nInvalid option. Must be 1-4.")
      monster_options()
  except ValueError:
    print("Invalid Value Type. Input must be integer between 1-4.")
    monster_options()
  except Exception:
    print("Input must be integer between 1-4.")
    monster_options()
# -------------------- Monster gameplay function --------------------
def monster_fight(): #monster fight options
  pass
# -------------------- Rooms function --------------------
def room_counter(increment=1):# only write room_counter() to increase the room by 1, write room_counter(x) (x being number above 1) to add more than 1 room
    global room_count
    if 'room_count' not in globals():
        room_count = 0
    room_count += increment
    user_details.loc[user_details['username'] == username, 'room'] = room_count
    user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
    return room_count
def empty_room(): #main controlling function for empty rooms
  room_count = room_counter()#updates room counter
  if room_count in [1.0,1,"1","1.0"]: #tutorial stage
    print(f"{spacing}\nThis room has nothing at all. Just a empty room...")
  elif room_count > 3 or room_count> 3.0: #normal stages
    print(f"{spacing}\nThis room is empty! Room number: {room_count}.")
    choice = proceedEmpty() #code can be shortened but makes it neater if its a function
    if choice == "skip":
      return
    empty_options()
def chest_room(): #main controlling function for chest rooms
  room_count = room_counter()#updates room counter
  print(f"{spacing}\nThis is a chest room! Room number: {room_count}.")
  if room_count in [2.0,2,"2","2.0"]: #tutorial stage
    print(f"Congrats! You unlocked a Minor Health Potion!")
  elif room_count> 2 or room_count > 1.0:#normal room stages
    return_option = chest_options()
    if return_option == "open":
      print("You open the chest")
      profession_type,level = update_details()
      chest_drop(profession_type,level)
    elif return_option == "proceed":
      return
    else:
      chest_room()
def monster_room(): #main controlling function for monster rooms
  room_count = room_counter()#updates room counter
  print(f"{spacing}\nThis is a monster room! Room number: {room_count}.")
  if room_count in [3.0,3,"3","3.0"]: #tutorial stage
    print("monster tutorial")
  elif room_count> 3 or room_count > 3.0:#normal room stages
    print("normal")
    return_option = monster_options()
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
  sleep(1)
  print(f"{spacing}{spacing}{spacing}{spacing}\n1) Magician\n{spacing}Magician Information{spacing}\n• Magician starts with 'Training Wand' with stats:\n Attack: 0\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 200\n Beginner Spell: 'Wind Strike' (10 mana per cast)\n{spacing}Magician Leveling Perks{spacing}\n• Magician's base magic attack increases by 10!\n• Magician's health increases by 100 and mana increases by 200!\n{spacing}{spacing}{spacing}{spacing}")
  sleep(1)
  print(f"2) Archer\n{spacing}Archer Information{spacing}\n• Archer starts with 'Training Bow' and 'Training Arrows' with stats:\n Attack: 10\n Magic Attack: 10\n Defense: 0\n• Other Stats:\n Health: 100\n Mana: 100\n Basic Arrow Shot (uses 1 arrow)\n Magic Arrow Shot (uses 1 arrow and 10 mana)\n{spacing}Archer Leveling Perks{spacing}\n• Archer's base attack and magic increase by 10!\n• Archer's health increases by 100 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  sleep(1)
  print(f"3) Knight\n{spacing}Knight Information{spacing}\n• Knight starts with 'Training Sword' and 'Training Shield'.\n• Training Sword stats: \n Attack: 10\n Magic Attack: 0\n• Training Shield:\n Defense: 1\n• Other Stats:\n Health: 200\n Mana: 100\n{spacing}Knight Leveling Perks{spacing}\n• Knight's base attack and defense increases by 10!\n• Knight's health increases by 200 and mana increases by 100!\n{spacing}{spacing}{spacing}{spacing}")
  sleep(1)
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
      continue
  while True:
    profession_choice = input(f"Pick an Option.\n• Magician (1)\n• Archer (2)\n• Knight (3)\n{spacing}\nEnter your choice: ").strip()
    #Needs to add inventory items to the list.
    global inventory
    if profession_choice in ['1', "Magician", "one", "magician","1.0",1,1.0]:
      print("Congrats! You have chosen the profession Magician!")
      user_details.loc[user_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Magician',0, 0, 10, 0,100,200]
      user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      user_inventory.loc[user_inventory['username'] == username, ['items','spells']] = [f"'Training Wand':{int(1)},'Minor Health Potion':{int(1)}","Wind Strike"]
      user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
      global inventory_spells
      inventory_spells = []
      inventory = inventory_assigner()
      break
    elif profession_choice in ['2', "Archer", "two", "archer","2.0",2,2.0]:
      print("Congrats! You have chosen the profession Archer!")
      user_details.loc[user_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Archer',0, 10, 0, 1,200,100]
      user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      user_inventory.loc[user_inventory['username'] == username, ['items']] = [f"'Trainer Bow': {int(1)},'Trainer Arrows':{int(16)},'Minor Health Potion':{int(1)}"]
      user_inventory.loc[user_inventory['username'] == username, 'spells'] = ''
      user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
      inventory = inventory_assigner()
      break
    elif profession_choice in ['3', "Knight", "three", "knight","3.0",3,3.0]:
      print("Congrats! You have chosen the profession Knight!")
      user_details.loc[user_details['username'] == username, ['profession','level','attack','magic_attack', 'defense', 'health','mana']] = ['Knight',0, 10, 10, 0,100,100]
      user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      user_inventory.loc[user_inventory['username'] == username, ['items']] = [f"'Training Sword':{int(1)},'Training Shield':{int(1)},'Minor Health Potion':{int(1)}"]
      user_inventory.loc[user_inventory['username'] == username, 'spells'] = ''
      user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
      inventory = inventory_assigner()
      break
    else:
      print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
      continue  
# -------------------- Main Game function --------------------
def game(): #main game controlling function
  print(f"Hello {username}!\n{spacing}\nTo start, pick a profession you will like to be.")
  profession()
  print(f"{spacing}\nYou will be going through 3 tutorial rooms.\nIn this game there 3 types of rooms:\n• Empty Room\n• Chest Room\n• Monster Room")
  sleep(1)
  print(f"{spacing}\nFirst Tutorial room.")
  sleep(1)
  empty_room() #sends player to empty room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  sleep(1)
  print(f"{spacing}\nSecond Tutorial room.")
  sleep(1)
  chest_room() #sends player to chest room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  sleep(1)
  print(f"{spacing}\nThird Tutorial room.")
  sleep(1)
  monster_room() #sends player to monster room (tutorial)
  inventory_updater() #updates inventory to csv after room is complete.
  sleep(1)
  print(f"{spacing}\nThis is the end of the tutorial. You now have the ability to exit the game moving forward.")
  while True: #infinitvely goes on until there is a breaking point
    sleep(1)
    random_room()
    inventory_updater() #updates inventory to csv after room is complete.
# chest_drop("Magician",0)
game() #Run the game
# -------------------- Extra things --------------------

""" TO-DO:
add options data to user_details
make datatype for user_inventory["items"] int.
add spells spell updating functions
fix chest drop; checking inventory then opening chest breaks the system
fix chet room increasing number if any other function is called and then returned back to old function.
fix chest room breaking sometimes when open chest is picked
remove equipped function and update it to be the inventory UI
"""