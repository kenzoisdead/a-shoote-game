#Create your own shooter

from pygame import *
from random import randint
lost = 0
score = 0
life = 101

win_width = 700
win_height = 500
font.init()
font2 = font.SysFont("Arial", 36)
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter-game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

img_enemy="ufo.png"
player = Player('rocket.png', 5, win_height - 80,65,65, 5)
monsters = sprite.Group()
for i in range(1, 20):
    monster = Enemy(img_enemy, randint(80, win_width - 80) ,80,65,65, randint(1, 11))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 5):
    asteroid = Enemy('asteroid.png', randint(80, win_width - 80) ,80,65,65, randint(1, 11))
    asteroids.add(asteroid)

bullets = sprite.Group()

# ai = Enemy('cyborg.png', win_width - 80,280 , 19)
# final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
game = True
clock = time.Clock()
fps = 60
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player .fire()

    
    if finish != True:
        window.blit(background,(0,0))

        text = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Skill issues: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        text_life = font2.render("Lives: " + str(life), 1, (255,255,255))
        window.blit(text_life, (10,80))

        
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score +1
            
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, monsters, True)
            life = life -1
            monster = Enemy('ufo.png', randint(80, win_width - 80) ,80,65,65, randint(1, 11))
            monsters.add(monster)

        if sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, asteroids, True)
            life = life -1
            asteroid = Enemy('asteroid.png', randint(80, win_width - 80) ,80,65,65, randint(1, 11))
            asteroids.add(asteroid)



        # ai.update()
        # ai.reset()
        # final.reset()
    display.update()
    clock.tick(fps)