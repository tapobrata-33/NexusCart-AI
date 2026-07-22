from PIL import Image, ImageDraw, ImageFont


# ============================
# CREATE NEXUSCART AI LOGO
# ============================

width = 1000
height = 400


# Create canvas
img = Image.new(
    "RGB",
    (width, height),
    "white"
)


draw = ImageDraw.Draw(img)


# Load fonts
try:

    title_font = ImageFont.truetype(
        "arial.ttf",
        90
    )

    sub_font = ImageFont.truetype(
        "arial.ttf",
        35
    )

except:

    title_font = ImageFont.load_default()

    sub_font = ImageFont.load_default()



# Logo Icon (AI + Cart)

# Cart body

draw.rounded_rectangle(
    (80,120,260,240),
    radius=25,
    outline=(0,120,255),
    width=8
)


# Cart handle

draw.line(
    (50,100,100,130),
    fill=(0,120,255),
    width=8
)


# Wheels

draw.ellipse(
    (110,240,150,280),
    fill=(0,120,255)
)

draw.ellipse(
    (200,240,240,280),
    fill=(0,120,255)
)



# AI network circles

points = [
    (160,70),
    (220,90),
    (180,130)
]


for p in points:

    draw.ellipse(
        (
            p[0]-15,
            p[1]-15,
            p[0]+15,
            p[1]+15
        ),
        fill=(0,200,150)
    )



# AI connection lines

draw.line(
    points,
    fill=(0,200,150),
    width=5
)



# Main text

draw.text(
    (330,100),
    "NexusCart AI",
    font=title_font,
    fill=(20,40,80)
)



# Subtitle

draw.text(
    (340,220),
    "Retail Intelligence Platform",
    font=sub_font,
    fill=(80,80,80)
)



# Save logo

img.save(
    "assets/logo.png"
)


print(
    "NexusCart AI logo created successfully!"
)