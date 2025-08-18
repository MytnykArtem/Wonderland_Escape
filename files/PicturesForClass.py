import pygame

b_size = 75
b_size = round(b_size)
p_size_x = (b_size // 5) * 4
p_size_y = b_size


pygame.init()
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption('Wonderland Escape')


mask_run_list = [
pygame.image.load("mask_run_1.png").convert_alpha(),
pygame.image.load("mask_run_2.png").convert_alpha(),
pygame.image.load("mask_run_5.png").convert_alpha(),
pygame.image.load("mask_run_7.png").convert_alpha(),
pygame.image.load("mask_run_8.png").convert_alpha(),
pygame.image.load("mask_run_11.png").convert_alpha()
]
mask_run_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in mask_run_list]
mask_running = [mask_run_list[0], mask_run_list[1], mask_run_list[1], mask_run_list[0], mask_run_list[2], mask_run_list[2], mask_run_list[3], mask_run_list[4], mask_run_list[4], mask_run_list[3], mask_run_list[5], mask_run_list[5]]

mask_stand_list = [
pygame.image.load("mask_stand_1.png").convert_alpha(),
pygame.image.load("mask_stand_2.png").convert_alpha(),
pygame.image.load("mask_stand_3.png").convert_alpha(),
pygame.image.load("mask_stand_4.png").convert_alpha()
]
mask_stand_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in mask_stand_list]
mask_standing = [mask_stand_list[0] for _ in range(5)] + [mask_stand_list[1] for _ in range(5)] + [mask_stand_list[2] for _ in range(5)] + [mask_stand_list[3] for _ in range(5)]

mask_jump = pygame.image.load("mask_jump.png").convert_alpha()
mask_jump = pygame.transform.scale(mask_jump, (p_size_x, p_size_y))

mask_fall = pygame.image.load("mask_fall.png").convert_alpha()
mask_fall = pygame.transform.scale(mask_fall, (p_size_x, p_size_y))

mask_wall = pygame.image.load("mask_wall.png").convert_alpha()
mask_wall = pygame.transform.scale(mask_wall, (p_size_x, p_size_y))

mask_pictures = [mask_running, mask_standing, mask_jump, mask_fall, mask_wall]



ninja_run_list = [
pygame.image.load("ninja_run_1.png").convert_alpha(),
pygame.image.load("ninja_run_2.png").convert_alpha(),
pygame.image.load("ninja_run_5.png").convert_alpha(),
pygame.image.load("ninja_run_7.png").convert_alpha(),
pygame.image.load("ninja_run_8.png").convert_alpha(),
pygame.image.load("ninja_run_11.png").convert_alpha()
]
ninja_run_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in ninja_run_list]
ninja_running = [ninja_run_list[0], ninja_run_list[1], ninja_run_list[1], ninja_run_list[0], ninja_run_list[2], ninja_run_list[2], ninja_run_list[3], ninja_run_list[4], ninja_run_list[4], ninja_run_list[3], ninja_run_list[5], ninja_run_list[5]]

ninja_stand_list = [
pygame.image.load("ninja_stand_1.png").convert_alpha(),
pygame.image.load("ninja_stand_2.png").convert_alpha(),
pygame.image.load("ninja_stand_3.png").convert_alpha(),
pygame.image.load("ninja_stand_4.png").convert_alpha()
]
ninja_stand_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in ninja_stand_list]
ninja_standing = [ninja_stand_list[0] for _ in range(5)] + [ninja_stand_list[1] for _ in range(5)] + [ninja_stand_list[2] for _ in range(5)] + [ninja_stand_list[3] for _ in range(5)]

ninja_jump = pygame.image.load("ninja_jump.png").convert_alpha()
ninja_jump = pygame.transform.scale(ninja_jump, (p_size_x, p_size_y))

ninja_fall = pygame.image.load("ninja_fall.png").convert_alpha()
ninja_fall = pygame.transform.scale(ninja_fall, (p_size_x, p_size_y))

ninja_wall = pygame.image.load("ninja_wall.png").convert_alpha()
ninja_wall = pygame.transform.scale(ninja_wall, (p_size_x, p_size_y))

ninja_pictures = [ninja_running, ninja_standing, ninja_jump, ninja_fall, ninja_wall]




pink_run_list = [
pygame.image.load("pink_run_1.png").convert_alpha(),
pygame.image.load("pink_run_2.png").convert_alpha(),
pygame.image.load("pink_run_5.png").convert_alpha(),
pygame.image.load("pink_run_7.png").convert_alpha(),
pygame.image.load("pink_run_8.png").convert_alpha(),
pygame.image.load("pink_run_11.png").convert_alpha()
]
pink_run_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in pink_run_list]
pink_running = [pink_run_list[0], pink_run_list[1], pink_run_list[1], pink_run_list[0], pink_run_list[2], pink_run_list[2], pink_run_list[3], pink_run_list[4], pink_run_list[4], pink_run_list[3], pink_run_list[5], pink_run_list[5]]

pink_stand_list = [
pygame.image.load("pink_stand_1.png").convert_alpha(),
pygame.image.load("pink_stand_2.png").convert_alpha(),
pygame.image.load("pink_stand_3.png").convert_alpha(),
pygame.image.load("pink_stand_4.png").convert_alpha()
]
pink_stand_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in pink_stand_list]
pink_standing = [pink_stand_list[0] for _ in range(5)] + [pink_stand_list[1] for _ in range(5)] + [pink_stand_list[2] for _ in range(5)] + [pink_stand_list[3] for _ in range(5)]

pink_jump = pygame.image.load("pink_jump.png").convert_alpha()
pink_jump = pygame.transform.scale(pink_jump, (p_size_x, p_size_y))

pink_fall = pygame.image.load("pink_fall.png").convert_alpha()
pink_fall = pygame.transform.scale(pink_fall, (p_size_x, p_size_y))

pink_wall = pygame.image.load("pink_wall.png").convert_alpha()
pink_wall = pygame.transform.scale(pink_wall, (p_size_x, p_size_y))

pink_pictures = [pink_running, pink_standing, pink_jump, pink_fall, pink_wall]



virtual_run_list = [
pygame.image.load("virtual_run_1.png").convert_alpha(),
pygame.image.load("virtual_run_2.png").convert_alpha(),
pygame.image.load("virtual_run_5.png").convert_alpha(),
pygame.image.load("virtual_run_7.png").convert_alpha(),
pygame.image.load("virtual_run_8.png").convert_alpha(),
pygame.image.load("virtual_run_11.png").convert_alpha()
]
virtual_run_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in virtual_run_list]
virtual_running = [virtual_run_list[0], virtual_run_list[1], virtual_run_list[1], virtual_run_list[0], virtual_run_list[2], virtual_run_list[2], virtual_run_list[3], virtual_run_list[4], virtual_run_list[4], virtual_run_list[3], virtual_run_list[5], virtual_run_list[5]]

virtual_stand_list = [
pygame.image.load("virtual_stand_1.png").convert_alpha(),
pygame.image.load("virtual_stand_2.png").convert_alpha(),
pygame.image.load("virtual_stand_3.png").convert_alpha(),
pygame.image.load("virtual_stand_4.png").convert_alpha()
]
virtual_stand_list = [pygame.transform.scale(x, (p_size_x, p_size_y)) for x in virtual_stand_list]
virtual_standing = [virtual_stand_list[0] for _ in range(5)] + [virtual_stand_list[1] for _ in range(5)] + [virtual_stand_list[2] for _ in range(5)] + [virtual_stand_list[3] for _ in range(5)]

virtual_jump = pygame.image.load("virtual_jump.png").convert_alpha()
virtual_jump = pygame.transform.scale(virtual_jump, (p_size_x, p_size_y))

virtual_fall = pygame.image.load("virtual_fall.png").convert_alpha()
virtual_fall = pygame.transform.scale(virtual_fall, (p_size_x, p_size_y))

virtual_wall = pygame.image.load("virtual_wall.png").convert_alpha()
virtual_wall = pygame.transform.scale(virtual_wall, (p_size_x, p_size_y))

virtual_pictures = [virtual_running, virtual_standing, virtual_jump, virtual_fall, virtual_wall]

player_pictures = mask_pictures



ground_grass = pygame.image.load("Grass.png").convert_alpha()
ground_grass = pygame.transform.scale(ground_grass, (b_size, b_size))
ground_default = pygame.image.load("Ground.png").convert_alpha()
ground_default = pygame.transform.scale(ground_default, (b_size, b_size))

brick_default = pygame.image.load("Block_Brick.png").convert_alpha()
brick_default = pygame.transform.scale(brick_default, (b_size, b_size))

silver_block_default = pygame.image.load("Block_Silver.png").convert_alpha()
silver_block_default = pygame.transform.scale(silver_block_default, (b_size, b_size))

gold_block_default = pygame.image.load("Block_Gold.png").convert_alpha()
gold_block_default = pygame.transform.scale(gold_block_default, (b_size, b_size))

brown_block_default = pygame.image.load("Block_Brown.png").convert_alpha()
brown_block_default = pygame.transform.scale(brown_block_default, (b_size, b_size))

orange_block_default = pygame.image.load("Block_Orange.png").convert_alpha()
orange_block_default = pygame.transform.scale(orange_block_default, (b_size, b_size))

snake_default = pygame.image.load("snake_1.png").convert_alpha()
snake_default = pygame.transform.scale(snake_default, (40, 20))
snake_1 = pygame.image.load("snake_2.png").convert_alpha()
snake_1 = pygame.transform.scale(snake_1, (40, 20))
snake_2 = pygame.image.load("snake_3.png").convert_alpha()
snake_2 = pygame.transform.scale(snake_2, (40, 20))
snake_3 = pygame.image.load("snake_4.png").convert_alpha()
snake_3 = pygame.transform.scale(snake_3, (40, 20))

mushroom_default = pygame.image.load("mushroom_1.png").convert_alpha()
mushroom_default = pygame.transform.scale(mushroom_default, (45, 50))
mushroom_1 = pygame.image.load("mushroom_2.png").convert_alpha()
mushroom_1 = pygame.transform.scale(mushroom_1, (45, 50))
mushroom_2 = pygame.image.load("mushroom_3.png").convert_alpha()
mushroom_2 = pygame.transform.scale(mushroom_2, (45, 50))
mushroom_3 = pygame.image.load("mushroom_4.png").convert_alpha()
mushroom_3 = pygame.transform.scale(mushroom_3, (45, 50))
mushroom_4 = pygame.image.load("mushroom_5.png").convert_alpha()
mushroom_4 = pygame.transform.scale(mushroom_4, (45, 50))
mushroom_5 = pygame.image.load("mushroom_6.png").convert_alpha()
mushroom_5 = pygame.transform.scale(mushroom_5, (45, 50))
mushroom_6 = pygame.image.load("mushroom_7.png").convert_alpha()
mushroom_6 = pygame.transform.scale(mushroom_6, (45, 50))
mushroom_7 = pygame.image.load("mushroom_8.png").convert_alpha()
mushroom_7 = pygame.transform.scale(mushroom_7, (45, 50))

horse_size_x = b_size * 2
horse_size_y = b_size * 2
horse_run_1 = pygame.image.load("horse_run_1.png").convert_alpha()
horse_run_1 = pygame.transform.scale(horse_run_1, (horse_size_x, horse_size_y))  # (186, 138)
horse_run_2 = pygame.image.load("horse_run_2.png").convert_alpha()
horse_run_2 = pygame.transform.scale(horse_run_2, (horse_size_x, horse_size_y))
horse_run_3 = pygame.image.load("horse_run_3.png").convert_alpha()
horse_run_3 = pygame.transform.scale(horse_run_3, (horse_size_x, horse_size_y))
horse_run_4 = pygame.image.load("horse_run_4.png").convert_alpha()
horse_run_4 = pygame.transform.scale(horse_run_4, (horse_size_x, horse_size_y))
horse_run_5 = pygame.image.load("horse_run_5.png").convert_alpha()
horse_run_5 = pygame.transform.scale(horse_run_5, (horse_size_x, horse_size_y))
horse_run_6 = pygame.image.load("horse_run_6.png").convert_alpha()
horse_run_6 = pygame.transform.scale(horse_run_6, (horse_size_x, horse_size_y))
horse_hit_1 = pygame.image.load("horse_hit_2.png").convert_alpha()
horse_hit_1 = pygame.transform.scale(horse_hit_1, (horse_size_x, horse_size_y))
horse_hit_2 = pygame.image.load("horse_hit_3.png").convert_alpha()
horse_hit_2 = pygame.transform.scale(horse_hit_2, (horse_size_x, horse_size_y))
horse_hit_3 = pygame.image.load("horse_hit_4.png").convert_alpha()
horse_hit_3 = pygame.transform.scale(horse_hit_3, (horse_size_x + horse_size_x // 3, horse_size_y))
horse_hit_4 = pygame.image.load("horse_hit_5.png").convert_alpha()
horse_hit_4 = pygame.transform.scale(horse_hit_4, (horse_size_x + horse_size_x // 1.5, horse_size_y))
horse_hit_5 = pygame.image.load("horse_hit_6.png").convert_alpha()
horse_hit_5 = pygame.transform.scale(horse_hit_5, (horse_size_x + horse_size_x // 10, horse_size_y))

mum_run_1 = pygame.image.load("mum_run_1.png").convert_alpha()
mum_run_1 = pygame.transform.rotozoom(mum_run_1, 0, 3)
mum_run_2 = pygame.image.load("mum_run_2.png").convert_alpha()
mum_run_2 = pygame.transform.rotozoom(mum_run_2, 0, 3)
mum_run_3 = pygame.image.load("mum_run_3.png").convert_alpha()
mum_run_3 = pygame.transform.rotozoom(mum_run_3, 0, 3)
mum_run_4 = pygame.image.load("mum_run_4.png").convert_alpha()
mum_run_4 = pygame.transform.rotozoom(mum_run_4, 0, 3)
mum_run_5 = pygame.image.load("mum_run_5.png").convert_alpha()
mum_run_5 = pygame.transform.rotozoom(mum_run_5, 0, 3)
mum_run_6 = pygame.image.load("mum_run_6.png").convert_alpha()
mum_run_6 = pygame.transform.rotozoom(mum_run_6, 0, 3)
mum_hit_1 = pygame.image.load("mum_hit_1.png").convert_alpha()
mum_hit_1 = pygame.transform.rotozoom(mum_hit_1, 0, 3)
mum_hit_2 = pygame.image.load("mum_hit_2.png").convert_alpha()
mum_hit_2 = pygame.transform.rotozoom(mum_hit_2, 0, 3)
mum_hit_3 = pygame.image.load("mum_hit_3.png").convert_alpha()
mum_hit_3 = pygame.transform.rotozoom(mum_hit_3, 0, 3)
mum_hit_4 = pygame.image.load("mum_hit_4.png").convert_alpha()
mum_hit_4 = pygame.transform.rotozoom(mum_hit_4, 0, 3)
mum_hit_5 = pygame.image.load("mum_hit_5.png").convert_alpha()
mum_hit_5 = pygame.transform.rotozoom(mum_hit_5, 0, 3)
mum_stand_1 = pygame.image.load("mum_stand_1.png").convert_alpha()
mum_stand_1 = pygame.transform.rotozoom(mum_stand_1, 0, 3)
mum_stand_2 = pygame.image.load("mum_stand_2.png").convert_alpha()
mum_stand_2 = pygame.transform.rotozoom(mum_stand_2, 0, 3)

fly_plat_default = pygame.image.load("Plat_Fly_1.png")
fly_plat_default = pygame.transform.scale(fly_plat_default, (b_size, b_size // 10 * 4))
fly_plat_1 = pygame.image.load("Plat_Fly_2.png")
fly_plat_1 = pygame.transform.scale(fly_plat_1, (b_size, b_size // 10 * 4))
fly_plat_2 = pygame.image.load("Plat_Fly_3.png")
fly_plat_2 = pygame.transform.scale(fly_plat_2, (b_size, b_size // 10 * 4))
fly_plat_3 = pygame.image.load("Plat_Fly_4.png")
fly_plat_3 = pygame.transform.scale(fly_plat_3, (b_size, b_size // 10 * 4))
fly_plat_default_2 = pygame.image.load("Banana.png")
fly_plat_default_2 = pygame.transform.scale(fly_plat_default_2, (b_size // 3, b_size // 3))

jump_pad_1 = pygame.image.load("jump_pad_1.png")
jump_pad_1 = pygame.transform.scale(jump_pad_1, (b_size, b_size / 2))
jump_pad_2 = pygame.image.load("jump_pad_2.png")
jump_pad_2 = pygame.transform.scale(jump_pad_2, (b_size, (b_size / 5) * 3))
jump_pad_3 = pygame.image.load("jump_pad_3.png")
jump_pad_3 = pygame.transform.scale(jump_pad_3, (b_size, b_size))
jump_pad_4 = pygame.image.load("jump_pad_4.png")
jump_pad_4 = pygame.transform.scale(jump_pad_4, (b_size, b_size * 1.1))
jump_pad_5 = pygame.image.load("jump_pad_5.png")
jump_pad_5 = pygame.transform.scale(jump_pad_5, (b_size, b_size * 1.1))
jump_pad_default_2 = pygame.image.load("Apple.png")
jump_pad_default_2 = pygame.transform.scale(jump_pad_default_2, (b_size // 3, b_size // 3))

expand_plat_i = b_size - b_size // 4
expand_plat_original = pygame.image.load("Plat_Thin_Wood.png")
expand_plat_default = pygame.transform.scale(expand_plat_original, (expand_plat_i, b_size / 5))
expand_plat_default_2 = pygame.image.load("Cherry.png")
expand_plat_default_2 = pygame.transform.scale(expand_plat_default_2, (b_size // 3, b_size // 3))

spike_default = pygame.image.load("Spike.webp")

saw_1 = pygame.image.load("Saw_1.png")
saw_2 = pygame.image.load("Saw_2.png")
saw_3 = pygame.image.load("Saw_3.png")
saw_4 = pygame.image.load("Saw_4.png")
saw_5 = pygame.image.load("Saw_5.png")
saw_6 = pygame.image.load("Saw_6.png")
saw_7 = pygame.image.load("Saw_7.png")
saw_8 = pygame.image.load("Saw_8.png")

saw_default = pygame.image.load("SpikedBall.png")

fruit_apple = pygame.image.load("Apple.png")
fruit_apple = pygame.transform.scale(fruit_apple, (b_size / 3, b_size / 3))
fruit_banana = pygame.image.load("Banana.png")
fruit_banana = pygame.transform.scale(fruit_banana, (b_size / 3, b_size / 3))
fruit_cherry = pygame.image.load("Cherry.png")
fruit_cherry = pygame.transform.scale(fruit_cherry, (b_size / 3, b_size / 3))

coin_default = pygame.image.load("coin.png")
coin_default = pygame.transform.scale(coin_default, (b_size / 2, b_size / 2))

box_default = pygame.image.load("Box.png")
box_default = pygame.transform.scale(box_default, (b_size, b_size))

break_block_default = pygame.image.load("BreakBlock.webp")
break_block_default = pygame.transform.scale(break_block_default, (b_size, b_size))

mystery_box = pygame.image.load("unknown_block.jpg")
mystery_box = pygame.transform.scale(mystery_box, (b_size, b_size))

potion = pygame.image.load("potion_2.png")
potion = pygame.transform.scale(potion, (b_size // 2, b_size // 2))

potion_2 = pygame.image.load("potion_3.png")
potion_2 = pygame.transform.scale(potion_2, (b_size // 2, b_size // 2))

heart = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart, (b_size // 2, b_size // 2))