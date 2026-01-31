# game_score.py

# Input collection
player_name = input("Enter player name: ")

# Numeric input processing
games_played = int(input("Enter number of games played: "))

# Score data entry
total_score = int(input("Enter total score: "))

# Computation
average_score = total_score / games_played

# Output display (exact format)
print("\nPlayer:", player_name)
print("\nGames Played:", games_played)
print("\nTotal Score:", total_score)
print("\nAverage Score:", average_score)
