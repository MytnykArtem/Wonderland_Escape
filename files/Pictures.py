import pygame

pygame.init()
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption('Wonderland Escape')

text = pygame.font.Font(None, 50)

blue_sky = pygame.image.load("Blue_Sky.webp")
blue_sky = pygame.transform.rotozoom(blue_sky, 0, 6)
blue_sky_rect = blue_sky.get_rect(center=(100, 100))

play_button = pygame.image.load("Play_Button.png")
play_button = pygame.transform.rotozoom(play_button, 0, 0.1)
play_button_rect = play_button.get_rect(center=(650, 250))

go_back_button = pygame.image.load("Go_Back.png")
go_back_button = pygame.transform.scale(go_back_button, (30, 30))
go_back_button_rect = go_back_button.get_rect(topright=(1300, 0))

restart_button = pygame.image.load("Restart.png")
restart_button = pygame.transform.scale(restart_button, (30, 30))
restart_button_rect = restart_button.get_rect(topright=(1270, 0))

pause_button = pygame.image.load("Stop_Button.png")
pause_button = pygame.transform.scale(pause_button, (30, 30))
pause_button_rect = restart_button.get_rect(topleft=(0, 0))

not_pause_button = pygame.image.load("Not_Stop_Button.png")
not_pause_button = pygame.transform.scale(not_pause_button, (30, 30))
not_pause_button_rect = restart_button.get_rect(topleft=(0, 0))

apple = pygame.image.load("Apple.png")
apple = pygame.transform.scale(apple, (30, 30))
apple_rect = apple.get_rect(topleft=(300, 5))

banana = pygame.image.load("Banana.png")
banana = pygame.transform.scale(banana, (30, 30))
banana_rect = banana.get_rect(topleft=(450, 5))

cherry = pygame.image.load("Cherry.png")
cherry = pygame.transform.scale(cherry, (30, 30))
cherry_rect = cherry.get_rect(topleft=(600, 5))

coin_1 = pygame.image.load("coin.png")
coin_1 = pygame.transform.scale(coin_1, (30, 30))
coin_1_rect = coin_1.get_rect(topleft=(850, 5))

coin_menu = pygame.image.load("Coins_Menu.png")
coin_menu = pygame.transform.scale(coin_menu, (60, 60))
coin_menu_rect = coin_menu.get_rect(topleft=(0, 0))

buy_menu = pygame.image.load("shopping_cart.png")
buy_menu = pygame.transform.scale(buy_menu, (60, 60))
buy_menu_rect = coin_menu.get_rect(topright=(1300, 0))

go_back_button_buy = pygame.transform.scale(go_back_button, (60, 60))
go_back_button_buy_rect = go_back_button_buy.get_rect(topright=(1300, 0))

green_bck = pygame.image.load("Green_Colour")
green_bck = pygame.transform.rotozoom(green_bck, 0, 1.5)
green_bck_rect = green_bck.get_rect(topleft=(0, 0))

orange_bck = pygame.image.load("Orange_Colour.png")
orange_bck_rect = orange_bck.get_rect(topleft=(0, 0))

dollar = pygame.image.load("dollar.png")

rect_buy_1_1 = pygame.Rect(1300 / 2, 20, -120, 50)

rect_buy_1_2 = pygame.Rect(1300 / 2, 20, 120, 50)

text_buy = pygame.font.Font(None, 25)

skins_text = text_buy.render(f"Skins", True, 'Black')
skins_text_rect = skins_text.get_rect(center=(1300 / 2 - 60, 20 + 25))

boosts_text = text_buy.render(f"Boosts", True, 'Black')
boosts_text_rect = boosts_text.get_rect(center=(1300 / 2 + 60, 20 + 25))

arrow_top = pygame.image.load("arrow_top.png")


big_text = pygame.font.Font(None, 75)

invincibility_text = big_text.render(f"Invincibility", True, 'White')
invincibility_text_rect = invincibility_text.get_rect(center=(1300 / 2, 75))

invincibility_text_2 = big_text.render(f"Invincibility", True, 'Red')
invincibility_text_rect_2 = invincibility_text.get_rect(center=(1300 / 2, 75))


gravity_text = big_text.render(f"Levitation", True, 'White')
gravity_text_rect = gravity_text.get_rect(center=(1300 / 2, 75))

gravity_text_2 = big_text.render(f"Levitation", True, 'Red')
gravity_text_rect_2 = gravity_text.get_rect(center=(1300 / 2, 75))
