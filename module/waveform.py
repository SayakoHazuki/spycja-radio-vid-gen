import os

def waveFormImage(path, size, frame = 1):
    print("Generating waveform image for " + path + "at frame " + str(frame), end="\r")
    
def WaveFormVideo(path, size):
    print("Generating waveform video for " + path)
    
    cmd = f'''
    ffmpeg -i ガーデン_1702091021.576941TEMP_MPY_wvf_snd.mp3 -filter_complex "[0:a]showwaves=s=1280x720:mode=cline,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy output/temp/waveform.mp4
    '''.strip()
    