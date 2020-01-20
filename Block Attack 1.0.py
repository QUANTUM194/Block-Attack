# to-do list
#
# utilize the block dictionary
# design color for menus
# make a map play in the background
# change how input default text work
# add color to text updating
# fix character icons
# generalize comments

import pygame
import socket
import threading
import math
import random
import sys
sys.path.append("./resources")

from classes import Block
from classes import Cloud
from classes import Player
from classes import Zombie
from classes import ZombieSpawn

from classes import Image
from classes import SpriteImage
from classes import Text
from classes import Outline
from classes import Button
from classes import Selection
from classes import Input
from classes import CharacterInput

from classes import Map

from maps import CampaignMaps
from maps import MultiplayerMaps

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

class Game:
    #################### Initiate #####################
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_icon(pygame.image.load("./resources/icon.png"))
        pygame.display.set_caption("Block Attack")
        pygame.mouse.set_visible(0)

        self.ipaddress = "0.0.0.0"
        self.portnumber = 30000

        self.screenwidth = 1200
        self.screenheight = 800
        self.center = (self.screenwidth/2,self.screenheight/2)
        
        #self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight),flags=pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight))
        
        self.clock = pygame.time.Clock()
        self.fps = 45
        self.font = "./resources/fonts/pixelmix.ttf"
        self.fpstext = Text([100,50],"0",self.font,20,BLACK)
        self.background = SKY

        self.arrow = Image(self.center[0],self.center[1],24,44,"./resources/mice/arrow.png")
        self.hand = Image(self.center[0],self.center[1],34,44,"./resources/mice/hand.png")
        self.text = Image(self.center[0],self.center[1],20,40,"./resources/mice/text.png")
        self.leftclick = False

        self.campaignname = "Player 1"
        self.wifiplayer1name = "Player 1"
        self.wifiplayer2name = "Player 2"
        self.localplayer1name = "Player 1"
        self.localplayer2name = "Player 2"
        self.campaignimagecounter = 0
        self.wifiplayer1imagecounter = 0
        self.wifiplayer2imagecounter = 1
        self.localplayer1imagecounter = 0
        self.localplayer2imagecounter = 1

        self.players = {
            "creator":     [TEAL,["./resources/sprites/creatorL.png","./resources/sprites/creatorR.png"]],
            "artist":      [GREEN,["./resources/sprites/artistL.png","./resources/sprites/artistR.png"]],
            "elmo":        [RED,["./resources/sprites/elmoL.png","./resources/sprites/elmoR.png"]],
            "sun":         [ORANGE,["./resources/sprites/sunL.png","./resources/sprites/sunR.png"]],
            "president":   [YELLOW,["./resources/sprites/presidentL.png","./resources/sprites/presidentR.png"]],
            "constantine": [BROWN,["./resources/sprites/constantineL.png","./resources/sprites/constantineR.png"]],
            "granny":      [BLUE,["./resources/sprites/grannyL.png","./resources/sprites/grannyR.png"]],
            "moon":        [WHITE,["./resources/sprites/moonL.png","./resources/sprites/moonR.png"]],
            "melvin":      [BLACK,["./resources/sprites/creatorL.png","./resources/sprites/creatorR.png"]]
        }
        self.blocks = {
            "player1":     ["1",["./resources/sprites/1L.png","./resources/sprites/1R.png"]],
            "player2":     ["2",["./resources/sprites/2L.png","./resources/sprites/2R.png"]],
            "zombie":      ["Z",["./resources/sprites/ZL.png","./resources/sprites/ZR.png"]],
            "zombiespawn": ["U",["./resources/blocks/spawn1.png","./resources/blocks/spawn2.png",
                                 "./resources/blocks/spawn3.png","./resources/blocks/spawn4.png","./resources/blocks/spawn5.png"]],
            
            "sand":       ["S","./resources/blocks/sand.png"],
            "vegetation": ["V","./resources/blocks/grass.png"],
            "topsoil":    ["T","./resources/blocks/topsoil.png"],
            "mud":        ["M","./resources/blocks/dirt.png"],
            "bedrock":    ["B","./resources/blocks/stone.png"],
            "diamond":    ["J","./resources/blocks/diamond.png"],
            "emerald":    ["E","./resources/blocks/emerald.png"],
            "gold":       ["G","./resources/blocks/gold.png"],
            "iron":       ["I","./resources/blocks/iron.png"],
            "ruby":       ["R","./resources/blocks/ruby.png"],
            "dynamite":   ["D","./resources/blocks/dynamite.png"],
            "tnt":        ["N","./resources/blocks/tnt.png"],
            "atombomb":   ["A","./resources/blocks/nuke.png"],
            "cloud":      ["C","./resources/blocks/cloud.png"],
            "water":      ["W","./resources/blocks/water.png"],
            "lava":       ["L","./resources/blocks/lava.png"],
            "bouncepad":  ["^","./resources/blocks/bouncepad.png"],
            "powerup":    ["P","./resources/blocks/powerup.png"]
        }
        self.keys = {
            "leave": pygame.K_1,
            "reset": pygame.K_2,
            
            "campaignjump": pygame.K_w,
            "campaigndive": pygame.K_s,
            "campaignleft": pygame.K_a,
            "campaignright": pygame.K_d,
            "campaignmissile": pygame.K_q,
            "campaignbomb": pygame.K_e,
            
            "player1jump": pygame.K_w,
            "player1dive": pygame.K_s,
            "player1left": pygame.K_a,
            "player1right": pygame.K_d,
            "player1missile": pygame.K_q,
            "player1bomb": pygame.K_e,

            "player2jump": pygame.K_i,
            "player2dive": pygame.K_k,
            "player2left": pygame.K_j,
            "player2right": pygame.K_l,
            "player2missile": pygame.K_o,
            "player2bomb": pygame.K_u
        }

        self.creatorimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/creatorL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/creatorR.png"),(25,25)))
        self.assistantimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/assistantL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/assistantR.png"),(25,25)))
        self.trumpimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/trumpL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/trumpR.png"),(25,25)))
        self.grannyimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/grannyL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/grannyR.png"),(25,25)))
        self.elmoimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/elmoL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/elmoR.png"),(25,25)))
        self.sunimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/sunL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/sunR.png"),(25,25)))
        self.moonimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/moonL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/moonR.png"),(25,25)))
        self.richguyimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/richguyL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/richguyR.png"),(25,25)))
        self.melvinimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/melvinL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/melvinR.png"),(25,25)))
        self.constantineimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/constantineL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/constantineR.png"),(25,25)))
        self.ironmanimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/ironmanL.png"),(25,25)),
                             pygame.transform.scale(pygame.image.load("./resources/sprites/ironmanR.png"),(25,25)))
        
        self.creatoricon = pygame.transform.scale(pygame.image.load("./resources/sprites/creatorR.png"),(40,40))
        self.assistanticon = pygame.transform.scale(pygame.image.load("./resources/sprites/assistantR.png"),(40,40))
        self.trumpicon = pygame.transform.scale(pygame.image.load("./resources/sprites/trumpR.png"),(40,40))
        self.grannyicon = pygame.transform.scale(pygame.image.load("./resources/sprites/grannyR.png"),(40,40))
        self.elmoicon = pygame.transform.scale(pygame.image.load("./resources/sprites/elmoR.png"),(40,40))
        self.sunicon = pygame.transform.scale(pygame.image.load("./resources/sprites/sunR.png"),(40,40))
        self.moonicon = pygame.transform.scale(pygame.image.load("./resources/sprites/moonR.png"),(40,40))
        self.richguyicon = pygame.transform.scale(pygame.image.load("./resources/sprites/richguyR.png"),(40,40))
        self.melvinicon = pygame.transform.scale(pygame.image.load("./resources/sprites/melvinR.png"),(40,40))
        self.constantineicon = pygame.transform.scale(pygame.image.load("./resources/sprites/constantineR.png"),(40,40))
        self.ironmanicon = pygame.transform.scale(pygame.image.load("./resources/sprites/ironmanR.png"),(40,40))
        
        self.characterimagelist = [self.creatorimage,self.assistantimage,self.trumpimage,self.grannyimage,self.elmoimage,self.sunimage,self.moonimage,self.richguyimage,self.melvinimage,self.constantineimage,self.ironmanimage]
        self.charactericonlist = [self.creatoricon,self.assistanticon,self.trumpicon,self.grannyicon,self.elmoicon,self.sunicon,self.moonicon,self.richguyicon,self.melvinicon,self.constantineicon,self.ironmanicon]
        self.charactercolorlist = [TEAL,GREEN,YELLOW,BLUE,RED,ORANGE,WHITE,VIOLET,BLACK,BROWN,RED]

        self.grassimage = pygame.transform.scale(pygame.image.load("./resources/blocks/grass.png"),(25,25))
        self.transitionimage = pygame.transform.scale(pygame.image.load("./resources/blocks/transition.png"),(25,25))
        self.dirtimage = pygame.transform.scale(pygame.image.load("./resources/blocks/dirt.png"),(25,25))
        self.sandimage = pygame.transform.scale(pygame.image.load("./resources/blocks/sand.png"),(25,25))
        self.stoneimage = pygame.transform.scale(pygame.image.load("./resources/blocks/stone.png"),(25,25))
        self.diamondimage = pygame.transform.scale(pygame.image.load("./resources/blocks/diamond.png"),(25,25))
        self.emeraldimage = pygame.transform.scale(pygame.image.load("./resources/blocks/emerald.png"),(25,25))
        self.goldimage = pygame.transform.scale(pygame.image.load("./resources/blocks/gold.png"),(25,25))
        self.ironimage = pygame.transform.scale(pygame.image.load("./resources/blocks/iron.png"),(25,25))
        self.rubyimage = pygame.transform.scale(pygame.image.load("./resources/blocks/ruby.png"),(25,25))
        self.waterimage = pygame.transform.scale(pygame.image.load("./resources/blocks/water.png"),(25,25))
        self.lavaimage = pygame.transform.scale(pygame.image.load("./resources/blocks/lava.png"),(25,25))
        self.bouncepadimage = pygame.transform.scale(pygame.image.load("./resources/blocks/bouncepad.png"),(25,25))
        self.powerupimage = pygame.transform.scale(pygame.image.load("./resources/blocks/powerup.png"),(25,25))
        self.dynamiteimage = pygame.transform.scale(pygame.image.load("./resources/blocks/dynamite.png"),(25,25))
        self.tntimage = pygame.transform.scale(pygame.image.load("./resources/blocks/tnt.png"),(25,25))
        self.nukeimage = pygame.transform.scale(pygame.image.load("./resources/blocks/nuke.png"),(25,25))
        self.cloudimage = pygame.transform.scale(pygame.image.load("./resources/blocks/cloud.png"),(25,25))
        self.zombieimage = (pygame.transform.scale(pygame.image.load("./resources/sprites/zombieL.png"),(25,25)),
                            pygame.transform.scale(pygame.image.load("./resources/sprites/zombieR.png"),(25,25)))
        self.zombiespawnimage = (pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 1.png"),(25,25)),
                                 pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 2.png"),(25,25)),
                                 pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 3.png"),(25,25)),
                                 pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 4.png"),(25,25)),
                                 pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 5.png"),(25,25)))

        self.player1icon = pygame.transform.scale(pygame.image.load("./resources/sprites/creatorR.png"),(4,4))
        self.player2icon = pygame.transform.scale(pygame.image.load("./resources/sprites/assistantR.png"),(4,4))
        self.grassicon = pygame.transform.scale(pygame.image.load("./resources/blocks/grass.png"),(4,4))
        self.transitionicon = pygame.transform.scale(pygame.image.load("./resources/blocks/transition.png"),(4,4))
        self.dirticon = pygame.transform.scale(pygame.image.load("./resources/blocks/dirt.png"),(4,4))
        self.sandicon = pygame.transform.scale(pygame.image.load("./resources/blocks/sand.png"),(4,4))
        self.stoneicon = pygame.transform.scale(pygame.image.load("./resources/blocks/stone.png"),(4,4))
        self.diamondicon = pygame.transform.scale(pygame.image.load("./resources/blocks/diamond.png"),(4,4))
        self.emeraldicon = pygame.transform.scale(pygame.image.load("./resources/blocks/emerald.png"),(4,4))
        self.goldicon = pygame.transform.scale(pygame.image.load("./resources/blocks/gold.png"),(4,4))
        self.ironicon = pygame.transform.scale(pygame.image.load("./resources/blocks/iron.png"),(4,4))
        self.rubyicon = pygame.transform.scale(pygame.image.load("./resources/blocks/ruby.png"),(4,4))
        self.watericon = pygame.transform.scale(pygame.image.load("./resources/blocks/water.png"),(4,4))
        self.lavaicon = pygame.transform.scale(pygame.image.load("./resources/blocks/lava.png"),(4,4))
        self.bouncepadicon = pygame.transform.scale(pygame.image.load("./resources/blocks/bouncepad.png"),(4,4))
        self.powerupicon = pygame.transform.scale(pygame.image.load("./resources/blocks/powerup.png"),(4,4))
        self.dynamiteicon = pygame.transform.scale(pygame.image.load("./resources/blocks/dynamite.png"),(4,4))
        self.tnticon = pygame.transform.scale(pygame.image.load("./resources/blocks/tnt.png"),(4,4))
        self.nukeicon = pygame.transform.scale(pygame.image.load("./resources/blocks/nuke.png"),(4,4))
        self.cloudicon = pygame.transform.scale(pygame.image.load("./resources/blocks/cloud.png"),(4,4))
        self.zombieicon = pygame.transform.scale(pygame.image.load("./resources/sprites/zombieR.png"),(4,4))
        self.zombiespawnicon = pygame.transform.scale(pygame.image.load("./resources/blocks/zombie spawn 1.png"),(4,4))
        #################### Main Menu ####################
        self.mmrect1 = Outline("rect",self.center,500,600,BLACK,TAN,7)
        self.mmheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Block Attack",self.font,50,BLACK)
        self.mmbutton1 = Button(self,[self.screenwidth/2,self.screenheight/2-150],250,75,"Tutorial",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mmbutton2 = Button(self,[self.screenwidth/2,self.screenheight/2-60],250,75,"Campaign",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mmbutton3 = Button(self,[self.screenwidth/2,self.screenheight/2+30],250,75,"Multiplayer",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mmbutton4 = Button(self,[self.screenwidth/2,self.screenheight/2+120],250,75,"Credits",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mmbutton5 = Button(self,[self.screenwidth/2,self.screenheight/2+210],250,75,"Exit",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        #################### Tutorial #####################
        self.turect1 = Outline("rect",[self.screenwidth/2-400,self.screenheight/2],350,600,BLACK,TAN,7)
        self.tukey1 = Outline("rect",[self.screenwidth/2-400,self.screenheight/2],50,50,RED,TAN,5)
        self.tukeyletter1 = Text([self.screenwidth/2-400,self.screenheight/2],"W",self.font,20,RED)
        self.tukey2 = Outline("rect",[self.screenwidth/2-475,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter2 = Text([self.screenwidth/2-475,self.screenheight/2+75],"A",self.font,20,RED)
        self.tukey3 = Outline("rect",[self.screenwidth/2-400,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter3 = Text([self.screenwidth/2-400,self.screenheight/2+75],"S",self.font,20,RED)
        self.tukey4 = Outline("rect",[self.screenwidth/2-325,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter4 = Text([self.screenwidth/2-325,self.screenheight/2+75],"D",self.font,20,RED)
        self.tutext1 = Text([self.screenwidth/2-400,self.screenheight/2+150],"Use WASD to move",self.font,20,BLACK)

        self.turect2 = Outline("rect",[self.screenwidth/2,self.screenheight/2],350,600,BLACK,TAN,7)
        self.tuheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Tutorial",self.font,50,BLACK)
        self.tukey5 = Outline("rect",[self.screenwidth/2-37,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter5 = Text([self.screenwidth/2-37,self.screenheight/2+75],"e",self.font,20,RED)
        self.tukey6 = Outline("rect",[self.screenwidth/2+37,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter6 = Text([self.screenwidth/2+37,self.screenheight/2+75],"u",self.font,20,RED)
        self.tutext2 = Text([self.screenwidth/2,self.screenheight/2+150],"Use e or u to shoot",self.font,20,BLACK)
        self.tubutton1 = Button(self,[self.screenwidth/2,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)

        self.turect3 = Outline("rect",[self.screenwidth/2+400,self.screenheight/2],350,600,BLACK,TAN,7)
        self.tukey7 = Outline("rect",[self.screenwidth/2+363,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter7 = Text([self.screenwidth/2+363,self.screenheight/2+75],"q",self.font,20,RED)
        self.tukey8 = Outline("rect",[self.screenwidth/2+437,self.screenheight/2+75],50,50,RED,TAN,5)
        self.tukeyletter8 = Text([self.screenwidth/2+437,self.screenheight/2+75],"o",self.font,20,RED)
        self.tutext3 = Text([self.screenwidth/2+400,self.screenheight/2+150],"Use q or o to shoot",self.font,20,BLACK)
        self.tutext4 = Text([self.screenwidth/2+400,self.screenheight/2+175],"a bomb",self.font,20,BLACK)
        #################### Campaign #####################
        self.camap1 = Map("campaign",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2-25],192,128,BLACK,RED,SKY,CampaignMaps.map1)
        self.camap2 = Map("campaign",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2-25],192,128,BLACK,RED,SKY,CampaignMaps.map2)
        self.camap3 = Map("campaign",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2-25],192,128,BLACK,RED,SKY,CampaignMaps.map3)
        self.camap4 = Map("campaign",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2-25],192,128,BLACK,RED,SKY,CampaignMaps.map4)
        self.camap5 = Map("campaign",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2+141],192,128,BLACK,RED,SKY,CampaignMaps.map5)
        self.camap6 = Map("campaign",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2+141],192,128,BLACK,RED,SKY,CampaignMaps.map6)
        self.camap7 = Map("campaign",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2+141],192,128,BLACK,RED,SKY,CampaignMaps.map7)
        self.camap8 = Map("campaign",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2+141],192,128,BLACK,RED,SKY,CampaignMaps.map8)
        
        self.carect1 = Outline("rect",self.center,1000,600,BLACK,TAN,7)
        self.caheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Campaign",self.font,50,BLACK)
        self.cainput1 = Input(self,[self.screenwidth/2+50,self.screenheight/2-150],300,50,
                              self.campaignname,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"campaignname",True)
        self.cacharacterinput1 = CharacterInput(self,[self.screenwidth/2-150,self.screenheight/2-150],50,50,self.charactericonlist,0,BLACK,RED,5,"campaignicon", True)
        self.cabutton1 = Button(self,[self.screenwidth/2,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        ################### Multiplayer ###################
        self.murect1 = Outline("rect",self.center,700,600,BLACK,TAN,7)
        self.muheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Multiplayer",self.font,50,BLACK)
        self.mubutton1 = Button(self,[self.screenwidth/2-150,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mubutton2 = Button(self,[self.screenwidth/2+150,self.screenheight/2+300],250,75,"Next",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.muselection1 = Selection(self,self.mubutton2,[self.screenwidth/2-150,self.screenheight/2],250,300,
                                      "Wifi",self.font,50,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.muselection2 = Selection(self,self.mubutton2,[self.screenwidth/2+150,self.screenheight/2],250,300,
                                      "Local",self.font,50,BLACK,BLACK,TAN,RED,RED,TAN,7)

                ### Wifi ###
        self.mwmap1 = Map("wifi",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map1)
        self.mwmap2 = Map("wifi",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map2)
        self.mwmap3 = Map("wifi",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map3)
        self.mwmap4 = Map("wifi",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map4)
        self.mwmap5 = Map("wifi",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map5)
        self.mwmap6 = Map("wifi",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map6)
        self.mwmap7 = Map("wifi",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map7)
        self.mwmap8 = Map("wifi",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map8)
        
        self.mwrect1 = Outline("rect",self.center,700,600,BLACK,TAN,7)
        self.mwheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Multiplayer (Wifi)",self.font,50,BLACK)
        self.mwbutton1 = Button(self,[self.screenwidth/2-150,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mwbutton2 = Button(self,[self.screenwidth/2+150,self.screenheight/2+300],250,75,"Next",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mwselection1 = Selection(self,self.mubutton2,[self.screenwidth/2-150,self.screenheight/2],250,300,
                                      "Host",self.font,50,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mwselection2 = Selection(self,self.mubutton2,[self.screenwidth/2+150,self.screenheight/2],250,300,
                                      "Join",self.font,50,BLACK,BLACK,TAN,RED,RED,TAN,7)        
        self.mwinput1 = Input(self,[self.screenwidth/2,self.screenheight/2+200],300,50,
                              self.ipaddress,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"ipaddress",True)
        
        self.mhrect1 = Outline("rect",self.center,1000,600,BLACK,TAN,7)
        self.mhheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Multiplayer (Host)",self.font,50,BLACK)
        self.mhinput1 = Input(self,[self.screenwidth/2-175,self.screenheight/2-150],300,50,
                              "You","",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"wifiplayer1name",True)
        self.mhinput2 = Input(self,[self.screenwidth/2+250,self.screenheight/2-150],300,50,
                              self.wifiplayer2name,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"wifiplayer2name",False)
        self.mhcharacterinput1 = CharacterInput(self,[self.screenwidth/2-375,self.screenheight/2-150],50,50,self.charactericonlist,0,BLACK,RED,5,"wifiplayer1icon", True)
        self.mhcharacterinput2 = CharacterInput(self,[self.screenwidth/2+50,self.screenheight/2-150],50,50,self.charactericonlist,1,BLACK,RED,5,"wifiplayer2icon", False)
        self.mhbutton1 = Button(self,[self.screenwidth/2-150,self.screenheight/2+300],250,75,"Leave",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mhbutton2 = Button(self,[self.screenwidth/2+150,self.screenheight/2+300],250,75,"Play",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mcrect1 = Outline("rect",self.center,1000,600,BLACK,TAN,7)
        self.mcheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Multiplayer (Client)",self.font,50,BLACK)
        self.mcinput1 = Input(self,[self.screenwidth/2-175,self.screenheight/2-150],300,50,
                              self.wifiplayer1name,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"wifiplayer1name",False)
        self.mcinput2 = Input(self,[self.screenwidth/2+250,self.screenheight/2-150],300,50,
                              "You","",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"wifiplayer2name",True)
        self.mccharacterinput1 = CharacterInput(self,[self.screenwidth/2-375,self.screenheight/2-150],50,50,self.charactericonlist,0,BLACK,RED,5,"wifiplayer1icon", False)
        self.mccharacterinput2 = CharacterInput(self,[self.screenwidth/2+50,self.screenheight/2-150],50,50,self.charactericonlist,1,BLACK,RED,5,"wifiplayer2icon", True)
        self.mcbutton1 = Button(self,[self.screenwidth/2-150,self.screenheight/2+300],250,75,"Leave",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        self.mcbutton2 = Button(self,[self.screenwidth/2+150,self.screenheight/2+300],250,75,"Ready up",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
                ### Local ###
        self.mlmap1 = Map("local",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map1)
        self.mlmap2 = Map("local",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map2)
        self.mlmap3 = Map("local",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map3)
        self.mlmap4 = Map("local",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2-25],192,128,BLACK,RED,SKY,MultiplayerMaps.map4)
        self.mlmap5 = Map("local",self,25,25,SKY,[self.screenwidth/2-345,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map5)
        self.mlmap6 = Map("local",self,25,25,SKY,[self.screenwidth/2-115,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map6)
        self.mlmap7 = Map("local",self,25,25,SKY,[self.screenwidth/2+115,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map7)
        self.mlmap8 = Map("local",self,25,25,SKY,[self.screenwidth/2+345,self.screenheight/2+141],192,128,BLACK,RED,SKY,MultiplayerMaps.map8)
        
        self.mlrect1 = Outline("rect",self.center,1000,600,BLACK,TAN,7)
        self.mlheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Multiplayer (Local)",self.font,50,BLACK)
        self.mlinput1 = Input(self,[self.screenwidth/2-175,self.screenheight/2-150],300,50,
                              self.localplayer1name,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"localplayer1name",True)
        self.mlinput2 = Input(self,[self.screenwidth/2+250,self.screenheight/2-150],300,50,
                              self.localplayer2name,"",self.font,20,BLACK,BLACK,WHITE,RED,RED,WHITE,GRAY,5,"localplayer2name",True)
        self.mlcharacterinput1 = CharacterInput(self,[self.screenwidth/2-375,self.screenheight/2-150],50,50,self.charactericonlist,0,BLACK,RED,5,"localplayer1icon", True)
        self.mlcharacterinput2 = CharacterInput(self,[self.screenwidth/2+50,self.screenheight/2-150],50,50,self.charactericonlist,1,BLACK,RED,5,"localplayer2icon", True)
        self.mlbutton1 = Button(self,[self.screenwidth/2,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
        ##################### Credits #####################
        self.crrect1 = Outline("rect",self.center,500,600,BLACK,TAN,7)
        self.crheader1 = Text([self.screenwidth/2,self.screenheight/2-245],"Credits",self.font,50,BLACK)
        self.crtext1 = Text([self.screenwidth/2,self.screenheight/2-150],"Game Designer:",self.font,30,BLACK)
        self.crtext2 = Text([self.screenwidth/2,self.screenheight/2-75],"Robby Teal",self.font,20,BLACK)
        self.crtext3 = Text([self.screenwidth/2,self.screenheight/2+0],"Game Artist:",self.font,30,BLACK)
        self.crtext4 = Text([self.screenwidth/2,self.screenheight/2+75],"Mitch Archer",self.font,20,BLACK)
        self.crbutton1 = Button(self,[self.screenwidth/2,self.screenheight/2+300],250,75,"Back",self.font,20,BLACK,BLACK,TAN,RED,RED,TAN,7)
    #################### Main Menu ####################
    def loadMainMenu(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
            self.screen.fill(self.background)
            self.mmrect1.blit(self.screen)
            self.mmheader1.blit(self.screen)
            self.mmbutton1.blit(self.screen)
            self.mmbutton2.blit(self.screen)
            self.mmbutton3.blit(self.screen)
            self.mmbutton4.blit(self.screen)
            self.mmbutton5.blit(self.screen)
            if self.mmbutton1.hover or self.mmbutton2.hover or self.mmbutton3.hover or self.mmbutton4.hover or self.mmbutton5.hover:
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.mmbutton1.clicked:
                action = 1
                done = True
            elif self.mmbutton2.clicked:
                action = 2
                done = True
            elif self.mmbutton3.clicked:
                action = 3
                done = True
            elif self.mmbutton4.clicked:
                action = 4
                done = True
            elif self.mmbutton5.clicked:
                action = 0
                done = True
        if action == 1:
            self.loadTutorial()
        elif action == 2:
            self.loadCampaign()
        elif action == 3:
            self.loadMultiplayer()
        elif action == 4:
            self.loadCredits()
        else:
            pygame.mixer.quit()
            pygame.quit()
    #################### Tutorial #####################
    def loadTutorial(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
            self.screen.fill(self.background)
            self.turect1.blit(self.screen)
            self.turect2.blit(self.screen)
            self.turect3.blit(self.screen)
            self.tuheader1.blit(self.screen)
            self.tukey1.blit(self.screen)
            self.tukeyletter1.blit(self.screen)
            self.tukey2.blit(self.screen)
            self.tukeyletter2.blit(self.screen)
            self.tukey3.blit(self.screen)
            self.tukeyletter3.blit(self.screen)
            self.tukey4.blit(self.screen)
            self.tukeyletter4.blit(self.screen)
            self.tukey5.blit(self.screen)
            self.tukeyletter5.blit(self.screen)
            self.tukey6.blit(self.screen)
            self.tukeyletter6.blit(self.screen)
            self.tukey7.blit(self.screen)
            self.tukeyletter7.blit(self.screen)
            self.tukey8.blit(self.screen)
            self.tukeyletter8.blit(self.screen)
            self.tutext1.blit(self.screen)
            self.tutext2.blit(self.screen)
            self.tutext3.blit(self.screen)
            self.tutext4.blit(self.screen)
            self.tubutton1.blit(self.screen)
            if self.tubutton1.hover:
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.tubutton1.clicked:
                action = 1
                done = True
        if action == 1:
            self.loadMainMenu()
        else:
            pygame.mixer.quit()
            pygame.quit()
    #################### Campaign #####################
    def loadCampaign(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
                elif event.type == pygame.KEYDOWN:
                    if self.cainput1.active:
                        if pygame.key.name(event.key) == "backspace":
                            self.cainput1.update("backspace")
                        elif pygame.key.name(event.key) == "delete":
                            self.cainput1.update("delete")
                        elif pygame.key.name(event.key) == "return":
                            self.cainput1.active = False
                        else:      
                            self.cainput1.update(event.unicode)
            self.screen.fill(self.background)
            self.carect1.blit(self.screen)
            self.caheader1.blit(self.screen)
            self.cainput1.blit(self.screen)
            self.cacharacterinput1.blit(self.screen)
            self.camap1.blit(self.screen)
            self.camap2.blit(self.screen)
            self.camap3.blit(self.screen)
            self.camap4.blit(self.screen)
            self.camap5.blit(self.screen)
            self.camap6.blit(self.screen)
            self.camap7.blit(self.screen)
            self.camap8.blit(self.screen)

            self.cabutton1.blit(self.screen)
            if self.cabutton1.hover or self.camap1.hover or self.camap2.hover or self.camap3.hover or self.camap4.hover or self.camap5.hover or self.camap6.hover or self.camap7.hover or self.camap8.hover or self.cacharacterinput1.hover:
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            elif self.cainput1.hover:
                self.text.update(pygame.mouse.get_pos())
                self.text.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.camap1.clicked:
                action = 1
                done = True
            elif self.camap2.clicked:
                action = 2
                done = True
            elif self.camap3.clicked:
                action = 3
                done = True
            elif self.camap4.clicked:
                action = 4
                done = True
            elif self.camap5.clicked:
                action = 5
                done = True
            elif self.camap6.clicked:
                action = 6
                done = True
            elif self.camap7.clicked:
                action = 7
                done = True
            elif self.camap8.clicked:
                action = 8
                done = True
            elif self.cabutton1.clicked:
                action = 9
                done = True
        if action == 1:
            self.camap1.reset()
            self.playCampaign(self.camap1)
        elif action == 2:
            self.camap2.reset()
            self.playCampaign(self.camap2)
        elif action == 3:
            self.camap3.reset()
            self.playCampaign(self.camap3)
        elif action == 4:
            self.camap4.reset()
            self.playCampaign(self.camap4)
        elif action == 5:
            self.camap5.reset()
            self.playCampaign(self.camap5)
        elif action == 6:
            self.camap6.reset()
            self.playCampaign(self.camap6)
        elif action == 7:
            self.camap7.reset()
            self.playCampaign(self.camap7)
        elif action == 8:
            self.camap8.reset()
            self.playCampaign(self.camap8)
        elif action == 9:
            self.loadMainMenu()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ################## Play Campaign ##################
    def playCampaign(self, gamemap):
        action = 0
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.keys["leave"]:
                        action = 1
                        done = True
                    elif event.key == self.keys["reset"]:
                        gamemap.reset()
                    elif event.key == self.keys["campaignjump"]:
                        gamemap.player1.jump()
                    elif event.key == self.keys["campaigndive"]:
                        gamemap.player1.dive()
                    elif event.key == self.keys["campaignleft"]:
                        gamemap.player1.moveLeft()
                    elif event.key == self.keys["campaignright"]:
                        gamemap.player1.moveRight()
                    elif event.key == self.keys["campaignmissile"]:
                        gamemap.player1.shootMissile()
                    elif event.key == self.keys["campaignbomb"]:
                        gamemap.player1.shootBomb()
                elif event.type == pygame.KEYUP:
                    if event.key == self.keys["campaignleft"] and gamemap.player1.xspeed < 0:
                        gamemap.player1.stop()
                    elif event.key == self.keys["campaignright"] and gamemap.player1.xspeed > 0:
                        gamemap.player1.stop()
            self.screen.fill(gamemap.background)
            gamemap.spritelist.update()

            if gamemap.updateblockscounter == 0:
                gamemap.updateblocks = True
                for block in gamemap.waterlist:
                    block.expanded = False
                for block in gamemap.lavalist:
                    block.expanded = False
            gamemap.updateblockscounter -= 1
            if gamemap.updateblocks:
                stopupdating = True
                for block in gamemap.waterlist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                for block in gamemap.lavalist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                if stopupdating:
                    gamemap.updateblocks = False
            
            gamemap.cloudlist.draw(self.screen)
            gamemap.waterlist.draw(self.screen)
            gamemap.lavalist.draw(self.screen)
            gamemap.blocklist.draw(self.screen)
            gamemap.playerlist.draw(self.screen)
            gamemap.zombielist.draw(self.screen)
            gamemap.missilelist.draw(self.screen)
            gamemap.bomblist.draw(self.screen)
            
            gamemap.player1text.update(gamemap.player1.texthealth)
            gamemap.player1text.blit(self.screen)
            gamemap.zombietext.update("Zombie Count: "+str(len(gamemap.zombielist)))
            gamemap.zombietext.blit(self.screen)

            self.fpstext.update("fps: "+str(round(self.clock.get_fps(),1)))
            self.fpstext.blit(self.screen)
            
            if gamemap.victory:
                gamemap.victorytext1.blit(self.screen)
                gamemap.victorytext2.blit(self.screen)
                gamemap.victorytext3.blit(self.screen)
            else:
                gamemap.checkVictory()
            pygame.display.flip()
            self.clock.tick(self.fps)
        if action == 1:
            self.loadCampaign()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ################ Load Multiplayer #################
    def loadMultiplayer(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
            self.screen.fill(self.background)
            self.murect1.blit(self.screen)
            self.muheader1.blit(self.screen)
            self.muselection1.blit(self.screen)
            self.muselection2.blit(self.screen)
            self.mubutton1.blit(self.screen)
            self.mubutton2.blit(self.screen)
            if self.muselection1.hover or self.muselection2.hover or self.mubutton1.hover or (self.mubutton2.hover and (self.muselection1.active or self.muselection2.active)):
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.mubutton1.clicked:
                action = 1
                done = True
            elif self.mubutton2.clicked:
                if self.muselection1.active:
                    action = 2
                    done = True
                elif self.muselection2.active:
                    action = 3
                    done = True
        if action == 1:
            self.loadMainMenu()
        elif action == 2:
            self.loadMultiplayerWifi()
        elif action == 3:
            self.loadMultiplayerLocal()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ############## Load Multiplayer Wifi ##############
    def loadMultiplayerWifi(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
                elif event.type == pygame.KEYDOWN:
                    if self.mwinput1.active:
                        if pygame.key.name(event.key) == "backspace":
                            self.mwinput1.update("backspace")
                        elif pygame.key.name(event.key) == "delete":
                            self.mwinput1.update("delete")
                        elif pygame.key.name(event.key) == "return":
                            self.mwinput1.active = False
                        else:      
                            self.mwinput1.update(event.unicode)
            self.screen.fill(self.background)
            self.mwrect1.blit(self.screen)
            self.mwheader1.blit(self.screen)
            self.mwselection1.blit(self.screen)
            self.mwselection2.blit(self.screen)
            self.mwinput1.blit(self.screen)
            self.mwbutton1.blit(self.screen)
            self.mwbutton2.blit(self.screen)
            if self.mwselection1.hover or self.mwselection2.hover or self.mwbutton1.hover or (self.mwbutton2.hover and (self.mwselection1.active or self.mwselection2.active) and (len(self.ipaddress.split("."))==4 and "".join(self.ipaddress.split(".")).isnumeric())):
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            elif self.mwinput1.hover:
                self.text.update(pygame.mouse.get_pos())
                self.text.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.mwbutton1.clicked:
                action = 1
                done = True
            elif self.mwbutton2.clicked:
                if len(self.ipaddress.split("."))==4 and "".join(self.ipaddress.split(".")).isnumeric():
                    if self.mwselection1.active:
                        action = 2
                        done = True
                    elif self.mwselection2.active:
                        action = 3
                        done = True
        if action == 1:
            self.loadMultiplayer()
        elif action == 2:
            self.mwmap1.reset()
            self.playMultiplayerHost(self.mwmap1)
        elif action == 3:
            self.mwmap1.reset()
            self.playMultiplayerClient(self.mwmap1)
        else:
            pygame.mixer.quit()
            pygame.quit()
    ############## Load Multiplayer Host ##############
    def playMultiplayerHost(self,gamemap):
        self.data = "0000000-0000000"
        self.datalock = threading.Lock()
        self.locallock = threading.Lock()
        self.var0 = "0"
        self.var1 = "0"
        self.var2 = "0"
        self.var3 = "0"
        self.var4 = "0"
        self.var5 = "0"
        self.var6 = "0"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.portnumber += 1
        self.server.bind((self.ipaddress,self.portnumber))
        self.servernetworkthread = threading.Thread(target=self.serverNetwork, daemon = True)
        self.servernetworkthread.start()
        action = 0
        done = False
        while not done:
            self.locallock.acquire()
            self.var0 = "0"
            self.var1 = "0"
            self.var2 = "0"
            self.var5 = "0"
            self.var6 = "0"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.keys["leave"]:
                        self.var0 = "1"
                        action = 1
                        done = True
                    elif event.key == self.keys["reset"]:
                        self.var0 = "2"
                    elif event.key == self.keys["player1jump"]:
                        self.var1 = "1"
                    elif event.key == self.keys["player1dive"]:
                        self.var2 = "1"
                    elif event.key == self.keys["player1left"]:
                        self.var3 = "1"
                    elif event.key == self.keys["player1right"]:
                        self.var4 = "1"
                    elif event.key == self.keys["player1missile"]:
                        self.var5 = "1"
                    elif event.key == self.keys["player1bomb"]:
                        self.var6 = "1"
                elif event.type == pygame.KEYUP:
                    if event.key == self.keys["player1left"]:
                        self.var3 = "0"
                    elif event.key == self.keys["player1right"]:
                        self.var4 = "0"
            self.locallock.release()
            self.datalock.acquire()
            if self.data[0] == "1":
                self.var0 = "1"
                action = 1
                done = True
            elif self.data[0] == "2":
                gamemap.reset()
            if self.data[1] == "1":
                gamemap.player1.jump()
            if self.data[2] == "1":
                gamemap.player1.dive()
            if self.data[3] == "1":
                gamemap.player1.moveLeft()
            elif self.data[3] == "0" and gamemap.player1.xspeed < 0:
                gamemap.player1.stop()
            if self.data[4] == "1":
                gamemap.player1.moveRight()
            elif self.data[4] == "0" and gamemap.player1.xspeed > 0:
                gamemap.player1.stop()
            if self.data[5] == "1":
                gamemap.player1.shootMissile()
            if self.data[6] == "1":
                gamemap.player1.shootBomb()

            if self.data[9] == "1":
                gamemap.player2.jump()
            if self.data[10] == "1":
                gamemap.player2.dive()
            if self.data[11] == "1":
                gamemap.player2.moveLeft()
            elif self.data[11] == "0" and gamemap.player2.xspeed < 0:
                gamemap.player2.stop()
            if self.data[12] == "1":
                gamemap.player2.moveRight()
            elif self.data[12] == "0" and gamemap.player2.xspeed > 0:
                gamemap.player2.stop()
            if self.data[13] == "1":
                gamemap.player2.shootMissile()
            if self.data[14] == "1":
                gamemap.player2.shootBomb()
            self.datalock.release()

            gamemap.spritelist.update()
            if gamemap.updateblockscounter == 0:
                gamemap.updateblocks = True
                for block in gamemap.waterlist:
                    block.expanded = False
                for block in gamemap.lavalist:
                    block.expanded = False
            gamemap.updateblockscounter -= 1
            if gamemap.updateblocks:
                stopupdating = True
                for block in gamemap.waterlist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                for block in gamemap.lavalist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                if stopupdating:
                    gamemap.updateblocks = False
            self.screen.fill(self.background)
            gamemap.cloudlist.draw(self.screen)
            gamemap.waterlist.draw(self.screen)
            gamemap.lavalist.draw(self.screen)
            gamemap.blocklist.draw(self.screen)
            gamemap.playerlist.draw(self.screen)
            gamemap.zombielist.draw(self.screen)
            gamemap.missilelist.draw(self.screen)
            gamemap.bomblist.draw(self.screen)

            gamemap.player1text.update(gamemap.player1.texthealth)
            gamemap.player1text.blit(self.screen)
            gamemap.player2text.update(gamemap.player2.texthealth)
            gamemap.player2text.blit(self.screen)

            self.fpstext.update("fps: "+str(round(self.clock.get_fps(),1)))
            self.fpstext.blit(self.screen)
            
            if gamemap.victory:
                gamemap.victorytext1.blit(self.screen)
                gamemap.victorytext2.blit(self.screen)
                gamemap.victorytext3.blit(self.screen)
            else:
                gamemap.checkVictory()
            pygame.display.flip()
            self.clock.tick(self.fps)
                
        if action == 1:
            self.loadMultiplayerWifi()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ############# Load Multiplayer Client #############
    def playMultiplayerClient(self,gamemap):
        self.data = "0000000-0000000"
        self.datalock = threading.Lock()
        var0 = "0"
        var1 = "0"
        var2 = "0"
        var3 = "0"
        var4 = "0"
        var5 = "0"
        var6 = "0"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientnetworkthread = threading.Thread(target=self.clientNetwork, daemon = True)
        self.clientnetworkthread.start()
        action = 0
        done = False
        while not done:
            self.datalock.acquire()
            if self.data[0] == "1":
                var0 = "1"
                action = 1
                done = True
            elif self.data[0] == "2":
                gamemap.reset()
            if self.data[1] == "1":
                gamemap.player1.jump()
            if self.data[2] == "1":
                gamemap.player1.dive()
            if self.data[3] == "1":
                gamemap.player1.moveLeft()
            elif self.data[3] == "0" and gamemap.player1.xspeed < 0:
                gamemap.player1.stop()
            if self.data[4] == "1":
                gamemap.player1.moveRight()
            elif self.data[4] == "0" and gamemap.player1.xspeed > 0:
                gamemap.player1.stop()
            if self.data[5] == "1":
                gamemap.player1.shootMissile()
            if self.data[6] == "1":
                gamemap.player1.shootBomb()

            if self.data[9] == "1":
                gamemap.player2.jump()
            if self.data[10] == "1":
                gamemap.player2.dive()
            if self.data[11] == "1":
                gamemap.player2.moveLeft()
            elif self.data[11] == "0" and gamemap.player2.xspeed < 0:
                gamemap.player2.stop()
            if self.data[12] == "1":
                gamemap.player2.moveRight()
            elif self.data[12] == "0" and gamemap.player2.xspeed > 0:
                gamemap.player2.stop()
            if self.data[13] == "1":
                gamemap.player2.shootMissile()
            if self.data[14] == "1":
                gamemap.player2.shootBomb()
            self.datalock.release()

            gamemap.spritelist.update()
            if gamemap.updateblockscounter == 0:
                gamemap.updateblocks = True
                for block in gamemap.waterlist:
                    block.expanded = False
                for block in gamemap.lavalist:
                    block.expanded = False
            gamemap.updateblockscounter -= 1
            if gamemap.updateblocks:
                stopupdating = True
                for block in gamemap.waterlist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                for block in gamemap.lavalist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                if stopupdating:
                    gamemap.updateblocks = False      
            self.screen.fill(self.background)
            gamemap.cloudlist.draw(self.screen)
            gamemap.waterlist.draw(self.screen)
            gamemap.lavalist.draw(self.screen)
            gamemap.blocklist.draw(self.screen)
            gamemap.playerlist.draw(self.screen)
            gamemap.zombielist.draw(self.screen)
            gamemap.missilelist.draw(self.screen)
            gamemap.bomblist.draw(self.screen)

            gamemap.player1text.update(gamemap.player1.texthealth)
            gamemap.player1text.blit(self.screen)
            gamemap.player2text.update(gamemap.player2.texthealth)
            gamemap.player2text.blit(self.screen)

            self.fpstext.update("fps: "+str(round(self.clock.get_fps(),1)))
            self.fpstext.blit(self.screen)
            
            if gamemap.victory:
                gamemap.victorytext1.blit(self.screen)
                gamemap.victorytext2.blit(self.screen)
                gamemap.victorytext3.blit(self.screen)
            else:
                gamemap.checkVictory()

            var0 = "0"
            var1 = "0"
            var2 = "0"
            var5 = "0"
            var6 = "0"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.keys["leave"]:
                        var0 = "1"
                        action = 1
                        done = True
                    elif event.key == self.keys["reset"]:
                        var0 = "2"
                    elif event.key == self.keys["player1jump"]:
                        var1 = "1"
                    elif event.key == self.keys["player1dive"]:
                        var2 = "1"
                    elif event.key == self.keys["player1left"]:
                        var3 = "1"
                    elif event.key == self.keys["player1right"]:
                        var4 = "1"
                    elif event.key == self.keys["player1missile"]:
                        var5 = "1"
                    elif event.key == self.keys["player1bomb"]:
                        var6 = "1"
                elif event.type == pygame.KEYUP:
                    if event.key == self.keys["player1left"]:
                        var3 = "0"
                    elif event.key == self.keys["player1right"]:
                        var4 = "0"
            self.datalock.acquire()
            self.data = self.data[0:8]+var0+var1+var2+var3+var4+var5+var6
            self.datalock.release()
            pygame.display.flip()
            self.clock.tick(self.fps)
        if action == 1:
            self.loadMultiplayerWifi()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ################# Network Threads #################
    def clientNetwork(self):
        self.portnumber += 1
        self.client.connect((self.ipaddress,self.portnumber))
        done = False
        while not done:
            #write
            self.datalock.acquire()
            writedata = self.data
            self.datalock.release()
            self.client.send(writedata.encode("ascii"))
            print("wrote: "+writedata)
            #read
            readdata = self.client.recv(1024).decode("ascii")
            print("read:  "+readdata)
            #update self
            self.datalock.acquire()
            self.data = readdata
            self.datalock.release()
            if self.data[0] == "1":
                done = True
            print("wait")
    def serverNetwork(self):
        self.server.listen(1)
        client, address = self.server.accept()
        done = False
        while not done:
            #read
            readdata = client.recv(1024).decode("ascii")
            print("read:  "+readdata)
            if readdata[0] == "1":
                done = True
            #write
            self.datalock.acquire()
            self.locallock.acquire()
            self.data = self.var0+self.var1+self.var2+self.var3+self.var4+self.var5+self.var6+readdata[7:15]
            writedata = self.data
            self.locallock.release()
            self.datalock.release()
            client.send(writedata.encode("ascii"))
            print("wrote: "+writedata)
    ############# Load Multiplayer Local ##############
    def loadMultiplayerLocal(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
                elif event.type == pygame.KEYDOWN:
                    if self.mlinput1.active:
                        if pygame.key.name(event.key) == "backspace":
                            self.mlinput1.update("backspace")
                        elif pygame.key.name(event.key) == "delete":
                            self.mlinput1.update("delete")
                        elif pygame.key.name(event.key) == "return":
                            self.mlinput1.active = False
                        else:      
                            self.mlinput1.update(event.unicode)
                    elif self.mlinput2.active:
                        if pygame.key.name(event.key) == "backspace":
                            self.mlinput2.update("backspace")
                        elif pygame.key.name(event.key) == "delete":
                            self.mlinput2.update("delete")
                        elif pygame.key.name(event.key) == "return":
                            self.mlinput2.active = False
                        else:      
                            self.mlinput2.update(event.unicode)
            self.screen.fill(self.background)
            self.mlrect1.blit(self.screen)
            self.mlheader1.blit(self.screen)
            self.mlmap1.blit(self.screen)
            self.mlmap2.blit(self.screen)
            self.mlmap3.blit(self.screen)
            self.mlmap4.blit(self.screen)
            self.mlmap5.blit(self.screen)
            self.mlmap6.blit(self.screen)
            self.mlmap7.blit(self.screen)
            self.mlmap8.blit(self.screen)
            self.mlinput1.blit(self.screen)
            self.mlinput2.blit(self.screen)
            self.mlcharacterinput1.blit(self.screen)
            self.mlcharacterinput2.blit(self.screen)
            self.mlbutton1.blit(self.screen)
            if self.mlbutton1.hover or self.mlmap1.hover or self.mlmap2.hover or self.mlmap3.hover or self.mlmap4.hover or self.mlmap5.hover or self.mlmap6.hover or self.mlmap7.hover or self.mlmap8.hover or self.mlcharacterinput1.hover or self.mlcharacterinput2.hover:
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            elif self.mlinput1.hover or self.mlinput2.hover:
                self.text.update(pygame.mouse.get_pos())
                self.text.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.mlmap1.clicked:
                action = 1
                done = True
            elif self.mlmap2.clicked:
                action = 2
                done = True
            elif self.mlmap3.clicked:
                action = 3
                done = True
            elif self.mlmap4.clicked:
                action = 4
                done = True
            elif self.mlmap5.clicked:
                action = 5
                done = True
            elif self.mlmap6.clicked:
                action = 6
                done = True
            elif self.mlmap7.clicked:
                action = 7
                done = True
            elif self.mlmap8.clicked:
                action = 8
                done = True
            elif self.mlbutton1.clicked:
                action = 9
                done = True
        if action == 1:
            self.mlmap1.reset()
            self.playMultiplayerLocal(self.mlmap1)
        elif action == 2:
            self.mlmap2.reset()
            self.playMultiplayerLocal(self.mlmap2)
        elif action == 3:
            self.mlmap3.reset()
            self.playMultiplayerLocal(self.mlmap3)
        elif action == 4:
            self.mlmap4.reset()
            self.playMultiplayerLocal(self.mlmap4)
        elif action == 5:
            self.mlmap5.reset()
            self.playMultiplayerLocal(self.mlmap5)
        elif action == 6:
            self.mlmap6.reset()
            self.playMultiplayerLocal(self.mlmap6)
        elif action == 7:
            self.mlmap7.reset()
            self.playMultiplayerLocal(self.mlmap7)
        elif action == 8:
            self.mlmap8.reset()
            self.playMultiplayerLocal(self.mlmap8)
        elif action == 9:
            self.loadMultiplayer()
        else:
            pygame.mixer.quit()
            pygame.quit()
    def playMultiplayerLocal(self, gamemap):
        action = 0
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.keys["leave"]:
                        action = 1
                        done = True
                    elif event.key == self.keys["reset"]:
                        gamemap.reset()
                    elif event.key == self.keys["player1jump"]:
                        gamemap.player1.jump()
                    elif event.key == self.keys["player1dive"]:
                        gamemap.player1.dive()
                    elif event.key == self.keys["player1left"]:
                        gamemap.player1.moveLeft()
                    elif event.key == self.keys["player1right"]:
                        gamemap.player1.moveRight()
                    elif event.key == self.keys["player1missile"]:
                        gamemap.player1.shootMissile()
                    elif event.key == self.keys["player1bomb"]:
                        gamemap.player1.shootBomb()

                    elif event.key == self.keys["player2jump"]:
                        gamemap.player2.jump()
                    elif event.key == self.keys["player2dive"]:
                        gamemap.player2.dive()
                    elif event.key == self.keys["player2left"]:
                        gamemap.player2.moveLeft()
                    elif event.key == self.keys["player2right"]:
                        gamemap.player2.moveRight()
                    elif event.key == self.keys["player2missile"]:
                        gamemap.player2.shootMissile()
                    elif event.key == self.keys["player2bomb"]:
                        gamemap.player2.shootBomb()
                        
                elif event.type == pygame.KEYUP:
                    if event.key == self.keys["player1left"] and gamemap.player1.xspeed < 0:
                        gamemap.player1.stop()
                    elif event.key == self.keys["player1right"] and gamemap.player1.xspeed > 0:
                        gamemap.player1.stop()
                    elif event.key == self.keys["player2left"] and gamemap.player2.xspeed < 0:
                        gamemap.player2.stop()
                    elif event.key == self.keys["player2right"] and gamemap.player2.xspeed > 0:
                        gamemap.player2.stop()
            self.screen.fill(gamemap.background)
            gamemap.spritelist.update()

            if gamemap.updateblockscounter == 0:
                gamemap.updateblocks = True
                for block in gamemap.waterlist:
                    block.expanded = False
                for block in gamemap.lavalist:
                    block.expanded = False
            gamemap.updateblockscounter -= 1
            if gamemap.updateblocks:
                stopupdating = True
                for block in gamemap.waterlist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                for block in gamemap.lavalist:
                    if not block.expanded:
                        stopupdating = False
                    block.expand()
                if stopupdating:
                    gamemap.updateblocks = False
            
            gamemap.cloudlist.draw(self.screen)
            gamemap.waterlist.draw(self.screen)
            gamemap.lavalist.draw(self.screen)
            gamemap.blocklist.draw(self.screen)
            gamemap.playerlist.draw(self.screen)
            gamemap.zombielist.draw(self.screen)
            gamemap.missilelist.draw(self.screen)
            gamemap.bomblist.draw(self.screen)

            gamemap.player1text.update(gamemap.player1.texthealth)
            gamemap.player1text.blit(self.screen)
            gamemap.player2text.update(gamemap.player2.texthealth)
            gamemap.player2text.blit(self.screen)

            self.fpstext.update("fps: "+str(round(self.clock.get_fps(),1)))
            self.fpstext.blit(self.screen)
            
            if gamemap.victory:
                gamemap.victorytext1.blit(self.screen)
                gamemap.victorytext2.blit(self.screen)
                gamemap.victorytext3.blit(self.screen)
            else:
                gamemap.checkVictory()
            pygame.display.flip()
            self.clock.tick(self.fps)
        if action == 1:
            self.loadMultiplayerLocal()
        else:
            pygame.mixer.quit()
            pygame.quit()
    ##################### Credits #####################
    def loadCredits(self):
        action = 0
        done = False
        while not done:
            self.leftclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftclick = True
            self.screen.fill(self.background)
            self.crrect1.blit(self.screen)
            self.crheader1.blit(self.screen)
            self.crtext1.blit(self.screen)
            self.crtext2.blit(self.screen)
            self.crtext3.blit(self.screen)
            self.crtext4.blit(self.screen)
            self.crbutton1.blit(self.screen)
            if self.crbutton1.hover:
                self.hand.update(pygame.mouse.get_pos())
                self.hand.blit(self.screen)
            else:
                self.arrow.update(pygame.mouse.get_pos())
                self.arrow.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            if self.crbutton1.clicked:
                action = 1
                done = True
        if action == 1:
            self.loadMainMenu()
        else:
            pygame.mixer.quit()
            pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.loadMainMenu()
