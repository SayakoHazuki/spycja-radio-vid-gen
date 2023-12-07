import datetime
import os
import moviepy.editor as mpy
from PIL import Image 
import re
# from skimage.filters import gaussian
import numpy as np
from PIL import Image, ImageFilter, ImageOps
  
print("All imports loaded.")
  
# Config
BACKGROUND_IMAGE = "assets/background.jpg"
THUMBNAIL_IMAGE = "assets/thumbnail.jfif"
SONG_TITLE = "さよならプリンセス"
SONG_ARTIST = "初音ミク"
POST_AUTHOR = "匿名"
MODE = "DEBUG" # "DEBUG", "PREVIEW" or "RELEASE"

# Constants
LOGO_IMAGE = "assets/logo.png"
MAKINAS_FONT = "Makinas-4-Flat"
NOTO_SANS_FONT = "Noto-Sans-JP"
NOTO_SERIF_FONT = "Noto-Serif-HK"
ZEN_OLD_MINCHO_FONT = "Zen-Old-Mincho-Regular"

SCREENSIZE = (1080,1920)

# def blur(image, r=24):
#     """ Returns a blurred (radius=r pixels) version of the image """
#     return gaussian(image.astype(float), sigma=r)

def make_shadow(img, blur_radius=24):
    mask = img.split()[0].convert("L")
    img = ImageOps.invert(img)
    
    mask.save("output/temp/mask.png")
    
    # create new blank rgba img
    shadow = Image.new('RGBA', img.size, (0,0,0,0))
    shadow.paste(img, mask=mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    shadow.save("output/temp/shadow.png")
    return shadow

def TextShadowClip(clip: mpy.TextClip, blur_radius=24):
    frameImg = Image.fromarray(clip.get_frame(0))
    
    clip = mpy.ImageClip(np.array(make_shadow(frameImg, blur_radius))) \
        .set_position(clip.pos).set_duration(clip.duration).set_start(clip.start).set_end(clip.end)
    return clip

def prioritizeImageSize(path, target_width, target_height):
    (width, height) = getSize(path)
    testFWidth = int(width * (target_height/height))
    if (testFWidth < target_width):
        priority = "w"
    else:
        priority = "h"
        
    fHeight = target_height if priority == "h" else None
    fWidth = target_width if priority == "w" else None
    
    return (fWidth, fHeight)

def getSize(path):
    pilImage = Image.open(path)
    height = pilImage.height
    width = pilImage.width
    return (width, height) 
    

# Background
print("Creating backgroundClip")
backgroundImageSize = prioritizeImageSize(BACKGROUND_IMAGE, SCREENSIZE[0], SCREENSIZE[1])
backgroundClip = mpy.ImageClip(BACKGROUND_IMAGE)
backgroundClip = backgroundClip.set_position('center')
backgroundClip = backgroundClip.resize(width=backgroundImageSize[0], height=backgroundImageSize[1])

# Header
print("Creating logoClip")
logoClip = mpy.ImageClip(LOGO_IMAGE)
logoClip = logoClip.set_position((74, 132))
logoClip = logoClip.resize(height=84)

print("Creating dateClip")
date = datetime.datetime.now().strftime("%d.%m.%Y")
dateClip = mpy.TextClip(date, fontsize=64, color='white', font=MAKINAS_FONT)
dateClip = dateClip.set_position((74, 228))

print("Creating tipClip")
tip = "SOUND ON"
tipClip = mpy.TextClip(tip, fontsize=40, color='white', font=MAKINAS_FONT)
tipClip = tipClip.set_position((74, 292))

# Song info
print("Creating thumbnailClip")
thumbnailClipSize = prioritizeImageSize(THUMBNAIL_IMAGE, 142, 142)
thumbnailSize = getSize(THUMBNAIL_IMAGE)
thumbnailClip = mpy.ImageClip(THUMBNAIL_IMAGE)
thumbnailClip = thumbnailClip.set_position((74,1702))
thumbnailClip = thumbnailClip.resize(width=thumbnailClipSize[0], height=thumbnailClipSize[1])
thumbnailClipW, thumbnailClipH = thumbnailClip.size
thumbnailClip = thumbnailClip.crop(x_center=thumbnailClipW/2, y_center=thumbnailClipH/2, width=142, height=142)

print("Creating titleClip")
titleClip = mpy.TextClip(SONG_TITLE, fontsize=48, color='white', font=MAKINAS_FONT)
titleClip = titleClip.set_position((229, 1702))

print("Creating artistClip")
artistClip = mpy.TextClip(SONG_ARTIST, fontsize=36, color='white', font=MAKINAS_FONT)
artistClip = artistClip.set_position((229, 1748))

print("Creating postAuthorClip")
postAuthorClip = mpy.TextClip(f"投稿: {POST_AUTHOR}", fontsize=36, color='white', font=NOTO_SANS_FONT)
postAuthorClip = postAuthorClip.set_position((229, 1792))


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
    
print("Creating lyricsClips")
allLyricsClips = []
for i in range(len(data)):
    timestamp, lyrics = data[i]
    if i < len(data) - 1:
        duration = data[i+1][0] - timestamp
    else:
        duration = 100
    
    jaLyric, roLyric, chLyric = lyrics.split("\n")
    
    lyricsJaClip = mpy.TextClip(jaLyric, fontsize=64, color='white', font=ZEN_OLD_MINCHO_FONT) \
        .set_position(("center",900)).set_duration(duration).set_start(timestamp).set_end(timestamp + duration)
    
    lyricsRoClip = mpy.TextClip(roLyric, fontsize=48, color='white', font=NOTO_SANS_FONT) \
        .set_position(("center", 852)).set_duration(duration).set_start(timestamp).set_end(timestamp + duration)
        
    lyricsChClip = mpy.TextClip(chLyric, fontsize=56, color='white', font=NOTO_SANS_FONT) \
        .set_position(("center", 987)).set_duration(duration).set_start(timestamp).set_end(timestamp + duration)
        
    allLyricsClips.append(TextShadowClip(lyricsJaClip, 32/5))
    allLyricsClips.append(lyricsJaClip)
    allLyricsClips.append(TextShadowClip(lyricsRoClip, 24/5))
    allLyricsClips.append(lyricsRoClip)
    allLyricsClips.append(TextShadowClip(lyricsChClip, 28/5))
    allLyricsClips.append(lyricsChClip)
    
    print(f"{i + 1} of {len(data)} done", end=(" \r" if i < len(data) - 1 else " \n"))

# Composite 
print("Compositing")
final = mpy.CompositeVideoClip([
        backgroundClip, 
        logoClip, dateClip, tipClip, 
        thumbnailClip, titleClip, artistClip, postAuthorClip,
        *allLyricsClips
    ], size=SCREENSIZE)


if MODE == "DEBUG":
    print("[DEBUG] Saving frame")    
    final.save_frame("frame.png", t=data[3][0] + 3) 
    os.startfile("frame.png")
    
if MODE == "PREVIEW":
    print("[PREVIEW] Saving frame")    
    final.save_frame("frame.png", t=50) 
    
    print("[PREVIEW] Exporting preview")
    filename = f"./output/temp/{datetime.datetime.now().timestamp()}.mp4"
    final.subclip(data[4][0] - 3, data[5][0] + 3).write_videofile(filename, fps=24, codec="libx264")
    abspath = os.path.abspath(filename)
    os.startfile(abspath)

if MODE == "RELEASE":
    print("[RELEASE] Exporting")
    filename = f"./output/{SONG_TITLE}_{datetime.datetime.now().timestamp()}.mp4"
    final.subclip(0, data[-1][0] + 20).write_videofile(filename, fps=60, codec="libx264")
    abspath = os.path.abspath(filename)
    os.startfile(abspath)
