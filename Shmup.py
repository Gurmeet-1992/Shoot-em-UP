import pygame as pg
import random
from  os import path

img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

pg.init()

width = 480
height = 600
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

display = pg.display.set_mode((width,height))
pg.display.set_caption('Shoot them up!')
clock = pg.time.Clock()
font_name = pg.font.match_font('arial')

def draw_text(surface,msg,size,x,y):
    font = pg.font.Font(font_name,size)
    text_surface = font.render(msg,True,blue)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct/100)*bar_length
    outline_rect = pg.Rect(x,y,bar_length,bar_height)
    fill_rect = pg.Rect(x,y,fill,bar_height)
    pg.draw.rect(surf,green,fill_rect)
    pg.draw.rect(surf,white,outline_rect,2)


class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (40,35))
        self.image.set_colorkey(black)
        self.radius = 20
        self.rect = self.image.get_rect()
        # pg.draw.circle(self.image,green,self.rect.center,self.radius)

        self.rect.centerx = width/2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100


    def update(self):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        b=bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(b)
        bullets.add(b)
        shoot_sound.play()



class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.orig_image = pg.transform.scale(meteor_img,(50,30))
        self.orig_image.set_colorkey(black)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        # pg.draw.circle(self.image,green,self.rect.center,self.radius)

        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pg.transform.rotate(self.orig_image,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x +=self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height +10 or self.rect.left < -25 or self.rect.right >width + 30:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class bullet(pg.sprite.Sprite):
    def __init__(self,x,y ):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom < 0:
            self.kill()

#load images
background = pg.image.load(path.join(img_dir,'back.png')).convert()
back_rect = background.get_rect()

player_img = pg.image.load(path.join(img_dir,'ufoYellow.png')).convert()
meteor_img = pg.image.load(path.join(img_dir,'big4.png')).convert()
bullet_img = pg.image.load(path.join(img_dir,'laser.png')).convert()
shoot_sound = pg.mixer.Sound(path.join(snd_dir,'Laser_Shoot2.wav'))
exp_snd = []
for snd in ['Explosion7.wav','Explosion8.wav','Explosion15.wav']:
    exp_snd.append(pg.mixer.Sound(path.join(snd_dir,snd)))

pg.mixer.music.load(path.join(snd_dir,'mullyman-the-life-the-hood-the-streetz_2.mp3'))
pg.mixer.music.set_volume(20)


all_sprites=pg.sprite.Group()
mobs=pg.sprite.Group()
bullets = pg.sprite.Group()
p=player()
all_sprites.add(p)
for i in range(8):
    newmob()
start = True
score = 0
pg.mixer.music.play(loops=-1)

while start:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            start = False
        elif event.type == pg.KEYDOWN:
            if event.key ==pg.K_SPACE:
                p.shoot()

    # update
    all_sprites.update()
    hits = pg.sprite.groupcollide(mobs,bullets,True,True)

    for hit in hits:
        random.choice(exp_snd).play()
        score+=1
        newmob()

    #if mob hits player
    hits = pg.sprite.spritecollide(p,mobs,True,pg.sprite.collide_circle)
    for hit in  hits:
        p.shield -= hit.radius *2
        if p.shield<=0:
            start = False
    # draw
    display.fill(black)
    display.blit(background,back_rect)
    all_sprites.draw(display)
    draw_text(display,str(score),18,width/2,20/2)
    draw_shield_bar(display,5,5,p.shield)
    pg.display.flip()
pg.quit()
quit()
