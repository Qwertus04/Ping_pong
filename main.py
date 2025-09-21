from pygame import *


init()
windows = display.set_mode((700, 500))
display.set_caption('Пинг-понг')
clock = time.Clock()
font2 = font.SysFont('Segoe UI', 50)

#Музыка
mixer.music.load('local_forecast.mp3')
silent = mixer.Sound('silent.ogg')
silent.set_volume(0.25)
mixer.music.set_volume(0.20)
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y)).convert_alpha()
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.mask = mask.from_surface(self.image)

    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN]:
            self.rect.y += self.speed
    def update_2(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w]:
            self.rect.y -= self.speed
        if keys_pressed[K_s]:
            self.rect.y += self.speed        

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, speed_y):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed_y
        global count_1
        global count_2
        if self.rect.y < 0 or self.rect.y > 450:
            self.speed_y *= -1
        if self.rect.x > 800 or ball.rect.x < 0:
            if self.rect.x > 800:
                count_1 += 1
            if self.rect.x < 0:
                count_2 += 1    
            self.rect.x = 200
            self.rect.y = 200    
        sprite_collide_1 = sprite.spritecollide(self, group_rocket_1, False, sprite.collide_mask)
        sprite_collide_2 = sprite.spritecollide(self, group_rocket_2, False, sprite.collide_mask)
        if sprite_collide_1 or sprite_collide_2:
            if sprite_collide_1:
                self.rect.x = player_1.rect.right
            if sprite_collide_2:
                self.rect.right = player_2.rect.x    
            self.speed *= -1
            silent.play()
                    
background = transform.scale(image.load('background.png'), (700, 500))

#Экземпляры класса
ball = Ball('ball.png',200,200,2,50,50,2)
player_1 = Player('racket.png',10,10,3,80,100)
player_2 = Player('racket.png',610,10,3,80,100)

#Группы
group_rocket_1 = sprite.Group()
group_rocket_1.add(player_1)
group_rocket_2 = sprite.Group()
group_rocket_2.add(player_2)

count_1 = 0
count_2 = 0
font1 = font.SysFont('Segoe UI', 40)
text_player_1 = font1.render('Счет игрока 2: ' + str(count_2), 1, (255,255,255))
text_player_2 = font1.render('Счет игрока 1: ' + str(count_1), 1, (255,255,255))

win = font2.render('ТЫ ПОБЕДИЛ!', True, (255, 215 ,0))
game_over = font2.render('ТЫ  ПРОИГРАЛ!', True, (255, 0, 0))
finish = False

game = True
while game:
    if finish != True:
        windows.blit(background,(0, 0))
        windows.blit(text_player_1,(210, 5))#ВТОРОЙ ИГРОК
        windows.blit(text_player_2,(210, 60))
        ball.reset()
        player_1.reset()
        player_2.reset()
        player_1.update_1()
        player_2.update_2()
        ball.update()
        text_player_1 = font1.render('Счет игрока 2: ' + str(count_2), 1, (255,255,255))
        text_player_2 = font1.render('Счет игрока 1: ' + str(count_1), 1, (255,255,255))
        if count_1 >= 5:
            finish = True
            win_player_1 = font2.render('ИГРОК 1 ПОБЕДИЛ!', True, (255, 255, 255))
            windows.blit(win_player_1, (220, 200))
        if count_2 >= 5:
            finish = True
            win_player_2 = font2.render('ИГРОК 2 ПОБЕДИЛ!', True, (255, 255, 255))
            windows.blit(win_player_2, (220, 200))       
    for e in event.get():
        if e.type == QUIT:
            game = False

    clock.tick(144)
    display.update()        