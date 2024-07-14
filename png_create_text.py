# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

def png_create_text(
    width,
    height,
    font_size,
    text,
    output_file="text.png",
):
    # create image
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # font text
    font = ImageFont.truetype(
        font="SF-Pro-Display-Bold.otf",
        size=font_size,
        encoding="utf-8",
    )
    lines, line_height = get_lines_wrap(
        text=text,
        font=font,
        max_width=width - 100,
    )

    position_center = [width / 2, height / 2]
    position = position_center
    position[1] -= line_height * len(lines) / 2

    for line in lines:
        font_x, font_y, font_width, font_height = font.getbbox(line)
        
        local_position = [position[0], position[1]]
        local_position[0] -= font_width / 2
        local_position[1] -= font_height / 2

        draw.text(
            xy=local_position,
            text=line,
            font=font,
            fill=(255, 255, 255),
            stroke_fill=(0, 0, 0),
            stroke_width=int(font_size / 22) + 1,
        )

        position[1] += line_height

    # save image
    image.save("text.png")

def get_lines_wrap(text, font, max_width):
    text_lines = text.split('\n')
    text_lines = [line.strip().split(' ') for line in text_lines]

    lines = []

    for text_line in text_lines:
        line_cursor = 0
        line_words_count = len(text_line)
        for i in range(line_words_count):
            cursor_words = text_line[line_cursor:i+1]
            cursor_text = ' '.join(cursor_words)

            font_x, font_y, font_width, font_height = font.getbbox(cursor_text)
            
            should_break_line = font_width > max_width
            if should_break_line:
                cursor_words = text_line[line_cursor:i]
                cursor_text = ' '.join(cursor_words)
                lines.append(cursor_text)
                line_cursor = i
            elif cursor_text and i == line_words_count - 1:
                lines.append(cursor_text)

    return lines, font.getbbox(text)[3]

if __name__ == "__main__":
    text = "Hola esto es un texto de prueba, pero con muchas palabras, para que se divida en varias lineas"
    width = 1080
    height = 1920
    font_size = height / 30
    output_file='text.png'

    png_create_text(
        width=width,
        height=height,
        text=text,
        font_size=font_size,
        output_file=output_file,
    ) 