import pandas as pd

# Read data from CSV file
df = pd.read_csv('users_information.csv')

# Define function to calculate level based on experience points
def calculate_level(xp):
    level = 0
    while xp >= 50 * (level**2) + 50 * level:
        level += 1
    return level

# Apply function to calculate level for each user
df['level'] = df['xp'].apply(calculate_level)

# Print updated DataFrame 
print(df)