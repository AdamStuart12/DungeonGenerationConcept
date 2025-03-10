import random
import pygame
import sys
import copy


class Grid:
    def __init__(self):
        self.grid_width = 6
        self.grid_height = 6

        # defines all possible rooms
        doorRoom = {"letter":"d", "shape":"rectangle", "width":2, "height":2, "origin":(0,0), "direction":"","door_direction":""}
        monsterRoom1 = {"letter":"1", "shape":"rectangle", "width":1, "height":1, "origin":(0,0), "direction":"","door_direction":""}
        monsterRoom2 = {"letter":"2", "shape":"rectangle", "width":1, "height":2, "origin":(0,0), "direction":"","door_direction":""}
        monsterRoom3 = {"letter":"3", "shape":"rectangle", "width":1, "height":3, "origin":(0,0), "direction":"","door_direction":""}
        spikePuzzle = {"letter":"s", "shape":"rectangle", "width":1, "height":1, "origin":(0,0), "direction":"","door_direction":""}
        fireTrapRoom = {"letter":"f", "shape":"rectangle", "width":2, "height":1, "origin":(0,0), "direction":"","door_direction":""}
        #jumpPuzzleRoom = {"letter":"j", "shape":"L", "origin":(0,0), "direction":"", "bend_direction":"left", "door_origin":(0,0)}

        self.possible_rooms = [doorRoom, monsterRoom1, monsterRoom2, monsterRoom3, spikePuzzle, fireTrapRoom] #, jumpPuzzleRoom, fireTrapRoom]

        self.grid = []
        self.bridges = []
        self.rooms = []


    def generateGrid(self):

        grid = [["" for x in range(self.grid_width)] for y in range(self.grid_height)]
            
        empty_count = self.grid_width * self.grid_height
        grid_empty = True
        while (empty_count > 0):
            connected_room = [0,0]

            # chose a room and chose the location of the room
            room_choice = random.choice(self.possible_rooms)
            origin_x = random.randint(0, self.grid_width-1) 
            origin_y = random.randint(0, self.grid_height-1)
            room_choice["origin"] = (origin_y, origin_x)
            adjacent_rooms = []


            # make sure origin point of new room is not occupied yet
            if grid[origin_y][origin_x] != "": 
                continue

            # makes sure there is enough remaining space for chosen room
            room_volume = room_choice["height"] * room_choice["width"]
            if room_volume > empty_count:
                continue

            # makes sure the room is beside an already existing room so it can be connected via a path
            if not grid_empty: 
                adjacent_rooms = []
                for y in range(-1,2):
                    for x in range(-1,2):
                        if not (x == 0 and y == 0) and (x == 0 or y == 0): # they cannot both be 0, but 1 must be 0
                            #print(f"{y},{x}")
                            if self.boundsCheck(origin_y + y,origin_x + x):
                                if grid[origin_y + y][origin_x + x] != "":
                                    adjacent_rooms.append([origin_y + y, origin_x + x])
                
                if len(adjacent_rooms) == 0:
                    continue
                else:
                    
                    connected_room = random.choice(adjacent_rooms)

                    
                    

            # makes a list of posisitions the room will take up
            positions = []
        
            for y in range(origin_y, origin_y+room_choice["height"]):
                for x in range(origin_x, origin_x+room_choice["width"]):
                    positions.append([y,x])



            # checks if all of the positions of the room are valid, if not discard room and move on the next random room
            direction_valid = True
            for pos in positions:
                if not self.boundsCheck(pos[0], pos[1]) or grid[pos[0]][pos[1]] != "": # y coord and x coord
                    direction_valid = False
                    continue

            # if room positions are valid, add room to grid
            if direction_valid:    
                self.rooms.append(copy.deepcopy(room_choice))
                if not grid_empty:
                    self.bridges.append([connected_room,[origin_y, origin_x]])
                for pos in positions:
                    grid[pos[0]][pos[1]] = room_choice["letter"]
                    empty_count -= 1
                    
                grid_empty = False
                    
            #print(empty_count)

        self.grid = grid
        return self.rooms, self.bridges
                    
    def boundsCheck(self, y, x):
        if y < 0 or y >= self.grid_height or x < 0 or x >= self.grid_width:
            return False
        else:
            return True

    def printGrid(self): # used for slightly nicer formatting when printing the grid
        for row in self.grid:
            print(row)
        print(self.bridges)

class GUI:
    def __init__(self):
        pygame.init()
        WINDOW_WIDTH = 1280
        WINDOW_HEIGHT = 720
        LIGHT_GRAY = (200, 200, 200)
        GRAY = (100, 100, 100)
        BLACK = (0,0,0)
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon")
        clock = pygame.time.Clock()
        FPS = 30
        TILE_WIDTH = 50

        gridGen = Grid()
        rooms, bridges = gridGen.generateGrid()
        gridGen.printGrid()
        for br in bridges:

                br[0][0] = 125 + (br[0][0] * TILE_WIDTH) + (br[0][0] * 10) 
                br[0][1] = 125 + (br[0][1] * TILE_WIDTH) + (br[0][1] * 10)
                temp = br[0][0]
                br[0][0] = br[0][1]
                br[0][1] = temp
                
                br[1][0] = 125 + (br[1][0] * TILE_WIDTH) + (br[1][0] * 10) 
                br[1][1] = 125 + (br[1][1] * TILE_WIDTH) + (br[1][1] * 10)
                temp = br[1][0]
                br[1][0] = br[1][1]
                br[1][1] = temp


        room_images = []
        room_rects = []
        for i in range(len(rooms)):
            room_images.append(pygame.image.load(f"{rooms[i]['letter']}.png"))
            room_rects.append(room_images[i].get_rect())
            room_rects[i].top = 100 + (rooms[i]["origin"][0] * TILE_WIDTH) + (rooms[i]["origin"][0] * 10)
            room_rects[i].left = 100 + (rooms[i]["origin"][1] * TILE_WIDTH) + (rooms[i]["origin"][1] * 10)

        running = True
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            window.fill(LIGHT_GRAY)


            for br in bridges:
                pygame.draw.line(window, GRAY, br[0], br[1], 10)

            for i in range(len(room_images)):
                window.blit(room_images[i], room_rects[i])

          
            pygame.display.flip()
if __name__ == "__main__":
    
    #gridGen = Grid()
    #gridGen.generateGrid()
    #gridGen.printGrid()

    gui = GUI()











    
