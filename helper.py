import keyboard
import datetime
import winsound
import time
import random
import math

start = None
time_record = []
counter = 0

# open assets/lyrics.txt, split lyrics by double newlines
with open('assets/lyrics.txt', 'r', encoding='utf-8',) as f:
    lyrics = f.read().split("\n\n")
    # remove empty lines before and after each item in lyrics
    lyrics = [item.strip() for item in lyrics]


def run():
    global start, counter
    if counter >= len(lyrics):
        print("esc to exit")
    else:
        if start is None:
            start = datetime.datetime.now()
            print("start")
        else:
            t = datetime.datetime.now() 
            time_record.append(t)
            print(f"{t.strftime('%M:%S.%f')}, {t - start}")
            print(lyrics[counter], "\n")
            counter += 1   
    

keyboard.add_hotkey('z', run)
print("z to start")
keyboard.wait('esc')

# export to file 
with open('output/time_record.txt', 'w', encoding="utf-8") as f:
    for i,item in enumerate(time_record):
        # time elapsed since start in mm:ss.ms \n lyric
        # f.write(f"[{item - start}]\n//{lyrics[i]}//\n\n")
        # considering earphone delay
        f.write(f"[{item - start}]\n//{lyrics[i]}//\n\n")
        
