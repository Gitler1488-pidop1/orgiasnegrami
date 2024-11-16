#Создай собственный Шутер!

from pygame import *
import random
from random import randint
import time as t
init()
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, name, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(name), (width, height) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_UP] or keys[K_w]) and self.rect.y > 0:
            self.rect.y -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < win_width-250:
            self.rect.x += self.speed
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 0:
            self.rect.x -= self.speed
        if (keys[K_DOWN] or keys[K_s]) and self.rect.y < win_height-250:
            self.rect.y += self.speed
    def fire(self):
        global fire, last_fire, score
        if (score%5==0) and score > 0:
            bullet1 = Bullet("bullet.png", self.rect.centerx-4, self.rect.top, 10, 100, 50)
        else:
            bullet1 = Bullet("bullet.png", self.rect.centerx-4, self.rect.top, 10, 10, 30)
        bullets.add(bullet1)
        last_fire = t.time()
        fire.play()
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()
class Enemy(GameSprite):
    def update(self):

        
        if (self.rect.y // 100) % 2 == 0:
            self.rect.x += self.speed 
        elif (self.rect.y // 100) % 2 == 1:
            self.rect.x -= self.speed 
        self.rect.y += self.speed
        


        if self.rect.y > win_height-150:
            global lost
            lost += 1
            self.kill()
            monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 60, 60))

win = display.set_mode((0, 0 ), FULLSCREEN)
win_width,win_height = display.get_surface().get_size()

gaym = True
finish = False
score = 0
FPS = 60
timer = time.Clock()
lost = 0


background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
display.set_caption("Shooter")
font0 = font.SysFont("Arial", 30)
font1 = font.SysFont("Arial", 88)
win_image = font0.render("You WIN", True, (0, 255, 255))
lose_image = font0.render("You LOSE", True, (255, 0, 0))
settings = font0.render('Esc-Quit; R-Restart', True, (255,255,255))

mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')



monsters = sprite.Group()
bullets = sprite.Group()

player = Player('rocket.png', 900, 750, 10, 100, 100 )
monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 45, 45))


last_fire = 0

for i in range(5):
    monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 60, 60))


while gaym:
    display.update()

    
    timer.tick()

    for e in event.get():
        if e.type == QUIT or ( e.type == KEYDOWN and e.key == K_ESCAPE ):
            gaym = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if t.time() - last_fire > 1 and not(finish):
                player.fire()
        elif (e.type == KEYDOWN and e.key == K_r):
            score = 0 
            lost = 0      
            player = Player('rocket.png', 900, 750, 10, 100, 100 )
            monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 60, 60))
            image_lost = font1.render('Пропущено:'+str(lost), True, (255,255,255))
            image_score = font1.render('Cчет:'+str(score), True, (255,255,255))
            monsters = sprite.Group()
            for i in range(5):
                monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 60, 60))
            finish = 0

    if not(finish):
        player.update()
        monsters.update()
        bullets.update()

        monsters_list = sprite.groupcollide(monsters, bullets, True, True)
        for monst in monsters_list:
            score += 1
            monsters.add(Enemy('ufo.png', randint(150, win_width-150), randint(-250, -30), randint(3,5), 60, 60))


        image_score = font1.render('Cчет:'+str(score), True, (255,255,255))
        image_lost = font1.render('Пропущено:'+str(lost), True, (255,255,255))

        
        win.blit(background, ((0, 0)))
        win.blit(image_score, ((250,150)))
        win.blit(image_lost, ((250,200)))
        player.reset()
        monsters.draw(win)
        bullets.draw(win)

        monsters_list = sprite.spritecollide(player, monsters, True)
        if len(monsters_list) > 0 or lost >= 15:
            finish = True 
            win.blit(settings, ((850, 400)))
            win.blit(lose_image, ((900, 500)))
            
        if score >= 15:
            finish = True
            win.blit(settings, ((850, 400)))
            win.blit(win_image, ((900, 500)))

        
        
#Спасибо за просмотр
    
