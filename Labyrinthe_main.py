from microbit import *
import radio
import time
import speech
import music
start=True
display.scroll("LABYRINTHE    o7    ",wait=False,delay=75,loop=True)
while start:
    if button_a.was_pressed() or button_b.was_pressed():
        display.show(Image('00009:'
                           '00090:'
                           '90900:'
                           '09000:'
                           '00000'))
        sleep(1000)
        #def
        radio.send("start")
        start=False
display.clear()
connection=True
player_connected=0
display.scroll("Player:",wait=False,delay=75)
while connection:
    message_connection=radio.receive()
    if message_connection and message_connection=="player":
        player_connected+=1
        display.clear()
        display.show(player_connected)
    if button_a.was_pressed() or button_b.was_pressed():
        connection=False
display.show("3")
sleep(1000)
display.show("2")
sleep(1000)
display.show("1")
sleep(1000)
radio.send("go")
music.play(music.POWER_DOWN)
display.clear()
game=True
time_=0
while game:
    time.sleep(1)
    time_+=1
    display.show(time_)
    message_game=radio.receive()
    if message_game and message_game=="end of player":
        radio.send("end")
        display.scroll("END OF GAME",loop=True)
    


        
