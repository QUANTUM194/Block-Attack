import pygame
import random

BLACK  = (0,  0,  0  )
GRAY   = (100,100,100)
WHITE  = (250,250,250)
RED    = (255,0,  0  )
ORANGE = (255,170,0  )
TAN    = (210,170,119)
BROWN  = (139,69, 19 )
YELLOW = (255,255,0  )
GREEN  = (0,  153,0  )
TEAL   = (0,  128,128)
BLUE   = (0,  0,  255)
SKY    = (135,206,235)
INDIGO = (75, 0,  130)
VIOLET = (148,0,  211)

###################### Block ######################
class Block(pygame.sprite.Sprite):
    def __init__(self, currentmap, classification, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.blocklist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = classification
class Cloud(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.cloudlist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "cloud"
        self.movespeed = 1
    def update(self):
        self.rect.x += self.movespeed
        if self.rect.left > self.map.game.screenwidth:
            self.rect.right = 0
class Water(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.waterlist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "water"
        self.expanded = False
    def expand(self):
        if not self.expanded:
            #down
            self.rect.y += 1
            makewater = True
            if self.rect.bottom >= self.map.game.screenheight:
                makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type != "bouncepad" and block.type != "powerup" and block.type != "zombie spawn":
                    makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                if block != self:
                    makewater = False
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
                makewater = False
            self.rect.y -= 1
            if makewater:
                block = Water(self.map,self.map.game.waterimage,self.rect.x,self.rect.y+25,self.map.blockwidth,self.map.blockheight)
            #left
            self.rect.x -= 1
            makewater = True
            if self.rect.left <= 0:
                makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type != "bouncepad" and block.type != "powerup" and block.type != "zombie spawn":
                    makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                if block != self:
                    makewater = False
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
                self.makewater = False
            self.rect.x += 1
            if makewater:
                block = Water(self.map,self.map.game.waterimage,self.rect.x-25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            #right
            self.rect.x += 1
            makewater = True
            if self.rect.right >= self.map.game.screenwidth:
                makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type != "bouncepad" and block.type != "powerup" and block.type != "zombie spawn":
                    makewater = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                if block != self:
                    makewater = False
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
                self.makewater = False
            self.rect.x -= 1
            if makewater:
                block = Water(self.map,self.map.game.waterimage,self.rect.x+25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            self.expanded = True
class Lava(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.lavalist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "lava"
        self.expanded = False
    def expand(self):
        if not self.expanded:
            #up
            self.rect.y -= 1
            makestone = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    if not block.exploding:
                        block.explode()
                elif block.type != "stone" and block.type != "diamond" and block.type != "emerald" and block.type != "gold" and block.type != "iron" and block.type != "ruby":
                    makestone = True
                    block.kill()
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                makestone = True
                block.kill()
            self.rect.y += 1
            if makestone:
                block = Block(self.map,"stone",self.map.game.stoneimage,self.rect.x,self.rect.y-25,self.map.blockwidth,self.map.blockheight)
            #down
            self.rect.y += 1
            makelava = True
            makestone = False
            if self.rect.bottom >= self.map.game.screenheight:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    if not block.exploding:
                        block.explode()
                    makelava = False
                else:
                    makelava = False
                    if block.type != "stone" and block.type != "diamond" and block.type != "emerald" and block.type != "gold" and block.type != "iron" and block.type != "ruby":
                        makestone = True
                        block.kill()
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 1:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                makelava = False
                makestone = True
                block.kill()
            self.rect.y -= 1
            if makelava:
                block = Lava(self.map,self.map.game.lavaimage,self.rect.x,self.rect.y+25,self.map.blockwidth,self.map.blockheight)
            elif makestone:
                block = Block(self.map,"stone",self.map.game.stoneimage,self.rect.x,self.rect.y+25,self.map.blockwidth,self.map.blockheight)
            #left
            self.rect.x -= 1
            makelava = True
            makestone = False
            if self.rect.left <= 0:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    if not block.exploding:
                        block.explode()
                    makelava = False
                else:
                    makelava = False
                    if block.type != "stone" and block.type != "diamond" and block.type != "emerald" and block.type != "gold" and block.type != "iron" and block.type != "ruby":
                        makestone = True
                        block.kill()
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 1:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                makelava = False
                makestone = True
                block.kill()
            self.rect.x += 1
            if makelava:
                block = Lava(self.map,self.map.game.lavaimage,self.rect.x-25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            elif makestone:
                block = Block(self.map,"stone",self.map.game.stoneimage,self.rect.x-25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            #right
            self.rect.x += 1
            makelava = True
            makestone = False
            if self.rect.right >= self.map.game.screenwidth:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    if not block.exploding:
                        block.explode()
                    makelava = False
                else:
                    makelava = False
                    if block.type != "stone" and block.type != "diamond" and block.type != "emerald" and block.type != "gold" and block.type != "iron" and block.type != "ruby":
                        makestone = True
                        block.kill()
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 1:
                makelava = False
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                makelava = False
                makestone = True
                block.kill()
            self.rect.x -= 1
            if makelava:
                block = Lava(self.map,self.map.game.lavaimage,self.rect.x+25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            elif makestone:
                block = Block(self.map,"stone",self.map.game.stoneimage,self.rect.x+25,self.rect.y,self.map.blockwidth,self.map.blockheight)
            self.expanded = True
class Dynamite(pygame.sprite.DirtySprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.blocklist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "dynamite"
        self.exploding = False
        self.damage = 25
        self.knockbackspeed = 10
        self.explosionsize = [125,125]
        self.explosionlife = 5
    def update(self):
        if self.exploding:
            self.explosionlife-=1
        if self.explosionlife < 0:
            self.kill()
    def explode(self):
        if not self.exploding:
            self.map.updateblockscounter = 10
            self.exploding = True
            self.center = self.rect.center
            self.image = pygame.Surface([self.explosionsize[0], self.explosionsize[1]])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                player.health -= self.damage
                if player.rect.center[0] < self.rect.center[0]:
                    player.knockback("left",self.knockbackspeed)
                else:
                    player.knockback("right",self.knockbackspeed)
                if player.rect.center[1] < self.rect.center[1]:
                    player.knockback("down",self.knockbackspeed)
                else:
                    player.knockback("up",self.knockbackspeed)
            for missile in pygame.sprite.spritecollide(self, self.map.missilelist, False):
                missile.kill()
            for bomb in pygame.sprite.spritecollide(self, self.map.bomblist, False):
                bomb.explode()
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "sand" or block.type == "grass" or block.type == "transition" or block.type == "dirt":
                    block.kill()
                elif block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    block.explode()
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                block.kill()
            for block in pygame.sprite.spritecollide(self, self.map.lavalist, False):
                block.kill()
            for zombie in pygame.sprite.spritecollide(self, self.map.zombielist, False):
                zombie.health -= self.damage
                if zombie.rect.center[0] < self.rect.center[0]:
                    zombie.knockback("left",self.knockbackspeed)
                else:
                    zombie.knockback("right",self.knockbackspeed)
                if zombie.rect.center[1] < self.rect.center[1]:
                    zombie.knockback("down",self.knockbackspeed)
                else:
                    zombie.knockback("up",self.knockbackspeed)
            for spawn in pygame.sprite.spritecollide(self, self.map.spawnlist, False):
                spawn.health -= self.damage
class TNT(pygame.sprite.DirtySprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.blocklist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "tnt"
        self.exploding = False
        self.damage = 50
        self.knockbackspeed = 10
        self.explosionsize = [225,225]
        self.explosionlife = 5
    def update(self):
        if self.exploding:
            self.explosionlife-=1
        if self.explosionlife < 0:
            self.kill()
    def explode(self):
        if not self.exploding:
            self.map.updateblockscounter = 10
            self.exploding = True
            self.center = self.rect.center
            self.image = pygame.Surface([self.explosionsize[0], self.explosionsize[1]])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                player.health -= self.damage
                if player.rect.center[0] < self.rect.center[0]:
                    player.knockback("left",self.knockbackspeed)
                else:
                    player.knockback("right",self.knockbackspeed)
                if player.rect.center[1] < self.rect.center[1]:
                    player.knockback("down",self.knockbackspeed)
                else:
                    player.knockback("up",self.knockbackspeed)
            for missile in pygame.sprite.spritecollide(self, self.map.missilelist, False):
                missile.kill()
            for bomb in pygame.sprite.spritecollide(self, self.map.bomblist, False):
                bomb.explode()
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "sand" or block.type == "grass" or block.type == "transition" or block.type == "dirt":
                    block.kill()
                elif block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    block.explode()
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                block.kill()
            for block in pygame.sprite.spritecollide(self, self.map.lavalist, False):
                block.kill()
            for zombie in pygame.sprite.spritecollide(self, self.map.zombielist, False):
                zombie.health -= self.damage
                if zombie.rect.center[0] < self.rect.center[0]:
                    zombie.knockback("left",self.knockbackspeed)
                else:
                    zombie.knockback("right",self.knockbackspeed)
                if zombie.rect.center[1] < self.rect.center[1]:
                    zombie.knockback("down",self.knockbackspeed)
                else:
                    zombie.knockback("up",self.knockbackspeed)
            for spawn in pygame.sprite.spritecollide(self, self.map.spawnlist, False):
                spawn.health -= self.damage
class Nuke(pygame.sprite.DirtySprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.blocklist.add(self)
        self.map.spritelist.add(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "nuke"
        self.exploding = False
        self.damage = 100
        self.knockbackspeed = 10
        self.explosionsize = [475,475]
        self.explosionlife = 5
    def update(self):
        if self.exploding:
            self.explosionlife-=1
        if self.explosionlife < 0:
            self.kill()
    def explode(self):
        if not self.exploding:
            self.map.updateblockscounter = 10
            self.exploding = True
            self.center = self.rect.center
            self.image = pygame.Surface([self.explosionsize[0], self.explosionsize[1]])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                player.health -= self.damage
                if player.rect.center[0] < self.rect.center[0]:
                    player.knockback("left",self.knockbackspeed)
                else:
                    player.knockback("right",self.knockbackspeed)
                if player.rect.center[1] < self.rect.center[1]:
                    player.knockback("down",self.knockbackspeed)
                else:
                    player.knockback("up",self.knockbackspeed)
            for missile in pygame.sprite.spritecollide(self, self.map.missilelist, False):
                missile.kill()
            for bomb in pygame.sprite.spritecollide(self, self.map.bomblist, False):
                bomb.explode()
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    block.explode()
                else:
                    block.kill()
            for block in pygame.sprite.spritecollide(self, self.map.waterlist, False):
                block.kill()
            for block in pygame.sprite.spritecollide(self, self.map.lavalist, False):
                block.kill()
            for zombie in pygame.sprite.spritecollide(self, self.map.zombielist, False):
                zombie.health -= self.damage
                if zombie.rect.center[0] < self.rect.center[0]:
                    zombie.knockback("left",self.knockbackspeed)
                else:
                    zombie.knockback("right",self.knockbackspeed)
                if zombie.rect.center[1] < self.rect.center[1]:
                    zombie.knockback("down",self.knockbackspeed)
                else:
                    zombie.knockback("up",self.knockbackspeed)
            for spawn in pygame.sprite.spritecollide(self, self.map.spawnlist, False):
                spawn.health -= self.damage

##################### Player ######################
class Player(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h, number, name, color):
        super().__init__()
        self.map = currentmap
        self.map.playerlist.add(self)
        self.map.spritelist.add(self)
        self.imageleft = image[0]
        self.imageright = image[1]
        self.image = self.imageright
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.rect.left > self.map.game.screenwidth/2:
            self.direction = "left"
            self.image = self.imageleft
        else:
            self.direction = "right"
            self.image = self.imageright
        self.type = "player"
        self.number = number
        self.name = name
        self.color = color
        self.alive = True
        self.inwater = False
        self.inlava = False
        self.health = 100
        self.texthealth = self.name+" health: "+str(int(round(self.health)))+"%"
        self.gravity = 0.3
        self.jumpspeed = 7
        self.divespeed = 7
        self.movespeed = 5
        self.bouncespeed = 10
        self.knockbackspeed = 5
        self.lavadamage = 1
        self.extrajumps = 1
        self.extrajumpsnow = 0
        self.missiledelay = 10
        self.missiledelaynow = 0
        self.bombdelay = 50
        self.bombdelaynow = 0
        self.xspeed = 0
        self.yspeed = 0
    def update(self):
        if self.alive:
            self.inwater = False
            self.inlava = False
            if len(pygame.sprite.spritecollide(self, self.map.waterlist, False)) > 0:
                self.inwater = True
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
                self.inlava = True
            if self.inlava:
                self.health -= self.lavadamage
            self.texthealth = self.name+" health: "+str(int(round(self.health)))+"%"
            self.missiledelaynow -= 1
            self.bombdelaynow -= 1
            #x collisions
            self.rect.x += self.xspeed
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                self.extrajumpsnow = self.extrajumps
                if block.type == "powerup":
                    block.kill()
                    self.health += 100
                else:
                    if self.xspeed > 0:
                        self.rect.right = block.rect.left
                    elif self.xspeed < 0:
                        self.rect.left = block.rect.right
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                if player != self:
                    self.extrajumpsnow = self.extrajumps
                    if self.xspeed > 0:
                        self.knockback("left",self.knockbackspeed)
                        player.knockback("right",self.knockbackspeed)
                    elif self.xspeed < 0:
                        self.knockback("right",self.knockbackspeed)
                        player.knockback("left",self.knockbackspeed)
            #y collisions
            self.yspeed += self.gravity
            self.rect.y += self.yspeed
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                self.extrajumpsnow = self.extrajumps
                if block.type == "powerup":
                    block.kill()
                    self.health += 100
                elif block.type == "bouncepad":
                    self.yspeed = 0-self.bouncespeed
                    self.rect.bottom = block.rect.top - 10
                else:
                    if self.yspeed > 0:
                        self.rect.bottom = block.rect.top
                        self.yspeed = 0
                    elif self.yspeed < 0:
                        self.rect.top = block.rect.bottom
                        self.yspeed = 0
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                if player != self:
                    self.extrajumpsnow = self.extrajumps
                    if self.yspeed > 0:
                        self.knockback("up",self.knockbackspeed)
                        player.knockback("down",self.knockbackspeed)
                    elif self.yspeed < 0:
                        self.knockback("up",self.knockbackspeed)
                        player.knockback("down",self.knockbackspeed)
            if self.rect.right > self.map.game.screenwidth:
                self.rect.right = self.map.game.screenwidth
            elif self.rect.left < 0:
                self.rect.left = 0
            if self.rect.y > self.map.game.screenheight:
                self.die()
            elif self.rect.y < 0-self.map.game.screenheight:
                self.die()
            if self.health <= 0:
                self.die()
    def jump(self):
        self.rect.y += 1
        if len(pygame.sprite.spritecollide(self, self.map.blocklist, False)) > 0 or self.inwater or self.inlava:
            self.yspeed = 0-self.jumpspeed
            self.extrajumpsnow = self.extrajumps
        elif self.extrajumpsnow > 0:
            self.yspeed = 0-self.jumpspeed
            self.extrajumpsnow -= 1
        self.rect.y -= 1
    def dive(self):
        self.yspeed = self.divespeed
    def moveLeft(self):
        self.direction = "left"
        self.image = self.imageleft
        self.xspeed = 0-self.movespeed
    def moveRight(self):
        self.direction = "right"
        self.image = self.imageright
        self.xspeed = self.movespeed
    def stop(self):
        self.xspeed = 0
    def knockback(self, direction, speed):
        if direction == "up":
            self.rect.y -= 10
            self.yspeed = 0-speed
        elif direction == "down":
            self.rect.y += 10
            self.yspeed = speed
        elif direction == "left":
            self.rect.x -= 10
            self.xspeed = 0-speed
        elif direction == "right":
            self.rect.x += 10
            self.xspeed = speed
    def shootMissile(self):
        if self.missiledelaynow <= 0:
            self.missiledelaynow = self.missiledelay
            if self.direction == "left":
                missile = Missile(self.map,self.rect.left-15,self.rect.y+self.rect.height/2-15/2,15,15,self.color,5,-20)
            elif self.direction == "right":
                missile = Missile(self.map,self.rect.right,self.rect.y+self.rect.height/2-15/2,15,15,self.color,5,20)
    def shootBomb(self):
        if self.bombdelaynow <= 0:
            self.bombdelaynow = self.bombdelay
            if self.direction == "left":
                bomb = Bomb(self.map,self.rect.left-15,self.rect.y-15,15,15,self.color,25,-3,-6)
            elif self.direction == "right":
                bomb = Bomb(self.map,self.rect.right,self.rect.y-15,15,15,self.color,25,3,-6)
    def die(self):
        self.alive = False
        self.health = 0
        self.texthealth = self.name+": DEAD"
        self.color = BLACK
        self.map.playerlist.remove(self)
        self.map.spritelist.remove(self)
##################### Missile #####################
class Missile(pygame.sprite.Sprite):
    def __init__(self, currentmap, x, y, w, h, color, damage, xspeed):
        super().__init__()
        self.map = currentmap
        self.map.missilelist.add(self)
        self.map.spritelist.add(self)
        self.image = pygame.Surface([w,h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "missile"
        self.damage = damage
        self.xspeed = xspeed
    def update(self):
        self.rect.x += self.xspeed
        for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
            if block.type == "tnt" or block.type == "dynamite" or block.type == "nuke":
                block.explode()
            self.kill()
        if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
            self.kill()
        for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
            player.health -= self.damage
            self.kill()
        for zombie in pygame.sprite.spritecollide(self, self.map.zombielist, False):
            zombie.health -= self.damage
            self.kill()
        for building in pygame.sprite.spritecollide(self, self.map.spawnlist, False):
            building.health -= self.damage
            self.kill()
        for missile in pygame.sprite.spritecollide(self, self.map.missilelist, False):
            if missile != self:
                missile.kill()
                self.kill()
        if self.rect.right > self.map.game.screenwidth:
            self.kill()
        elif self.rect.left < 0:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.top < 0-self.map.game.screenheight:
            self.kill()
##################### Bomb #####################
class Bomb(pygame.sprite.Sprite):
    def __init__(self, currentmap, x, y, w, h, color, damage, xspeed, yspeed):
        super().__init__()
        self.map = currentmap
        self.map.bomblist.add(self)
        self.map.spritelist.add(self)
        self.image = pygame.Surface([w,h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "bomb"
        self.exploding = False
        self.gravity = .2
        self.damage = damage
        self.knockbackspeed = 6
        self.fuse = 150
        self.explosionsize = [100,100]
        self.explosionlife = 5
        self.xspeed = xspeed
        self.yspeed = yspeed
    def update(self):
        if not self.exploding:
            self.fuse -= 1
            self.rect.x += self.xspeed
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if self.xspeed > 0:
                    self.rect.right = block.rect.left
                    self.xspeed = 0
                elif self.xspeed < 0:
                    self.rect.left = block.rect.right
                    self.xspeed = 0
            self.yspeed += self.gravity
            self.rect.y += self.yspeed
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "bouncepad" and self.yspeed >= 0:
                    self.rect.bottom = block.rect.top
                    self.yspeed = -10
                else:
                    if self.yspeed > 0:
                        self.rect.bottom = block.rect.top
                        self.yspeed = 0
                    elif self.yspeed < 0:
                        self.rect.top = block.rect.bottom
                        self.yspeed = 0
            if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
                self.explode()
            if len(pygame.sprite.spritecollide(self, self.map.playerlist, False)) > 0:
                self.explode()
            if len(pygame.sprite.spritecollide(self, self.map.zombielist, False)) > 0:
                self.explode()
            if len(pygame.sprite.spritecollide(self, self.map.missilelist, False)) > 0:
                self.explode()
            if self.rect.right > self.map.game.screenwidth:
                self.rect.right = self.map.game.screenwidth
                self.xspeed = 0
            elif self.rect.left < 0:
                self.rect.left = 0
                self.xspeed = 0
            if self.rect.y > self.map.game.screenheight:
                self.kill()
            elif self.rect.y < 0-self.map.game.screenheight:
                self.kill()
        else:
            self.explosionlife -= 1
        if self.fuse <= 0:
            self.explode()
        if self.explosionlife <= 0:
            self.kill()
    def explode(self):
        if self.exploding == False:
            self.exploding = True
            self.center = self.rect.center
            self.image = pygame.Surface([self.explosionsize[0], self.explosionsize[1]])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
                player.health -= self.damage
                if player.rect.center[0] < self.rect.center[0]:
                    player.knockback("left",self.knockbackspeed)
                else:
                    player.knockback("right",self.knockbackspeed)
                if player.rect.center[1] < self.rect.center[1]:
                    player.knockback("down",self.knockbackspeed)
                else:
                    player.knockback("up",self.knockbackspeed)
            for missile in pygame.sprite.spritecollide(self, self.map.missilelist, False):
                missile.kill()
            for bomb in pygame.sprite.spritecollide(self, self.map.bomblist, False):
                bomb.explode()
            for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
                if block.type == "dynamite" or block.type == "tnt" or block.type == "nuke":
                    block.explode()
            for zombie in pygame.sprite.spritecollide(self, self.map.zombielist, False):
                zombie.health -= self.damage
                if zombie.rect.center[0] < self.rect.center[0]:
                    zombie.knockback("left",self.knockbackspeed)
                else:
                    zombie.knockback("right",self.knockbackspeed)
                if zombie.rect.center[1] < self.rect.center[1]:
                    zombie.knockback("down",self.knockbackspeed)
                else:
                    zombie.knockback("up",self.knockbackspeed)
            for spawn in pygame.sprite.spritecollide(self, self.map.spawnlist, False):
                spawn.health -= self.damage
##################### Zombie ######################
class Zombie(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h):
        super().__init__()
        self.map = currentmap
        self.map.zombielist.add(self)
        self.map.spritelist.add(self)
        self.imageleft = image[0]
        self.imageright = image[1]
        self.image = self.imageright
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.rect.left > self.map.game.screenwidth/2:
            self.image = self.imageleft
        else:
            self.image = self.imageright
        self.type = "zombie"
        self.alive = True
        self.inwater = False
        self.inlava = False
        self.health = 15
        self.gravity = 0.1
        self.jumpspeed = 3
        self.divespeed = 3
        self.movespeed = 1
        self.bouncespeed = 3
        self.knockbackspeed = 3
        self.damage = 5
        self.lavadamage = 1
        self.freezedelay = 20
        self.freezedelaynow = 0
        self.jumpdelay = 5
        self.jumpdelaynow = 0
        self.extrajumps = 1
        self.extrajumpsnow = self.extrajumps
        self.xspeed = 0
        self.yspeed = 0
    def update(self):
        self.inwater = False
        self.inlava = False
        if len(pygame.sprite.spritecollide(self, self.map.waterlist, False)) > 0:
            self.inwater = True
        if len(pygame.sprite.spritecollide(self, self.map.lavalist, False)) > 0:
            self.inlava = True
        if self.inlava:
            self.health -= self.lavadamage
        self.freezedelaynow -= 1
        self.jumpdelaynow -= 1
        self.decideMovement()
        #x collisions
        self.rect.x += self.xspeed
        for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
            self.extrajumpsnow = self.extrajumps
            if block.type != "zombie spawn":
                if self.xspeed > 0:
                    self.rect.right = block.rect.left
                    self.moveLeft()
                elif self.xspeed < 0:
                    self.rect.left = block.rect.right
                    self.moveRight()
        for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
            self.extrajumpsnow = self.extrajumps
            if self.xspeed > 0:
                player.health -= self.damage
                player.knockback("right",self.knockbackspeed)
                self.rect.x -= 10
            elif self.xspeed < 0:
                player.health -= self.damage
                player.knockback("left",self.knockbackspeed)
                self.rect.x += 10
        #y collisions
        self.yspeed += self.gravity
        self.rect.y += self.yspeed
        for block in pygame.sprite.spritecollide(self, self.map.blocklist, False):
            self.extrajumpsnow = self.extrajumps
            if block.type == "bouncepad":
                self.yspeed = 0-self.bouncespeed
                self.rect.bottom = block.rect.top
            elif block.type != "zombie spawn":
                if self.yspeed > 0:
                    self.rect.bottom = block.rect.top
                    self.yspeed = 0
                elif self.yspeed < 0:
                    self.rect.top = block.rect.bottom
                    self.yspeed = 0
        for player in pygame.sprite.spritecollide(self, self.map.playerlist, False):
            self.extrajumpsnow = self.extrajumps
            if self.yspeed > 0:
                player.health -= self.damage
                player.knockback("down",self.knockbackspeed)
                self.rect.y += 10
            elif self.yspeed < 0:
                player.health -= self.damage
                player.knockback("up",self.knockbackspeed)
                self.rect.y -= 10
        if self.rect.right > self.map.game.screenwidth:
            self.rect.right = self.map.game.screenwidth
            self.moveLeft()
        elif self.rect.left < 0:
            self.rect.left = 0
            self.moveRight()
        if self.rect.y > self.map.game.screenheight:
            self.kill()
        elif self.rect.y < 0-self.map.game.screenheight:
            self.kill()
        if self.health <= 0:
            self.kill()
    def decideMovement(self):
        if self.freezedelaynow <= 0:
            for player in self.map.playerlist:
                if player.rect.x < self.rect.x:
                    self.moveLeft()
                elif player.rect.x > self.rect.x:
                    self.moveRight()
                if player.rect.y < self.rect.y:
                    self.jump()
                elif player.rect.y > self.rect.y:
                    self.dive()
            if self.xspeed == 0:
                startdir = random.randint(0,1)
                if startdir == 0:
                    self.moveLeft()
                else:
                    self.moveRight()
    def jump(self):
        if self.freezedelaynow <= 0 and self.jumpdelaynow <= 0:
            self.freezedelaynow = self.freezedelay
            self.jumpdelaynow = self.jumpdelay
            self.rect.y += 1
            if len(pygame.sprite.spritecollide(self, self.map.blocklist, False)) > 0 or self.inwater or self.inlava:
                self.yspeed = 0-self.jumpspeed
                self.extrajumpsnow = self.extrajumps
            elif self.extrajumpsnow > 0:
                self.yspeed = 0-self.jumpspeed
                self.extrajumpsnow -= 1
    def dive(self):
        self.yspeed = self.divespeed
    def moveLeft(self):
        self.image = self.imageleft
        self.xspeed = 0-self.movespeed
    def moveRight(self):
        self.image = self.imageright
        self.xspeed = self.movespeed
    def knockback(self, direction, speed):
        self.freezedelaynow = self.freezedelay
        if direction == "up":
            self.yspeed = 0-speed
        elif direction == "down":
            self.yspeed = speed
        elif direction == "left":
            self.image = self.imageleft
            self.xspeed = 0-speed
        elif direction == "right":
            self.image = self.imageright
            self.xspeed = speed
class ZombieSpawn(pygame.sprite.Sprite):
    def __init__(self, currentmap, image, x, y, w, h, spawnspeed, spawnlimit,):
        super().__init__()
        self.map = currentmap
        self.map.spawnlist.add(self)
        self.map.blocklist.add(self)
        self.map.spritelist.add(self)
        self.image1 = image[0]
        self.image2 = image[1]
        self.image3 = image[2]
        self.image4 = image[3]
        self.image5 = image[4]
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "zombie spawn"
        self.health = 100
        self.spawnspeed = spawnspeed
        self.spawnlimit = spawnlimit
        self.spawndelay = 100
        self.spawndelaynow = 0
    def update(self):
        self.spawndelaynow -= 1
        if 0 < self.health <= 20:
            self.image = self.image5
        elif 20 < self.health <= 40:
            self.image = self.image4
        elif 40 < self.health <= 60:
            self.image = self.image3
        elif 60 < self.health <= 80:
            self.image = self.image2
        elif 80 < self.health <= 100:
            self.image = self.image1
        if self.spawndelaynow <= 0 and len(self.map.zombielist) < self.spawnlimit:
            self.spawndelaynow = self.spawndelay
            zombie = Zombie(self.map,self.map.game.zombieimage,self.rect.x,self.rect.y,self.rect.width,self.rect.height)
        if self.health <= 0:
            self.kill()

###################### Image ######################
class Image:
    def __init__(self, x, y, w, h, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(w),int(h)))
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
    def update(self, topleft):
        self.image_rect.x = topleft[0]
        self.image_rect.y = topleft[1]
    def blit(self, screen):
        screen.blit(self.image, self.image_rect)
class SpriteImage(pygame.sprite.Sprite):
    def __init__(self, x, y, icon):
        super().__init__()
        self.image = icon
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, topleft):
        self.rect.x = topleft[0]
        self.rect.y = topleft[1]
###################### Text #######################
class Text:
    def __init__(self, center, text, font, size, color):
        self.message = text
        self.center = center
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.text_obj = self.font.render(text, False, color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.center = center
    def update(self, text):
        self.message = text
        self.text_obj = self.font.render(text, False, self.color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.center = self.center
    def blit(self, screen):
        screen.blit(self.text_obj, self.text_rect)
##################### Outline #####################
class Outline:
    def __init__(self, shape, center, w, h, outline, fill, thickness):
        self.shape = shape
        self.x = center[0]-w/2
        self.y = center[1]-h/2
        self.w = w
        self.h = h
        self.outline = outline
        self.fill = fill
        self.thickness = thickness
    def update(self, outline, fill):
        self.outline = outline
        self.fill = fill
    def blit(self, screen):
        if self.shape == "rect":
            pygame.draw.rect(screen,self.outline,(self.x,self.y,self.w,self.h))
            pygame.draw.rect(screen,self.fill,(self.x+self.thickness,self.y+self.thickness,
                                               self.w-self.thickness*2,self.h-self.thickness*2))
        elif self.shape == "oval":
            pygame.draw.ellipse(screen,self.outline,(self.x,self.y,self.w,self.h))
            pygame.draw.ellipse(screen,self.fill,(self.x+self.thickness,self.y+self.thickness,
                                               self.w-self.thickness*2,self.h-self.thickness*2))
##################### Button ######################
class Button:
    def __init__(self, game, center, w, h, text, font, size, c1, c2, c3, c4, c5, c6, thickness):
        self.game = game
        self.hover = False
        self.clicked = False
        self.top = center[1]-h/2
        self.bottom = center[1]+h/2
        self.left = center[0]-w/2
        self.right = center[0]+w/2
        self.outline = Outline("oval",center,w,h,c2,c3,thickness)
        self.text = Text(center,text,font,size,c1)
        self.hoveroutline = Outline("oval",center,w,h,c5,c6,thickness)
        self.hovertext = Text(center,text,font,size,c4)
    def blit(self, screen):
        mousepos = pygame.mouse.get_pos()
        if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
            self.hover = True
            if self.game.leftclick:
                self.clicked = True
            else:
                self.clicked = False
            self.hoveroutline.blit(screen)
            self.hovertext.blit(screen)
        else:
            self.hover = False
            self.clicked = False
            self.outline.blit(screen)
            self.text.blit(screen)
################### Selection #####################
class Selection:
    def __init__(self, game, nextbutton, center, w, h, text, font, size, c1, c2, c3, c4, c5, c6, thickness):
        self.game = game
        self.nextbutton = nextbutton
        self.hover = False
        self.active = False
        self.top = center[1]-h/2
        self.bottom = center[1]+h/2
        self.left = center[0]-w/2
        self.right = center[0]+w/2
        self.outline = Outline("rect",center,w,h,c2,c3,thickness)
        self.text = Text(center,text,font,size,c1)
        self.activeoutline = Outline("rect",center,w,h,c5,c6,thickness)
        self.activetext = Text(center,text,font,size,c4)
    def blit(self, screen):
        mousepos = pygame.mouse.get_pos()
        if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
            self.hover = True
            if self.game.leftclick:
                self.active = True
        else:
            self.hover = False
            if not(self.nextbutton.left <= mousepos[0] <= self.nextbutton.right and self.nextbutton.top <= mousepos[1] <= self.nextbutton.bottom) and self.game.leftclick:
                self.active = False

        if self.active:
            self.activeoutline.blit(screen)
            self.activetext.blit(screen)
        else:
            self.outline.blit(screen)
            self.text.blit(screen)
###################### Input ######################
class Input:
    def __init__(self, game, center, w, h, defaulttext, startingtext, font, size, c1, c2, c3, c4, c5, c6, c7, thickness, parent, editable):
        self.game = game
        self.hover = False
        self.active = False
        self.top = center[1]-h/2
        self.bottom = center[1]+h/2
        self.left = center[0]-w/2
        self.right = center[0]+w/2
        
        self.outline = Outline("rect",center,w,h,c2,c3,thickness)
        self.text = Text(center,startingtext,font,size,c1)
        self.activeoutline = Outline("rect",center,w,h,c5,c6,thickness)
        self.activetext = Text(center,startingtext,font,size,c4)
        self.defaulttext = Text(center,defaulttext,font,size,c7)
        self.parent = parent
        self.editable = editable
    def update(self,char):
        if char == "backspace":
            if len(self.text.message) >= 1:
                self.text.update(self.text.message[:-1])
                self.activetext.update(self.activetext.message[:-1])
        elif char == "delete":
            self.text.update("")
            self.activetext.update("")
        else:
            self.text.update(self.text.message+char)
            self.activetext.update(self.activetext.message+char)
        if self.parent == "campaignname":
            if len(self.text.message) >= 1:
                self.game.campaignname = self.text.message
            else:
                self.game.campaignname = self.defaulttext.message
        elif self.parent == "wifiplayer1name":
            if len(self.text.message) >= 1:
                self.game.wifiplayer1name = self.text.message
            else:
                self.game.wifiplayer1name = self.defaulttext.message
        elif self.parent == "wifiplayer2name":
            if len(self.text.message) >= 1:
                self.game.wifiplayer2name = self.text.message
            else:
                self.game.wifiplayer2name = self.defaulttext.message
        elif self.parent == "localplayer1name":
            if len(self.text.message) >= 1:
                self.game.localplayer1name = self.text.message
            else:
                self.game.localplayer1name = self.defaulttext.message
        elif self.parent == "localplayer2name":
            if len(self.text.message) >= 1:
                self.game.localplayer2name = self.text.message
            else:
                self.game.localplayer2name = self.defaulttext.message
        elif self.parent == "ipaddress":
            if len(self.text.message) >= 1:
                self.game.ipaddress = self.text.message
            else:
                self.game.ipaddress = self.defaulttext.message
    def blit(self, screen):
        if self.editable:
            mousepos = pygame.mouse.get_pos()
            if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
                self.hover = True
                if self.game.leftclick:
                    self.active = True
            else:
                self.hover = False
                if self.game.leftclick:
                    self.active = False

            if self.active:
                self.activeoutline.blit(screen)
                self.activetext.blit(screen)
            else:
                self.outline.blit(screen)
                if len(self.text.message) >= 1:
                    self.text.blit(screen)
                else:
                    self.defaulttext.blit(screen)
        else:
            self.outline.blit(screen)
            if len(self.text.message) >= 1:
                self.text.blit(screen)
            else:
                self.defaulttext.blit(screen)
################# Character Input #################
class CharacterInput:
    def __init__(self, game, center, w, h, playericonlist, startingvalue, c1, c2, thickness, parent, editable):
        self.game = game
        self.hover = False
        self.clicked = False
        self.top = center[1]-h/2
        self.bottom = center[1]+h/2
        self.left = center[0]-w/2
        self.right = center[0]+w/2

        self.playericonlist = playericonlist
        self.currenticon = playericonlist[startingvalue]
        self.image = self.currenticon
        self.rect = self.image.get_rect()
        self.rect.x = self.left+5
        self.rect.y = self.top+5
        self.counter = startingvalue
        self.parent = parent
        self.editable = editable
        
        self.outline = Outline("rect",center,w,h,c1,WHITE,thickness)
        self.hoveroutline = Outline("rect",center,w,h,c2,WHITE,thickness)
    def nextIcon(self):
        if self.counter == len(self.playericonlist)-1:
            self.counter = 0
        else:
            self.counter += 1
        self.currenticon = self.playericonlist[self.counter]
        self.image = self.currenticon
        if self.parent == "campaignicon":
            self.game.campaignimagecounter = self.counter
        elif self.parent == "wifiplayer1icon":
            self.game.wifiplayer1imagecounter = self.counter
        elif self.parent == "wifiplayer2icon":
            self.game.wifiplayer2imagecounter = self.counter
        elif self.parent == "localplayer1icon":
            self.game.localplayer1imagecounter = self.counter
        elif self.parent == "localplayer2icon":
            self.game.localplayer2imagecounter = self.counter
    def blit(self, screen):
        if self.editable:
            mousepos = pygame.mouse.get_pos()
            if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
                self.hover = True
                if self.game.leftclick:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.hover = False
                if self.game.leftclick:
                    self.clicked = False

            if self.clicked:
                self.nextIcon()
            if self.hover:
                self.hoveroutline.blit(screen)
                screen.blit(self.image, self.rect)
            else:
                self.outline.blit(screen)
                screen.blit(self.image, self.rect)
        else:
            self.outline.blit(screen)
            screen.blit(self.image, self.rect)

class Map:
    def __init__(self, gamemode, game, blockwidth, blockheight, background, center, w, h, outline, hoveroutline, fill, array):
        self.gamemode = gamemode
        self.game = game
        self.updateblocks = False
        self.updateblockscounter = 0

        self.outline = Outline("rect",center,w+2*(w/len(array[0])),h+2*(h/len(array)),outline,fill,w/len(array[0]))
        self.hoveroutline = Outline("rect",center,w+2*(w/len(array[0])),h+2*(h/len(array)),hoveroutline,fill,w/len(array[0]))
        self.top = center[1]-h/2-(w/len(array[0]))
        self.bottom = center[1]+h/2+(w/len(array[0]))
        self.left = center[0]-w/2-(h/len(array))
        self.right = center[0]+w/2+(h/len(array))
        self.extralist = pygame.sprite.Group()
        x = center[0]-w/2
        y = center[1]-h/2
        for row in array:
            for character in row:
                if character == "1":
                    block = SpriteImage(x,y,self.game.player1icon)
                    self.extralist.add(block)
                elif character == "2":
                    block = SpriteImage(x,y,self.game.player2icon)
                    self.extralist.add(block)
                elif character == "Z":
                    block = SpriteImage(x,y,self.game.zombieicon)
                    self.extralist.add(block)
                elif character == "U":
                    block = SpriteImage(x,y,self.game.zombiespawnicon)
                    self.extralist.add(block)
                elif character == "V":
                    block = SpriteImage(x,y,self.game.grassicon)
                    self.extralist.add(block)
                elif character == "T":
                    block = SpriteImage(x,y,self.game.transitionicon)
                    self.extralist.add(block)
                elif character == "M":
                    block = SpriteImage(x,y,self.game.dirticon)
                    self.extralist.add(block)
                elif character == "S":
                    block = SpriteImage(x,y,self.game.sandicon)
                    self.extralist.add(block)
                elif character == "B":
                    block = SpriteImage(x,y,self.game.stoneicon)
                    self.extralist.add(block)
                elif character == "J":
                    block = SpriteImage(x,y,self.game.diamondicon)
                    self.extralist.add(block)
                elif character == "E":
                    block = SpriteImage(x,y,self.game.emeraldicon)
                    self.extralist.add(block)
                elif character == "G":
                    block = SpriteImage(x,y,self.game.goldicon)
                    self.extralist.add(block)
                elif character == "I":
                    block = SpriteImage(x,y,self.game.ironicon)
                    self.extralist.add(block)
                elif character == "R":
                    block = SpriteImage(x,y,self.game.rubyicon)
                    self.extralist.add(block)
                elif character == "W":
                    block = SpriteImage(x,y,self.game.watericon)
                    self.extralist.add(block)
                elif character == "L":
                    block = SpriteImage(x,y,self.game.lavaicon)
                    self.extralist.add(block)
                elif character == "^":
                    block = SpriteImage(x,y,self.game.bouncepadicon)
                    self.extralist.add(block)
                elif character == "P":
                    block = SpriteImage(x,y,self.game.powerupicon)
                    self.extralist.add(block)
                elif character == "D":
                    block = SpriteImage(x,y,self.game.dynamiteicon)
                    self.extralist.add(block)
                elif character == "N":
                    block = SpriteImage(x,y,self.game.tnticon)
                    self.extralist.add(block)
                elif character == "A":
                    block = SpriteImage(x,y,self.game.nukeicon)
                    self.extralist.add(block)
                elif character == "C":
                    block = SpriteImage(x,y,self.game.cloudicon)
                    self.extralist.add(block)
                x += w/len(array[0])
            x = center[0]-w/2
            y += h/len(array)

        self.blockwidth = blockwidth
        self.blockheight = blockheight
        self.background = background
        self.array = array
        
        self.victory = False
        self.victorytext1 = Text([self.game.screenwidth/2,self.game.screenheight/2-50],
                                "You broke the game!",self.game.font,50,BLACK)
        self.victorytext2 = Text([self.game.screenwidth/2,self.game.screenheight/2],
                                "Press 1 to exit",self.game.font,20,BLACK)
        self.victorytext3 = Text([self.game.screenwidth/2,self.game.screenheight/2+25],
                                "Press 2 to restart",self.game.font,20,BLACK)

        self.spritelist = pygame.sprite.Group()
        self.playerlist = pygame.sprite.Group()
        self.missilelist = pygame.sprite.Group()
        self.bomblist = pygame.sprite.Group()
        self.blocklist = pygame.sprite.Group()
        self.waterlist = pygame.sprite.Group()
        self.lavalist = pygame.sprite.Group()
        self.cloudlist = pygame.sprite.Group()
        self.zombielist = pygame.sprite.Group()
        self.spawnlist = pygame.sprite.Group()
    def reset(self):
        self.updateblockscounter = 0
        self.victory = False
        self.spritelist.empty()
        self.playerlist.empty()
        self.missilelist.empty()
        self.bomblist.empty()
        self.blocklist.empty()
        self.waterlist.empty()
        self.lavalist.empty()
        self.cloudlist.empty()
        self.zombielist.empty()
        self.spawnlist.empty()

        x = 0
        y = 0
        for row in self.array:
            for character in row:
                if character == "1":
                    if self.gamemode == "campaign":
                        self.player1 = Player(self,self.game.characterimagelist[self.game.campaignimagecounter],x,y,self.blockwidth,self.blockheight,
                                              1,self.game.campaignname,self.game.charactercolorlist[self.game.campaignimagecounter])
                        self.player1text = Text([self.game.screenwidth/3,self.game.screenheight/2-350],
                                                self.player1.texthealth,self.game.font,20,self.game.charactercolorlist[self.game.campaignimagecounter])
                    elif self.gamemode == "wifi":
                        self.player1 = Player(self,self.game.characterimagelist[self.game.wifiplayer1imagecounter],x,y,self.blockwidth,self.blockheight,
                                              1,self.game.wifiplayer1name,self.game.charactercolorlist[self.game.wifiplayer2imagecounter])
                        self.player1text = Text([self.game.screenwidth/3,self.game.screenheight/2-350],
                                                self.player1.texthealth,self.game.font,20,self.game.charactercolorlist[self.game.wifiplayer1imagecounter])
                    elif self.gamemode == "local":
                        self.player1 = Player(self,self.game.characterimagelist[self.game.localplayer1imagecounter],x,y,self.blockwidth,self.blockheight,
                                              1,self.game.localplayer1name,self.game.charactercolorlist[self.game.localplayer1imagecounter])
                        self.player1text = Text([self.game.screenwidth/3,self.game.screenheight/2-350],
                                                self.player1.texthealth,self.game.font,20,self.game.charactercolorlist[self.game.localplayer1imagecounter])
                elif character == "2":
                    if self.gamemode == "wifi":
                        self.player2 = Player(self,self.game.characterimagelist[self.game.wifiplayer2imagecounter],x,y,self.blockwidth,self.blockheight,
                                              2,self.game.wifiplayer2name,self.game.charactercolorlist[self.game.wifiplayer2imagecounter])
                        self.player2text = Text([self.game.screenwidth/3*2,self.game.screenheight/2-350],
                                                self.player2.texthealth,self.game.font,20,self.game.charactercolorlist[self.game.wifiplayer2imagecounter])
                    elif self.gamemode == "local":
                        self.player2 = Player(self,self.game.characterimagelist[self.game.localplayer2imagecounter],x,y,self.blockwidth,self.blockheight,
                                              1,self.game.localplayer2name,self.game.charactercolorlist[self.game.localplayer2imagecounter])
                        self.player2text = Text([self.game.screenwidth/3*2,self.game.screenheight/2-350],
                                                self.player2.texthealth,self.game.font,20,self.game.charactercolorlist[self.game.localplayer2imagecounter])
                elif character == "Z":
                    zombie = Zombie(self,self.game.zombieimage,x,y,self.blockwidth,self.blockheight)
                    self.zombietext = Text([self.game.screenwidth/3*2,self.game.screenheight/2-350],
                                            "Zombie Count: "+str(len(self.zombielist)),
                                            self.game.font,20,GRAY)
                elif character == "U":
                    zombiespawn = ZombieSpawn(self,self.game.zombiespawnimage,x,y,self.blockwidth,self.blockheight,20,25)
                    self.zombietext = Text([self.game.screenwidth/3*2,self.game.screenheight/2-350],
                                            "Zombie Count: "+str(len(self.zombielist)),
                                            self.game.font,20,GRAY)
                elif character == "V":
                    block = Block(self,"grass",self.game.grassimage,x,y,self.blockwidth,self.blockheight)
                elif character == "T":
                    block = Block(self,"transition",self.game.transitionimage,x,y,self.blockwidth,self.blockheight)
                elif character == "M":
                    block = Block(self,"dirt",self.game.dirtimage,x,y,self.blockwidth,self.blockheight)
                elif character == "S":
                    block = Block(self,"sand",self.game.sandimage,x,y,self.blockwidth,self.blockheight)
                elif character == "B":
                    block = Block(self,"stone",self.game.stoneimage,x,y,self.blockwidth,self.blockheight)
                elif character == "J":
                    block = Block(self,"diamond",self.game.diamondimage,x,y,self.blockwidth,self.blockheight)
                elif character == "E":
                    block = Block(self,"emerald",self.game.emeraldimage,x,y,self.blockwidth,self.blockheight)
                elif character == "G":
                    block = Block(self,"gold",self.game.goldimage,x,y,self.blockwidth,self.blockheight)
                elif character == "I":
                    block = Block(self,"iron",self.game.ironimage,x,y,self.blockwidth,self.blockheight)
                elif character == "R":
                    block = Block(self,"ruby",self.game.rubyimage,x,y,self.blockwidth,self.blockheight)
                elif character == "^":
                    block = Block(self,"bouncepad",self.game.bouncepadimage,x,y,self.blockwidth,self.blockheight)
                elif character == "P":
                    block = Block(self,"powerup",self.game.powerupimage,x,y,self.blockwidth,self.blockheight)
                elif character == "D":
                    block = Dynamite(self,self.game.dynamiteimage,x,y,self.blockwidth,self.blockheight)
                elif character == "N":
                    block = TNT(self,self.game.tntimage,x,y,self.blockwidth,self.blockheight)
                elif character == "A":
                    block = Nuke(self,self.game.nukeimage,x,y,self.blockwidth,self.blockheight)
                elif character == "C":
                    cloud = Cloud(self,self.game.cloudimage,x,y,self.blockwidth,self.blockheight)
                x += self.blockwidth
            x = 0
            y += self.blockheight

        x = 0
        y = 0
        for row in self.array:
            for character in row:
                if character == "W":
                    block = Water(self,self.game.waterimage,x,y,self.blockwidth,self.blockheight)
                elif character == "L":
                    block = Lava(self,self.game.lavaimage,x,y,self.blockwidth,self.blockheight)
                x += self.blockwidth
            x = 0
            y += self.blockheight
    def checkVictory(self):
        if len(self.playerlist) == 1 and len(self.zombielist) == 0 and len(self.spawnlist) == 0:
            self.victory = True
            for player in self.playerlist:
                self.victorytext1.update(player.name+" Wins!")
        elif len(self.playerlist) == 0 and (len(self.zombielist) > 0 or len(self.spawnlist) > 0):
            self.victory = True
            self.victorytext1.update("The Zombies Win!")
        elif len(self.playerlist) == 0 and len(self.zombielist) == 0 and len(self.spawnlist) == 0:
            self.victory = True
            self.victorytext1.update("Draw!")
    def blit(self, screen):
        mousepos = pygame.mouse.get_pos()
        if self.left <= mousepos[0] <= self.right and self.top <= mousepos[1] <= self.bottom:
            self.hover = True
            if self.game.leftclick:
                self.clicked = True
            else:
                self.clicked = False
            self.hoveroutline.blit(screen)
            self.extralist.draw(screen)
        else:
            self.hover = False
            self.clicked = False
            self.outline.blit(screen)
            self.extralist.draw(screen)

