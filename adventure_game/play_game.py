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
        user_details.loc[user_details['username'] == username, 'options'] = [options]
        user_details.to_csv('adventure_game/data/user_details.csv', index=False)  
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
  # ---------- Updating Inventory ----------
  global inventory
  inventory = inventory_assigner() #updates inventory
  # ---------- Giving a valid drop ----------
  while True: #while loop to give them a drop that they don't have.
    # ---------- Sorting drop options ----------
    if profession_type == "Magician":
      filtered_spells = spells[spells['Level'] <= level + 10]#gets all spells that is within 10 level or same level
      drop_data = random.randint(1,3)
      global inventory_spells
      inventory_spells = spells_assigner()
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
        print(f"There was an Error with chest drop. ID: {item_name}")
    
    # ---------- Iteration for item and amount of item ----------
    # ---------- Equipment not stackable ----------
    if drop_type == "Equipments" and item_name != "Trainer Arrows":
      if item_name not in inventory: #checks if the item is not in inventory
        inventory[item_name] = 1 #adds 1 of the item to inventory
        print(f"Added 1 {item_name} to inventory!")
        break
      else:
        inventory[item_name] = int(inventory[item_name]) + 1
        print(f"Added 1 {item_name} to inventory!")
        break
    # ---------- Spells not stackable and stored in spells ----------
    elif drop_type == "Spells":
      if item_name in inventory_spells:
        continue  # Exit the loop without adding the spell to inventory

      inventory_spells.append(item_name)
      updated_spells = ','.join(sorted(set(inventory_spells)))
      user_inventory.loc[user_inventory['username'] == username, 'spells'] = updated_spells
      user_inventory.to_csv('adventure_game/data/user_inventory.csv', index=False)
      print(f"Added 1 {item_name} to spells!")
      break

    # ---------- Stackable Potion amount ----------
    elif drop_type == "Potions":
      if item_name not in inventory:
        inventory[item_name] = 1 #adds 1 of the item to inventory
        print(f"Added 1 {item_name} to inventory!")
        break
      else:
        inventory[item_name] = int(inventory[item_name]) + 1
        print(f"Added 1 {item_name} to inventory!")
        break
    # ---------- Multiple arrows awarded and stackable ----------
    elif drop_type=="Equipments" and item_name == "Trainer Arrows":
      if item_name not in inventory:
        inventory[item_name] = 8 #8 arrows per drop
        print(f"Added 8 {item_name} to inventory!")
        break
      else:
        inventory[item_name] = int(inventory[item_name]) + 8 #8 arrows per drop
        print(f"Added 8 more {item_name} to inventory!")
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
def spells_assigner():
    spells_data = user_inventory.loc[user_inventory['username'] == username, 'spells'].values[0]
    spells_list = [spell.strip() for spell in spells_data.split(',')]
    return spells_list  # stores the spells temporarily
def inventory_updater(): #updates inventory on csv
  formatted_inventory = ','.join(f"'{key}':{value}" for key, value in inventory.items())
  user_inventory.loc[user_inventory['username'] == username, ['items']] = formatted_inventory
  user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
def inventory_UI():  # UI to see item, spells, and stats
  inventory = inventory_assigner() #assigns updated inventory
  inventory_spells = spells_assigner() #assigns updated spells
  print(f"{'-' * 50}\n{'':15}User Statistics{'':10}\n{'-' * 50}") #user stats under the inventory and spells 
  for index,row in userdata.iterrows(): #prints user stats
    print("• Username:", row['username'])
    print("• Profession:", row['profession'])
    print("• Level:", int(row['level']))
    print("• Experience:", int(row['experience']))
    print("• Health:", int(row['health']))
    print("• Mana:", int(row['mana']))
    print("• Attack:", int(row['attack']))
    print("• Magic Attack:", int(row['magic_attack']))
    print("• Defense:", int(row['defense']))
    print("• Room:", int(room_count))
    print("• Options:")
    print("  ↳ Keep Slowdown:", options['sleep'])
    print("  ↳ Skip Empty Rooms:", options['skipEmpty'])
  print(f"{'-' * 50}\n{'':5}Inventory{'':20}Spells\n{'-' * 50}") #inventory and spells title
  max_item_length = max(len(item) for item in inventory.keys()) #finds max lenght of the name
  for item, quantity in inventory.items(): #prints out all the inventory items and spells 
    spell = inventory_spells.pop(0) if inventory_spells else ""
    max_quantity_width = max(len(str(quantity)) for item, quantity in inventory.items())
    line = f"• {item:<{max_item_length}} : x{quantity:>{max_quantity_width}}  | • {spell:<20}" if spell else f"• {item:<{max_item_length}} : x{quantity:>{max_quantity_width}}"
    print(line)
  print('-' * 50)
  inventory_spells = spells_assigner() #reassigns spells
  sleep(1)
  while True: #loop to let them check info of item/spell/potion
    choice = input(f"Pick an item/spell from inventory to check information, or type 'return' to exit.\n{spacing}\n")
    try:
      if choice == "return": #exits function
        return
      elif choice in inventory.keys() and ("Potion" in choice): #prints info for potion
        potion_data = potions[(potions['Name'] == choice)]
        for index,row in potion_data.iterrows():
          print("↳ Effect:", row['Stat Effect'])
          print("↳ Power:", int(row['Effect Increase']))
        print(spacing*3)
      elif choice in inventory.keys(): #prints info for item
        item_data = equipment[(equipment['Name'] == choice)]
        for index,row in item_data.iterrows(): 
          print("↳ Type:", row['Type'])
          print("↳ Attack:", int(row['Attack']))
          print("↳ Magic Attack:", int(row['Magic_Attack']))
          print("↳ Defense:", int(row['Defense']))
          print("↳ Level:", int(row['Level']))
          print("↳ Class:", row['Class'])
        print(spacing*3)
      elif choice in inventory_spells: #prints info for spells
        spell_data = spells[(spells['Spells'] == choice)]
        for index,row in spell_data.iterrows():
          print("↳ Mana Loss:", int(row['Mana_Loss_Min']))
          print("↳ Level:", int(row['Level']))
        print(spacing*3)
      elif choice not in inventory_spells or inventory.keys():
        print("Invalid item/spell.\nTry again.")
        continue
    except Exception:
      print("Invalid input.\nInput item name or type 'return' to exit.")
      continue
# -------------------- Room options function --------------------
def empty_options(): #option list for empty rooms.
  while True:
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
        inventory_UI()
        continue
      elif option_choice == 3:
        exit_menu()
        return
      elif option_choice == 4:
        options_menu()
      else:
        print(f"{spacing*4}\nInvalid option. Must be 1-4.")
        continue
    except ValueError:
      print("Invalid Value Type.\nInput must be integer between 1-4.")
      continue
def chest_options(): #option list for chest rooms.
  while True:
    option_choice = input(f"""\
------- Chest Room Options -------
1) Open chest
2) Check Inventory.
3) Proceed to room {room_count + 1}
4) Save & Quit Game.
5) Check options
----------------------------------
""")
    try:
      option_choice = int(option_choice)
      if option_choice == 1:
        return "open"
      elif option_choice == 2:
        inventory_UI()
      elif option_choice == 3:
        return "proceed"
      elif option_choice == 4:
        exit_menu()
      elif option_choice == 5:
        options_menu()
      else:
        print(f"{spacing * 4}\nInvalid option. Must be 1-5.")
        continue
    except ValueError:
      print("Invalid Value Type.\nInput must be an integer between 1-5.")
      continue
def monster_options(): #option list for monster rooms.
  while True:
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
        inventory_UI()
        continue
      elif option_choice == 3:
        exit_menu()
      elif option_choice == 4:
        options_menu()
      else:
        print(f"{spacing * 4}\nInvalid option. Must be 1-4.")
        continue
    except ValueError:
      print("Invalid Value Type.\nInput must be an integer between 1-4.")
      continue
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
      print("Chest opening...")
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
      user_details.loc[user_details['username'] == username, ['profession','experience','level','attack','magic_attack', 'defense', 'health','mana','options']] = ['Magician',0,0, 0, 10, 0,100,200,options]
      user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      user_inventory.loc[user_inventory['username'] == username, ['items','spells']] = [f"'Training Wand':{int(1)},'Minor Health Potion':{int(1)}","Wind Strike"]
      user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
      global inventory_spells
      inventory_spells = spells_assigner()
      inventory = inventory_assigner()
      break
    elif profession_choice in ['2', "Archer", "two", "archer","2.0",2,2.0]:
      print("Congrats! You have chosen the profession Archer!")
      user_details.loc[user_details['username'] == username, ['profession','experience','level','attack','magic_attack', 'defense', 'health','mana','options']] = ['Archer',0,0,10,0,1,200,100,options]
      user_details.to_csv("adventure_game/data/user_details.csv", index=False, mode='w')
      user_inventory.loc[user_inventory['username'] == username, ['items']] = [f"'Trainer Bow': {int(1)},'Trainer Arrows':{int(16)},'Minor Health Potion':{int(1)}"]
      user_inventory.loc[user_inventory['username'] == username, 'spells'] = ''
      user_inventory.to_csv("adventure_game/data/user_inventory.csv", index=False, mode='w')
      inventory = inventory_assigner()
      break
    elif profession_choice in ['3', "Knight", "three", "knight","3.0",3,3.0]:
      print("Congrats! You have chosen the profession Knight!")
      user_details.loc[user_details['username'] == username, ['profession','experience','level','attack','magic_attack', 'defense', 'health','mana','options']] = ['Knight',0,0,10,10,0,100,100,options]
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

game() #Run the game
# -------------------- Extra things --------------------


""" TO-DO:
add monster ui function
make monster_fight be functional.
Add fight_options function
Experience function with the math
proper leveling system based on monster beaten or progression in levels
"""