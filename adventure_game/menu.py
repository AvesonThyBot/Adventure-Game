def menu():
    user_choice = input("1.Start Game \n2.Load Game\n3.View High Score ")
    if user_choice == "1":
        from adventure_game import play_game
    elif user_choice == "2":
        from adventure_game import load_game
    elif user_choice == "3":
        from adventure_game import leaderboard
    else:
        menu()
menu()
