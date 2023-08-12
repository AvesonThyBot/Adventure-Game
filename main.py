# -------------------- Menu code --------------------
# -------------------- Imports and variable --------------------
try: #try except for imports
    import time, pandas as pd, re
    spacing = "---------" #variable for design
    user_data = pd.read_csv("adventure_game/data/user_details.csv")
except Exception as error: #error message
  print(f"There was an {error}. Stopping program.")
  time.sleep(3)
  print("Exiting...")
  exit()
# -------------------- Function to import files --------------------
def leaderboard(): #leaderboard.py
  from adventure_game import leaderboard
def load_game(): #load_game.py
  from adventure_game import load_game
def play_game(): #play_game.py
  from adventure_game import play_game

# -------------------- Account Login/Sign Up --------------------
# -------------------- Create Account --------------------
def create_account(user_data): #main account creation system
  while True:
    global username
    username = input(f"{spacing}\nPlease enter the username you wish to use: ").strip()
    if username == "":
      print(f"{spacing}\nUsername cannot be empty.")
      continue
    # check if the username is already taken
    if username in user_data['username'].values:
      print(f"{spacing}\nUsername already taken. Please choose another.")
      continue
    # check if the username is between 3 to 20 letters and contains only letters and numbers
    if not re.match("^\S[a-zA-Z0-9]{2,19}$", username):
      print(f"{spacing}\nUsername must be between 3 to 20 letters and can only contain letters and numbers.")
      continue
    break
  while True:
    password = input(f"{spacing}\nPlease create a password. ").strip()
    if not re.match("^\S[a-zA-Z0-9!@#$%^&*()_+}{\":?><;.,';\][=-]{7,}$",password):
      print(f"{spacing}\nPassword must be at least 8 characters, with no spaces, and could include at least special characters.")
      continue
    else:
      print(f"{spacing}\nSigning Up...\n{spacing}")
      break
  new_user = pd.DataFrame({'username': [username], 'password': [password]})
  user_data = pd.concat([user_data, new_user])
  user_data.to_csv("adventure_game/data/user_details.csv", index=False)
  return user_data
# -------------------- Login to Account --------------------
def login(user_data): #main login system
  while True:
    global username
    username = input(f"{spacing}\nPlease enter your username: ").strip()
    password = input("Please enter your password: ").strip()
    if user_data[(user_data['username'] == username) & (user_data['password'] == password)].empty:
      print(f"{spacing}\nInvalid username or password. Please try again.")
      continue
    else:
      print(
        f"{spacing}\nCorrect username and password.\nLogging In...\n{spacing}")
    break
# -------------------- Login Menu Function --------------------
def account_menu(): #main menu for login system
  while True:
    global user_data
    choice = input(f"{spacing}\nWhat do you want to do?\n{spacing}\n1.Log in\n2.Create a new account\n3.Return to Menu\n{spacing}\nEnter your choice: ").strip()
    try:
      choice = int(choice)
      if choice == 1: #login
        login(user_data)
        print(f"Login successful!\n{spacing}")
        break
      elif choice == 2: #login
        user_data = create_account(user_data)
        print(f"Sign Up successful!\n{spacing}")
        break
      elif choice == 3:
        print(f"{spacing}\nReturning to Menu!\n{spacing}")
        menu()
      else:
        print(f"{spacing}\nInvalid choice. Please try again.")
        continue
    except ValueError:
      print(f"{spacing}\nInput must be an Integer between 1-4.\n{spacing}")
    except Exception as error:
      print(f"{spacing}\nThere was an {error}.")
      time.sleep(1)
      print(f"{spacing}\nQuitting...\n{spacing}")
      exit()
# -------------------- Function to save login data --------------------
def login_data(): #username data
    return username
# -------------------- End of Account Login/Sign Up --------------------

# -------------------- Menu function --------------------
def menu(): #code for the menu
  print(f"Welcome to the Adventure Game!\n{spacing}")
  while True:
    menu_choice = input(f"What do you want to do?\n{spacing}\n1.Start Game\n2.Load Game\n3.View High Score\n4.Exit Game\n{spacing}\nEnter your choice: ").strip()
    try:
      menu_choice = int(menu_choice)
      if menu_choice == 1: #play game
        account_menu()
        play_game()
      elif menu_choice == 2: #load game
        account_menu()
        load_game()
      elif menu_choice == 3: #leaderboard
        return_option = leaderboard()
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
# -------------------- End of menu code --------------------
