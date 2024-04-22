import subprocess

subprocess.run(["python", 'game.py'])

with open("player_position.txt", 'r') as file:
        content = file.read()

coordinates = content.split(": ")[1].split(" ")
player_x = int(coordinates[1])
player_y = int(coordinates[3])

print(player_x, player_y)