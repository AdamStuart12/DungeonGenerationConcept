import random

def printGrid(grid): # used for slightly nicer formatting when printing the grid
    for row in grid:
        print(row)

grid_width = 5
grid_height = 5

DIRECTIONS = ["north", "east", "south", "west"]
BEND_DIRECTIONS = ["left", "right"]

doorRoom = {"letter":"d", "shape":"rectangle", "width":2, "height":2, "origin":(0,0), "direction":"", "door_origin":(0,0)}
monsterRoom1 = {"letter":"m", "shape":"rectangle", "width":1, "height":1, "origin":(0,0), "direction":"", "door_origin":(0,0)}
monsterRoom2 = {"letter":"m", "shape":"rectangle", "width":1, "height":2, "origin":(0,0), "direction":"", "door_origin":(0,0)}
monsterRoom3 = {"letter":"m", "shape":"rectangle", "width":1, "height":3, "origin":(0,0), "direction":"", "door_origin":(0,0)}
jumpPuzzleRoom = {"letter":"j", "shape":"L", "origin":(0,0), "direction":"", "bend_direction":"left", "door_origin":(0,0)}
fireTrapRoom = {"letter":"f", "shape":"L", "origin":(0,0), "direction":"", "bend_direction":"right", "door_origin":(0,0)}

possible_rooms = [doorRoom, monsterRoom1, monsterRoom2, monsterRoom3]

grid = [["" for x in range(grid_width)] for y in range(grid_height)]


def generateGrid(grid):
    empty_count = grid_width * grid_height
    grid_empty = True
    while (empty_count > 0):
        


if __name__ == "__main__":
    printGrid(grid)
