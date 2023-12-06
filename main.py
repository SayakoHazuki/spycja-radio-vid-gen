import datetime
import os
import moviepy.editor as mpy
from PIL import Image 
  
print("All imports loaded.")
  
# Config
BACKGROUND_IMAGE = "assets/background.jpg"
THUMBNAIL_IMAGE = "assets/thumbnail.jfif"
SONG_TITLE = "さよならプリンセス"
SONG_ARTIST = "初音ミク"
POST_AUTHOR = "匿名"

# Constants
LOGO_IMAGE = "assets/logo.png"
MAKINAS_FONT = "Makinas-4-Flat"
NOTO_SANS_FONT = "Noto-Sans-JP"

SCREENSIZE = (1080,1920)

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
backgroundClip = mpy.ImageClip(BACKGROUND_IMAGE, duration=10)
backgroundClip = backgroundClip.set_position('center')
backgroundClip = backgroundClip.resize(width=backgroundImageSize[0], height=backgroundImageSize[1]).set_duration(10)

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


# Composite 
print("Compositing")
final = mpy.CompositeVideoClip([backgroundClip, logoClip, dateClip, tipClip, thumbnailClip, titleClip, artistClip, postAuthorClip], size=SCREENSIZE)
# final.subclip(0,5).write_videofile(f"./output/{datetime.datetime.now().timestamp()}.mp4", fps=24, codec="libx264")

print("Saving preview")
final.save_frame("frame.png", t=1.5) 

print("Exported preview. Opening...")
os.startfile("frame.png")