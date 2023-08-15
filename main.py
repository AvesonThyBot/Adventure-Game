# [ -------------------- Imports and variables -------------------- ]
try: #try except for imports
    import time, pandas as pd, re
    spacing = "---------" #variable for design
    username = " " #for fetching username at load_game and play_game
    user_data = pd.read_csv("adventure_game/data/user_details.csv")
except Exception as error: #error message
  print(f"There was an {error}. Stopping program.")
  time.sleep(3)
  print("Exiting...")
  exit()
# [ -------------------- End of Imports and variables -------------------- ]


# [ -------------------- Account Login/Sign Up Code -------------------- ]
# -------------------- Create Account Function --------------------
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
  player_updater(username)
# -------------------- Login to Account Function --------------------
def login(user_data): #main login system
    while True:
      global username
      username = input(f"{spacing}\nPlease enter your username: ").strip()
      password = input("Please enter your password: ").strip()
      if user_data[(user_data['username'] == username) & (user_data['password'] == password)].empty:
          print(f"{spacing}\nInvalid username or password. Please try again.")
          continue
      else:
          print(f"{spacing}\nCorrect username and password.\nLogging In...\n{spacing}")
          player_updater(username)
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
      elif choice == 2: #create acccount
        create_account(user_data)
        print(f"Sign Up successful!\n{spacing}")
        break
      elif choice == 3: #return to menu()
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
# -------------------- Player.txt updater --------------------
def player_updater(user): #updates username at player.txt
    with open("adventure_game/data/player.txt", "w") as file:
        file.write(f"{username}")
# [ -------------------- End of Account Login/Sign Up -------------------- ]


# [ -------------------- Menu Code -------------------- ]
# -------------------- Function to import files --------------------
def leaderboard(): #leaderboard.py
  from adventure_game import leaderboard
def load_game(): #load_game.py
  from adventure_game import load_game
def play_game(): #play_game.py
  from adventure_game import play_game
# -------------------- Menu Function --------------------
def menu(): #code for the menu
  print(f"Welcome to the Adventure Game!\n{spacing}")
  while True:
    menu_choice = input(f"What do you want to do?\n{spacing}\n1.Start Game\n2.Load Game\n3.View High Score\n4.Exit Game\n{spacing}\nEnter your choice: ").strip()
    try:
      menu_choice = int(menu_choice)
      if menu_choice == 1: #play game
        account_menu()
        play_game()
        break
      elif menu_choice == 2: #load game
        account_menu()
        load_game()
        break
      elif menu_choice == 3: #leaderboard
        leaderboard()
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
# [ -------------------- End of menu code -------------------- ]

if __name__ == "__main__": # Start the menu when the script is run directly
    menu()