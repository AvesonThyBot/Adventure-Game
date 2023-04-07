#variable
spacing = "---------"

#function to call certain files as importing it may cause errors.
def login():
  from adventure_game import login


def leaderboard():
  from adventure_game import leaderboard


def load_game():
  from adventure_game import load_game


def play_game():
  from adventure_game import play_game


def return_menu():
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
      continue
# The return menu checks whether  the game returns back to the menu

#menu login function
def menu():
  print(f"Welcome to the Adventure Game!\n{spacing}")
  while True:
    menu_choice = input(
      f"What do you want to do?\n{spacing}\n1.Start Game\n2.Load Game\n3.View High Score\n4.Exit Game\n{spacing}\nEnter your choice: "
    ).strip()
    if menu_choice in [
        1, "one", "Start Game", "start game", "start", "startgame", "1.0"
    ] or menu_choice.lower() == "start game" or "startgame":
      menu_choice == 1
      login()
      return_menu()
      play_game()
      return menu_choice
    elif menu_choice in [
        2, "two", "Load Game", "load game", "load", "loadgame", "2.0"
    ] or menu_choice.lower() == "start game" or "startgame":
      menu_choice == 2
      login()
      return_menu()
      load_game()
      return menu_choice
    elif menu_choice in [
        3, "three", "Leaderboard", "leaderboard", "leader", "board", "3.0"
    ] or menu_choice.lower() == "leaderboard":
      menu_choice == 3
      leaderboard()
    elif menu_choice in [
        4, "four", "exit", "leave", "exit game", "exitgame", "4.0"
    ] or menu_choice.lower() == "exitgame" or "exit game":
      menu_choice == 4
      exit()
    else:
      print(f"{spacing}\nInvalid choice. Please try again.\n{spacing}")
      continue

# list of inputs and outputs and code directory 
menu()
