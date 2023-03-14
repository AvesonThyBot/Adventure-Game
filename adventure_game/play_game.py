import pandas as pd 
import random 
import time 
equipment = pd.read_csv('adventure_game/data/equipments.csv')
#print(equipment.Class.loc[equipment['Class'].str.contains("Archer")])

def random_row_index(Class,level):
  filtered_equipment = equipment[(equipment['Class'] == Class) & (equipment['Level'] <= level)]
  num_rows = len(equipment)
  random_row = random.randint(0,num_rows-1)
  selected_row = equipment.iloc[random_row]
  print(selected_row)
  print(filtered_equipment)
  

def chest_roomT():
    print("T")
    print("You have entered the chest room")
    print("You open the chest")
    r_open = random.randint(0,3)
    if r_open == 1 :
        random_row_index()

def game():
    print("Welcome To W")
    print("we will first be putting you through a tutorial")
    user_choice = input("Please choose between the 3 rooms , 1,2,3")
    if user_choice == "1":
        chest_roomT()
    #elif user_choice == "2":
        #monster_roomT()
    #else :
        #empty_room()
    

        
random_row_index('Knight',15)