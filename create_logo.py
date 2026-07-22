from PIL import Image, ImageDraw, ImageFont
import os


# =====================================
# NEXUSCART AI PROFESSIONAL LOGO CREATOR
# =====================================


# Create assets folder automatically

if not os.path.exists("assets"):
    os.makedirs("assets")



# =====================================
# CANVAS
# =====================================

width = 1200
height = 500


img = Image.new(
    "RGB",
    (width, height),
    "#FFFFFF"
)


draw = ImageDraw.Draw(img)



# =====================================
# FONT SETTINGS
# =====================================

try:

    title_font = ImageFont.truetype(
        "arial.ttf",
        100
    )

    subtitle_font = ImageFont.truetype(
        "arial.ttf",
        40
    )

except:

    title_font = ImageFont.load_default()

    subtitle_font = ImageFont.load_default()



# =====================================
# AI SHOPPING CART ICON
# =====================================


# Cart body

draw.rounded_rectangle(
    (100,170,330,320),
    radius=35,
    outline="#0066FF",
    width=12
)



# Cart handle

draw.line(
    (40,130,130,180),
    fill="#0066FF",
    width=12
)



# Wheels

draw.ellipse(
    (150,320,200,370),
    fill="#0066FF"
)


draw.ellipse(
    (260,320,310,370),
    fill="#0066FF"
)



# =====================================
# AI NETWORK DESIGN
# =====================================


nodes = [

    (200,80),
    (280,120),
    (160,130)

]


# Connection lines

draw.line(
    nodes,
    fill="#00B894",
    width=8
)



# AI nodes

for x,y in nodes:

    draw.ellipse(
        (
            x-20,
            y-20,
            x+20,
            y+20
        ),
        fill="#00B894"
    )



# =====================================
# BRAND NAME
# =====================================


draw.text(
    (420,130),
    "NexusCart AI",
    font=title_font,
    fill="#12355B"
)



# =====================================
# TAGLINE
# =====================================


draw.text(
    (430,260),
    "AI Powered Retail Intelligence",
    font=subtitle_font,
    fill="#555555"
)



draw.text(
    (430,320),
    "Sales • Analytics • Machine Learning",
    font=subtitle_font,
    fill="#00B894"
)



# =====================================
# SAVE LOGO
# =====================================


logo_path = "assets/logo.png"


img.save(
    logo_path
)


print(
    "NexusCart AI professional logo created successfully!"
)

print(
    "Saved at:",
    logo_path
)