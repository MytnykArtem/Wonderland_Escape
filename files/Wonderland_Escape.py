import pygame
import random
from pymongo import MongoClient
from Sounds import *
from Pictures import *
from PicturesForClass import *

#python -m cProfile -o profile_data.prof Wonderland_Escape.py
#snakeviz profile_data.prof

#Player size = x 50, y 60

# variables
# -------------------------
best_score = 0
level = "menu"
track_width = 186 * b_size
track_height = 1000
fall_jump = 0
move_scene_x = 0
move_scene_y = 0
mode = "fall"
side = "r"
checkpoints = 0
objects_on = False
game_paused = False
coins_total_menu = 0
mouse_on_buy_change = [False, False]
invincibility_timer = 0
gravity_timer = 0
# -------------------------


#
#names
#-------------------------
# b_size = block_size
# gr = ground
# p_size_x = player_size_x
# p_size_y = player_size_y
#-------------------------


pygame.init()
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption('Wonderland Escape')



class Object:
    """
    Parent class that gives many useful methods to child classes
    """
    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos:
        :param y_pos:
        """
        self.x_position = (x_pos * b_size) - b_size
        self.y_position = 700 - ((y_pos * b_size) - b_size)

    def MakeSides(self):
        """
        Writes sides of the current rect
        :return: Nothing
        """
        self.right = self.MakeSelfRect().right
        self.left = self.MakeSelfRect().left
        self.top = self.MakeSelfRect().top
        self.bottom = self.MakeSelfRect().bottom
        self.centerx = self.MakeSelfRect().centerx
        self.centery = self.MakeSelfRect().centery

    def MakeSelfRect(self):
        """
        Makes rect for default image
        :return: rect
        """
        return self.default.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - move_scene_y))


    # def MakeRect(self, surface):
    #     """
    #     Makes rect for surface.
    #     :param surface: surface tht is going to be used
    #     :return: Made rect
    #     """
    #     return surface.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - move_scene_y))

    def MakeRect2(self, s):
        """
        Returns the number ascosiated with side(s) - move_scene of the shape
        :param s: which side of the shape
        :return: the number ascosiated with side(s) - move_scene
        """
        if s == "r":
            self.return_s = self.right - move_scene_x
        elif s == "l":
            self.return_s = self.left - move_scene_x
        elif s == "t":
            self.return_s = self.top - move_scene_y
        elif s == "b":
            self.return_s = self.bottom - move_scene_y
        elif s == "x":
            self.return_s = self.centerx - move_scene_x
        elif s == "y":
            self.return_s = self.centery - move_scene_y
        return self.return_s


    def ObjectRight(self, surface):
        """
        Checks if surface has object to the right
        :param surface: surface that is going to be used
        :return: True if the surface has object to the right, else False
        """
        # TF = any(surface.right == i.MakeRect2("l") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b") for i in touch_objects)
        #      any(x.MakeSelfRect().right == i.MakeRect2("l") and x.MakeSelfRect().bottom > i.MakeRect2("t") and x.MakeSelfRect().top < i.MakeRect2("b") for i in bricks)
        # if not TF: TF = any(surface.right == i.MakeRect(i.default).left and surface.bottom > i.MakeRect(i.default).top and surface.top < i.MakeRect(i.default).bottom and i.work for i in fly_plats + jump_pads + expand_plats)
        # if not TF: TF = any(surface.right == i.MakeRect2("l") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b") for i in bricks)

        TF = False
        for i in touch_objects + boxes + break_blocks + mystery_boxes:
            if surface.right == i.MakeRect2("l") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
                TF = True
        for i in fly_plats + jump_pads + expand_plats:
            if surface.right == i.MakeSelfRect().left and surface.bottom > i.MakeSelfRect().top and surface.top < i.MakeSelfRect().bottom and i.work:
                TF = True
        # for i in bricks:
        #     if surface.right == i.MakeRect2("l") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
        #         TF = True
        return TF

    def ObjectLeft(self, surface):
        """
        Checks if surface has object to the left
        :param surface: surface that is going to be used
        :return: True if the surface has object to the left, else False
        """
        # TF = any(surface.left == i.MakeRect2("r") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b") for i in touch_objects)
        # if not TF: TF = any(surface.left == i.MakeRect(i.default).right and surface.bottom > i.MakeRect(i.default).top and surface.top < i.MakeRect(i.default).bottom and i.work for i in fly_plats + jump_pads + expand_plats)
        # if not TF: TF = any(surface.left == i.MakeRect2("r") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b") for i in bricks)

        TF = False
        for i in touch_objects + boxes + break_blocks + mystery_boxes:
            if surface.left == i.MakeRect2("r") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
                TF = True
        for i in fly_plats + jump_pads + expand_plats:
            if surface.left == i.MakeSelfRect().right and surface.bottom > i.MakeSelfRect().top and surface.top < i.MakeSelfRect().bottom  and i.work:
                TF = True
        # for i in bricks:
        #     if surface.left == i.MakeRect2("r") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
        #         TF = True
        return TF

    def ObjectUp(self, surface):
        """
        Checks if surface has object at the top
        :param surface: surface that is going to be used
        :return: True if the surface has object at the top, else False
        """
        # TF = any(surface.top == i.MakeRect2("b") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l") for i in touch_objects)
        # if not TF: TF = any(surface.top == i.MakeRect(i.default).bottom and surface.left < i.MakeRect(i.default).right and surface.right > i.MakeRect(i.default).left and i.work for i in fly_plats + jump_pads + expand_plats)
        # if not TF: TF = any(surface.top == i.MakeRect2("b") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l") for i in bricks)

        TF = False
        for i in touch_objects + boxes + break_blocks + mystery_boxes:
            if surface.top == i.MakeRect2("b") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l"):
                TF = True
        for i in fly_plats + jump_pads + expand_plats:
            if surface.top == i.MakeSelfRect().bottom and surface.left < i.MakeSelfRect().right and surface.right > i.MakeSelfRect().left  and i.work:
                TF = True
        # for i in bricks:
        #     if surface.top == i.MakeRect2("b") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l"):
        #         TF = True
        return TF

    def ObjectDown(self, surface, width = 0):
        """
        Checks if surface has object at the bottom
        :param surface: surface that is going to be used
        :return: True if the surface has object at the bottom, else False
        """
        # TF = any(surface.bottom == i.MakeRect2("t") and surface.left + width < i.MakeRect2("r") and surface.right + width > i.MakeRect2("l") for i in touch_objects)
        # if not TF: TF = any(surface.bottom == i.MakeRect(i.default).top and surface.left + width < i.MakeRect(i.default).right and surface.right + width > i.MakeRect(i.default).left and i.work for i in fly_plats + jump_pads + expand_plats)
        # if not TF: TF = any(surface.bottom == i.MakeRect2("t") and surface.left + width < i.MakeRect2("r") and surface.right + width > i.MakeRect2("l") for i in bricks)

        TF = False
        for i in touch_objects + boxes + break_blocks + mystery_boxes:
            if surface.bottom == i.MakeRect2("t") and surface.left + width < i.MakeRect2("r") and surface.right + width > i.MakeRect2("l"):
                TF = True
        for i in fly_plats + jump_pads + expand_plats:
            if surface.bottom == i.MakeSelfRect().top and surface.left + width < i.MakeSelfRect().right and surface.right + width > i.MakeSelfRect().left and i.work:
                TF = True
        return TF


    def BrickRightLeftUpDown(self, surface, side):
        """
        checks if surface has any bricks at surface's side
        :param surface: surface
        :param side: side of the surface
        :return: True or False
        """
        TF = False
        if side == "r":
            for i in bricks:
                if surface.right == i.MakeRect2("l") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
                    TF = True
        elif side == "l":
            for i in bricks:
                if surface.left == i.MakeRect2("r") and surface.bottom > i.MakeRect2("t") and surface.top < i.MakeRect2("b"):
                    TF = True
        elif side == "u":
            for i in bricks:
                if surface.top == i.MakeRect2("b") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l"):
                    TF = True
        else:
            for i in bricks:
                if surface.bottom == i.MakeRect2("t") and surface.left < i.MakeRect2("r") and surface.right > i.MakeRect2("l"):
                    TF = True

        return TF



    def FallRight(self, surface):
        # FallRightTF = self.ObjectDown(surface, surface.width)
        return self.ObjectDown(surface, surface.width)

    def FallLeft(self, surface):
        # FallLeftTF = True
        # for i in touch_objects:
        #     if surface.bottom == i.MakeRect(i.default).top and surface.left - b_size < i.MakeRect(i.default).right and surface.right - b_size > i.MakeRect(i.default).left:
        #         FallLeftTF = False
        return self.ObjectDown(surface, -surface.width)



class Player(Object):
    """
    Player class that will move on screen
    """
    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: x position
        :param y_pos: y position
        """
        # super().__init__(x_pos, y_pos)

        self.x_position = x_pos
        self.y_position = y_pos

        self.transparency = 255

        # self.default = player_default
        # self.stand_1 = player_stand_1
        # self.stand_2 = player_stand_2
        #
        # self.standing = [player_stand_1 for _ in range(10)] + [player_stand_2 for _ in range(10)]
        #
        # self.run_1 = player_run_1
        # self.run_2 = player_run_2
        # self.run_3 = player_run_3
        # self.run_4 = player_run_4
        # self.run_5 = player_run_5
        # self.run_6 = player_run_6
        # self.run_7 = player_run_7
        # self.run_8 = player_run_8
        #
        # self.running = [player_run_1, player_run_2, player_run_3, player_run_4, player_run_5, player_run_6, player_run_7, player_run_8]
        #
        # self.jump = player_jump
        # self.wall_jump = player_wall_jump
        # self.fall = player_fall

        self.apples = 0
        self.bananas = 0
        self.cherries = 0

        self.coins = 0


    def MakeSelfRect(self):
        """
        Returns a rect of the image
        """
        # self.default_rect = self.default.get_rect(bottomleft=(self.x_position, self.y_position))
        self.default_rect = pygame.Rect(self.x_position, self.y_position - p_size_y, p_size_x, p_size_y)
        return self.default_rect


    def WallJumpRightTF(self):
        """
        Checks if the player can stick to wall to the right
        :return: True or False
        """
        TF = any(self.MakeSelfRect().right == i.MakeRect(i.default).left and self.MakeSelfRect().bottom < i.MakeRect(i.default).bottom and self.MakeSelfRect().top > i.MakeRect(i.default).top for i in touch_objects + boxes + break_blocks + mystery_boxes)

        # TF = False
        # for i in touch_objects:
        #     if self.MakeSelfRect().right == i.MakeRect(i.default).left and self.MakeSelfRect().bottom < i.MakeRect(i.default).bottom and self.MakeSelfRect().top > i.MakeRect(i.default).top:
        #         TF = True
        return TF

    def WallJumpLeftTF(self):
        """
        Checks if the player can stick to wall to the left
        :return: True or False
        """
        TF = any(self.MakeSelfRect().left == i.MakeRect(i.default).right and self.MakeSelfRect().bottom < i.MakeRect(i.default).bottom and self.MakeSelfRect().top > i.MakeRect(i.default).top for i in touch_objects + boxes + break_blocks + mystery_boxes)

        # TF = False
        # for i in touch_objects:
        #     if self.MakeSelfRect().left == i.MakeRect(i.default).right and self.MakeSelfRect().bottom < i.MakeRect(i.default).bottom and self.MakeSelfRect().top > i.MakeRect(i.default).top:
        #         TF = True
        return TF


    def MoveRight(self, num = 8):
        """
        Moves player to the right
        """
        if num == 8:
            num = 8 if boosts_products[0].level == 0 else 9 if boosts_products[0].level == 1 else 10 if boosts_products[0].level == 2 else 11

        global move_scene_x
        for x in boxes:
            if self.MakeSelfRect().right == x.MakeSelfRect().left and self.MakeSelfRect().bottom > x.MakeSelfRect().top and self.MakeSelfRect().top < x.MakeSelfRect().bottom:
                for _ in range(num // 2):
                    if not x.ObjectRight(x.MakeSelfRect()) and not x.BrickRightLeftUpDown(x.MakeSelfRect(), "r"):
                        x.x_position += 1
                        x.right += 1
                        x.left += 1
                        for i in boxes:
                            if x.MakeSelfRect().top == i.MakeRect2("b") and x.MakeSelfRect().left < i.MakeRect2("r") and x.MakeSelfRect().right > i.MakeRect2("l"):
                                if not i.ObjectRight(i.MakeSelfRect()) and not i.BrickRightLeftUpDown(i.MakeSelfRect(), "r"):
                                    i.x_position += 1
                                    i.right += 1
                                    i.left += 1


                    if not self.ObjectRight(self.MakeSelfRect()):
                        if self.MakeSelfRect().centerx < 650:  # move_scene == 0 and
                            self.x_position += 1
                        elif move_scene_x == track_width - 1300 and self.MakeSelfRect().centerx >= 650 and self.MakeSelfRect().right != 1300:
                            self.x_position += 1
                        elif move_scene_x < track_width - 1300:
                            move_scene_x += 1

        for i in range(num):
            for n in boxes:
                if player_1.MakeSelfRect().right == n.MakeRect2("l") and player_1.MakeSelfRect().bottom > n.MakeRect2("t") and player_1.MakeSelfRect().top < n.MakeRect2("b"):
                    print(1)
            if not self.ObjectRight(self.MakeSelfRect()):
                # TF = any(player_1.MakeSelfRect().right == i.MakeRect2("l") and player_1.MakeSelfRect().bottom > i.MakeRect2("t") and player_1.MakeSelfRect().top < i.MakeRect2("b") for i in bricks)

                # TF = True
                # for i in bricks:
                #     if player_1.MakeSelfRect().right == i.MakeRect2("l") and player_1.MakeSelfRect().bottom > i.MakeRect2("t") and player_1.MakeSelfRect().top < i.MakeRect2("b"):
                #         TF = False
                if not player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), "r"):
                    if self.MakeSelfRect().centerx < 650:  # move_scene == 0 and
                        self.x_position += 1
                    elif move_scene_x == track_width - 1300 and self.MakeSelfRect().centerx >= 650 and self.MakeSelfRect().right != 1300:
                        self.x_position += 1
                    elif move_scene_x < track_width - 1300:
                        move_scene_x += 1

    def MoveLeft(self, num = 8):
        """
        Moves player to the left
        """
        if num == 8:
            num = 8 if boosts_products[0].level == 0 else 9 if boosts_products[0].level == 1 else 10 if boosts_products[0].level == 2 else 11

        global move_scene_x
        for x in boxes:
            if self.MakeSelfRect().left == x.MakeSelfRect().right and self.MakeSelfRect().bottom > x.MakeSelfRect().top and self.MakeSelfRect().top < x.MakeSelfRect().bottom:
                for _ in range(num // 2):
                    if not x.ObjectLeft(x.MakeSelfRect()) and not x.BrickRightLeftUpDown(x.MakeSelfRect(), "l"):
                        x.x_position -= 1
                        x.right -= 1
                        x.left -= 1
                        for i in boxes:
                            if x.MakeSelfRect().top == i.MakeRect2("b") and x.MakeSelfRect().left < i.MakeRect2("r") and x.MakeSelfRect().right > i.MakeRect2("l"):
                                if not i.ObjectLeft(i.MakeSelfRect()) and not i.BrickRightLeftUpDown(i.MakeSelfRect(), "l"):
                                    i.x_position -= 1
                                    i.right -= 1
                                    i.left -= 1

                    if not self.ObjectLeft(self.MakeSelfRect()):
                        if self.MakeSelfRect().centerx > 650:
                            self.x_position -= 1
                        elif move_scene_x == 0 and self.MakeSelfRect().centerx <= 650 and self.MakeSelfRect().left != 0:
                            self.x_position -= 1
                        elif move_scene_x > 0:
                            move_scene_x -= 1

        for i in range(num):
            if not self.ObjectLeft(self.MakeSelfRect()):
                # TF = any(player_1.MakeSelfRect().left == i.MakeRect2("r") and player_1.MakeSelfRect().bottom > i.MakeRect2("t") and player_1.MakeSelfRect().top < i.MakeRect2("b") for i in bricks)


                # TF = False
                # for i in bricks:
                #     if player_1.MakeSelfRect().left == i.MakeRect2("r") and player_1.MakeSelfRect().bottom > i.MakeRect2("t") and player_1.MakeSelfRect().top < i.MakeRect2("b"):
                #         TF = True
                if not player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), "l"):
                    if self.MakeSelfRect().centerx > 650:
                        self.x_position -= 1
                    elif move_scene_x == 0 and self.MakeSelfRect().centerx <= 650 and self.MakeSelfRect().left != 0:
                        self.x_position -= 1
                    elif move_scene_x > 0:
                        move_scene_x -= 1

    def Move_Up_Down(self, dir):
        """
        Moves player up or down once (whaen the player is on flying platform)
        :param dir: direction -1 = down, 1 = up
        :return: Nothing
        """
        global move_scene_y
        if dir > 0:
            if self.MakeSelfRect().centery > 350:
                self.y_position += 1
            elif move_scene_y == 0 and self.MakeSelfRect().centery <= 350 and self.MakeSelfRect().bottom != 0:
                self.y_position += 1
            elif move_scene_y < 0:
                move_scene_y += 1

        else:
            if self.MakeSelfRect().centery > 350:  # move_scene == 0 and
                self.y_position -= 1
            elif move_scene_y == track_height - 700 and self.MakeSelfRect().centery <= 350 and self.MakeSelfRect().top != 700:
                self.x_position -= 1
            elif move_scene_y < track_height - 700:
                move_scene_y -= 1


    def Minus_Fall_Jump_Speed(self, num):
        """
        Changes the y position of player
        :param num: fall_jump
        :return: None
        """
        # global mode
        global move_scene_y
        global fall_jump
        for i in range(abs(num)):
            # print(fall_jump)
            if num != fall_jump:
                break
            if num < 0:
                if not self.ObjectDown(self.MakeSelfRect()):
                    # TF = any(player_1.MakeSelfRect().bottom == i.MakeRect2("t") and player_1.MakeSelfRect().left < i.MakeRect2("r") and player_1.MakeSelfRect().right > i.MakeRect2("l") for i in bricks)

                    check_die()
                    if not player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), "b"):
                        if self.MakeSelfRect().centery > 350:
                            self.y_position += 1
                        elif move_scene_y == 0 and self.MakeSelfRect().centery <= 350 and self.MakeSelfRect().bottom != 0:
                            self.y_position += 1
                        elif move_scene_y < 0:
                            move_scene_y += 1

            elif num > 0:
                if not self.ObjectUp(self.MakeSelfRect()):
                    # TF = any(player_1.MakeSelfRect().top == i.MakeRect2("b") and player_1.MakeSelfRect().left < i.MakeRect2("r") and player_1.MakeSelfRect().right > i.MakeRect2("l") for i in bricks)

                    if not player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), "u"):
                        if self.MakeSelfRect().centery > 350:  # move_scene == 0 and
                            self.y_position -= 1
                        elif move_scene_y == track_height - 700 and self.MakeSelfRect().centery <= 350 and self.MakeSelfRect().top != 700:
                            self.x_position -= 1
                        elif move_scene_y < track_height - 700:
                            move_scene_y -= 1
                    else:
                        fall_jump = 0

            for x in range(len(horses)):
                if self.MakeSelfRect().bottom == horses[x].MakeSelfRect().top and self.MakeSelfRect().left < \
                        horses[x].MakeSelfRect().right and self.MakeSelfRect().right > horses[x].MakeSelfRect().left:
                    fall_jump = 20
                    horses[x].lives -= 1
            for x in range(len(mummys)):
                if self.MakeSelfRect().bottom == mummys[x].MakeSelfRect().top and self.MakeSelfRect().left < \
                        mummys[x].MakeSelfRect().right and self.MakeSelfRect().right > mummys[x].MakeSelfRect().left:
                    fall_jump = 20
                    mummys[x].lives -= 1


    def Change_Fall_Jump(self):
        """
        Checks if Minus_Fall_Jump_Speed can be called
        :return: None
        """
        global fall_jump, break_blocks, mystery_boxes, player_1, potions_1, potions_2
        if self.ObjectUp(self.MakeSelfRect()):
            fall_jump = -1
            try:
                for i in range(len(mystery_boxes)):
                    if player_1.MakeSelfRect().top == mystery_boxes[i].MakeRect2("b") and player_1.MakeSelfRect().left < mystery_boxes[i].MakeRect2("r") and player_1.MakeSelfRect().right > mystery_boxes[i].MakeRect2("l"):
                        random_answer = random.choices(['coin', 'invincibility potion', 'gravity potion'], weights=[90 if mystery_boxes[i].got_potion == False else 100,
                                                                                                                    5 if mystery_boxes[i].got_potion == False else 0,
                                                                                                                    5 if mystery_boxes[i].got_potion == False else 0], k=1)[0]
                        if random_answer == 'coin':
                            player_1.coins += 1
                        elif random_answer == 'invincibility potion':
                            mystery_boxes[i].got_potion = True
                            potions_1.append(HealthPotion(mystery_boxes[i].x_position, mystery_boxes[i].y_position - b_size))
                        elif random_answer == 'gravity potion':
                            mystery_boxes[i].got_potion = True
                            potions_2.append(GravityPotion(mystery_boxes[i].x_position, mystery_boxes[i].y_position - b_size))

                        mystery_boxes[i].hits_left -= 1
                        if mystery_boxes[i].hits_left <= 0:
                            mystery_boxes.pop(i)
            except:
                pass
        try:
            for i in range(len(break_blocks)):
                if player_1.MakeSelfRect().bottom == break_blocks[i].MakeRect2("t") and player_1.MakeSelfRect().left < break_blocks[i].MakeRect2("r") and player_1.MakeSelfRect().right > break_blocks[i].MakeRect2("l") and fall_jump <= -49:
                    break_blocks.pop(i)
                    fall_jump = 0
        except:
            pass
        if fall_jump <= 0 and self.ObjectDown(self.MakeSelfRect()):
            fall_jump = 0
        elif fall_jump <= 0 and player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), 'b'):
            fall_jump = 0
        else:
            self.Minus_Fall_Jump_Speed(fall_jump)
            if gravity_timer == 0:
                fall_jump -= 2
            else:
                if gravity_timer.Show() > 10000:
                    fall_jump -= 2
                else:
                    if find_mode() == "fall":
                        if fall_jump > -10:
                            fall_jump -= 1
                    else:
                        fall_jump -= 2

    def Transparency(self):
        """
        Changes player's trancparecy up if it is below 254
        :return: None
        """
        if self.transparency < 255:
            self.transparency += 10
        else:
            self.transparency = 255


    def CheckFruitCoin(self):
        """
        Checks if the player can collect any fruit or coin
        :return: None
        """
        global fruits
        global coins
        global invincibility_timer, gravity_timer
        for x in range(len(fruits)):
                try:
                    if player_1.MakeSelfRect().colliderect(fruits[x].MakeSelfRect()):
                        if fruits[x].name == "a":
                            self.apples += 1
                        elif fruits[x].name == "b":
                            self.bananas += 1
                        elif fruits[x].name == "c":
                            self.cherries += 1
                        fruits.pop(x)
                        collect_fruit_sound.play()
                except:
                    pass

        for x in range(len(coins)):
                try:
                    if player_1.MakeSelfRect().colliderect(coins[x].MakeSelfRect()):
                        self.coins += 1
                        coins.pop(x)
                        collect_coin_sound.play()
                except:
                    pass

        for x in range(len(potions_1)):
                try:
                    if player_1.MakeSelfRect().colliderect(potions_1[x].MakeSelfRect()):
                        potions_1.pop(x)
                        invincibility_timer = Timer(0)
                        invincibility_timer.Start()
                        collect_fruit_sound.play()
                except:
                    pass

        for x in range(len(potions_2)):
                try:
                    if player_1.MakeSelfRect().colliderect(potions_2[x].MakeSelfRect()):
                        potions_2.pop(x)
                        gravity_timer = Timer(0)
                        gravity_timer.Start()
                        collect_fruit_sound.play()
                except:
                    pass

    def CheckDieAnimal(self):
        """
        Checks if any animal died
        :return: None
        """
        global horses
        global mummys
        for x in range(len(horses)):
            try:
                if horses[x].lives <= 0:
                    horses.pop(x)
                    tap_sound.play()
            except:
                pass

        for x in range(len(mummys)):
            try:
                if mummys[x].lives <= 0:
                    mummys.pop(x)
                    tap_sound.play()
            except:
                pass


class Ground(Object):
    """
    Class that represents a block of ground and grass
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.grass = ground_grass
        self.default = ground_default

        self.MakeSides()

class BrickBlock(Object):
    """
    Class that represents a block of bricks
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.default = brick_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SilverBlock(Object):
    """
    Class that represents a silver block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.default = silver_block_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class GoldBlock(Object):
    """
    Class that represents a gold block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.default = gold_block_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class BrownBlock(Object):
    """
    Class that represents a copper block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.default = brown_block_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class OrangeBlock(Object):
    """
    Class that represents an orange block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.default = orange_block_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


class SmallSilverBlock(Object):
    """
    Class that represents a small silver block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        # self.y_position -= 1

        self.default = pygame.image.load("Block_Silver.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size / 2, b_size / 2))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SmallGoldBlock(Object):
    """
    Class that represents a small gold block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        # self.y_position -= 1

        self.default = pygame.image.load("Block_Gold.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size / 2, b_size / 2))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SmallBrownBlock(Object):
    """
    Class that represents a small copper block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        # self.y_position -= 1

        self.default = pygame.image.load("Block_Brown.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size / 2, b_size / 2))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SmallOrangeBlock(Object):
    """
    Class that represents a small orange block
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        # self.y_position -= 1

        self.default = pygame.image.load("Block_Orange.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size / 2, b_size / 2))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


class GoldThickPlat(Object):
    """
    Class that represents a thick gold platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 3 * 2

        self.default = pygame.image.load("Plat_Thick_Gold.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 3))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SilverThickPlat(Object):
    """
    Class that represents a thick silver platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 3 * 2

        self.default = pygame.image.load("Plat_Thick_Silver.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 3))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class BrownThickPlat(Object):
    """
    Class that represents a thick copper platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 3 * 2

        self.default = pygame.image.load("Plat_Thick_Brown.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 3))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class OrangeThickPlat(Object):
    """
    Class that represents a thick orange platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 3 * 2

        self.default = pygame.image.load("Plat_Thick_Orange.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 3))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


class GoldThinPlat(Object):
    """
    Class that represents a thin gold platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 10 * 9


        self.default = pygame.image.load("Plat_Thin_Gold.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 10))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SilverThinPlat(Object):
    """
    Class that represents a thin silver platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 10 * 9

        self.default = pygame.image.load("Plat_Thin_Silver.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 10))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class WoodThinPlat(Object):
    """
    Class that represents a thin wooden platform
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.y_position = self.y_position - b_size / 10 * 9

        self.default = pygame.image.load("Plat_Thin_Wood.png").convert_alpha()
        self.default = pygame.transform.scale(self.default, (b_size, b_size / 10))

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


class StartGame(Object):
    """
    Class for stage and arrow at the start of the game
    """
    def __init__(self, x_pos, y_pos, num):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param num: arrow if 1, else stage
        """
        super().__init__(x_pos, y_pos)

        self.start_arrow = pygame.image.load('Start_arrow.png').convert_alpha()
        self.start_arrow = pygame.transform.scale(self.start_arrow, (b_size // 10 * 6, b_size))
        self.start_stage = pygame.image.load('Start_stage.png').convert_alpha()
        self.start_stage = pygame.transform.scale(self.start_stage, (b_size, b_size // 4))

        if num == 1:
            self.default = self.start_arrow
        else:
            self.default = self.start_stage
            self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class Checkpoint(Object):
    """
    Class for checkpoint (for respawning)
    """
    def __init__(self, x_pos, y_pos, TF = False, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param TF: If the checkpoint on or not
        :param m: False if the object is being made, True if the object is made
        """

        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.checkpoint_TF = TF

        self.no_checkpoint = pygame.image.load("Checkpoint_No.png").convert_alpha()

        self.checkpoint_1 = pygame.image.load("Checkpoint_Flag_1.png").convert_alpha()
        self.checkpoint_2 = pygame.image.load("Checkpoint_Flag_2.png").convert_alpha()
        self.checkpoint_3 = pygame.image.load("Checkpoint_Flag_3.png").convert_alpha()
        self.checkpoint_4 = pygame.image.load("Checkpoint_Flag_4.png").convert_alpha()
        self.checkpoint_5 = pygame.image.load("Checkpoint_Flag_5.png").convert_alpha()
        self.checkpoint_6 = pygame.image.load("Checkpoint_Flag_6.png").convert_alpha()

        self.checkpointing = [self.checkpoint_1, self.checkpoint_1,
                              self.checkpoint_2, self.checkpoint_2,
                              self.checkpoint_3, self.checkpoint_3,
                              self.checkpoint_4, self.checkpoint_4,
                              self.checkpoint_5, self.checkpoint_5,
                              self.checkpoint_6, self.checkpoint_6]

        if not self.checkpoint_TF:
            self.default = self.no_checkpoint
        else:
            self.default = self.checkpoint_1


    def CheckPoint(self):
        """
        Checks if the checkpoint can be turned on
        :return: None
        """
        global checkpoints
        # if not self.checkpoint_TF:
        #     self.default = self.no_checkpoint
        # else:
        #     self.default = self.checkpoint_1
        if not self.checkpoint_TF:
            if player_1.MakeSelfRect().colliderect(self.MakeSelfRect()):
                self.checkpoint_TF = True
                checkpoints += 1

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class EndGame(Object):
    """
    Class for prise at the end (for finishing the game)
    """
    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.end_no = pygame.image.load('End_No.png').convert_alpha()
        self.end_no = pygame.transform.scale(self.end_no, (b_size * 2, b_size * 2))
        self.end_1 = pygame.image.load('End_1.png').convert_alpha()
        self.end_1 = pygame.transform.scale(self.end_1, (b_size * 2, b_size * 2))
        self.end_2= pygame.image.load('End_2.png').convert_alpha()
        self.end_2 = pygame.transform.scale(self.end_2, (b_size * 2, b_size * 2 - b_size // 10))
        self.end_3 = pygame.image.load('End_3.png').convert_alpha()
        self.end_3 = pygame.transform.scale(self.end_3, (b_size * 2, b_size * 2 - b_size // 5))

        self.default = self.end_1

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def CheckPressed(self):
        """
        Checks if pressed
        :return: True if pressed, else False
        """
        if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
            return True
        else:
            return False

    def CheckChange(self):
        """
        Checks if pressed and changes default image and ends the game
        :return: None
        """
        if self.CheckPressed():
            if self.default == self.end_1:
                self.default = self.end_2
        if self.default == self.end_2:
            self.default = self.end_3
        elif self.default == self.end_3:
            global level
            global best_score
            global coins_total_menu
            coins_total_menu += player_1.coins
            coins_total_menu += player_1.coins + 0 if boosts_products[3].level == 0 \
                else round(player_1.coins * 0.1) if boosts_products[3].level == 1 \
                else round(player_1.coins * 0.2) if boosts_products[3].level == 2 \
                else round(player_1.coins * 0.4)

            timer.End()
            timer_boosts = timer.Show()
            timer_boosts -= 0 if boosts_products[4].level == 0 \
                else 5000 if boosts_products[4].level == 1 \
                else 10000 if boosts_products[4].level == 2 \
                else 20000
            if best_score == 0:
                best_score = timer_boosts
            else:
                if timer_boosts < best_score:
                    best_score = timer_boosts
            # reset_database()
            level = "menu"


class Snake(Object):
    """
    Moving snake that will kill the player
    """
    def __init__(self, x_pos, y_pos, pos_2, pos_1 = -1, side = "r", m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param pos_2: position_2, boundary for the object
        :param pos_1: position_1, boundary for the object
        :param side: to which side is the object turned on
        :param m: False if the object is being made, True if the object is made
        """

        # super().__init__(x_pos, y_pos)
        # if pos_1 == -1:
        #     self.position_1 = self.x_position
        # else:
        #     self.position_1 = pos_1
        # self.position_2 = (pos_2 * b_size) - b_size
        #
        # self.side = "r"

        if not m:
            super().__init__(x_pos, y_pos)
            self.position_2 = (pos_2 * b_size)
        else:
            self.x_position = x_pos
            self.y_position = y_pos
            self.position_2 = pos_2

        if pos_1 == -1:
            self.position_1 = self.x_position
        else:
            self.position_1 = pos_1

        self.side = side

        self.default = snake_default
        self.snake_1 = snake_1
        self.snake_2 = snake_2
        self.snake_3 = snake_3

        self.going = [self.default, self.default, self.default, self.default, self.default, self.snake_1, self.snake_1, self.snake_1, self.snake_1, self.snake_1, self.snake_2, self.snake_2, self.snake_2, self.snake_2, self.snake_2, self.snake_3, self.snake_3, self.snake_3, self.snake_3, self.snake_3]


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def Move(self):
        """
        Moves the snake
        :return: None
        """
        for _ in range(3 if boosts_products[2].level > 1 else 2 ):
            if self.side == "r":
                if self.MakeSelfRect().right + move_scene_x != self.position_2:
                    self.x_position += 1
                else:
                    self.side = "l"

            else:
                if self.MakeSelfRect().left + move_scene_x != self.position_1:
                    self.x_position -= 1
                else:
                    self.side = "r"
        # if self.side == "r":
        #     for i in range(3):
        #         if not self.ObjectRight(self.MakeSelfRect()) and self.FallRight(self.MakeSelfRect()):
        #             if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #                 self.side = "l"
        #             else:
        #                 self.x_position += 1
        #         else:
        #             self.side = "l"
        #
        # if self.side == "l":
        #     for i in range(3):
        #         if not self.ObjectLeft(self.MakeSelfRect()) and self.FallLeft(self.MakeSelfRect()):
        #             if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #                 self.side = "r"
        #             else:
        #                 self.x_position -= 1
        #         else:
        #             self.side = "r"

class Mushroom(Object):
    """
    Moving mushroom that will kill the player
    """
    def __init__(self, x_pos, y_pos, pos_2, pos_1 = -1, side = "r", m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param pos_2: position_2, boundary for the object
        :param pos_1: position_1, boundary for the object
        :param side: to which side is the object turned on
        :param m: False if the object is being made, True if the object is made
        """
        if not m:
            super().__init__(x_pos, y_pos)
            self.position_2 = (pos_2 * b_size)
        else:
            self.x_position = x_pos
            self.y_position = y_pos
            self.position_2 = pos_2

        if pos_1 == -1:
            self.position_1 = self.x_position
        else:
            self.position_1 = pos_1

        self.side = side

        self.default = mushroom_default
        self.mushroom_1 = mushroom_1
        self.mushroom_2 = mushroom_2
        self.mushroom_3 = mushroom_3
        self.mushroom_4 = mushroom_4
        self.mushroom_5 = mushroom_5
        self.mushroom_6 = mushroom_6
        self.mushroom_7 = mushroom_7

        self.going = [self.default, self.default,
                        self.mushroom_1, self.mushroom_1,
                        self.mushroom_2, self.mushroom_2,
                        self.mushroom_3, self.mushroom_3,
                        self.mushroom_4, self.mushroom_4,
                        self.mushroom_5, self.mushroom_5,
                        self.mushroom_6, self.mushroom_6,
                        self.mushroom_7, self.mushroom_7
                      ]



        # while not self.ObjectLeft(self.MakeSelfRect()) and self.FallLeft(self.MakeSelfRect()):
        #     self.x_position -= 1
        # self.position_1 = self.x_position
        #
        # while not self.ObjectRight(self.MakeSelfRect()) and self.FallRight(self.MakeSelfRect()):
        #     self.x_position += 1
        # self.position_2 = self.x_position

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def Move(self):
        """
        Moves the mushroom
        :return: None
        """
        for _ in range(5 if boosts_products[0].level == 0 else 4 if boosts_products[0].level == 1 else 3):
            if self.side == "r":
                if self.MakeSelfRect().right + move_scene_x != self.position_2:
                    self.x_position += 1
                else:
                    self.side = "l"

            else:
                if self.MakeSelfRect().left + move_scene_x != self.position_1:
                    self.x_position -= 1
                else:
                    self.side = "r"

        # if self.side == "r":
        #     for i in range(4):
        #         if not self.ObjectRight(self.MakeSelfRect()) and self.FallRight(self.MakeSelfRect()):
        #             self.x_position += 1
        #             # if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #             #     self.side = "l"
        #             # else:
        #             #     self.x_position += 1
        #         else:
        #             self.side = "l"
        #
        # if self.side == "l":
        #     for i in range(4):
        #         if not self.ObjectLeft(self.MakeSelfRect()) and self.FallLeft(self.MakeSelfRect()):
        #             self.x_position -= 1
        #             # if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #             #     self.side = "r"
        #             # else:
        #             #     self.x_position -= 1
        #         else:
        #             self.side = "r"

class Horse(Object):
    """
    Moving horse that will kill the player
    """
    def __init__(self, x_pos, y_pos, pos_2, pos_1 = -1, side = "r", m = False, lives = 4):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param pos_2: position_2, boundary for the object
        :param pos_1: position_1, boundary for the object
        :param side: to which side is the object turned on
        :param m: False if the object is being made, True if the object is made
        :param lives: how many lives does the object have
        """
        # super().__init__(x_pos, y_pos)
        # if pos_1 == -1:
        #     self.position_1 = self.x_position
        # else:
        #     self.position_1 = pos_1
        # self.position_2 = (pos_2 * b_size) - b_size

        if not m:
            super().__init__(x_pos, y_pos)
            self.position_2 = (pos_2 * b_size)
        else:
            self.x_position = x_pos
            self.y_position = y_pos
            self.position_2 = pos_2

        if pos_1 == -1:
            self.position_1 = self.x_position
        else:
            self.position_1 = pos_1

        self.side = side

        self.lives = lives

        self.size_x = b_size * 2
        self.size_y = b_size * 2

        # self.side = "r"

        self.run_1 = horse_run_1
        self.run_2 = horse_run_2
        self.run_3 = horse_run_3
        self.run_4 = horse_run_4
        self.run_5 = horse_run_5
        self.run_6 = horse_run_6

        self.hit_1 = horse_hit_1
        self.hit_2 = horse_hit_2
        self.hit_3 = horse_hit_3
        self.hit_4 = horse_hit_4
        self.hit_5 = horse_hit_5

        self.default = self.run_1

        self.run = [self.run_1] * 3 + [self.run_2] * 3 + [self.run_3] * 3 + [self.run_4] * 3 + [self.run_5] * 3 + [self.run_6] * 3
        self.hit = [self.hit_1, self.hit_2, self.hit_3, self.hit_4, self.hit_5]

        self.default_to_die = False


    def CheckMode(self):
        """
        Checks if the horse can eat player
        :return: None
        """
        if self.side == "r":
            if player_1.MakeSelfRect().left <= self.MakeSelfRect().right + b_size and player_1.MakeSelfRect().left >= self.MakeSelfRect().right and player_1.MakeSelfRect().top < self.MakeSelfRect().bottom and player_1.MakeSelfRect().bottom > self.MakeSelfRect().top:
                if self.default not in self.hit:
                    self.default = self.hit_1
            else:
                pass
                # self.mode = "run"

        elif self.side == "l":
            if player_1.MakeSelfRect().right >= self.MakeSelfRect().left - b_size and player_1.MakeSelfRect().right <= self.MakeSelfRect().left and player_1.MakeSelfRect().top < self.MakeSelfRect().bottom and player_1.MakeSelfRect().bottom > self.MakeSelfRect().top:
                if self.default not in self.hit:
                    self.default = self.hit_1
            else:
                pass
                # self.mode = "run"

        # return self.mode

    def ChangeDefault(self):
        """
        Changes the default image
        :return: None
        """
        if self.default in self.run:
            self.default = self.run[0]
            self.run.append(self.run[0])
            self.run.pop(0)
            # self.default not in self.hit

        else:
            if self.default == self.hit_1:
                self.default = self.hit_2
            elif self.default == self.hit_2:
                self.default = self.hit_3
            elif self.default == self.hit_3:
                self.default = self.hit_4
            elif self.default == self.hit_4:
                self.default = self.hit_5
            elif self.default == self.hit_5:
                self.default = self.run[0]
                self.run.append(self.run[0])
                self.run.pop(0)
            # if self.side == "r":
            #     self.default = pygame.transform.flip(self.hit[0], True, False)
            # else:
            #     self.default = self.hit[0]
            # self.hit.append(self.hit[0])
            # self.hit.pop(0)

    def MakeSelfRect(self):
        """
        Makes rect for default image
        :return: rect
        """
        if self.side == "r":
            return self.default.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - move_scene_y))
        else:
            return self.default.get_rect(bottomright=(self.x_position - move_scene_x + self.size_x, self.y_position - move_scene_y))

    def Move(self):
        """
        Moves the horse
        :return: None
        """
        if self.default not in self.hit:
            for _ in range(4 if boosts_products[0].level == 0 or 1 or 2 else 3):
                if self.side == "r":
                    if self.MakeSelfRect().right + move_scene_x != self.position_2:
                        self.x_position += 1
                    else:
                        self.side = "l"

                else:
                    if self.MakeSelfRect().left + move_scene_x != self.position_1:
                        self.x_position -= 1
                    else:
                        self.side = "r"
        # if self.default not in self.hit:
        #     if self.side == "r":
        #         for i in range(2):
        #             if not self.ObjectRight(self.MakeSelfRect()) and self.FallRight(self.MakeSelfRect()):
        #                 if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #                     self.side = "l"
        #                 else:
        #                     self.x_position += 1
        #             else:
        #                 self.side = "l"
        #
        #     elif self.side == "l":
        #         for i in range(2):
        #             if not self.ObjectLeft(self.MakeSelfRect()) and self.FallLeft(self.MakeSelfRect()):
        #                 if move_scene_x == track_width - 1300 and self.MakeSelfRect().right == 1300:
        #                     self.side = "r"
        #                 else:
        #                     self.x_position -= 1
        #             else:
        #                 self.side = "r"
        #
        # else:
        #     if self.side == "r":
        #         pass
        #
        #     elif self.side == "l":
        #         pass

class Mummy(Object):
    """
    Moving mummy that will kill the player
    """
    def __init__(self, x_pos, y_pos, pos_2, pos_1 = -1, side = "r", m = False, lives = 5):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param pos_2: position_2, boundary for the object
        :param pos_1: position_1, boundary for the object
        :param side: to which side is the object turned on
        :param m: False if the object is being made, True if the object is made
        :param lives: how many lives does the object have
        """
        # super().__init__(x_pos, y_pos)
        #
        # self.position_1 = (pos_1 * b_size) - b_size
        # self.position_2 = (pos_2 * b_size) - b_size

        if not m:
            super().__init__(x_pos, y_pos)
            self.position_2 = (pos_2 * b_size)
        else:
            self.x_position = x_pos
            self.y_position = y_pos
            self.position_2 = pos_2

        if pos_1 == -1:
            self.position_1 = self.x_position
        else:
            self.position_1 = pos_1

        self.side = side

        self.size_x = b_size * 1.5
        self.size_y = b_size * 2

        self.lives = lives

        self.mode = "stand"

        # self.side = "l"

        self.run_1 = mum_run_1
        self.run_2 = mum_run_2
        self.run_3 = mum_run_3
        self.run_4 = mum_run_4
        self.run_5 = mum_run_5
        self.run_6 = mum_run_6

        self.hit_1 = mum_hit_1
        self.hit_2 = mum_hit_2
        self.hit_3 = mum_hit_3
        self.hit_4 = mum_hit_4
        self.hit_5 = mum_hit_5

        self.stand_1 = mum_stand_1
        self.stand_2 = mum_stand_2

        self.default = self.run_1

        self.run = [self.run_1] * 2 + [self.run_2] * 2 + [self.run_3] * 2 + [self.run_4] * 2 + [self.run_5] * 2 + [self.run_6] * 2
        self.hit = [self.hit_1, self.hit_2, self.hit_3, self.hit_4, self.hit_5]
        self.stand = [self.stand_1] * 4 + [self.stand_2] * 4

        self.default_to_die = False


    def CheckMode(self):
        """
        Checks if the mummy can hit the player
        :return: None
        """
        if self.side == "r":
            if player_1.MakeSelfRect().left <= self.MakeSelfRect().right + b_size // 2 and player_1.MakeSelfRect().left >= self.MakeSelfRect().right and player_1.MakeSelfRect().top < self.MakeSelfRect().bottom and player_1.MakeSelfRect().bottom > self.MakeSelfRect().top:
                if self.default not in self.hit:
                    self.default = self.hit_1
        elif self.side == "l":
            if player_1.MakeSelfRect().right >= self.MakeSelfRect().left - b_size // 2 and player_1.MakeSelfRect().right <= self.MakeSelfRect().left and player_1.MakeSelfRect().top < self.MakeSelfRect().bottom and player_1.MakeSelfRect().bottom > self.MakeSelfRect().top:
                if self.default not in self.hit:
                    self.default = self.hit_1

        if self.side == "l":
            if self.MakeSelfRect().right - move_scene_x - b_size * 2 <= self.position_1 and self.default not in self.stand:
                self.default = self.stand[0]
        elif self.side == "r":
            if self.MakeSelfRect().left + move_scene_x + b_size * 2 >= self.position_2 and self.default not in self.stand:
                self.default = self.stand[0]

    def ChangeDefault(self):
        """
        Changes the default image
        :return: None
        """
        if self.default in self.run:
            self.default = self.run[0]
            self.run.append(self.run[0])
            self.run.pop(0)

        else:
            if self.default == self.hit_1:
                self.default = self.hit_2
            elif self.default == self.hit_2:
                self.default = self.hit_3
            elif self.default == self.hit_3:
                self.default = self.hit_4
            elif self.default == self.hit_4:
                self.default = self.hit_5
            elif self.default == self.hit_5:
                self.default = self.run[0]
                self.run.append(self.run[0])
                self.run.pop(0)
            # if self.side == "r":
            #     self.default = pygame.transform.flip(self.hit[0], True, False)
            # else:
            #     self.default = self.hit[0]
            # self.hit.append(self.hit[0])
            # self.hit.pop(0)

    def MakeSelfRect(self):
        """
        Makes rect for default image
        :return: rect
        """
        if self.side == "r":
            return self.default.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - move_scene_y))
        else:
            return self.default.get_rect(bottomright=(self.x_position - move_scene_x + self.size_x, self.y_position - move_scene_y))

    def Move(self):
        """
        Moves the mummy
        :return: None
        """
        if self.default not in self.hit:
            for i in range(4 if boosts_products[0].level == 0 else 3):
                if player_1.MakeSelfRect().right < self.MakeSelfRect().left:
                    self.side = "l"
                    if self.MakeSelfRect().right - move_scene_x - b_size * 2 > self.position_1:
                        self.x_position -= 1
                    else:
                        self.mode = "stand"
                elif player_1.MakeSelfRect().left < self.MakeSelfRect().right:
                    self.side = "r"
                    if self.MakeSelfRect().left + move_scene_x + b_size * 2 < self.position_2:
                        self.x_position += 1
                    else:
                        self.mode = "stand"

        # if self.default not in self.hit:
        #     if self.side == "r":
        #         for i in range(3):
        #             if self.MakeSelfRect().left + move_scene_x + b_size * 2 < self.position_2:
        #                 self.x_position += 1
        #
        #
        #     elif self.side == "l":
        #         for i in range(3):
        #             if self.MakeSelfRect().right - move_scene_x - b_size * 2 > self.position_1:
        #                 self.x_position -= 1


class FlyPlat(Object):
    """
    Flying platform for player
    """
    def __init__(self, x_pos, y_pos, pos_2, fly, pos_1 = -1, work = objects_on, dir = -1, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param pos_2: position_2, boundary for the object
        :param fly: how to fly
        :param pos_1: position_1, boundary for the object
        :param work: is it working or not
        :param dir: dirrection the object is going to now
        :param m: False if the object is being made, True if the object is made
        """
        # super().__init__(x_pos, y_pos)

        # self.position_1 = (pos_1 * b_size) - b_size
        # self.position_2 = 700 - ((pos_2 * b_size) - b_size)

        if not m:
            super().__init__(x_pos, y_pos)
            self.position_2 = (pos_2 * b_size) - b_size
        else:
            self.x_position = x_pos
            self.y_position = y_pos
            self.position_2 = pos_2

        if pos_1 == -1:
            self.position_1 = self.x_position
        else:
            self.position_1 = pos_1

        self.work = work

        self.transparency = 125

        self.fly = fly
        self.num = 5

        if dir == -1:
            if fly == "RightLeft":
                if pos_1 == -1:
                    self.position_1 = self.x_position
                else:
                    self.position_1 = pos_1
                self.position_2 = (pos_2 * b_size) - b_size
                self.direction = "r"
            else:
                if pos_1 == -1:
                    self.position_1 = self.y_position
                else:
                    self.position_1 = pos_1
                self.position_2 = 700 - ((pos_2 * b_size) - b_size)
                self.direction = "d"

        else:
            self.direction = dir


        self.default = fly_plat_default
        self.fly_plat_1 = fly_plat_1
        self.fly_plat_2 = fly_plat_2
        self.fly_plat_3 = fly_plat_3

        self.going = [self.default, self.default, self.fly_plat_1, self.fly_plat_1,
                           self.fly_plat_2, self.fly_plat_2, self.fly_plat_3, self.fly_plat_3]

        self.default_2 = fly_plat_default_2


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def MakeSelfRectFruit(self):
        """
        Makes rect for fruit
        :return: None
        """
        return self.default_2.get_rect(bottomleft=(self.x_position - move_scene_x + b_size // 3, self.y_position - move_scene_y - b_size // 20))

    def Move(self):
        """
        Moves the flying platform
        :return: None
        """
        if self.work:
            global fall_jump
            global player_1
            for x in range(self.num):
                if self.fly == "UpDown":
                    if self.MakeSelfRect().bottom == player_1.MakeSelfRect().top and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                        fall_jump = -1
                    if self.direction == "u":
                        if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                            if player_1.ObjectUp(player_1.MakeSelfRect()):
                                self.direction = "d"
                                reset()
                    else:
                        if self.MakeSelfRect().bottom == player_1.MakeSelfRect().top and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                            self.direction = "u"
                            fall_jump = -1
                        if self.MakeSelfRect().bottom == player_1.MakeSelfRect().top and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                            if player_1.ObjectDown(player_1.MakeSelfRect()):
                                self.direction = "u"
                                reset()

                if self.fly == "RightLeft":
                    if self.direction == "r":
                        if self.MakeSelfRect().left + move_scene_x != self.position_2:
                            self.x_position += 1
                            if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                                player_1.MoveRight(1)
                                # player_1.x_position += 1
                        else:
                            self.direction = "l"

                    if self.direction == "l":
                        if self.MakeSelfRect().left + move_scene_x != self.position_1:
                            self.x_position -= 1
                            if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                                player_1.MoveLeft(1)
                                # player_1.x_position -= 1
                        else:
                            self.direction = "r"
                else:
                    if self.direction == "d":
                        if self.MakeSelfRect().bottom + move_scene_y != self.position_2:
                            if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                                player_1.Move_Up_Down(1)
                                fall_jump = 0
                            self.y_position += 1
                        else:
                            self.direction = "u"

                    if self.direction == "u":
                        if self.MakeSelfRect().bottom + move_scene_y != self.position_1:
                            if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
                                player_1.Move_Up_Down(-1)
                                fall_jump = 0
                            self.y_position -= 1
                        else:
                            self.direction = "d"

class JumpPad(Object):
    """
    Jump pad for higher jump
    """

    def __init__(self, x_pos, y_pos, work = objects_on, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param work: is it working or not
        :param m: m
        """
        # super().__init__(x_pos, y_pos)

        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.work = work

        self.transparency = 125

        self.jump_pad_1 = jump_pad_1
        self.jump_pad_2 = jump_pad_2
        self.jump_pad_3 = jump_pad_3
        self.jump_pad_4 = jump_pad_4
        self.jump_pad_5 = jump_pad_5
        self.default_2 = jump_pad_default_2

        self.default = self.jump_pad_1


    def MakeSelfImage(self):
        """
        Returns the default picture
        :return: default image
        """
        return self.default

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def MakeSelfRectFruit(self):
        """
        Makes rect for the fruit
        :return: rect
        """
        return self.default_2.get_rect(bottomleft=(self.x_position - move_scene_x + b_size // 3, self.y_position - move_scene_y - b_size // 10))

    def CheckJump(self):
        """
        Checks if the player on the JumpPad
        :return: None
        """
        if self.work:
            global fall_jump
            if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left and self.default == self.jump_pad_1:
                self.default = self.jump_pad_4
                fall_jump = 40
                bounce_sound.play()

            elif self.default == self.jump_pad_1:
                pass
            elif self.default == self.jump_pad_2:
                self.default = self.jump_pad_1
            elif self.default == self.jump_pad_3:
                self.default = self.jump_pad_2
            elif self.default == self.jump_pad_4:
                self.default = self.jump_pad_3

class ExpandPlat(Object):
    """
    platform that expands for player to stand on it
    """

    def __init__(self, x_pos, y_pos, expand, i = b_size, work = objects_on, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param expand: how much to expand
        :param i: how much it has already expanded
        :param work: is it working or not
        :param m: False if the object is being made, True if the object is made
        """

        # super().__init__(x_pos, y_pos)
        # self.position_2 = (pos_2 * b_size) - b_size
        # self.original_x = self.x_position

        if not m:
            super().__init__(x_pos, y_pos)
            self.y_position -= b_size - b_size / 5
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.work = work

        self.transparency = 125

        self.stop_i = expand
        self.i = i

        self.original = expand_plat_original
        self.default = expand_plat_default
        self.default_2 = expand_plat_default_2

        # while self.MakeSelfRect().right <= self.position_2 - move_scene_x:
        #     self.x_position += 1
        # self.stop_i = self.x_position - self.original_x

        # self.x_position = self.original_x
        # self.i = 50


    # def MakeSelfRect(self):
    #     return self.default.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - move_scene_y))

    def MakeSelfRectFruit(self):
        """
        Makes rect for the fruit
        :return:
        """
        return self.default_2.get_rect(bottomleft=(self.x_position - move_scene_x + b_size // 8, self.y_position - move_scene_y))

    def CheckWork(self):
        """
        Checks if works and if yes expands or not
        :return: None
        """
        if self.work:
            self.default = pygame.transform.scale(self.original, (self.i, b_size / 5))
            for i in range(5):
                if self.i < self.stop_i:
                    self.i += 1


class Spike(Object):
    """
    Spike to kill the player
    """

    def __init__(self, x_pos, y_pos, sz = 2):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param sz: Size of the spike
        """
        super().__init__(x_pos, y_pos)

        self.size = sz

        self.default = spike_default
        self.default = pygame.transform.scale(self.default, (b_size / self.size, b_size / self.size))


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class Saw(Object):
    """
    Moving saw to kill the player
    """

    def __init__(self, x_pos, y_pos, sz):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param sz: Size of the saw
        """
        super().__init__(x_pos, y_pos)

        self.size = sz

        self.saw_1 = saw_1
        self.saw_1 = pygame.transform.scale(self.saw_1, (b_size * self.size , b_size * self.size))
        self.saw_2 = saw_2
        self.saw_2 = pygame.transform.scale(self.saw_2, (b_size * self.size , b_size * self.size))
        self.saw_3 = saw_3
        self.saw_3 = pygame.transform.scale(self.saw_3, (b_size * self.size , b_size * self.size))
        self.saw_4 = saw_4
        self.saw_4 = pygame.transform.scale(self.saw_4, (b_size * self.size , b_size * self.size))
        self.saw_5 = saw_5
        self.saw_5 = pygame.transform.scale(self.saw_5, (b_size * self.size , b_size * self.size))
        self.saw_6 = saw_6
        self.saw_6 = pygame.transform.scale(self.saw_6, (b_size * self.size , b_size * self.size))
        self.saw_7 = saw_7
        self.saw_7 = pygame.transform.scale(self.saw_7, (b_size * self.size , b_size * self.size))
        self.saw_8 = saw_8
        self.saw_8 = pygame.transform.scale(self.saw_8, (b_size * self.size , b_size * self.size))

        self.going = [self.saw_1, self.saw_2, self.saw_3, self.saw_4, self.saw_5, self.saw_6, self.saw_7, self.saw_8]

        self.default = self.saw_1


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class SpikedBall(Object):
    """
    Spiked ball tha falls and kills the player
    """

    def __init__(self, x_pos, y_pos, gravity_pull = 0, fall = False, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param gravity_pull: gravity pull
        :param fall: is it ment to fall now or not
        :param m: False if the object is being made, True if the object is made
        """
        # super().__init__(x_pos, y_pos)

        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.fall = fall

        self.gravity_pull = gravity_pull

        self.default = saw_default
        self.default = pygame.transform.scale(self.default, (b_size * 0.75, b_size * 0.75))


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def CheckFall(self):
        """
        Checks if the object falling or not
        :return: None
        """
        if not self.fall:
            if player_1.MakeSelfRect().right >= self.MakeSelfRect().left and not self.ObjectDown(self.MakeSelfRect()):
                self.fall = True
        if self.ObjectDown(self.MakeSelfRect()):
            self.fall = False
        if self.fall:
            self.gravity_pull += 4
            for i in range(self.gravity_pull):
                if not self.ObjectDown(self.MakeSelfRect()):
                    self.y_position += 1

class Fire(Object):
    """
    Block that player can stand on but goes on fire after
    """

    def __init__(self, x_pos, y_pos):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        super().__init__(x_pos, y_pos)

        self.stage_off = pygame.image.load("fire_stage_off.png")
        self.stage_off = pygame.transform.scale(self.stage_off, (b_size , b_size))

        self.stage_on = pygame.image.load("fire_stage_on.png")
        self.stage_on = pygame.transform.scale(self.stage_on, (b_size , b_size))

        self.fire_1 = pygame.image.load("fire_1.png")
        self.fire_1 = pygame.transform.scale(self.fire_1, (b_size , b_size))
        self.fire_2 = pygame.image.load("fire_2.png")
        self.fire_2 = pygame.transform.scale(self.fire_2, (b_size , b_size))
        self.fire_3 = pygame.image.load("fire_3.png")
        self.fire_3 = pygame.transform.scale(self.fire_3, (b_size , b_size))

        self.going = [self.fire_1, self.fire_1, self.fire_2, self.fire_2, self.fire_3, self.fire_3]

        self.default = self.stage_off

        self.delay = 1500
        self.delay_after = 3000

        self.start = 0
        self.over = 0

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

    def MakeSelfRectFire(self):
        """
        Makes rect for the fire
        :return:
        """
        return self.fire_1.get_rect(bottomleft=(self.x_position - move_scene_x, self.y_position - b_size - move_scene_y))

    def CheckOn(self):
        """
        Checks if the player is standing on itself
        :return: None
        """
        self.now = pygame.time.get_ticks()
        if self.MakeSelfRect().top == player_1.MakeSelfRect().bottom and self.MakeSelfRect().left < player_1.MakeSelfRect().right and self.MakeSelfRect().right > player_1.MakeSelfRect().left:
            if self.start == 0:
                self.start = pygame.time.get_ticks()
        # else:
        #     if self.over == 0:
        #         self.over = pygame.time.get_ticks()

        if self.over + self.delay_after <= self.now and self.over != 0:
            self.start = 0
            self.over = 0

        if self.start + self.delay <= self.now and self.start != 0:
            self.default = self.stage_on
            if self.over == 0:
                self.over = pygame.time.get_ticks()
        else:
            self.default = self.stage_off
            self.over = 0


class Fruit(Object):
    """
    Fruit that player can pick up and use it for their advantage later
    """

    def __init__(self, x_pos, y_pos, nm, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param nm: name
        :param m: False if the object is being made, True if the object is made
        """
        # super().__init__(x_pos, y_pos)

        if not m:
            super().__init__(x_pos, y_pos)
            self.x_position += b_size / 3
            self.y_position -= b_size / 3
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.original_y = self.y_position

        self.name = nm

        if  self.name == "a":
            self.default = fruit_apple
        elif  self.name == "b":
            self.default = fruit_banana
        elif  self.name == "c":
            self.default = fruit_cherry

        # self.default = pygame.transform.scale(self.default, (b_size / 3, b_size / 3))

        self.go = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2]


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)

class Coin(Object):
    """
    Coin that player can pick up and use it to buy things
    """

    def __init__(self, x_pos, y_pos, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param m: False if the object is being made, True if the object is made
        """
        # super().__init__(x_pos, y_pos)

        if not m:
            super().__init__(x_pos, y_pos)
            self.x_position += b_size / 4
            self.y_position -= b_size / 4
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.original_y = self.y_position

        self.default = coin_default

        self.go = [1, 1, 1, 1,  2, 2, 2, 2,  3, 3, 3, 3,  4, 4, 4, 4,  3, 3, 3, 3,  2, 2, 2, 2]


    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


class Box(Object):
    """
    Box that can be moved to stand on
    """

    def __init__(self, x_pos, y_pos, gravity_pull = 0, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        :param gravity_pull: gravity pull
        :param m: False if the object is being made, True if the object is made
        """
        # super().__init__(x_pos, y_pos)

        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.gravity_pull = gravity_pull

        self.default = box_default

        self.MakeSides()

    # def MakeSelfRect(self):
    #     return self.MakeRect(self.default)


    def CheckFall(self):
        """
        Checks if the object is falling
        :return: None
        """
        if not self.ObjectDown(self.MakeSelfRect()):
            self.gravity_pull += 3
        else:
            self.gravity_pull = 0

        for i in range(self.gravity_pull):
            if not self.ObjectDown(self.MakeSelfRect()):
                self.y_position += 1
                self.bottom += 1
                self.top += 1


class Timer:
    """
    Timer class that allows to time something
    """
    def __init__(self, time = 0):
        """
        Initializes all variables
        :param time: starting time of the timer
        """
        self.start_time = 0
        self.end_time = 0
        self.time = time
        self.result = 0

    def Start(self):
        """
        Starts the timer
        :return: None
        """
        self.start_time = pygame.time.get_ticks()

    def End(self):
        """
        Ends the timer
        :return: None
        """
        self.end_time = pygame.time.get_ticks()

    def Show(self):
        """
        Shows the result of the timer
        :return: result
        """
        if self.end_time != 0:
            self.result = self.end_time - self.start_time + self.time
        else:
            self.result = pygame.time.get_ticks() - self.start_time + self.time
        return self.result


class SkinProduct:
    """
    Class for buying a skin and picking it
    """
    def __init__(self, x_pos, y_pos, img, mn, bgt, pict, pck = False):
        """
        Initializes all variables
        :param x_pos: x_positions
        :param y_pos: y_position
        :param img: image of a skin
        :param mn: how much it costs
        :param bgt_or_mn: is it bought
        :param pict: what pictures does this class represents
        :param pck: is it picked
        """
        self.x_position = x_pos
        self.y_position = y_pos
        self.image = pygame.transform.scale(img, (200, 250))
        self.picked = pck
        self.pictures = pict
        self.mouse_on_image = False
        self.mouse_on_text = False
        self.money = mn
        self.bought = bgt


        self.image_rect = self.image.get_rect(topleft = (self.x_position, self.y_position))

        self.text = pygame.font.Font(None, 50)
        self.money_text = text.render(f" {self.money} ", True, 'White')
        self.money_text_rect = self.money_text.get_rect(center=(self.x_position + 100, self.y_position + 250 + 100))

        self.dollar = pygame.transform.scale(dollar, (40, 40))
        self.dollar_rect_1 = self.dollar.get_rect(midright=(self.money_text_rect.left, self.money_text_rect.centery))

        self.dollar_rect_2 = self.dollar.get_rect(midleft=(self.money_text_rect.right, self.money_text_rect.centery))

        self.rect_skin = pygame.Rect(self.x_position - 20, self.y_position - 20, 240, 290)

        self.rect_money = pygame.Rect(self.dollar_rect_1.left - 10, self.dollar_rect_1.top - 10,
                                      (self.dollar_rect_2.right + 10) - (self.dollar_rect_1.left - 10),
                                      (self.dollar_rect_2.bottom + 10) - (self.dollar_rect_1.top - 10))

    def DrawSelf(self):
        """
        Draws everything in this class
        :return: None
        """
        if self.picked:
            pygame.draw.rect(screen, (255, 255, 0), self.rect_skin, border_radius=20)
        elif self.bought:
            pygame.draw.rect(screen, (0, 200, 255), self.rect_skin, border_radius=20)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect_skin, border_radius=20)
        if self.mouse_on_image and self.bought:
            pygame.draw.rect(screen, (0, 0, 0), self.rect_skin, width=3, border_radius=20)

        screen.blit(self.image, self.image_rect)

        if self.bought is False:
            pygame.draw.rect(screen, (0, 255, 0), self.rect_money, border_radius=20)
            if self.mouse_on_text or self.mouse_on_image:
                if self.money <= coins_total_menu:
                    pygame.draw.rect(screen, (0, 0, 0), self.rect_money, width=3, border_radius=20)
            screen.blit(self.money_text, self.money_text_rect)
            screen.blit(self.dollar, self.dollar_rect_1)
            screen.blit(self.dollar, self.dollar_rect_2)

class BoostProduct:
    "Class that allows to buy level ups"
    def __init__(self, x_pos, y_pos, nm, lv, mn1, mn2, mn3):
        """
        Initializes all variables
        :param x_pos: x_position
        :param y_pos: y_position
        :param nm: list of names for each level
        :param lv: current level
        :param mn1: first price
        :param mn2: second price
        :param mn3: third price
        """
        self.x_position = x_pos
        self.y_position = y_pos
        self.name_1 = nm[0]
        self.name_2 = nm[1]
        self.name_3 = nm[2]
        self.name_4 = nm[3]
        self.level = lv
        self.price_1 = mn1
        self.price_2 = mn2
        self.price_3 = mn3

        self.name_text = pygame.font.Font(None, 60)

        # self.level_text = text.render(f"Level {self.level}", True, 'Black')
        # self.level_text_rect = self.level_text.get_rect(midright=(self.x_position + 990, self.y_position + 40))
        # self.level_text_white = text.render(f"Level {self.level}", True, 'Black')
        # self.level_text_white_rect = self.level_text_white.get_rect(midright=(self.x_position + 990, self.y_position + 40))

        self.rect_1 = pygame.Rect(self.x_position, self.y_position, 1000, 80)
        self.rect_2 = pygame.Rect(self.x_position + 1010, self.y_position, 280, 80)

        self.price_1_text = text.render(f" {self.price_1} ", True, 'Black')
        self.price_1_text_rect = self.price_1_text.get_rect(center=(self.rect_2.centerx, self.rect_2.centery))

        self.price_2_text = text.render(f" {self.price_2} ", True, 'Black')
        self.price_2_text_rect = self.price_2_text.get_rect(center=(self.rect_2.centerx, self.rect_2.centery))

        self.price_3_text = text.render(f" {self.price_3} ", True, 'Black')
        self.price_3_text_rect = self.price_3_text.get_rect(center=(self.rect_2.centerx, self.rect_2.centery))

        self.price_MAX_text = text.render(f" MAX ", True, 'White')
        self.price_MAX_text_rect = self.price_MAX_text.get_rect(center=(self.rect_2.centerx, self.rect_2.centery))

        self.dollar = pygame.transform.scale(dollar, (40, 40))
        self.arrow = pygame.transform.scale(arrow_top, (40, 40))


        self.mouse_on_big = False
        self.mouse_on_small = False

        # self.image_rect = self.image.get_rect(topleft = (self.x_position, self.y_position))
        #
        # self.text = pygame.font.Font(None, 50)
        # self.money_text = text.render(f" {self.money} ", True, 'White')
        # self.money_text_rect = self.money_text.get_rect(center=(self.x_position + 100, self.y_position + 250 + 100))
        #
        # self.dollar = pygame.transform.scale(dollar, (40, 40))
        # self.dollar_rect_1 = self.dollar.get_rect(midright=(self.money_text_rect.left, self.money_text_rect.centery))
        #
        # self.dollar_rect_2 = self.dollar.get_rect(midleft=(self.money_text_rect.right, self.money_text_rect.centery))
        #
        # self.rect_skin = pygame.Rect(self.x_position - 20, self.y_position - 20, 240, 290)

    def DrawSelf(self):
        """
        Draws everything
        :return: None
        """
        if self.level == 0:
            pygame.draw.rect(screen, (0, 255, 128), self.rect_1, border_radius=10)
            pygame.draw.rect(screen, (0, 255, 128), self.rect_2, border_radius=10)
        elif self.level == 1:
            pygame.draw.rect(screen, (0, 255, 255), self.rect_1, border_radius=10)
            pygame.draw.rect(screen, (0, 255, 255), self.rect_2, border_radius=10)
        elif self.level == 2:
            pygame.draw.rect(screen, (0, 128, 255), self.rect_1, border_radius=10)
            pygame.draw.rect(screen, (0, 128, 255), self.rect_2, border_radius=10)
        elif self.level == 3:
            pygame.draw.rect(screen, (0, 0, 255), self.rect_1, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 255), self.rect_2, border_radius=10)


        if self.level == 0:self.name_text = text.render(f"{self.name_1}", True, 'White' if self.level == 3 else 'Black')
        elif self.level == 1:self.name_text = text.render(f"{self.name_2}", True, 'White' if self.level == 3 else 'Black')
        elif self.level == 2:self.name_text = text.render(f"{self.name_3}", True, 'White' if self.level == 3 else 'Black')
        else:self.name_text = text.render(f"{self.name_4}", True, 'White' if self.level == 3 else 'Black')
        self.name_text_rect = self.name_text.get_rect(midleft=(self.x_position + 10, self.y_position + 40))

        screen.blit(self.name_text, self.name_text_rect)


        if self.mouse_on_big or self.mouse_on_small:
            if self.level == 0:
                if self.price_1 <= coins_total_menu:
                    pygame.draw.rect(screen, (0, 0, 0), self.rect_2, width=3, border_radius=10)
            elif self.level == 1:
                if self.price_2 <= coins_total_menu:
                    pygame.draw.rect(screen, (0, 0, 0), self.rect_2, width=3, border_radius=10)
            elif self.level == 2:
                if self.price_3 <= coins_total_menu:
                    pygame.draw.rect(screen, (0, 0, 0), self.rect_2, width=3, border_radius=10)

        self.level_text = text.render(f"Level {self.level}", True, 'White' if self.level == 3 else 'Black')
        self.level_text_rect = self.level_text.get_rect(midright=(self.x_position + 990, self.y_position + 40))
        screen.blit(self.level_text, self.level_text_rect)

        if self.level == 0:
            screen.blit(self.price_1_text, self.price_1_text_rect)
            self.dollar_rect = self.dollar.get_rect(midleft=(self.price_1_text_rect.right, self.price_1_text_rect.centery))
            self.arrow_rect = self.arrow.get_rect(midright=(self.price_1_text_rect.left, self.price_1_text_rect.centery))
            screen.blit(self.dollar, self.dollar_rect)
            screen.blit(self.arrow, self.arrow_rect)
        elif self.level == 1:
            screen.blit(self.price_2_text, self.price_2_text_rect)
            self.dollar_rect = self.dollar.get_rect(midleft=(self.price_2_text_rect.right, self.price_2_text_rect.centery))
            self.arrow_rect = self.arrow.get_rect(midright=(self.price_2_text_rect.left, self.price_2_text_rect.centery))
            screen.blit(self.dollar, self.dollar_rect)
            screen.blit(self.arrow, self.arrow_rect)
        elif self.level == 2:
            screen.blit(self.price_3_text, self.price_3_text_rect)
            self.dollar_rect = self.dollar.get_rect(midleft=(self.price_3_text_rect.right, self.price_3_text_rect.centery))
            self.arrow_rect = self.arrow.get_rect(midright=(self.price_3_text_rect.left, self.price_3_text_rect.centery))
            screen.blit(self.dollar, self.dollar_rect)
            screen.blit(self.arrow, self.arrow_rect)
        else:
            screen.blit(self.price_MAX_text, self.price_MAX_text_rect)


class BreakBlock(Object):
    """
    Class that represents an orange block
    """

    def __init__(self, x_pos, y_pos, m = False):
        """
        Initializes all variables
        :param x_pos: position on x co-ordinates
        :param y_pos: position on y co-ordinates
        """
        # super().__init__(x_pos, y_pos)
        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.default = break_block_default

        self.MakeSides()

class MysteryBox(Object):
    """
    Mystery box
    """

    def __init__(self, x_pos, y_pos, bumbs, got_p = False, m = False):
        """
        Initializes all variables
        :param x_pos: x_position
        :param y_pos: y_position
        :param bumbs: hits left that the box has
        :param got_p: if the player gotb potion from this box
        :param m: m
        """
        if not m:
            super().__init__(x_pos, y_pos)
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.hits_left = bumbs

        self.got_potion = got_p

        self.default = mystery_box

        self.MakeSides()


class HealthPotion(Object):
    """
    Potion that player can collect to get invincibility
    """

    def __init__(self, x_pos, y_pos, m = False):
        """
        Initializes all variables
        :param x_pos: x_position
        :param y_pos: y_position
        :param m: m
        """
        if not m:
            self.x_position = x_pos
            self.y_position = y_pos
            self.x_position += b_size // 4
            self.y_position -= b_size // 4
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.default = potion

class GravityPotion(Object):
    """
    Potion that player can collect to get levitation
    """

    def __init__(self, x_pos, y_pos, m = False):
        """
        Initializes all variables
        :param x_pos: x_position
        :param y_pos: y_position
        :param m: m
        """
        if not m:
            self.x_position = x_pos
            self.y_position = y_pos
            self.x_position += b_size // 4
            self.y_position -= b_size // 4
        else:
            self.x_position = x_pos
            self.y_position = y_pos

        self.default = potion_2


# player_1 = Player(0, 0)
# check_p_1 = Checkpoint(0, 0)


def blit_level():
    """
    Draws everything related to the game level
    :return: Nothing
    """
    global player_1, find_find_mode, player_pictures

    screen.blit(blue_sky, blue_sky_rect)

    for x in saws:
        if check_visible(x):
            if not game_paused:
                screen.blit(x.going[0], x.MakeSelfRect())
                x.going.append(x.going[0])
                x.going.pop(0)
            else:
                screen.blit(x.going[0], x.MakeSelfRect())

    for i in range(len(list_grs)):
        if check_visible(list_grs[i]):
            if list_grounds_decide[i] == "grass":
                screen.blit(list_grs[i].grass, list_grs[i].MakeSelfRect())
            elif list_grounds_decide[i] == "ground":
                screen.blit(list_grs[i].default, list_grs[i].MakeSelfRect())

    for x in set(touch_objects + boxes + break_blocks + mystery_boxes) - set(list_grs) - set(fly_plats) - set(jump_pads) - set(expand_plats):
        if check_visible(x):
            screen.blit(x.default, x.MakeSelfRect())

    for x in bricks:
        if check_visible(x):
            screen.blit(x.default, x.MakeSelfRect())

    for x in spikes + spiked_balls:
        if check_visible(x):
            screen.blit(x.default, x.MakeSelfRect())

    for x in fires:
        if x.default == x.stage_on:
            if check_visible(x):
                if not game_paused:
                    screen.blit(x.going[0], x.MakeSelfRectFire())
                    x.going.append(x.going[0])
                    x.going.pop(0)
                else:
                    screen.blit(x.going[0], x.MakeSelfRectFire())




    for x in start_games:
        if x.default == x.start_arrow:
            if check_visible(x):
               screen.blit(x.start_arrow, x.MakeSelfRect())

    for x in check_ps:
        if x.checkpoint_TF:
            if not game_paused:
                screen.blit(x.checkpointing[0], x.MakeSelfRect())
                x.checkpointing.append(x.checkpointing[0])
                x.checkpointing.pop(0)
            else:
                screen.blit(x.checkpointing[0], x.MakeSelfRect())
        else:
            screen.blit(x.no_checkpoint, x.MakeSelfRect())


    for x in snakes + mushrooms:
        if check_visible(x):
            if not game_paused:
                if x.side == "l":
                    screen.blit(x.going[0], x.MakeSelfRect())
                if x.side == "r":
                    screen.blit(pygame.transform.flip(x.going[0], True, False), x.MakeSelfRect())
                x.going.append(x.going[0])
                x.going.pop(0)
            else:
                if x.side == "l":
                    screen.blit(x.going[0], x.MakeSelfRect())
                if x.side == "r":
                    screen.blit(pygame.transform.flip(x.going[0], True, False), x.MakeSelfRect())

    for x in horses + mummys:
        if check_visible(x):
            if x.side == "r":
                screen.blit(pygame.transform.flip(x.default, True, False), x.MakeSelfRect())
            else:
                screen.blit(x.default, x.MakeSelfRect())


    for x in fly_plats:
        if check_visible(x):
            if not game_paused:
                if x.work:
                    x.going[0].set_alpha(255)
                    screen.blit(x.going[0], x.MakeSelfRect())
                else:
                    x.going[0].set_alpha(x.transparency)
                    screen.blit(x.going[0], x.MakeSelfRect())
                    screen.blit(x.default_2, x.MakeSelfRectFruit())
                x.going.append(x.going[0])
                x.going.pop(0)
            else:
                if x.work:
                    x.going[0].set_alpha(255)
                    screen.blit(x.going[0], x.MakeSelfRect())
                else:
                    x.going[0].set_alpha(x.transparency)
                    screen.blit(x.going[0], x.MakeSelfRect())
                    screen.blit(x.default_2, x.MakeSelfRectFruit())

    for x in jump_pads:
        if check_visible(x):
            if x.work:
                x.default.set_alpha(255)
                screen.blit(x.default, x.MakeSelfRect())
            else:
                x.default.set_alpha(x.transparency)
                screen.blit(x.default, x.MakeSelfRect())
                screen.blit(x.default_2, x.MakeSelfRectFruit())

    for x in expand_plats:
        if check_visible(x):
            if x.work:
                x.default.set_alpha(255)
                screen.blit(x.default, x.MakeSelfRect())
            else:
                x.default.set_alpha(x.transparency)
                screen.blit(x.default, x.MakeSelfRect())
                screen.blit(x.default_2, x.MakeSelfRectFruit())


    if not game_paused:
        find_find_mode = find_mode()


    if find_find_mode == "stand":
        if not game_paused:
            player_pictures[1][0].set_alpha(player_1.transparency)
            if side == "r":
                screen.blit(player_pictures[1][0], player_1.MakeSelfRect())
            else:
                screen.blit(pygame.transform.flip(player_pictures[1][0], True, False), player_1.MakeSelfRect())
            player_pictures[1].append(player_pictures[1][0])
            player_pictures[1].pop(0)
        else:
            player_pictures[1][0].set_alpha(player_1.transparency)
            if side == "r":
                screen.blit(player_pictures[1][0], player_1.MakeSelfRect())
            else:
                screen.blit(pygame.transform.flip(player_pictures[1][0], True, False), player_1.MakeSelfRect())

    elif find_find_mode == "run":
        if not game_paused:
            player_pictures[0][0].set_alpha(player_1.transparency)
            if side == "r":
                screen.blit(player_pictures[0][0], player_1.MakeSelfRect())
            else:
                screen.blit(pygame.transform.flip(player_pictures[0][0], True, False), player_1.MakeSelfRect())
            player_pictures[0].append(player_pictures[0][0])
            player_pictures[0].pop(0)
        else:
            player_pictures[0][0].set_alpha(player_1.transparency)
            if side == "r":
                screen.blit(player_pictures[0][0], player_1.MakeSelfRect())
            else:
                screen.blit(pygame.transform.flip(player_pictures[0][0], True, False), player_1.MakeSelfRect())

    elif find_find_mode == "jump":
        player_pictures[2].set_alpha(player_1.transparency)
        if side == "r":
            screen.blit(player_pictures[2], player_1.MakeSelfRect())
        else:
            screen.blit(pygame.transform.flip(player_pictures[2], True, False), player_1.MakeSelfRect())

    elif find_find_mode == "fall":
        player_pictures[3].set_alpha(player_1.transparency)
        if side == "r":
            screen.blit(player_pictures[3], player_1.MakeSelfRect())
        else:
            screen.blit(pygame.transform.flip(player_pictures[3], True, False), player_1.MakeSelfRect())

    elif find_find_mode == "wall":
        player_pictures[4].set_alpha(player_1.transparency)
        if side == "r":
            screen.blit(player_pictures[4], player_1.MakeSelfRect())
        else:
            screen.blit(pygame.transform.flip(player_pictures[4], True, False), player_1.MakeSelfRect())


    for x in fruits + coins:
        if check_visible(x):
            if not game_paused:
                x.y_position = x.original_y + x.go[0]
                screen.blit(x.default, x.MakeSelfRect())
                x.go.append(x.go[0])
                x.go.pop(0)
            else:
                x.y_position = x.original_y + x.go[0]
                screen.blit(x.default, x.MakeSelfRect())


    for x in potions_1 + potions_2:
        screen.blit(x.default, x.MakeSelfRect())


    screen.blit(apple, apple_rect)
    screen.blit(banana, banana_rect)
    screen.blit(cherry, cherry_rect)
    screen.blit(coin_1, coin_1_rect)

    global apples, bananas, cherries, coins_not_list, apples_count, apples_count_rect, banana_count, banana_count_rect, cherry_count, cherry_count_rect, coin_count, coin_count_rect

    if apples != player_1.apples:
        apples = player_1.apples
        apples_count = text.render(f"{player_1.apples}", True, 'Black')
        apples_count_rect = apples_count.get_rect(topleft=(340, 5))
    screen.blit(apples_count, apples_count_rect)

    if bananas != player_1.bananas:
        bananas = player_1.bananas
        banana_count = text.render(f"{player_1.bananas}", True, 'Black')
        banana_count_rect = apples_count.get_rect(topleft=(490, 5))
    screen.blit(banana_count, banana_count_rect)

    if cherries != player_1.cherries:
        cherries = player_1.cherries
        cherry_count = text.render(f"{player_1.cherries}", True, 'Black')
        cherry_count_rect = cherry_count.get_rect(topleft=(640, 5))
    screen.blit(cherry_count, cherry_count_rect)

    if coins_not_list != player_1.coins:
        coins_not_list = player_1.coins
        coin_count = text.render(f"{player_1.coins}", True, 'Black')
        coin_count_rect = coin_count.get_rect(topleft=(890, 5))
    screen.blit(coin_count, coin_count_rect)

    screen.blit(go_back_button, go_back_button_rect)
    screen.blit(restart_button, restart_button_rect)

    if game_paused:
        screen.blit(not_pause_button, not_pause_button_rect)
    else:
        screen.blit(pause_button, pause_button_rect)


    if invincibility_timer == 0:
        pass
    else:
        if invincibility_timer.Show() < 10000:
            if round(pygame.time.get_ticks() / 500) % 2 == 0:
                screen.blit(invincibility_text, invincibility_text_rect)
            else:
                screen.blit(invincibility_text_2, invincibility_text_rect_2)


    if gravity_timer == 0:
        pass
    else:
        if gravity_timer.Show() < 10000:
            if round(pygame.time.get_ticks() / 500) % 2 == 0:
                screen.blit(gravity_text, gravity_text_rect)
            else:
                screen.blit(gravity_text_2, gravity_text_rect_2)

def blit_menu():
    """
    Draws everything in menu
    :return: Nothing
    """
    screen.blit(green_bck, green_bck_rect)
    screen.blit(play_button, play_button_rect)

    text = pygame.font.Font(None, 75)

    best_score_text = text.render(f"Best Score:", True, 'Black')
    best_score_text_rect = best_score_text.get_rect(center=(650, 450))

    screen.blit(best_score_text, best_score_text_rect)

    best_score_num_text = text.render(f"{"0" if best_score == 0 else best_score / 1000} s", True, 'Black')
    best_score_num_text_rect = best_score_num_text.get_rect(center=(650, 530))
    screen.blit(best_score_num_text, best_score_num_text_rect)

    screen.blit(coin_menu, coin_menu_rect)
    screen.blit(buy_menu, buy_menu_rect)

    # text = pygame.font.Font(None, 50)

    total_coins_text = text.render(f"{coins_total_menu}", True, 'Black')
    total_coins_text_rect = total_coins_text.get_rect(topleft=(70, 10))
    screen.blit(total_coins_text, total_coins_text_rect)

    # if best_score == 0:
    #     best_score_num_text = text.render("0s", True, 'Black')
    #     best_score_num_text_rect = best_score_num_text.get_rect(center=(650, 525))
    #     screen.blit(best_score_num_text, best_score_num_text_rect)
    # else:
    #     best_score_num_text = text.render(f"{best_score[0] / 1000}s -     {best_score[1]}", True, 'Black')
    #     best_score_num_text_rect = best_score_num_text.get_rect(center=(650, 530))
    #     screen.blit(best_score_num_text, best_score_num_text_rect)
    #
    #     best_score_num_text = text.render(f"{best_score[2] / 1000}s", True, 'Black')
    #     best_score_num_text_rect = best_score_num_text.get_rect(center=(650, 590))
    #     screen.blit(best_score_num_text, best_score_num_text_rect)
    #
    #     screen.blit(coin_2, coin_2_rect)

def blit_buy_1():
    """
    Draws everything related to buying skins
    :return: None
    """
    screen.blit(orange_bck, orange_bck_rect)
    screen.blit(coin_menu, coin_menu_rect)
    screen.blit(go_back_button_buy, go_back_button_buy_rect)


    text = pygame.font.Font(None, 75)

    total_coins_text = text.render(f"{coins_total_menu}", True, 'Black')
    total_coins_text_rect = total_coins_text.get_rect(topleft=(70, 10))
    screen.blit(total_coins_text, total_coins_text_rect)

    pygame.draw.rect(screen,(127, 0, 255), rect_buy_1_1, border_top_left_radius=30, border_bottom_left_radius=30)

    pygame.draw.rect(screen,(178, 102, 255), rect_buy_1_2, border_top_right_radius=30, border_bottom_right_radius=30)

    if mouse_on_buy_change[1]:
        pygame.draw.rect(screen, (0, 0, 0), rect_buy_1_2, width=2, border_top_right_radius=30,border_bottom_right_radius=30)

    screen.blit(skins_text, skins_text_rect)
    screen.blit(boosts_text, boosts_text_rect)

    for x in skins_products:
        x.DrawSelf()

def blit_buy_2():
    """
    Draws everything related to buying boosts
    :return: None
    """
    screen.blit(orange_bck, orange_bck_rect)
    screen.blit(coin_menu, coin_menu_rect)
    screen.blit(go_back_button_buy, go_back_button_buy_rect)


    text = pygame.font.Font(None, 75)

    total_coins_text = text.render(f"{coins_total_menu}", True, 'Black')
    total_coins_text_rect = total_coins_text.get_rect(topleft=(70, 10))
    screen.blit(total_coins_text, total_coins_text_rect)

    pygame.draw.rect(screen,(178, 102, 255), rect_buy_1_1, border_top_left_radius=30, border_bottom_left_radius=30)

    pygame.draw.rect(screen,(127, 0, 255), rect_buy_1_2, border_top_right_radius=30, border_bottom_right_radius=30)

    if mouse_on_buy_change[0]:
        pygame.draw.rect(screen, (0, 0, 0), rect_buy_1_1, width=2, border_top_left_radius=30, border_bottom_left_radius=30)

    for x in boosts_products:
        x.DrawSelf()

    screen.blit(skins_text, skins_text_rect)
    screen.blit(boosts_text, boosts_text_rect)

def keys_pressed():
    """
    What happens when certain keys are pressed
    :return: Nothing
    """
    global fall_jump, move_scene_y, run_sound_play
    keys = pygame.key.get_pressed()
    find_find_mode = find_mode()
    object_down = player_1.ObjectDown(player_1.MakeSelfRect())
    if keys[pygame.K_RIGHT]:
        if find_find_mode == "wall":
            fall_jump = 0
            if not object_down:
                check_die()
                if player_1.MakeSelfRect().centery > 350:
                    player_1.y_position += 1
                elif move_scene_y == 0 and player_1.MakeSelfRect().centery <= 350 and player_1.MakeSelfRect().bottom != 0:
                    player_1.y_position += 1
                elif move_scene_y < 0:
                    move_scene_y += 1
        else:
            player_1.MoveRight()

    if keys[pygame.K_LEFT]:
        if find_find_mode == "wall":
            fall_jump = 0
            if not object_down:
                check_die()
                if player_1.MakeSelfRect().centery > 350:
                    player_1.y_position += 1
                elif move_scene_y == 0 and player_1.MakeSelfRect().centery <= 350 and player_1.MakeSelfRect().bottom != 0:
                    player_1.y_position += 1
                elif move_scene_y < 0:
                    move_scene_y += 1
        else:
            player_1.MoveLeft()

    if keys[pygame.K_UP]:
        if object_down:
            fall_jump = 28 if boosts_products[1].level == 0 else 29 if boosts_products[1].level == 1 else 30 if boosts_products[1].level == 2 else 31
            jump_sound.play()
        if player_1.BrickRightLeftUpDown(player_1.MakeSelfRect(), 'b'):
            fall_jump = 28 if boosts_products[1].level == 0 else 29 if boosts_products[1].level == 1 else 30 if boosts_products[1].level == 2 else 31
            jump_sound.play()
            jump_sound.play()

    if keys[pygame.K_DOWN]:
        if fall_jump <= 10:
            fall_jump = -50

    if keys[pygame.K_UP] and not object_down and fall_jump == 0 and find_find_mode == "wall":
        fall_jump = 17
        jump_sound.play()


    if keys[pygame.K_RIGHT]:
        if object_down and find_find_mode != "wall":
            if run_sound_play == 1:
                run_sound_play = run_sound.play()
            elif not run_sound_play.get_busy():
                run_sound.play()
    elif keys[pygame.K_LEFT]:
        if object_down and find_find_mode != "wall":
            if run_sound_play == 1:
                run_sound_play = run_sound.play()
            elif not run_sound_play.get_busy():
                run_sound.play()
    else:
        run_sound.stop()

def find_mode():
    """
    Finds at which state(position) is the player right now e.g. running, falling
    :return: state
    """
    global mode, fall_jump
    global side
    keys = pygame.key.get_pressed()
    object_right = player_1.ObjectRight(player_1.MakeSelfRect())
    object_left = player_1.ObjectLeft(player_1.MakeSelfRect())
    object_down = player_1.ObjectDown(player_1.MakeSelfRect())
    player_1_rect = player_1.MakeSelfRect()
    if keys[pygame.K_RIGHT]:
        side = "r"
        if object_down:
            if object_right:
                mode = "stand"
            else:
                mode = "run"
        if not object_down and object_right:
            mode = "wall"
        if not object_down and not object_right:
            if fall_jump >= 0:
                mode = "jump"
            else:
                mode = "fall"

        for x in boxes:
            if player_1_rect.right == x.MakeSelfRect().left and player_1_rect.bottom > x.MakeSelfRect().top and player_1_rect.top < x.MakeSelfRect().bottom:
                if not x.ObjectRight(x.MakeSelfRect()):
                    mode = "run"


    elif keys[pygame.K_LEFT]:
        side = "l"
        if object_down:
            if object_left:
                mode = "stand"
            else:
                mode = "run"
        if not object_down and object_left:
            mode = "wall"
        if not object_down and not object_left:
            if fall_jump >= 0:
                mode = "jump"
            else:
                mode = "fall"

        for x in boxes:
            if player_1_rect.left == x.MakeSelfRect().right and player_1_rect.bottom > x.MakeSelfRect().top and player_1.MakeSelfRect().top < x.MakeSelfRect().bottom:
                if not x.ObjectLeft(x.MakeSelfRect()):
                    mode = "run"

    else:
        mode = "stand"

    if fall_jump > 0:
        mode = "jump"
    elif fall_jump < 0 and not object_left and not object_right:
        mode = "fall"

    TF = True
    if not object_down:
        for i in bricks:
            if check_visible(i):
                if player_1.MakeSelfRect().bottom == i.MakeRect2("t") and player_1.MakeSelfRect().left < i.MakeRect2("r") and player_1.MakeSelfRect().right > i.MakeRect2("l"):
                    TF = False
        if not TF:
            fall_jump = 28
    if not TF:
        fall_jump = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            mode = "run"
        else:
            mode = "stand"

    return mode

def start_play_not_changeable():
    """
    Makes unchangeable variables for the game
    :return: Nothing
    """
    global list_grounds_decide
    global start_games
    global spikes
    global saws
    global fires
    global list_grs
    global touch_objects
    global bricks, player_1
    global skins_products, boosts_products, coins_total_menu
    global mushrooms, snakes, horses, mummys, fruits, coins, fly_plats, expand_plats, jump_pads, check_ps, spiked_balls, boxes,\
        original_snakes, original_mushrooms, original_horses, original_mummys, original_fruits, original_coins, \
        original_fly_plats, original_expand_plats, original_jump_pads, original_check_ps, original_spiked_balls, original_boxes
    global break_blocks, original_break_blocks, mystery_boxes, original_mystery_boxes, potions_1, original_potions_1, potions_2, original_potions_2
    global player_pictures
    # global apples, bananas, cherries, coins_not_list
    # global find_find_mode

    # variables
    # -------------------------
    # fall_jump = 0
    # move_scene_x = 0
    # move_scene_y = 0
    # mode = "fall"
    # side = "r"
    # checkpoints = 0
    # apples = -1
    # bananas = -1
    # cherries = -1
    # coins_not_list = -1
    # timer = Timer()
    # find_find_mode = None
    # -------------------------

    with MongoClient() as fl:
        if len(fl['Final_Project_DB_Buy'].list_collection_names()) > 0:
            new_fl = fl['Final_Project_DB_Buy']
            skins_products = [
                SkinProduct(100, 200, mask_stand_list[2], 0, new_fl['Skins'].find()[0]['mask'], mask_pictures,
                            new_fl['Skins'].find()[0]['mask_picked']),
                SkinProduct(400, 200, ninja_stand_list[2], 50, new_fl['Skins'].find()[0]['ninja'], ninja_pictures,
                            new_fl['Skins'].find()[0]['ninja_picked']),
                SkinProduct(700, 200, pink_stand_list[2], 100, new_fl['Skins'].find()[0]['pink'], pink_pictures,
                            new_fl['Skins'].find()[0]['pink_picked']),
                SkinProduct(1000, 200, virtual_stand_list[2], 1000, new_fl['Skins'].find()[0]['virtual'],
                            virtual_pictures, new_fl['Skins'].find()[0]['virtual_picked'])
            ]

            for i in skins_products:
                if i.picked:
                    player_pictures = i.pictures


            boosts_products = [
                BoostProduct(5,
                             100,
                             ['Player Speed: +0%', 'Player Speed: +10%', 'Player Speed: +20%', 'Player Speed: +35%'],
                             new_fl['Boosts'].find()[0]['PlayerSpeed'],
                             20,50, 100),
                BoostProduct(5,
                             200,
                             ['Player Jump: +0%', 'Player Jump: +5%', 'Player Jump: +10%', 'Player Jump: +20%'],
                             new_fl['Boosts'].find()[0]['PlayerJump'],
                             10, 20, 30),
                BoostProduct(5,
                             300,
                             ['Enemies Speed: -0%', 'Enemies Speed: -5%', 'Enemies Speed: -10%', 'Enemies Speed: -20%'],
                             new_fl['Boosts'].find()[0]['EnemiesSpeed'],
                             15, 35, 50),
                BoostProduct(5, 400, ['Coins at the end of the game: +0%', 'Coins at the end of the game: +10%','Coins at the end of the game: +20%', 'Coins at the end of the game: +40%'],
                             new_fl['Boosts'].find()[0]['CoinsAtEnd'],
                             5,25,80),
                BoostProduct(5,
                             500,
                             ['Time at the end of the game: -0s', 'Time at the end of the game: -5s','Time at the end of the game: +10s', 'Time at the end of the game: -20s'],
                             new_fl['Boosts'].find()[0]['TimeAtEnd'],
                             20,40,70),
            ]

            coins_total_menu = new_fl['Coins'].find()[0]['coins']
        else:
            skins_products = [
                SkinProduct(100, 200, mask_stand_list[2], 0, True, mask_pictures, True),
                SkinProduct(400, 200, ninja_stand_list[2], 50, True, ninja_pictures),
                SkinProduct(700, 200, pink_stand_list[2], 100, False, pink_pictures),
                SkinProduct(1000, 200, virtual_stand_list[2], 1000, False, virtual_pictures)
            ]

            boosts_products = [
                BoostProduct(5, 100,
                             ['Player Speed: +0%', 'Player Speed: +10%', 'Player Speed: +20%', 'Player Speed: +35%'], 0,
                             20,
                             50, 100),
                BoostProduct(5, 200, ['Player Jump: +0%', 'Player Jump: +5%', 'Player Jump: +10%', 'Player Jump: +20%'],
                             0,
                             10, 20, 30),
                BoostProduct(5, 300,
                             ['Enemies Speed: -0%', 'Enemies Speed: -5%', 'Enemies Speed: -10%', 'Enemies Speed: -20%'],
                             0,
                             15, 35, 50),
                BoostProduct(5, 400, ['Coins at the end of the game: +0%', 'Coins at the end of the game: +10%',
                                      'Coins at the end of the game: +20%', 'Coins at the end of the game: +40%'], 0, 5,
                             25,
                             80),
                BoostProduct(5, 500, ['Time at the end of the game: -0s', 'Time at the end of the game: -5s',
                                      'Time at the end of the game: +10s', 'Time at the end of the game: -20s'], 0, 20,
                             40,
                             70),
            ]

            coins_total_menu = 0


    mushrooms = [
        Mushroom(4, 2, 8),
        Mushroom(18, 2, 20),
        Mushroom(22, 4, 26),
        Mushroom(61, 8, 64),
        Mushroom(71, 9, 73),
        Mushroom(118, 3, 120),
        Mushroom(133, 2, 135),
        Mushroom(40, 6, 43),
    ]

    snakes = [
        Snake(22, 4, 26),
        Snake(36, 2, 39),
        Snake(49, 7, 53),
        Snake(127, 3, 129),
        Snake(137, 2, 143),
    ]

    horses = [
        # Horse(4, 2, 8),
        Horse(155, 2, 157),
    ]

    mummys = [
        # Mummy(4, 2, 10)
    ]



    fruits = [
        Fruit(6, 9, "b"),
        Fruit(27, 3, "a"),
        Fruit(29, 14, "c"),
        Fruit(33, 4, "a"),
        Fruit(40, 6, "a"),
        Fruit(52, 7, "b"),
        Fruit(63, 8, "b"),
        Fruit(65, 6, "b"),
        Fruit(72, 9, "b"),
        Fruit(94, 19, "c"),
        Fruit(149, 10, "b"),
    ]

    coins = [
        Coin(1, 5),
        Coin(2, 5),
        Coin(3, 5),
        Coin(1, 6),
        Coin(2, 6),
        Coin(3, 6),

        Coin(13, 11),
        Coin(14, 11),

        Coin(15, 14),
        Coin(16, 14),

        Coin(23, 7),
        Coin(24, 7),
        Coin(25, 7),

        Coin(37, 2),
        Coin(38, 2),
        Coin(39, 2),

        Coin(42, 6),
        Coin(43, 6),

        Coin(49, 2),
        Coin(51, 3),

        Coin(49, 7),
        Coin(50, 7),

        Coin(56, 2),
        Coin(57, 2),

        Coin(72, 5),
        Coin(73, 4),
        Coin(73, 5),
        Coin(73, 6),

        Coin(89, 13),
        Coin(90, 13),

        Coin(89, 17),
        Coin(90, 17),

        Coin(93, 15),
        Coin(94, 15),

        Coin(150, 8),
        Coin(151, 8),

        Coin(151, 5),
        Coin(152, 5),

        Coin(158, 2),
        Coin(159, 2),
        Coin(160, 2),
        Coin(159, 3),
        Coin(160, 3),
        Coin(160, 4),

        Coin(164, 5),
        Coin(165, 5),

        Coin(167, 7),
        Coin(168, 7),

        Coin(163, 9),
        Coin(164, 9),

        Coin(140, 9),
        Coin(141, 9),
        Coin(140, 10),
        Coin(141, 10),
        Coin(140, 11),
        Coin(141, 11),
        Coin(140, 12),
        Coin(141, 12),
        Coin(140, 13),
        Coin(141, 13),
        Coin(140, 14),
        Coin(141, 14),
        Coin(140, 15),
        Coin(141, 15),
        Coin(140, 16),
        Coin(141, 16),
        Coin(140, 17),
        Coin(141, 17),
        Coin(140, 18),
        Coin(141, 18),
        Coin(140, 19),
        Coin(141, 19),
    ]


    # jump_pad = apple, fly_plat = banana, expand_plat = cherry

    fly_plats = [
        FlyPlat(17, 16, 25, "RightLeft"),
        FlyPlat(44, 8, 54, "RightLeft"),
        FlyPlat(78, 7, 2, "UpDown"),
        FlyPlat(80, 8, 84, "RightLeft"),
        FlyPlat(86, 11, 4, "UpDown"),
        FlyPlat(164, 1, 174, "RightLeft"),
    ]

    jump_pads = [
        JumpPad(11, 5),
        JumpPad(47, 2),
        JumpPad(59, 3),
    ]

    expand_plats = [
        # ExpandPlat(1, 4, b_size * 4),
        ExpandPlat(65, 3, b_size * 3),
        ExpandPlat(121, 2, b_size * 6)
    ]



    check_ps = [
        Checkpoint(73, 9),
        Checkpoint(134, 9),
        Checkpoint(165, 5)
    ]


    spiked_balls = [
        # Spiked_Ball(7, 7),
        SpikedBall(36, 7)
    ]

    boxes = [
        # Box(1, 8),
        Box(155, 8),
        Box(157, 10)
    ]


    break_blocks = [
        BreakBlock(135, 8),
        BreakBlock(136, 8),
        BreakBlock(137, 8),
        BreakBlock(185, 4),
        BreakBlock(186, 4),

        BreakBlock(59, 4),
        BreakBlock(59, 5),

        # BreakBlock(116, 6),
        # BreakBlock(117, 6),
        # BreakBlock(118, 6),
        # BreakBlock(119, 6),
        # BreakBlock(120, 6),
        # BreakBlock(121, 6),

        # BreakBlock(147, 5),
        # BreakBlock(148, 5),
        # BreakBlock(149, 5),
        # BreakBlock(150, 5),
        # BreakBlock(150, 6),
        # BreakBlock(150, 7),
    ]

    mystery_boxes = [
        MysteryBox(48, 6, 10),
        MysteryBox(70, 8, 5),
        MysteryBox(160, 7, 15),
    ]


    potions_1 = []

    potions_2 = []


    original_snakes = snakes
    original_mushrooms = mushrooms
    original_horses = horses
    original_mummys = mummys

    original_fruits = fruits
    original_coins = coins

    original_fly_plats = fly_plats
    original_expand_plats = expand_plats
    original_jump_pads = jump_pads

    original_check_ps = check_ps
    original_spiked_balls = spiked_balls
    original_boxes = boxes

    original_break_blocks = break_blocks


    original_mystery_boxes = mystery_boxes
    original_potions_1 = potions_1
    original_potions_2 = potions_2


    list_grs = [
        Ground(1, 2),
        Ground(2, 2),
        Ground(3, 2),
        Ground(4, 1),
        Ground(5, 1),
        Ground(6, 1),
        Ground(7, 1),
        Ground(8, 1),
        Ground(9, 1),
        Ground(10, 1),
        # Ground(11, 1),
        Ground(9, 2),
        Ground(10, 3),
        # Ground(11, 4),
        Ground(17, 2),
        Ground(16, 3),
        # Ground(15, 4),
        # Ground(15, 1),
        Ground(16, 1),
        Ground(17, 1),
        Ground(18, 1),
        Ground(19, 1),
        Ground(20, 1),
        Ground(21, 2),
        Ground(22, 3),
        Ground(23, 3),
        Ground(24, 3),
        Ground(25, 3),
        Ground(26, 3),
        Ground(26, 2),
        Ground(27, 2),
        Ground(28, 2),
        Ground(29, 2),
        Ground(30, 2),
        Ground(31, 4),
        Ground(32, 4),
        Ground(33, 3),
        Ground(34, 2),
        Ground(35, 2),
        Ground(36, 1),
        Ground(37, 1),
        Ground(38, 1),
        Ground(39, 1),
        Ground(40, 1),
        Ground(41, 1),
        Ground(42, 1),
        Ground(43, 1),
        Ground(44, 1),
        Ground(45, 1),
        Ground(46, 1),
        Ground(47, 1),
        Ground(48, 1),
        Ground(49, 1),
        Ground(50, 2),
        Ground(51, 2),
        Ground(52, 3),
        Ground(53, 1),
        Ground(54, 1),
        Ground(55, 1),
        Ground(56, 1),
        Ground(57, 1),
        Ground(58, 1),
        Ground(59, 2),
        Ground(60, 2),
        # Ground(61, 7),
        Ground(62, 7),
        Ground(63, 7),
        Ground(64, 7),
        Ground(65, 1),
        Ground(66, 1),
        Ground(67, 1),
        Ground(68, 1),
        Ground(69, 1),
        Ground(70, 1),
        Ground(71, 8),
        Ground(72, 7),
        Ground(72, 8),
        Ground(73, 8),
        Ground(72, 3),
        Ground(73, 2),
        Ground(74, 1),
        Ground(75, 1),
        Ground(110, 1),
        Ground(111, 3),
        Ground(112, 4),
        Ground(113, 5),
        Ground(114, 6),
        Ground(115, 6),
        Ground(116, 5),
        Ground(117, 3),
        Ground(118, 2),
        Ground(119, 2),
        Ground(120, 2),
        Ground(127, 2),
        Ground(128, 2),
        Ground(129, 2),
        Ground(130, 3),
        Ground(131, 4),
        Ground(132, 6),
        Ground(133, 5),
        Ground(133, 6),
        Ground(133, 7),
        Ground(134, 6),
        Ground(134, 7),
        Ground(134, 8),
        Ground(133, 1),
        Ground(134, 1),
        Ground(135, 1),
        Ground(136, 1),
        Ground(137, 1),
        Ground(138, 1),
        Ground(139, 1),
        Ground(140, 1),
        Ground(141, 1),
        Ground(142, 1),
        Ground(143, 1),
        Ground(144, 9),
        Ground(145, 8),
        Ground(146, 6),
        Ground(147, 5),
        Ground(148, 1),
        Ground(149, 1),
        Ground(150, 1),
        Ground(151, 1),
        Ground(152, 1),
        Ground(153, 1),
        Ground(154, 1),
        Ground(155, 1),
        Ground(156, 1),
        Ground(157, 1),
        Ground(158, 1),
        Ground(159, 1),
        Ground(160, 1),
        Ground(161, 1),
        Ground(162, 1),
        Ground(163, 1),
        Ground(177, 1),
        Ground(178, 1),
        Ground(179, 1),
        Ground(180, 1),
        Ground(181, 1),
        Ground(182, 1),
        Ground(183, 1),
        Ground(184, 1),
        Ground(185, 1),
        Ground(186, 1),
    ]

    plats = [
        SilverThickPlat(7, 8),
        SilverThickPlat(6, 8),

        SilverThickPlat(13, 10),
        SilverThickPlat(14, 10),

        SilverThickPlat(15, 13),
        SilverThickPlat(16, 13),

        SilverThickPlat(27, 13),
        SilverThickPlat(28, 13),
        SilverThickPlat(29, 13),

        SilverThickPlat(23, 6),
        SilverThickPlat(24, 6),
        SilverThickPlat(25, 6),

        OrangeThickPlat(89, 12),
        OrangeThickPlat(90, 12),
        OrangeThickPlat(89, 16),
        OrangeThickPlat(90, 16),

        OrangeThickPlat(93, 14),
        OrangeThickPlat(94, 14),
        OrangeThickPlat(93, 18),
        OrangeThickPlat(94, 18),

        SilverThinPlat(98, 18),
        SilverThinPlat(99, 18),
        SilverThinPlat(100, 18),
        SilverThinPlat(101, 18),
        SilverThinPlat(102, 18),
        SilverThinPlat(103, 18),
        SilverThinPlat(104, 18),
        SilverThinPlat(105, 18),
        SilverThinPlat(106, 18),

        BrownThickPlat(108, 15),
        BrownThickPlat(109, 15),

        BrownThickPlat(110, 12),
        BrownThickPlat(111, 12),

        BrownThickPlat(112, 9),
        BrownThickPlat(113, 9),

        OrangeThickPlat(73, 7),
        OrangeThickPlat(72, 6),

        OrangeThickPlat(134, 5),
        OrangeThickPlat(133, 4),

        GoldThickPlat(143, 4),
        GoldThickPlat(143, 7),
        GoldThickPlat(140, 8),

        OrangeThickPlat(151, 4),
        OrangeThickPlat(152, 4),

        OrangeThickPlat(157, 7),
        OrangeThickPlat(148, 7),
        OrangeThickPlat(149, 7),
        OrangeThickPlat(150, 7),

        OrangeThickPlat(154, 7),
        OrangeThickPlat(155, 7),
        OrangeThickPlat(156, 7),
        OrangeThickPlat(157, 7),
        OrangeThickPlat(158, 7),

        # OrangeThickPlat(159, 8),
        # OrangeThickPlat(160, 8),
        # OrangeThickPlat(161, 8),

        GoldThickPlat(164, 4),
        GoldThickPlat(165, 4),

        GoldThickPlat(167, 6),
        GoldThickPlat(168, 6),

        GoldThickPlat(163, 8),
        GoldThickPlat(164, 8),
    ]

    list_blocks = [
        GoldBlock(40, 5),
        GoldBlock(41, 5),
        GoldBlock(42, 5),
        GoldBlock(43, 5),
        GoldBlock(39, 6),
        GoldBlock(44, 6),
        SmallSilverBlock(39.5, 5.5),
        SmallSilverBlock(44, 5.5),

        # SmallSilverBlock(60.5, 7.5),

        # BrownBlock(62, 1),
        # BrownBlock(62, 2),
        # BrownBlock(62, 3),
        # BrownBlock(62, 4),
        # BrownBlock(62, 5),
        # BrownBlock(62, 6),
        # BrownBlock(63, 1),
        # BrownBlock(63, 2),
        # BrownBlock(63, 3),
        # BrownBlock(63, 4),
        # BrownBlock(63, 5),
        # BrownBlock(63, 6),

        SilverBlock(98, 18),
        SilverBlock(107, 18),

        SmallBrownBlock(138.5, 4.5),

        SilverBlock(49, 6),
        SilverBlock(50, 6),
        SilverBlock(51, 6),
        SilverBlock(52, 6),
        SilverBlock(53, 6),

        BrownBlock(138, 5),
        BrownBlock(138, 6),
        BrownBlock(138, 7),
        BrownBlock(138, 8),
        BrownBlock(138, 9),
        BrownBlock(138, 10),
        BrownBlock(138, 11),
        BrownBlock(138, 12),
        BrownBlock(138, 13),
        BrownBlock(138, 14),
        BrownBlock(138, 15),
        BrownBlock(138, 16),
        BrownBlock(138, 17),
        BrownBlock(138, 18),
        BrownBlock(138, 19),
        BrownBlock(138, 20),
        BrownBlock(138, 21),
        BrownBlock(138, 22),
        BrownBlock(138, 23),
        BrownBlock(138, 24),
        BrownBlock(138, 25),
        BrownBlock(138, 26),
        BrownBlock(138, 27),
        BrownBlock(138, 28),
        BrownBlock(138, 29),
        BrownBlock(138, 30),

        BrownBlock(139, 4),
        BrownBlock(139, 5),
        BrownBlock(139, 6),
        BrownBlock(139, 7),
        BrownBlock(139, 8),
        BrownBlock(139, 9),
        BrownBlock(139, 10),
        BrownBlock(139, 11, ),
        BrownBlock(139, 12),
        BrownBlock(139, 13),
        BrownBlock(139, 14),
        BrownBlock(139, 15),
        BrownBlock(139, 16),
        BrownBlock(139, 17),
        BrownBlock(139, 18),
        BrownBlock(139, 19),

        SmallSilverBlock(166.5, 2),
        # SmallSilverBlock(166, 2),

        SmallSilverBlock(169.5, 2),
        # SmallSilverBlock(169, 2),

        SmallSilverBlock(172.5, 2),
        # SmallSilverBlock(172, 2),
    ]

    bricks = [
        BrickBlock(161, 2),
        BrickBlock(161, 3),
        BrickBlock(161, 4),
        BrickBlock(161, 5),
        BrickBlock(161, 6),

        BrickBlock(159, 8),
        BrickBlock(159, 9),

        BrickBlock(11, 1),
        BrickBlock(11, 2),
        BrickBlock(11, 3),
        BrickBlock(11, 4),

        BrickBlock(15, 1),
        BrickBlock(15, 2),
        BrickBlock(15, 3),
        BrickBlock(15, 4),

        BrickBlock(61, 1),
        BrickBlock(61, 2),
        BrickBlock(61, 3),
        BrickBlock(61, 4),
        BrickBlock(61, 5),
        BrickBlock(61, 6),
        BrickBlock(61, 7),

        BrownBlock(139, 20),
        BrownBlock(139, 21),
        BrownBlock(139, 22),
        BrownBlock(139, 23),
        BrownBlock(139, 24),
        BrownBlock(139, 25),
        BrownBlock(139, 26),
        BrownBlock(139, 27),
        BrownBlock(139, 28),
    ]

    list_grs_copy = []

    for i in list_grs:
        No_Blocks_Down = True
        for x in plats + list_blocks + list_grs:
            if i.MakeSelfRect().bottom == x.MakeSelfRect().top and i.MakeSelfRect().left == x.MakeSelfRect().left:
                No_Blocks_Down = False
        if No_Blocks_Down:
            for m in range((((700 - i.y_position) + b_size) // b_size)):
                list_grs_copy.append(Ground(((i.x_position + b_size) // b_size), m))

    list_grs = list_grs_copy + list_grs

    list_grounds_decide = []
    for i in list_grs:
        grass_TF = True
        for x in list_grs:
            if i.MakeSelfRect().top == x.MakeSelfRect().bottom and i.MakeSelfRect().left == x.MakeSelfRect().left:
                grass_TF = False
        if grass_TF:
            list_grounds_decide.append("grass")
        else:
            list_grounds_decide.append("ground")

    # start_game_arrow = StartGame(2, 3, 1)
    # start_game_stage = StartGame(2.4, 3, 2)
    start_games = [
        StartGame(2, 3, 1),
        StartGame(2.4, 3, 2)
    ]

    spikes = [
        Spike(21, 3),
        Spike(21.5, 3),

        Spike(28, 14),
        Spike(28.5, 14),

        Spike(39, 7, 1),
        Spike(44, 7, 1),

        Spike(50, 3),
        Spike(50.5, 3),

        Spike(58, 2, 1),

        Spike(65, 2, 1),
        Spike(66, 2, 1),
        Spike(67, 2, 1),
        Spike(68, 2, 1),
        Spike(69, 2, 1),
        Spike(70, 2, 1),

        Spike(136, 2),
        Spike(136.5, 2),

        Spike(149, 8),
        Spike(149.6, 8),
        Spike(148, 8, 1),

        # Spike(119, 7, 1),
        # Spike(120, 7, 1),
        # Spike(120, 7, 1),

        # Spike(159, 9),
        # Spike(159.5, 9),
        # Spike(160, 9),
        # Spike(160.5, 9),
        # Spike(161, 9),
        # Spike(161.5, 9),

        Spike(162, 2, 1),

        # Spike(166, 2.5),
        # Spike(169, 2.5),
        # Spike(172, 2.5),

        Spike(166.5, 2.5),
        Spike(169.5, 2.5),
        Spike(172.5, 2.5),

        Spike(159, 10, 1),
    ]

    saws = [
        Saw(29.5, 1.5, 3),
        Saw(52.5, 0.5, 3),
        Saw(137, 6, 3),
        Saw(147, 2, 2),
    ]

    fires = [
        Fire(40, 2),
        Fire(41, 2),
        Fire(42, 2),
        Fire(43, 2),

        Fire(161, 7),
    ]

    touch_objects = list_grs + plats + fires + list_blocks
    touch_objects.append(start_games[1])

def start_play_changeable():
    """
    Makes all changeable variables in the game
    :return:
    """
    global checkpoints
    global fall_jump
    global move_scene_x
    global move_scene_y
    global mode
    global side
    global check_ps
    global player_1
    global snakes
    global mushrooms
    global horses
    global mummys
    global fly_plats
    global jump_pads
    global expand_plats
    global spiked_balls
    global fruits
    global coins
    global boxes
    global touch_objects
    global apples, bananas, cherries, coins_not_list
    global timer, invincibility_timer, gravity_timer
    global find_find_mode
    global end_games
    global level
    global break_blocks
    global mystery_boxes, potions_1, potions_2

    # variables
    # -------------------------
    fall_jump = 0
    move_scene_x = 0
    move_scene_y = 0
    mode = "fall"
    side = "r"
    checkpoints = 0
    apples = -1
    bananas = -1
    cherries = -1
    coins_not_list = -1
    timer = Timer()
    find_find_mode = None
    # player_1.x_position = 123
    # player_1.y_position = 532
    # -------------------------

    background_music.stop()
    background_music.play(-1)

    # for i in touch_objects + mystery_boxes:
    #     i.MakeSides()

    timer.Start()



    player_1 = Player(123, 532)

    end_games = [
        EndGame(185, 2)
    ]

    with MongoClient() as fl:
        # new_fl = fl['Final_Project_DB']
        if len(fl['Final_Project_DB_Changeable'].list_collection_names()) > 0:
            new_fl = fl['Final_Project_DB_Changeable']

            player_1.x_position = new_fl['Player'].find()[0]['x_position']
            player_1.y_position = new_fl['Player'].find()[0]['y_position']
            move_scene_x = new_fl['Player'].find()[0]['move_scene_x']
            move_scene_y = new_fl['Player'].find()[0]['move_scene_y']
            fall_jump = new_fl['Player'].find()[0]['fall_jump']
            checkpoints = new_fl['Player'].find()[0]['checkpoints']
            timer = Timer(new_fl['Player'].find()[0]['timer'])
            timer.Start()
            player_1.coins = new_fl['Player'].find()[0]['coins']
            player_1.apples = new_fl['Player'].find()[0]['apples']
            player_1.bananas = new_fl['Player'].find()[0]['bananas']
            player_1.cherries = new_fl['Player'].find()[0]['cherries']

            mushrooms = []
            snakes = []
            horses = []
            mummys = []
            for x in new_fl['Creatures'].find({'Type':'Mushroom'}):
                mushrooms.append(Mushroom(x['x_position'], x['y_position'], x['position_2'], x['position_1'], x['side'], True))

            for x in new_fl['Creatures'].find({'Type':'Snake'}):
                snakes.append(Snake(x['x_position'], x['y_position'], x['position_2'], x['position_1'], x['side'], True))

            for x in new_fl['Creatures'].find({'Type':'Horse'}):
                horses.append(Horse(x['x_position'], x['y_position'], x['position_2'], x['position_1'], x['side'], True, x['lives']))

            for x in new_fl['Creatures'].find({'Type':'Mummy'}):
                mummys.append(Mummy(x['x_position'], x['y_position'], x['position_2'], x['position_1'], x['side'], True, x['lives']))

            fruits = []
            for x in new_fl['Fruits'].find():
                fruits.append(Fruit(x['x_position'], x['y_position'], x['Type'], True))

            coins = []
            for x in new_fl['Coins'].find():
                coins.append(Coin(x['x_position'], x['y_position'], True))

            fly_plats = []
            for x in new_fl['FlyPlats'].find():#(self, x_pos, y_pos, pos_2, fly, pos_1 = -1, work = objects_on, dir = -1, m = False)
                fly_plats.append(FlyPlat(x['x_position'], x['y_position'], x['position_2'], x['Type'], x['position_1'], x['work'], x['direction'], True))

            #(self, x_pos, y_pos, expand, i = b_size, work = objects_on, m = False)
            expand_plats = []
            for x in new_fl['ExpandPlats'].find():
                expand_plats.append(ExpandPlat(x['x_position'], x['y_position'], x['stop_i'], x['i'], x['work'], True))

            jump_pads = []
            for x in new_fl['JumpPads'].find():
                jump_pads.append(JumpPad(x['x_position'], x['y_position'], x['work'], True))


            check_ps = []
            for x in new_fl['Checkpoints'].find():
                check_ps.append(Checkpoint(x['x_position'], x['y_position'], x['TF'], True))

            spiked_balls = []
            for x in new_fl['Spiked_Balls'].find():
                spiked_balls.append(SpikedBall(x['x_position'], x['y_position'], x['gravity_pull'], x['fall'], True))

            boxes = []
            for x in new_fl['Boxes'].find():
                boxes.append(Box(x['x_position'], x['y_position'], x['gravity_pull'], True))

            break_blocks = []
            for x in new_fl['BreakBlocks'].find():
                break_blocks.append(BreakBlock(x['x_position'], x['y_position'], True))

            mystery_boxes = []
            for x in new_fl['MysteryBoxes'].find():
                mystery_boxes.append(MysteryBox(x['x_position'], x['y_position'], x['hits_left'], x['got_potion'],True))

            potions_1 = []
            for x in new_fl['HealthPotions'].find():
                potions_1.append(HealthPotion(x['x_position'], x['y_position'], True))

            potions_2 = []
            for x in new_fl['GravityPotions'].find():
                potions_2.append(GravityPotion(x['x_position'], x['y_position'], True))


            if Timer(new_fl['InvincibilityTimer'].find()[0]['timer']) == -10:
                invincibility_timer = Timer(new_fl['InvincibilityTimer'].find()[0]['timer'])
                invincibility_timer.Start()
            else:
                invincibility_timer = 0

            if Timer(new_fl['GravityTimer'].find()[0]['timer']) == -10:
                gravity_timer = Timer(new_fl['GravityTimer'].find()[0]['timer'])
                gravity_timer.Start()
            else:
                gravity_timer = 0



        if len(fl['Final_Project_DB_Screen'].list_collection_names()) > 0:
            new_fl_2 = fl['Final_Project_DB_Screen']

            if new_fl_2['Screen'].find()[0]['screen'] == 'menu':
                level = 'menu'
            else:
                level = 'level_1'
        else:
            level = 'menu'


    touch_objects += end_games

def reset():
    """
    Resets the position of the player when the player dies
    :return: Nothing
    """
    global move_scene_x
    global move_scene_y
    global player_1
    global fall_jump
    death_sound.play()
    if checkpoints == 0:
        move_scene_x = 0
        move_scene_y = 0
        player_1.x_position = 123
        player_1.y_position = 532 - 1
        # move_scene_x = 12000
        # move_scene_y = 0
        # player_1.x_position = 350
        # player_1.y_position = 550 - 1 - 300
    if checkpoints == 1:
        move_scene_x = 4770
        move_scene_y = -288
        player_1.x_position = 620
        player_1.y_position = 388 - 1
    if checkpoints == 2:
        move_scene_x = 9350
        move_scene_y = -288
        player_1.x_position = 620
        player_1.y_position = 388 - 1
    if checkpoints == 3:
        move_scene_x = 11664
        move_scene_y = 0
        player_1.x_position = 620
        player_1.y_position = 400 - 1
    fall_jump = 0
    player_1.transparency = 0

def check_die():
    """
    Checks if the player died
    :return: Nothing
    """
    global fall_jump
    global mushrooms

    for x in snakes:
        if player_1.MakeSelfRect().colliderect(x.MakeSelfRect()):
            if invincibility_timer == 0:
                reset()
            else:
                if invincibility_timer.Show() > 10000:
                    reset()

    for x in range(len(mushrooms)):
        try:
            player_1.MakeSelfRect().bottom == mushrooms[x].MakeSelfRect().top and player_1.MakeSelfRect().left < mushrooms[x].MakeSelfRect().right and player_1.MakeSelfRect().right > mushrooms[x].MakeSelfRect().left
        except:
            pass

        else:
            if player_1.MakeSelfRect().bottom == mushrooms[x].MakeSelfRect().top and player_1.MakeSelfRect().left < mushrooms[x].MakeSelfRect().right and player_1.MakeSelfRect().right > mushrooms[x].MakeSelfRect().left:
                fall_jump = 15
                mushrooms.pop(x)
                tap_sound.play()
            elif player_1.MakeSelfRect().colliderect(mushrooms[x].MakeSelfRect()):
                if invincibility_timer == 0:
                    reset()
                else:
                    if invincibility_timer.Show() > 10000:
                        reset()

    for x in spikes + saws + spiked_balls:
        if player_1.MakeSelfRect().colliderect(x.MakeSelfRect()):
            if invincibility_timer == 0:
                reset()
            else:
                if invincibility_timer.Show() > 10000:
                    reset()

    for x in fires:
        if player_1.MakeSelfRect().colliderect(x.MakeSelfRectFire()) and x.default == x.stage_on:
            if invincibility_timer == 0:
                reset()
            else:
                if invincibility_timer.Show() > 10000:
                    reset()

    for x in horses + mummys:
        if player_1.MakeSelfRect().colliderect(x.MakeSelfRect()): # and x.default == x.hit_4:
            if invincibility_timer == 0:
                reset()
            else:
                if invincibility_timer.Show() > 10000:
                    reset()

    if player_1.MakeSelfRect().top > 700:
        reset()

def check_make_work():
    """
    Checks if fly_plats, jump_pads and expand_plats can be turned on
    :return: Nothing
    """
    if not game_paused:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in jump_pads + fly_plats + expand_plats:
                if not x.work:
                    if x.MakeSelfRect().collidepoint(event.pos):

                        if x in jump_pads:
                            if player_1.apples >= 1:
                                player_1.apples -= 1
                                x.work = True

                        elif x in fly_plats:
                            if player_1.bananas >= 1:
                                player_1.bananas -= 1
                                x.work = True

                        elif x in expand_plats:
                            if player_1.cherries >= 1:
                                player_1.cherries -= 1
                                x.work = True

def init_all():
    """
    Runs every function for every object
    :return: Nothing
    """
    if not game_paused:
        # for x in mystery_boxes + break_blocks + boxes:
        #     x.MakeSides()
        for x in snakes:
            x.Move()
        for x in mushrooms:
            x.Move()
        for x in horses:
            x.ChangeDefault()
            x.Move()
            x.CheckMode()
        for x in mummys:
            x.ChangeDefault()
            x.Move()
            x.CheckMode()

        for x in fly_plats:
            x.Move()

        for x in jump_pads:
            x.CheckJump()
        for x in expand_plats:
            x.CheckWork()
        for x in spiked_balls:
            x.CheckFall()
        for x in fires:
            x.CheckOn()

        for x in check_ps:
            x.CheckPoint()
        for x in end_games:
            x.CheckChange()

        for x in boxes:
            x.CheckFall()

def check_visible(x):
    """
    Checks if x is visible(inside this screen)
    :param x: The object that will be checked if it's visible or not
    :return: True if visible, else False
    """
    surface_rect = x.MakeSelfRect()
    if surface_rect.left <= 1300 and surface_rect.right >= 0 and surface_rect.top <= 700 and surface_rect.bottom >= 0:
        return True
    else:
        return False

def reset_database():
    """
    Fully resets the database data to it's initial data
    :return: Nothing
    """
    global level
    global mushrooms, snakes, horses, mummys, coins, fruits, fly_plats, spiked_balls, boxes, touch_objects#, original_snakes, original_mushrooms, original_horses, original_mummys
    with MongoClient() as fl:
        new_fl = fl['Final_Project_DB_Changeable']

        new_fl['Player'].drop()
        new_fl['Player'].insert_one({
            'x_position': 123,
            'y_position': 532,
            'move_scene_x': 0,
            'move_scene_y': 0,
            'fall_jump': 0,
            'checkpoints':0,
            'timer':0,
            'coins': 0,
            'apples': 0,
            'bananas': 0,
            'cherries': 0,
        })

        snakes = original_snakes
        mushrooms = original_mushrooms
        horses = original_horses
        mummys = original_mummys

        new_fl['Creatures'].drop()
        for x in snakes + mushrooms + horses + mummys:
            new_fl['Creatures'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'position_1': x.position_1,
                'position_2': x.position_2,
                'side': x.side,
                'Type': "Snake" if isinstance(x, Snake)
                else "Mushroom" if isinstance(x,Mushroom)
                else "Horse" if isinstance(x, Horse)
                else "Mummy",
                'lives': x.lives if isinstance(x, Horse) or isinstance(x, Mummy) else 0
            })

        fruits = original_fruits
        coins = original_coins

        new_fl['Fruits'].drop()
        for x in fruits:
            new_fl['Fruits'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'Type': x.name
            })

        new_fl['Coins'].drop()
        for x in coins:
            new_fl['Coins'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
            })

        fly_plats = original_fly_plats

        new_fl['FlyPlats'].drop()
        for x in fly_plats:
            new_fl['FlyPlats'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'position_1': x.position_1,
                'position_2': x.position_2,
                'Type': x.fly,
                'work': x.work,
                'direction': x.direction
            })

        expand_plats = original_expand_plats

        new_fl['ExpandPlats'].drop()
        for x in expand_plats:
            new_fl['ExpandPlats'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'stop_i': x.stop_i,
                'i': x.i,
                'work': x.work,
            })



        jump_pads = original_jump_pads

        new_fl['JumpPads'].drop()
        for x in jump_pads:
            new_fl['JumpPads'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'work': x.work,
            })


        check_ps = original_check_ps

        new_fl['Checkpoints'].drop()
        for x in check_ps:
            new_fl['Checkpoints'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'TF': x.checkpoint_TF,
            })


        spiked_balls = original_spiked_balls

        new_fl['Spiked_Balls'].drop()
        for x in spiked_balls:
            new_fl['Spiked_Balls'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'gravity_pull': x.gravity_pull,
                'fall': x.fall,
            })

        # copy = [i for i in touch_objects if i not in boxes]
        # touch_objects = copy
        # touch_objects += original_boxes
        boxes = original_boxes

        new_fl['Boxes'].drop()
        for x in boxes:
            new_fl['Boxes'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'gravity_pull': x.gravity_pull
            })


        break_blocks = original_break_blocks
        new_fl['BreakBlocks'].drop()
        for x in break_blocks:
            new_fl['BreakBlocks'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position
            })


        mystery_boxes = original_mystery_boxes
        new_fl['MysteryBoxes'].drop()
        for x in mystery_boxes:
            new_fl['MysteryBoxes'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position,
                'hits_left': x.hits_left,
                'got_potion': x.got_potion
            })


        potions_1 = original_potions_1
        new_fl['HealthPotions'].drop()
        for x in potions_1:
            new_fl['HealthPotions'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position
            })


        potions_2 = original_potions_2
        new_fl['GravityPotions'].drop()
        for x in potions_2:
            new_fl['GravityPotions'].insert_one({
                'x_position': x.x_position,
                'y_position': x.y_position
            })


        new_fl['InvincibilityTimer'].drop()
        new_fl['InvincibilityTimer'].insert_one({
            'timer': 0
        })


        new_fl['GravityTimer'].drop()
        new_fl['GravityTimer'].insert_one({
            'timer': 0
        })

        # invincibility_timer = 0
        # gravity_timer = 0

    # level = lvl

def write_buy_database():
    """
    Writes down Skins, Boosts and Coins at this moment to the database
    :return:
    """
    with MongoClient() as fl:
        new_fl_3 = fl['Final_Project_DB_Buy']

        new_fl_3['Skins'].drop()
        new_fl_3['Skins'].insert_one({
            'mask': skins_products[0].bought,
            'mask_picked': skins_products[0].picked,
            'ninja': skins_products[1].bought,
            'ninja_picked': skins_products[1].picked,
            'pink': skins_products[2].bought,
            'pink_picked': skins_products[2].picked,
            'virtual': skins_products[3].bought,
            'virtual_picked': skins_products[3].picked
        })

        new_fl_3['Boosts'].drop()
        new_fl_3['Boosts'].insert_one({
            'PlayerSpeed': boosts_products[0].level,
            'PlayerJump': boosts_products[1].level,
            'EnemiesSpeed': boosts_products[2].level,
            'CoinsAtEnd': boosts_products[3].level,
            'TimeAtEnd': boosts_products[4].level,
        })

        new_fl_3['Coins'].drop()
        new_fl_3['Coins'].insert_one({
            'coins': coins_total_menu
        })


clock = pygame.time.Clock()
start_play_not_changeable()
start_play_changeable()
while True:
    while level == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with MongoClient() as fl:
                    # timer.End()
                    new_fl_2 = fl['Final_Project_DB_Screen']

                    new_fl_2['Screen'].drop()
                    new_fl_2['Screen'].insert_one({
                        'screen': 'menu'
                    })

                write_buy_database()

                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    with MongoClient() as fl:
                        # timer.End()
                        new_fl_2 = fl['Final_Project_DB_Screen']

                        new_fl_2['Screen'].drop()
                        new_fl_2['Screen'].insert_one({
                            'screen': 'level'
                        })
                    level = "level_1"
                    reset_database()
                    start_play_changeable()
                if buy_menu_rect.collidepoint(event.pos):
                    level = "buy_1"

        blit_menu()

        pygame.display.update()
        clock.tick(60)

    while level == "buy_1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_buy_database()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_back_button_buy_rect.collidepoint(event.pos):
                    level = "menu"
                if rect_buy_1_2.collidepoint(event.pos):
                    level = "buy_2"

                for x in skins_products:
                    if x.image_rect.collidepoint(event.pos):
                        if not x.picked and x.bought:
                            for i in skins_products:
                                if i.picked:
                                    i.picked = False
                                    x.picked = True
                                    player_pictures = x.pictures

                    if x.rect_money.collidepoint(event.pos):
                        if not x.bought:
                            if x.money <= coins_total_menu:
                                coins_total_menu -= x.money
                                x.bought = True
                                for i in skins_products:
                                    if i.picked:
                                        i.picked = False
                                        x.picked = True
                                        player_pictures = x.pictures
                                        buy_sound.play()
                            else:
                                declined_sound.play()

            try:
                for x in skins_products:
                    if x.rect_skin.collidepoint(event.pos):
                        x.mouse_on_image = True
                    else:
                        x.mouse_on_image = False

                    if x.rect_money.collidepoint(event.pos):
                        x.mouse_on_text = True
                    else:
                        x.mouse_on_text = False

                if rect_buy_1_1.collidepoint(event.pos):
                    mouse_on_buy_change[0] = True
                else:
                    mouse_on_buy_change[0] = False

                if rect_buy_1_2.collidepoint(event.pos):
                    mouse_on_buy_change[1] = True
                else:
                    mouse_on_buy_change[1] = False
            except:
                pass

        blit_buy_1()

        pygame.display.update()
        clock.tick(60)

    while level == "buy_2":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_buy_database()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_back_button_buy_rect.collidepoint(event.pos):
                    level = "menu"
                if rect_buy_1_1.collidepoint(event.pos):
                    level = "buy_1"

                for x in boosts_products:
                    if x.rect_2.collidepoint(event.pos):
                        if x.level < 3:
                            if x.level == 0:
                                if x.price_1 <= coins_total_menu:
                                    x.level = 1
                                    coins_total_menu -= x.price_1
                                    buy_sound.play()
                                else:
                                    declined_sound.play()
                            elif x.level == 1:
                                if x.price_2 <= coins_total_menu:
                                    x.level = 2
                                    coins_total_menu -= x.price_2
                                    buy_sound.play()
                                else:
                                    declined_sound.play()
                            elif x.level == 2:
                                if x.price_3 <= coins_total_menu:
                                    x.level = 3
                                    coins_total_menu -= x.price_3
                                    buy_sound.play()
                                else:
                                    declined_sound.play()

            try:
                for x in boosts_products:
                    if x.rect_1.collidepoint(event.pos):
                        x.mouse_on_big = True
                    else:
                        x.mouse_on_big = False

                    if x.rect_2.collidepoint(event.pos):
                        x.mouse_on_small = True
                    else:
                        x.mouse_on_small = False


                if rect_buy_1_1.collidepoint(event.pos):
                    mouse_on_buy_change[0] = True
                else:
                    mouse_on_buy_change[0] = False

                if rect_buy_1_2.collidepoint(event.pos):
                    mouse_on_buy_change[1] = True
                else:
                    mouse_on_buy_change[1] = False
            except:
                pass

            #         if x.rect_money.collidepoint(event.pos):
            #             if not x.bought:
            #                 if x.money <= coins_total_menu:
            #                     coins_total_menu -= x.money
            #                     x.bought = True
            #                     player_pictures = x.pictures
            #
            # try:
            #     for x in skins_products:
            #         if x.rect_skin.collidepoint(event.pos):
            #             x.mouse_on_image = True
            #         else:
            #             x.mouse_on_image = False
            #
            #         if x.rect_money.collidepoint(event.pos):
            #             x.mouse_on_text = True
            #         else:
            #             x.mouse_on_text = False
            #
            #     if rect_buy_1_1.collidepoint(event.pos):
            #         mouse_on_buy_change[0] = True
            #     else:
            #         mouse_on_buy_change[0] = False
            #
            #     if rect_buy_1_2.collidepoint(event.pos):
            #         mouse_on_buy_change[1] = True
            #     else:
            #         mouse_on_buy_change[1] = False
            # except:
            #     pass

        blit_buy_2()

        pygame.display.update()
        clock.tick(60)

    while level == "level_1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with MongoClient() as fl:
                    timer.End()
                    new_fl = fl['Final_Project_DB_Changeable']
                    new_fl_2 = fl['Final_Project_DB_Screen']
                    new_fl_3 = fl['Final_Project_DB_Buy']

                    new_fl['Player'].drop()
                    new_fl['Player'].insert_one({
                        'x_position':player_1.x_position,
                        'y_position':player_1.y_position,
                        'move_scene_x':move_scene_x,
                        'move_scene_y':move_scene_y,
                        'fall_jump':fall_jump,
                        'checkpoints':checkpoints,
                        'timer': timer.Show(),
                        'coins': player_1.coins,
                        'apples': player_1.apples,
                        'bananas': player_1.bananas,
                        'cherries': player_1.cherries
                    })

                    new_fl['Creatures'].drop()
                    for x in snakes + mushrooms + horses + mummys:
                        new_fl['Creatures'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'position_1': x.position_1,
                            'position_2': x.position_2,
                            'side': x.side,
                            'Type': "Snake" if isinstance(x, Snake) else "Mushroom" if isinstance(x, Mushroom) else "Horse" if isinstance(x, Horse) else "Mummy",
                            'lives': x.lives if isinstance(x, Horse) or isinstance(x, Mummy) else 0
                        })

                    new_fl['Fruits'].drop()
                    for x in fruits:
                        new_fl['Fruits'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.original_y,
                            'Type': x.name
                        })

                    new_fl['Coins'].drop()
                    for x in coins:
                        new_fl['Coins'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.original_y,
                        })

                    new_fl['FlyPlats'].drop()
                    for x in fly_plats:
                        new_fl['FlyPlats'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'position_1': x.position_1,
                            'position_2': x.position_2,
                            'Type': x.fly,
                            'work': x.work,
                            'direction': x.direction
                        })

                    #(self, x_pos, y_pos, expand, i = b_size, work = objects_on, m = False)
                    new_fl['ExpandPlats'].drop()
                    for x in expand_plats:
                        new_fl['ExpandPlats'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'stop_i': x.stop_i,
                            'i': x.i,
                            'work': x.work,
                        })


                    new_fl['JumpPads'].drop()
                    for x in jump_pads:
                        new_fl['JumpPads'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'work': x.work,
                        })

                    #(self, x_pos, y_pos, TF = False, m = False)
                    new_fl['Checkpoints'].drop()
                    for x in check_ps:
                        new_fl['Checkpoints'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'TF': x.checkpoint_TF,
                        })

                    #(self, x_pos, y_pos, gravity_pull = 0, fall = False, m = False)
                    new_fl['Spiked_Balls'].drop()
                    for x in spiked_balls:
                        new_fl['Spiked_Balls'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'gravity_pull': x.gravity_pull,
                            'fall': x.fall,
                        })

                    new_fl['Boxes'].drop()
                    for x in boxes:
                        new_fl['Boxes'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'gravity_pull': x.gravity_pull
                        })


                    new_fl['BreakBlocks'].drop()
                    for x in break_blocks:
                        new_fl['BreakBlocks'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position
                        })


                    new_fl['MysteryBoxes'].drop()
                    for x in mystery_boxes:
                        new_fl['MysteryBoxes'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                            'hits_left': x.hits_left,
                            'got_potion': x.got_potion
                        })


                    new_fl['HealthPotions'].drop()
                    for x in potions_1:
                        new_fl['HealthPotions'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                        })


                    new_fl['GravityPotions'].drop()
                    for x in potions_2:
                        new_fl['GravityPotions'].insert_one({
                            'x_position': x.x_position,
                            'y_position': x.y_position,
                        })


                    if invincibility_timer != 0:
                        invincibility_timer.End()

                    new_fl['InvincibilityTimer'].drop()
                    new_fl['InvincibilityTimer'].insert_one({
                        'timer': invincibility_timer.Show() if invincibility_timer != 0 else -1
                    })


                    new_fl['GravityTimer'].drop()
                    new_fl['GravityTimer'].insert_one({
                        'timer': gravity_timer.Show() if gravity_timer != 0 else -10
                    })


                    if invincibility_timer != 0:
                        invincibility_timer.Start()


                    new_fl_2['Screen'].drop()
                    new_fl_2['Screen'].insert_one({
                        'screen': 'level'
                    })

                write_buy_database()

                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_back_button_rect.collidepoint(event.pos):
                    reset_database()
                    level = "menu"

                if restart_button_rect.collidepoint(event.pos):
                    reset_database()
                    start_play_changeable()

                if pause_button_rect.collidepoint(event.pos) and game_paused is False:
                    game_paused = True
                    if invincibility_timer != 0:
                        invincibility_timer.End()
                    if gravity_timer != 0:
                        gravity_timer.End()
                    timer.End()
                elif not_pause_button_rect.collidepoint(event.pos) and game_paused is True:
                    game_paused = False
                    if invincibility_timer != 0:
                        invincibility_timer = Timer(invincibility_timer.Show())
                        invincibility_timer.Start()
                    if gravity_timer != 0:
                        gravity_timer = Timer(gravity_timer.Show())
                        gravity_timer.Start()
                    timer = Timer(timer.Show())
                    timer.Start()

            check_make_work()

        init_all()

        if not game_paused:
            player_1.CheckFruitCoin()
            player_1.CheckDieAnimal()
            keys_pressed()
            player_1.Change_Fall_Jump()
            player_1.Transparency()
            check_die()
        blit_level()

        pygame.display.update()
        clock.tick(60)