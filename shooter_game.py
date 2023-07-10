from pygame import *
from random import randint
from time import time as timer

import sys
import os
 
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
 
image_folder = resource_path(".")

mixer.init()
back_music = os.path.join(image_folder, "space.ogg")
mixer.music.load(back_music)
mixer.music.set_volume(0.01)
mixer.music.play()
f_sound = os.path.join(image_folder, "fire.ogg")
fire_sound = mixer.Sound(f_sound)
fire_sound.set_volume(0.01)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
win = font2.render('YOU WIN!', True, (0, 255, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))

score = 0
lost = 0
max_lost = 10
goal = 20 
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y)) 


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        img_bullet = os.path.join(image_folder, "bullet.png")
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        fire_sound.play()
        fire_sound.set_volume(0.01)




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0

win_width = 700
win_height = 500
display.set_caption('жаренная попка муравья')
window = display.set_mode((win_width, win_height))
background_sound = os.path.join(image_folder, img_back)
background = transform.scale(image.load(background_sound), (win_width, win_height))

ship = Player(img_hero, 5, win_height-100, 80, 100, 10)

bullets = sprite.Group()

monsters = sprite.Group()

asteroids = sprite.Group()

for i in range(1, 6):
    img_ufo = os.path.join(image_folder, "ufo.png")
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(1, 3):
    img_asteroid = os.path.join(image_folder, "asteroid.png")
    asteroid = Asteroid(img_asteroid, randint(80, win_width-80), -40, 80, 50, randint(2, 2))
    asteroids.add(asteroid)

num_fire = 0
rel_time = False
last_time = 0
now_time = True

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True
       
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                rel = font2.render('Wait, reload...', 1, (255, 255, 255))
                window.blit(rel, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:   
            score +=1
            img_ufo = os.path.join(image_folder, "ufo.png")
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 3))    
            monsters.add(monster)

        collide1 = sprite.groupcollide(asteroids, bullets, False, True)
        


        if life < 1 or lost >= max_lost:
            finish = True
            window.blit(lose, (300, 250))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            asteroid = Asteroid(img_asteroid, randint(80, win_width-80), -40, 80, 50, randint(1, 1))
            asteroids.add(asteroid)
            life -= 1
        
        if score >= goal:
            finish = True
            window.blit(win, (300, 250))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)   

        if life == 1:
            life_color = (150, 0, 0)

        if life == 0:
            life_color = (100, 100, 100)
        text_life = font2.render('Жизни: ' + str(life), 1, life_color)
        window.blit(text_life, (570, 20))

        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3

        mixer.music.load(back_music)
        mixer.music.set_volume(0.01)
        mixer.music.play()

        for bullet in bullets:
            bullet.kill()
        
        for monster in monsters:
            monster.kill()
        
        for asteroid in asteroids:
            asteroid.kill()

        time.delay(5000)

        for i in range(1, 6):
            img_ufo = os.path.join(image_folder, "ufo.png")
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        for i in range(1, 3):
            img_asteroid = os.path.join(image_folder, "asteroid.png")
            asteroid = Asteroid(img_asteroid, randint(80, win_width-80), -40, 80, 50, randint(2, 2))
            asteroids.add(asteroid)

    time.delay(40)  