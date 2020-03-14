import random
from tkinter import *
from math import *
class Hexagon:
    def __init__(self, row, col, canvas):
        self.row = row
        self.col = col
        self.points = [None, None, None, None, None, None] #NE, E, SE, SW, W, NW
        self.type = random.choice(Hexagon.list_of_areas)
        Hexagon.list_of_areas.remove(self.type)
        if self.type != 'desert':
            self.dice_throw = random.choice(Hexagon.list_of_dice_throw)
            Hexagon.list_of_dice_throw.remove(self.dice_throw)
        else:
            self.dice_throw = None
            Hexagon.thieves = self
        Hexagon.canvas = canvas
        ##############################################
        h = 2 * a * sin(radians(60))
        y = 2 * a + self.row * 0.5 * h
        x = 2 * a + self.col * 1.5 * a
        self.dice_throw_text = canvas.create_text(x - 0.5 * a, y - 0.5 * h, text=self.dice_throw, fill='black')
        self.canvas_hexagon = canvas.create_polygon(x - a, y, x, y, x + 0.5 * a, y - 0.5 * h, x, y - h, x - a, y - h, x - 1.5 * a,
                              y - 0.5 * h, fill=Hexagon.dic_of_type_to_color[self.type], outline='black')
        canvas.tag_lower(self.canvas_hexagon )
        canvas.tag_bind(self.canvas_hexagon, '<Button-1>', self.click_on_hexagon)
        ##############################################
    thieves  = None
    dic_of_type_to_color = {'tree':'green', 'wheat':'wheat1', 'sheep':'white', 'clay':'IndianRed3', 'stone':'grey', 'desert':'black'}
    list_of_dice_throw = [6,5,9,4,3,8,10,6,5,9,12,3,2,10,11,11,4,8]
    list_of_areas = ['tree', 'tree', 'tree', 'tree', 'wheat', 'wheat', 'wheat', 'wheat', 'sheep', 'sheep', 'sheep', 'sheep', 'clay', 'clay', 'clay', 'stone', 'stone', 'stone', 'desert']
    board = []

    def click_on_hexagon(self, event):
        if Player.move_thieves == True:
            Player.move_thieves = False
            if Hexagon.thieves.type == 'desert':
                pass
            else:
                Hexagon.canvas.itemconfig(Hexagon.thieves.dice_throw_text, fill='black')
            Hexagon.thieves = self
            Hexagon.canvas.itemconfig(Hexagon.thieves.dice_throw_text, fill='red')

    def create_board_of_hexagon(self, hexagon_canvas):
        col_to_row = {0: 3, 1: 4, 2: 5, 3: 4, 4: 3}
        col_to_start_index = {0: 2, 1: 1, 2: 0, 3: 1, 4: 2}
        for col in range(0, 5):
            temp_row = []
            index = col_to_start_index[col]
            for row in range(0, col_to_row[col]):
                temp_row.append(Hexagon(2*row + col_to_start_index[col], col, hexagon_canvas))
                index += 2
            Hexagon.board.append(temp_row)

    def print_hexagon_board(self):
        for row in Hexagon.board:
            for hexagon in row:
                print (hexagon.dice_throw, end=' ')
            print ('\n')

    def check_and_append (self, point, hexagon):
        if hexagon not in point.hexagons:
            point.hexagons.append(hexagon)

    def check_close_hexagons_and_add_points(self):
        #DOWN
        for row in Hexagon.board:
            for hexagon in row:
                if self.col == hexagon.col and hexagon.row - self.row == 2:
                    hexagon.points[5] = self.points[3]
                    hexagon.points[0] = self.points[2]
                    Hexagon.check_and_append(self, self.points[2], hexagon)
                    Hexagon.check_and_append(self, self.points[3], hexagon)
                elif hexagon.col - self.col == 1 and hexagon.row - self.row == 1:
                    hexagon.points[5] = self.points[1]
                    hexagon.points[4] = self.points[2]
                    Hexagon.check_and_append(self, self.points[1], hexagon)
                    Hexagon.check_and_append(self, self.points[2], hexagon)
                elif hexagon.col - self.col == 1 and self.row - hexagon.row == 1:
                    hexagon.points[4] = self.points[0]
                    hexagon.points[3] = self.points[1]
                    Hexagon.check_and_append(self, self.points[0], hexagon)
                    Hexagon.check_and_append(self, self.points[1], hexagon)

    def set_points_to_hexagons(self, canvas):
        for row in Hexagon.board:
            for hexagon in row:
                for index in range (0,6):
                    if hexagon.points[index] == None:
                        hexagon.points[index] = Point(canvas, hexagon.row, hexagon.col, index)
                        hexagon.points[index].hexagons.append(hexagon)
                hexagon.check_close_hexagons_and_add_points()

    def set_all_roads(self, canvas):
        for row in Hexagon.board:
            for hexagon in row:
                for point_index in range(0, 6):
                    if point_index == 5:
                        Point.set_road_between_two_points(Point, canvas, hexagon.points[5], hexagon.points[0], point_index)
                    else:
                        Point.set_road_between_two_points(Point, canvas, hexagon.points[point_index], hexagon.points[point_index + 1], point_index)

class Point:
    radius = 5
    h = 0
    canvas = None
    def __init__(self, canvas, row, col, index):
        self.hexagons = []
        self.roads = []
        self.player = None
        self.building = None
        self.can_build_on = True
        Point.point_list.append(self)
        self.id = Point.point_id
        Point.point_id += 1
        self.upgraded = False
        Point.canvas = canvas
        ##############################################
        h = 2 * a * sin(radians(60))
        Point.h = h
        self.x = 2 * a + col * 1.5 * a
        self.y = 2 * a + row * 0.5 * h
        if index == 0:
            self.x = self.x
            self.y = self.y
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill='white', outline = 'black', width = 1)
        elif index == 1:
            self.x = self.x + 0.5*a
            self.y = self.y +0.5*h
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1 , self.y1 , self.x2 , self.y2 , fill='white', outline = 'black', width = 1)
        elif index == 2:
            self.x = self.x
            self.y = self.y + h
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill='white', outline = 'black', width = 1)
        elif index == 3:
            self.x = self.x - a
            self.y = self.y + h
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1 , self.y1 , self.x2 , self.y2 , fill='white', outline = 'black', width = 1)
        elif index == 4:
            self.x = self.x - 1.5*a
            self.y = self.y + 0.5*h
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1, self.y1, self.x2 , self.y2 , fill='white', outline = 'black', width = 1)
        elif index == 5:
            self.x = self.x - a
            self.y = self.y
            self.x1 = self.x - Point.radius
            self.y1 = self.y - h - Point.radius
            self.x2 = self.x + Point.radius
            self.y2 = self.y - h + Point.radius
            self.point_on_canvas = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill='white', outline = 'black' , width = 1)
        canvas.tag_bind(self.point_on_canvas,'<Button-1>', self.click_point_function)
        #############################################
    def click_point_function(self, event):
        Player.alter_chosen_item(Player, self)
        build_button_change_according_to_chosen_item()


    point_id = 0
    point_list = []

    def set_road_between_two_points (self,canvas, point_a, point_b, point_index):
        if [point_a, point_b] not in Road.connection_list and [point_b, point_a] not in Road.connection_list:
            current_road = Road(canvas, point_a, point_b, point_index)
            point_a.roads.append(current_road)
            point_b.roads.append(current_road)
            Road.roads_list.append(current_road)
            Road.connection_list.append([point_a, point_b])

    def raise_tag_for_all_poins(self, canvas):
        for point in Point.point_list:
            canvas.tag_raise(point.point_on_canvas)

    def disable_close_points(self):
        for road in self.roads:
            if road.point_a == self:
                road.point_b.can_build_on = False
            else:
                road.point_a.can_build_on = False

    def check_if_continued_road(self):
        if self.player in (Player.current_player, None):
            for road in self.roads:
                if road in Player.current_player.roads_list:
                    return True
        return False

class Road:
    roads_list = []
    connection_list = []
    player = None
    canvas = None
    def __init__(self, canvas, point_a, point_b, point_index):
        self.point_a = point_a
        self.point_b = point_b
        self.player = None
        self.road_active = False
        self.canvas_line = canvas.create_line(self.point_a.x, self.point_a.y - Point.h, self.point_b.x, self.point_b.y - Point.h, fill='black', width=2)
        canvas.tag_bind(self.canvas_line, '<Button-1>', self.click_road_function)
        Road.canvas = canvas

    def click_road_function(self, event):
        Player.alter_chosen_item(Player, self)
        build_button_change_according_to_chosen_item()

class Player:
    master = None
    chosen_item = None
    current_player = None
    player_with_most_roads = None
    player_with_most_knights = None
    player_list = []
    id = 0
    colors = {0:'blue', 1:'yellow3', 2:'red', 3:'purple'}
    sum_dice_throw = None
    move_thieves = False
    is_first_turn = False###############################################################################################
    is_second_turn = False
    def __init__(self, root):
        self.id = Player.id
        Player.id += 1
        self.color = Player.colors[self.id]
        self.points = 0
        self.wheat = 99
        self.sheep = 99
        self.stone = 99
        self.clay = 99
        self.tree = 99
        self.knights = 0
        self.roads = 0
        self.roads_list = []
        self.cards = []
        self.did_throw_dice_yet = False
        Player.player_list.append(self)
        Player.master = root

    def check_if_winner(self):
        if self.points >= 10:
            Player.master.quit()
            print ('Player', self.id, 'Won')

    def alter_chosen_item(self, item):
        if Player.chosen_item == None:
            pass
        elif Player.chosen_item.__class__.__name__ == 'Point':
            Point.canvas.itemconfig(Player.chosen_item.point_on_canvas, outline='black', width=1)
        elif Player.chosen_item.__class__.__name__ == 'Road':
            Road.canvas.itemconfig(Player.chosen_item.canvas_line, width=2)
        Player.chosen_item = item
        if Player.chosen_item == None:
            pass
        elif Player.chosen_item.__class__.__name__ == 'Point':
            Point.canvas.itemconfig(Player.chosen_item.point_on_canvas, outline='black', width=4)
        elif Player.chosen_item.__class__.__name__ == 'Road':
            Road.canvas.itemconfig(Player.chosen_item.canvas_line, width=4)

    def update_player_stats(self):
        player_label_text.set(self.id)
        points_label_text.set(self.points)
        stone_label_text.set(self.tree)
        tree_label_text.set(self.tree)
        clay_label_text.set(self.clay)
        wheat_label_text.set(self.wheat)
        sheep_label_text.set(self.sheep)
        knight_label_text.set(self.knights)
        road_label_text.set(self.roads)
        Player.current_player.check_if_winner()

    def check_if_player_can_build_settelment(self):
        if self.clay >= 1 and self.wheat >= 1 and self.sheep >= 1 and self.tree >= 1:
            self.clay -= 1
            self.wheat -= 1
            self.sheep -= 1
            self.tree -= 1
            return True

    def check_if_player_can_build_road(self):
        if self.clay >= 1 and self.tree >= 1:
            self.clay -= 1
            self.tree -= 1
            return True

    def check_if_player_can_upgrade(self):
        if self.stone >= 3 and self.wheat >= 2:
            self.stone -= 3
            self.wheat -= 2
            return True

    def check_who_has_longest_road(self):
        for player in Player.player_list:
            if player.roads < 5 and Player.player_with_most_roads == None:
                pass

            elif player.roads >= 5 and Player.player_with_most_roads == None:
                Player.player_with_most_roads = player
                player.points += 2
                Player.player_with_most_roads.update_player_stats()

            elif player.roads > Player.player_with_most_roads.roads:
                Player.player_with_most_roads.points -= 2
                Player.player_with_most_roads.update_player_stats()
                Player.player_with_most_roads = player
                player.points += 2
                Player.player_with_most_roads.update_player_stats()

class OpeningScreen:
    OS = None
    number_of_players = 4
    def __init__(self, open_screen):
        open_screen.title = 'Catan'
        self.open_screen_label = Label(open_screen, text='Number of Players(3 or 4): ')
        self.open_screen_entry = Entry(open_screen)
        self.open_screen_button = Button(open_screen, text='Enter')
        OpeningScreen.OS = open_screen
        self.open_screen_button.bind('<Button-1>', self.open_screen_get_number_of_players)
        self.open_screen_label.pack(side='left')
        self.open_screen_entry.pack(side='left')
        self.open_screen_button.pack(side='left')

    def open_screen_get_number_of_players(self, event):
        input = self.open_screen_entry.get()
        print (input)
        if input == '3':
            OpeningScreen.number_of_players = 3
            OpeningScreen.OS.quit()
        elif input == '4':
            OpeningScreen.number_of_players = 4
            OpeningScreen.OS.quit()

def build_button_change_according_to_chosen_item():
    type = Player.chosen_item.__class__.__name__
    if type == 'Road':
        build_button_text.set('Build Road')
    elif type == 'Point':
        if Player.chosen_item.player == None:
            build_button_text.set('Build City')
        elif Player.chosen_item.upgraded == False:
            build_button_text.set('Upgrade City')
        else:
            build_button_text.set('City Upgraded')
    else:
        build_button_text.set('No Item Chosen')

def throw_dice(event):
    if Player.is_first_turn == False and Player.is_second_turn == False:
        if Player.current_player.did_throw_dice_yet == False:
            possible_dice = [1,2,3,4,5,6]
            first_dice = random.choice(possible_dice)
            second_dice = random.choice(possible_dice)
            dice1_string.set(first_dice)
            dice2_string.set(second_dice)
            Player.sum_dice_throw = first_dice + second_dice
            if Player.sum_dice_throw == 7:
                Player.move_thieves = True
            for row in Hexagon.board:
                for hexagon in row:
                    if hexagon.dice_throw == Player.sum_dice_throw:
                        for point in hexagon.points:
                            if point.player != None:
                                if hexagon.type == 'wheat' and Hexagon.thieves != hexagon:
                                    point.player.wheat += 1
                                elif hexagon.type == 'clay' and Hexagon.thieves != hexagon:
                                    point.player.clay += 1
                                elif hexagon.type == 'stone' and Hexagon.thieves != hexagon:
                                    point.player.stone += 1
                                elif hexagon.type == 'sheep' and Hexagon.thieves != hexagon:
                                    point.player.sheep += 1
                                elif hexagon.type == 'tree' and Hexagon.thieves != hexagon:
                                    point.player.tree += 1
            Player.current_player.update_player_stats()
            Player.current_player.did_throw_dice_yet = True

def check_if_player_can_build(event):
    if Player.chosen_item.__class__.__name__ == 'Point':
        if Player.chosen_item.player == None and Player.chosen_item.can_build_on == True:
            if Player.is_first_turn == True or Player.is_second_turn == True:
                Player.chosen_item.player = Player.current_player
                Player.chosen_item.canvas.itemconfig(Player.chosen_item.point_on_canvas, fill = Player.colors[Player.current_player.id])
                Player.chosen_item.disable_close_points()
                Player.current_player.points += 1
                Player.current_player.update_player_stats()

            elif Player.current_player.check_if_player_can_build_settelment() == True:
                Player.chosen_item.player = Player.current_player
                Player.chosen_item.canvas.itemconfig(Player.chosen_item.point_on_canvas, fill=Player.colors[Player.current_player.id])
                Player.chosen_item.disable_close_points()
                Player.current_player.points += 1
                Player.current_player.update_player_stats()

            elif Player.current_player.upgraded == False and Player.current_player.check_if_player_can_upgrade() == True:
                Player.chosen_item.upgraded = True
                Player.current_player.points += 1
                Player.current_player.update_player_stats()

    elif Player.chosen_item.__class__.__name__ == 'Road':
        if Player.chosen_item.player == None:

            #For the last player to have a double first turn:
            if Player.is_first_turn == True and Player.current_player.points == 1 and (Player.chosen_item.point_a.player == Player.current_player or Player.chosen_item.point_b.player == Player.current_player):
                Player.chosen_item.player = Player.current_player
                Player.chosen_item.canvas.itemconfig(Player.chosen_item.canvas_line, fill=Player.colors[Player.current_player.id])
                Player.current_player.roads += 1
                Player.current_player.roads_list.append(Player.chosen_item)
                Player.check_who_has_longest_road(Player)
                Player.current_player.update_player_stats()
                if Player.current_player == Player.player_list[-1]:
                    Player.is_second_turn = True
                end_turn_function_without_event()

            elif Player.is_second_turn == True and Player.current_player.points == 2 and (Player.chosen_item.point_a.player == Player.current_player or Player.chosen_item.point_b.player == Player.current_player):
                Player.chosen_item.player = Player.current_player
                Player.chosen_item.canvas.itemconfig(Player.chosen_item.canvas_line, fill=Player.colors[Player.current_player.id])
                Player.current_player.roads += 1
                Player.current_player.roads_list.append(Player.chosen_item)
                Player.check_who_has_longest_road(Player)
                Player.current_player.update_player_stats()
                if Player.current_player.id == 0:
                    Player.is_second_turn = False
                end_turn_function_without_event()

            #Normal Turn:
            elif Player.is_first_turn == False and Player.is_second_turn == False:
                if Player.chosen_item.point_a.player == Player.current_player or Player.chosen_item.point_b.player == Player.current_player:
                    if Player.current_player.check_if_player_can_build_road() == True:
                        Player.chosen_item.player = Player.current_player
                        Player.chosen_item.canvas.itemconfig(Player.chosen_item.canvas_line, fill=Player.colors[Player.current_player.id])
                        Player.current_player.roads += 1
                        Player.current_player.roads_list.append(Player.chosen_item)
                        Player.check_who_has_longest_road(Player)
                        Player.current_player.update_player_stats()

                elif Player.chosen_item.point_a.check_if_continued_road()== True and Player.is_second_turn == False :
                    if Player.current_player.check_if_player_can_build_road() == True:
                        Player.chosen_item.player = Player.current_player
                        Player.chosen_item.canvas.itemconfig(Player.chosen_item.canvas_line,fill=Player.colors[Player.current_player.id])
                        Player.current_player.roads += 1
                        Player.current_player.roads_list.append(Player.chosen_item)
                        Player.check_who_has_longest_road(Player)
                        Player.current_player.update_player_stats()

                elif Player.chosen_item.point_b.check_if_continued_road() == True and Player.is_second_turn == False:
                    if Player.current_player.check_if_player_can_build_road() == True:
                        Player.chosen_item.player = Player.current_player
                        Player.chosen_item.canvas.itemconfig(Player.chosen_item.canvas_line,fill=Player.colors[Player.current_player.id])
                        Player.current_player.roads += 1
                        Player.current_player.roads_list.append(Player.chosen_item)
                        Player.check_who_has_longest_road(Player)
                        Player.current_player.update_player_stats()


def end_turn_function(event):
    if Player.is_first_turn == False and Player.is_second_turn == False:
        Player.current_player.did_throw_dice_yet = False
        Player.move_thieves = False
        if Player.current_player.id == len(Player.player_list) - 1:
            Player.current_player = Player.player_list[0]
        else:
            Player.current_player = Player.player_list[Player.current_player.id + 1]
        Player.current_player.update_player_stats()
        dice1_string.set(0)
        dice2_string.set(0)

        if Player.chosen_item == None:
            pass
        elif Player.chosen_item.__class__.__name__ == 'Point':
            Point.canvas.itemconfig(Player.chosen_item.point_on_canvas, outline='black', width=1)
        elif Player.chosen_item.__class__.__name__ == 'Road':
            Road.canvas.itemconfig(Player.chosen_item.canvas_line, width=2)
        Player.chosen_item = None
        Player.sum_dice_throw = None
        Player.current_player.check_if_winner()

def end_turn_function_without_event():
    Player.current_player.did_throw_dice_yet = False
    Player.move_thieves = False
    if Player.is_first_turn == True and Player.is_second_turn == False:
        if Player.current_player.id == len(Player.player_list) - 1:
            Player.current_player = Player.player_list[0]
        else:
            Player.current_player = Player.player_list[Player.current_player.id + 1]

    elif Player.is_first_turn == True and Player.is_second_turn == True: #Another Round for the last player
        Player.is_first_turn = False

    else: #if second turn
        if Player.current_player.id != 0:
            Player.current_player = Player.player_list[Player.current_player.id - 1]
        else:
            Player.current_player = Player.player_list[0]

    Player.current_player.update_player_stats()
    dice1_string.set(0)
    dice2_string.set(0)

    if Player.chosen_item == None:
        pass
    elif Player.chosen_item.__class__.__name__ == 'Point':
        Point.canvas.itemconfig(Player.chosen_item.point_on_canvas, outline='black', width=1)
    elif Player.chosen_item.__class__.__name__ == 'Road':
        Road.canvas.itemconfig(Player.chosen_item.canvas_line, width=2)
    Player.chosen_item = None
    Player.sum_dice_throw = None
    Player.current_player.check_if_winner()
##########################################################
##########################################################
"""open_screen = Tk()
OpeningScreen(open_screen)
open_screen.mainloop()
open_screen.destroy()"""
##########################################################
##########################################################
root = Tk()
for i in range (0,OpeningScreen.number_of_players):######################
    Player(root)

Player.current_player = Player.player_list[0]
a = 50
hexagon_canvas = Canvas(root, width=a*10, height=a*10)
###############################################################
Hexagon.create_board_of_hexagon(Hexagon, hexagon_canvas)
Hexagon.set_points_to_hexagons(Hexagon, hexagon_canvas)
Hexagon.set_all_roads(Hexagon, hexagon_canvas)
Point.raise_tag_for_all_poins(Point, hexagon_canvas)
button_frame = Frame(root)
###############################################################
throw_dice_button = Button(button_frame, text='Throw Dice')
throw_dice_button.bind('<Button-1>', throw_dice)
throw_dice_button.grid(row = 0, column = 0)

dice1_string = IntVar()
dice2_string = IntVar()
dice1_string.set(0)
dice2_string.set(0)
dice1 = Label(button_frame, textvariable = dice1_string)
dice2 = Label(button_frame, textvariable = dice2_string)
dice1.grid(row = 1, column = 0)
dice2.grid(row = 1, column = 1)

build_button_text = StringVar()
build_button_index = 0
build_button_text.set('Build City')
build_button = Button(button_frame , textvariable=build_button_text)
build_button.grid(row = 2, column = 0)
build_button.bind('<Button-1>', check_if_player_can_build)

end_turn_button = Button(button_frame , text = 'End Turn')
end_turn_button.bind ('<Button-1>', end_turn_function)
end_turn_button.grid(row = 3, column = 0)

draw_card_button = Button(button_frame, text = 'Draw Card')
#draw_card_button.grid(row = 4, column = 0)

player_frame = Frame(root)
player_label_text = StringVar()
points_label_text = StringVar()
tree_label_text = StringVar()
clay_label_text = StringVar()
wheat_label_text = StringVar()
stone_label_text = StringVar()
sheep_label_text = StringVar()
knight_label_text = StringVar()
road_label_text = StringVar()
player_label_text.set(Player.current_player.id)
points_label_text.set(Player.current_player.points)
tree_label_text.set(Player.current_player.tree)
clay_label_text.set(Player.current_player.clay)
wheat_label_text.set(Player.current_player.wheat)
stone_label_text.set(Player.current_player.stone)
sheep_label_text.set(Player.current_player.sheep)
knight_label_text.set(Player.current_player.knights)
road_label_text.set(Player.current_player.roads)
variable_player_label = Label (player_frame, textvariabl = player_label_text)
variable_points_label = Label (player_frame, textvariabl = points_label_text)
variable_tree_label  = Label (player_frame, textvariabl = tree_label_text)
variable_clay_label  = Label (player_frame, textvariabl = clay_label_text)
variable_wheat_label  = Label (player_frame, textvariabl = wheat_label_text)
variable_stone_label  = Label (player_frame, textvariabl = stone_label_text)
variable_sheep_label  = Label (player_frame, textvariabl = sheep_label_text)
variable_knight_label  = Label (player_frame, textvariabl = knight_label_text)
variable_road_label  = Label (player_frame, textvariabl = road_label_text)
player_label = Label (player_frame, text='Player: ')
points_label = Label (player_frame, text='Points: ')
tree_label = Label (player_frame, text='Tree: ')
clay_label = Label (player_frame, text='Clay: ')
wheat_label = Label (player_frame, text='Wheat: ')
stone_label = Label (player_frame, text='Stone: ')
sheep_label = Label (player_frame, text='Sheep: ')
knight_label = Label (player_frame, text='Knights: ')
road_label = Label (player_frame, text='Roads: ')

player_label.grid(row=0, column=0)
points_label .grid(row=1, column=0)
tree_label.grid(row=2, column=0)
clay_label.grid(row=3, column=0)
wheat_label.grid(row=4, column=0)
stone_label.grid(row=5, column=0)
sheep_label.grid(row=6, column=0)
knight_label.grid(row=7, column=0)
road_label.grid(row=8, column=0)
variable_player_label.grid(row=0, column=1)
variable_points_label.grid(row=1, column=1)
variable_tree_label.grid(row=2, column=1)
variable_clay_label.grid(row=3, column=1)
variable_wheat_label.grid(row=4, column=1)
variable_stone_label.grid(row=5, column=1)
variable_sheep_label.grid(row=6, column=1)
variable_knight_label.grid(row=7, column=1)
variable_road_label.grid(row=8, column=1)

button_frame.grid(row = 0, column = 2)
player_frame.grid(row = 0, column = 1)
hexagon_canvas.grid(row = 0, column = 0)
root.mainloop()