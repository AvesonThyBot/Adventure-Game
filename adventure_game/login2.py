import pandas as pd, re, time

# read in user details from CSV
user_data = pd.read_csv("adventure_game/data/user_details.csv")

#variables
spacing = "---------"
special_chars = ['?', '/', '!', '¬', '|', '.', '+', '_', '-', '^', '*']

# function for making account
def create_account(user_data):
  while True:
    username = input("Please enter the username you wish to use: ").strip()
    if username == "":
        print("Username cannot be empty.")
        continue
    # check if the username is already taken
    if username in user_data['username'].values:
        print("Username already taken. Please choose another.")
        continue
    # check if the username is between 3 to 20 letters and contains only letters and numbers
    if not re.match("^\S[a-zA-Z0-9]{2,19}$", username): 
        print("Username must be between 3 to 20 letters and can only contain letters and numbers.")
        continue
    break

  while True:
    password = input(
      "Please create a password.\n(Password must be at least 8 characters, must include at least one special character): "
    ).strip()
    # check if the password contains only letters and numbers
    if not re.match("^[a-zA-Z0-9]{8,}$", password):
      print("Password can only contain letters and numbers.")
      continue
    # check if the password includes at least one special character
    if not any(char in special_chars for char in password):
      print("Password must include at least one special character.")
      continue
    break

  new_user = pd.DataFrame({'username': [username], 'password': [password]})
  user_data = pd.concat([user_data, new_user])
  user_data.to_csv("adventure_game/data/user_details.csv", index=False)
  return user_data


#function to log in
def login(user_data):
  while True:
    username = input(f"{spacing}\nPlease enter your username: ").strip()
    password = input("Please enter your password: ").strip()
    if user_data[(user_data['username'] == username)& (user_data['password'] == password)].empty:
      print(f"{spacing}\nInvalid username or password. Please try again.")
      continue
    else:
      print(f"{spacing}\nCorrect username and password.\nLogging In...\n{spacing}")
    break
  user_dict = user_data[user_data['username'] == username].iloc[0].to_dict()
  return user_dict

# # mini menu to ask 

while True:
  choice = input(f"Welcome to the Adventure Game!\n{spacing}\nWhat do you want to do?\n1. Log in\n2. Create a new account\n3. Exit\n{spacing}\nEnter your choice: ").strip()
  if choice == '1':
    user_dict = login(user_data)
    print(f"\nLogin successful!\n{spacing}\n")
    from adventure_game import play_game
    break
  elif choice == '2':
    user_data = create_account(user_data)
  elif choice == '3':
    print(f"{spacing}\nReturning to Menu!\n{spacing}")
    from adventure_game import menu
    break
  else:
    print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
    continue
