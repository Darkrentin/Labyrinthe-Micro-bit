#-[import]-
from music_background import notes
from microbit import *
import time
import speech
import music
import radio
from random import random
#-[Phase d'attente]-

music.play(music.FUNK,wait=False,loop=True)
display.scroll("LABYRINTHE    o7    ",wait=False,delay=75,loop=True)
start=True
while start:
    message_start=radio.receive()
    if message_start and message_start=="start":
        music.stop()
        display.show(Image('00009:'
                           '00090:'
                           '90900:'
                           '09000:'
                           '00000'))
        sleep(1000)
        while True:
            if button_a.was_pressed() or button_b.was_pressed():
                radio.send("player")
                break
    elif message_start and message_start=="go":
        start=False
display.show("3")
music.play("c")
time.sleep(0.75)
display.show("2")
music.play("c")
time.sleep(0.75)
display.show("1")
music.play("c")
time.sleep(0.75)
music.play(notes,wait=False,loop=True)
#--Init-
map_x, map_y = 40,40               #  On initialise toute les variables du débuts 
lv=1                               #  comme la position du joueur ou la taille de la map
posy,posx=2,2
lum=9
start_x,start_y = [2,2],[2,2]
#--Def-
def draw_map(map_chunk):                   # Cette def s'occuper d'afficher un "chunk"               # de notre map sur l'écran de la micro:bit, 
    for i in range(5):                     # il update chaque LED pour ne pas avoir 
        for k in range(5):                 # l'écran qui clignote à chaque fois que l'on bouge
            if map_chunk[i][k]==1:
                display.set_pixel(k, i,9)
            elif map_chunk[i][k]==2:
                display.set_pixel(k,i,5)
            elif map_chunk[i][k]==0:
                display.set_pixel(k,i,0)

def gen_chunk(posx,posy,map):              # Cette def s'occupe pour sa part de générer 
    map_chunk=[]                           # un "Chunk" de notre map, c'est a dire un 
    map_chunk_line=[]                      # morceaux de la map de 5 par 5 autour de 
    for i in range(posy-2,posy+3):         # notre personnage ce qui nous permetera de
        for k in range(posx-2,posx+3):     # l'afficher sur l'écran
            map_chunk_line.append(map[i][k])
        map_chunk.append(map_chunk_line)
        map_chunk_line=[]
    return map_chunk

def find_exit(map_x,map_y):
    end_x, end_y = None , None
    for i in range(map_x):
        for k in range(map_y):
            if map[i][k]==2:
                end_x, end_y = k, i
    return end_x, end_y

def gen_map(map_x,map_y):# à modifer (pathfinding)
    map_line=[]
    map=[]
    for i in range(map_y):
       for j in range(map_x):
         if i == 0 or j == 0 or i == map_y - 1 or j == map_x -1:
           map_line.append(1)
         elif i % 2 == 0 and random() < 0.6:
           map_line.append(1)
         elif j % 5 == 0 and random() < 0.5:
           map_line.append(1)
         else:
           map_line.append(0)
       map.append(map_line)
       map_line=[]
    for M in map:
        print(M)
    return map

#--Init_post_def-
map=gen_map(map_x,map_y)             #on appele la def pour créer la map avant de lancer le jeu
map_chunk=gen_chunk(posx,posy,map)   # et on génére le premier chunk
end_x,end_y=find_exit(map_x,map_y)
#--Game-
game=True

while game:
    map_chunk=gen_chunk(posx,posy,map)
    draw_map(map_chunk)
    time.sleep_ms(100)
    display.set_pixel(2,2,5)
    message=radio.receive()
    
    if accelerometer.get_y() >= 100:
        if map[posy+1][posx]!=1:
            posy+=1
            
            map_chunk=gen_chunk(posx,posy,map)
            time.sleep_ms(100)
        
    if accelerometer.get_x() >=100:
        if map[posy][posx+1]!=1:
            posx+=1
            
            map_chunk=gen_chunk(posx,posy,map)
            time.sleep_ms(100)
    if accelerometer.get_x() <= -100:
        if map[posy][posx-1]!=1:
            posx-=1
            
            map_chunk=gen_chunk(posx,posy,map)
            time.sleep_ms(150)
    if accelerometer.get_y() <= -100:
        if map[posy-1][posx]!=1:
            posy-=1
            
            map_chunk=gen_chunk(posx,posy,map)
            time.sleep_ms(100)

    if accelerometer.was_gesture("shake"):
        music.stop()
    if message and message=="end":
        display.scroll("Loose")
        music.play(music.FUNERAL)
        break
    if pin_logo.is_touched():
        cal_x,cal_y=accelerometer.get_x(),accelerometer.get_y()
    if posx==end_x and posy==end_y:
        display.scroll("Win !")
        radio.send("end of player")
        break
display.scroll("END OF GAME",loop=True)
    