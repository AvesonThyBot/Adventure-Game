# -------------------- Imports and variable --------------------
try: #try except for imports
    import time
    spacing = "---------" #variable for design
except Exception as error: #error message
  print(f"There was an {error}. Stopping program.")
  time.sleep(3)
  print("Exiting...")
  exit()
# -------------------- Function to import files --------------------
def login(): #login.py
  from adventure_game import login
def leaderboard(): #leaderboard.py
  from adventure_game import leaderboard
def load_game(): #load_game.py
  from adventure_game import load_game
def play_game(): #play_game.py
  from adventure_game import play_game
# -------------------- Return to Menu function --------------------
def return_menu(): #checks if user returned to menu
  while True:
    from adventure_game.login import login_menu
    choice = login_menu()
    if choice is None:
      continue
    choice = int(choice)
    if choice == 3:
      leaderboard()
    elif choice in (1, 2, 3):
      break
    else:
      continue # The return menu checks whether  the game returns back to the menu

# -------------------- Menu function --------------------
def menu(): #code for the menu
  print(f"Welcome to the Adventure Game!\n{spacing}")
  while True:
    menu_choice = input(f"What do you want to do?\n{spacing}\n1.Start Game\n2.Load Game\n3.View High Score\n4.Exit Game\n{spacing}\nEnter your choice: ").strip()
    try:
      menu_choice = int(menu_choice)
      if menu_choice == 1: #play game
        login()
        return_menu()
        return_option = play_game()
        if return_option == "menu":
          print("test")
          menu()
        return menu_choice
      elif menu_choice == 2: #load game
        login()
        return_menu()
        return_option = load_game()
        if return_option == "menu":
          menu()
        return menu_choice
      elif menu_choice == 3: #leaderboard
        return_option = leaderboard()
        if return_option == "menu":
          menu()
      elif menu_choice == 4: #exit
        exit()
      else:
        print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
        continue
    except ValueError:
      print(f"{spacing}\nInput must be an Integer between 1-4.\n{spacing}")
    except Exception as error:
      print(f"{spacing}\nThere was an {error}.")
      time.sleep(1)
      print(f"{spacing}\nQuitting...\n{spacing}")
      exit()

menu() #runs the menu
