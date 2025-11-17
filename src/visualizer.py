from PIL import Image, ImageFont, ImageDraw
from font_source_sans_pro import SourceSansProSemibold
from font_fredoka_one import FredokaOne

def create_image(inky_display, color="black"):
    inky_display.set_border(inky_display.WHITE)
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    font_small = ImageFont.truetype(SourceSansProSemibold, 12)
    font_main = ImageFont.truetype(SourceSansProSemibold, 14)
    font_large = ImageFont.truetype(SourceSansProSemibold, 18)
    font_xlarge = ImageFont.truetype(SourceSansProSemibold, 24)
    font_xxlarge = ImageFont.truetype(SourceSansProSemibold, 32)
    font_xxxlarge = ImageFont.truetype(FredokaOne, 38)

    news_out = choose_news()

    # 2. create the image to display, news type at the top, then title, then description
    ## 2.1. News Type
    # put a new line in the news type if it's too long
    if len(news_out[0][2]) > 15:
        news_out[0][2] = news_out[0][2][:15] + '\n' + news_out[0][2][15:]
    w, h = font_xxxlarge.getsize(news_out[0][2])
    x = 400 / 2 - w / 2
    y = 50 / 2 - h / 2
    # news type is colored! Wow so fancy
    if color == "black":
        draw.text((x, y), news_out[0][2], inky_display.BLACK, font=font_xxxlarge)
    elif color == "yellow":
        draw.text((x, y), news_out[0][2], inky_display.YELLOW, font=font_xxxlarge)
    else:
        draw.text((x, y), news_out[0][2], inky_display.RED, font=font_xxxlarge)

    ## 2.2. Title (put on the left side)
    # for after 24 chars put a new line in the title
    break_length = 34
    last_space = 0
    last_break = 0
    for i in range(0, len(news_out[0][0])):
        if news_out[0][0][i] == ' ':
            last_space = i
        if i - last_break > break_length:
            news_out[0][0] = news_out[0][0][:last_space] + '\n' + news_out[0][0][last_space + 1:]
            last_break = last_space
    w, h = font_xlarge.getsize(news_out[0][0])
    x = 10
    y = 100 / 2 - h / 2 + 25

    draw.text((x, y), news_out[0][0], inky_display.BLACK, font=font_xlarge)

    ## 2.3. Description (put on the right side)
    # for after 24 chars put a new line in the description
    break_length = 60
    last_space = 0
    last_break = 0
    for i in range(0, len(news_out[0][1])):
        if news_out[0][1][i] == ' ':
            last_space = i
        if i - last_break > break_length:
            news_out[0][1] = news_out[0][1][:last_space] + '\n' + news_out[0][1][last_space + 1:]
            last_break = last_space

    w, h = font_main.getsize(news_out[0][1])
    x = 10
    y = 400 / 2 - h / 2
    draw.text((x, y), news_out[0][1], inky_display.BLACK, font=font_main)

    return img