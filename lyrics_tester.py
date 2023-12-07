import re
import keyboard
import time

with open('output/time_record.txt', 'r', encoding='utf-8') as f:
    lyrics = f.read().split("\n\n")
    lyrics = [item.strip() for item in lyrics]
    data = []
    for item in lyrics[:-1]:
        timestamp = re.search(r'\[(.+)\]', item).group(1)
        m1,s1,ms1 = re.search(r'(\d+):(\d+)\.(\d+)', timestamp).groups()
        seconds_since_start = int(m1) * 60 + int(s1) + int(ms1) / 1000000
        lyrics = re.search(r'//([\w\W]+)//', item, flags=re.M).group(1)
        data.append((seconds_since_start, lyrics))
    

print("Press space to start")
keyboard.wait('space')

start_time = time.time()
for i in range(len(data)):
    timestamp, lyrics = data[i]
    print(lyrics, "\n\n")
    if i < len(data) - 1:
        time.sleep(data[i+1][0] - timestamp)
    else:
        time.sleep(100)

