import random, re, time, pandas as pd

user_d = pd.read_csv("data/user_details.csv")

special_charecters = ['?','/','!','¬','|','.','+','_','-','^','*']
space1 = ("==============================")

def user_details():
    username = input("Please enter the username you wish to use").strip()
    while username == "":
        username = input("Please enter the username you wish to use").strip()
        continue
    password = input("Please create a password , length > 7 , must include at least one special charecters, e.g ?,!,%").strip()
    while len(password) < 7 or password == "" or not re.search(special_charecters,password):
        password = input("Please create a password").strip()
        continue
    if re.search(special_charecters,password) and len(password) >= 7 :
        user_input_2 = pd.DataFrame({'Username':[username], 'Password':[password]})
        df = [user_d,user_input_2]
        new_df = pd.concat(df)
 

def load_game_login():
     username = input("Please enter your username").strip()
     while username not in user_d ['Username']:
        username = input("Please enter your username").strip()
        continue
     password = input("Please enter your password").strip()
     while password not in user_d['Password']:
        password = input("PLease enter your password")
     if username  in user_d['Username'] and password in user_d['Password']:
        choice = user_d[user_d.iloc[:,0]== username and password]
        print(choice)
        


user_details()
load_game_login()