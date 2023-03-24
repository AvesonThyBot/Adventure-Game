import pandas as pd, re, time

# read in user details from CSV
user_data = pd.read_csv("adventure_game/data/user_details.csv")

#variables
spacing = "---------"


def return_login(): #something like this will need to be in every script that will let them return to menu or going back to the code won't work as it finished interpreting the whole code already.
  while True:
    from adventure_game.menu import menu
    choice = menu()
    choice = int(choice)
    if choice is None:
      continue
    elif choice in (1,2):
      login_menu()
    elif choice == 3:
      break
    else:
      continue



# function for making account
def create_account(user_data):
  while True:
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
  
  new_user = pd.DataFrame({'username': [username], 'password': [password], 'level': 0})
  user_data = pd.concat([user_data, new_user])
  user_data.to_csv("adventure_game/data/user_details.csv", index=False)
  return user_data


#function to log in
def login(user_data):
  while True:
    username = input(f"{spacing}\nPlease enter your username: ").strip()
    password = input("Please enter your password: ").strip()
    if user_data[(user_data['username'] == username) & (user_data['password'] == password)].empty:
      print(f"{spacing}\nInvalid username or password. Please try again.")
      continue
    else:
      print(
        f"{spacing}\nCorrect username and password.\nLogging In...\n{spacing}")
    break
  user_dict = user_data[user_data['username'] == username].iloc[0].to_dict()
  return user_dict


# # mini menu to ask

def login_menu():
  global user_data
  while True:
    choice = input(f"{spacing}\nWhat do you want to do?\n{spacing}\n1.Log in\n2.Create a new account\n3.Return to Menu\n{spacing}\nEnter your choice: ").strip()
    if choice == '1':
      user_dict = login(user_data)
      print(f"Login successful!\n{spacing}\n")
      return choice
      break
    elif choice == '2':
      user_data = create_account(user_data)
      print(f"Sign Up successful!\n{spacing}")
      return choice
      break
    elif choice == '3':
      print(f"{spacing}\nReturning to Menu!\n{spacing}")
      from adventure_game import menu
      return choice
      break
    else:
      print(f"{spacing}\nInvalid choice. Please try again.")
      continue

