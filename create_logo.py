from PIL import Image, ImageDraw, ImageFont
import os
WIDTH = 900
HEIGHT = 260
img = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    (10, 18, 35)
)
draw = ImageDraw.Draw(img)
try:
    title_font = ImageFont.truetype(
        "arialbd.ttf",
        70
    )
    sub_font = ImageFont.truetype(
        "arial.ttf",
        28
    )
except:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
draw.ellipse(
    (55,55,205,205),
    fill=(0,140,255)
)
draw.ellipse(
    (75,75,185,185),
    fill=(15,23,42)
)
draw.rounded_rectangle(
    (105,105,155,160),
    radius=8,
    fill="white"
)
draw.arc(
    (115,85,145,125),
    180,
    360,
    fill="white",
    width=6
)
draw.line(
    (130,80,130,55),
    fill=(0,200,255),
    width=5
)
draw.ellipse(
    (122,45,138,61),
    fill=(0,200,255)
)
draw.text(
    (250,55),
    "NexusCart AI",
    font=title_font,
    fill=(255,255,255)
)
draw.text(
    (255,140),
    "AI Powered Retail Intelligence",
    font=sub_font,
    fill=(150,190,220)
)
draw.rounded_rectangle(
    (255,190,560,230),
    radius=15,
    fill=(0,140,255)
)
draw.text(
    (285,198),
    "SMART BUSINESS ANALYTICS",
    font=sub_font,
    fill="white"
)
if not os.path.exists("assets"):
    os.makedirs("assets")
img.save(
    "assets/logo.png"
)
print(
    "Professional NexusCart AI logo created!"
)