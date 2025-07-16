from PIL import Image, ImageDraw, ImageFont
from random_word import RandomWords
import random
import argparse
import os

TEXT_MODES = [
    "DEFINED_LIST",
    "DEFINED_LIST_LINES",
    "DEFINED_LIST_RANDOM",
    "DEFINED_LIST_RANDOM_LINE",
    "RANDOM_LOWER",
    "RANDOM_UPPER",
    "RANDOM_CASE"
]

def parse_args():
    parser = argparse.ArgumentParser(description="Tesseract data generator config")

    parser.add_argument("--data-count", type=int, default=1, help="Number of data items to generate")
    parser.add_argument("--test-font", type=str, required=True, help="Path to the font file")
    parser.add_argument("--font-size", type=int, default=45, help="Font size in points")
    parser.add_argument("--num-words", type=int, default=1, help="Number of words generated per image")
    parser.add_argument("--height-padding", type=int, default=5, help="Vertical padding")
    parser.add_argument("--width-padding", type=int, default=5, help="Horizontal padding")
    parser.add_argument("--base-x", type=int, default=0, help="Base X offset")
    parser.add_argument("--base-y", type=int, default=0, help="Base Y offset")
    parser.add_argument("--base-x-padding", type=float, default=2.5, help="Base X padding")
    parser.add_argument("--base-y-padding", type=float, default=0, help="Base Y padding")
    parser.add_argument("--output-path", type=str, default="GeneratedData", help="Output path for data")
    parser.add_argument("--text-mode", type=str, choices=TEXT_MODES, default="RANDOM_LOWER", help="Text generation mode")
    parser.add_argument("--input-file", type=str, help="Path to input file for predefined text modes")
    parser.add_argument("--text-color", type=str, default="#000000", help="Text color (in hex)")
    parser.add_argument("--bg-color", type=str, default="#ffffff",help="Image background color (in hex)")
    parser.add_argument("--outline-thickness", type=int, default=0, help="Thickness of the outline around text (0 = no outline)")
    parser.add_argument("--outline-color", type=str, default="#000000",help="Outline color in HEX format")

    return parser.parse_args()

import random

def get_words_from_file(filepath, count, lines=False, line_index=0, randomWords=False):
    with open(filepath, "r", encoding="utf-8") as file:
        if lines:

            if(randomWords):
                line_index =  random.randint(0,len(all_lines))

            all_lines = [line.strip() for line in file if line.strip()]
            
            if 0 < line_index < len(all_lines):

                selected = all_lines[i]
                return "".join(selected)
            
            if not randomWords:
                return " ".join(all_lines[:count])
            
            if count > len(all_lines):
                count = len(all_lines)
            selected_lines = random.sample(all_lines, count)
            return " ".join(selected_lines)

        else:
            text = file.read()
            words = text.split()

            if not randomWords:
                return " ".join(words[:count])

            if count > len(words):
                count = len(words)
            selected_words = random.sample(words, count)
            return " ".join(selected_words)



if __name__ == "__main__":
    args = parse_args()

    if args.text_mode in ["DEFINED_LIST", "DEFINED_LIST_RANDOM"] and not args.input_file:
        print("--input-file is required when --text-mode is DEFINED_LIST or DEFINED_LIST_RANDOM")
        exit(1)

    DATA_COUNT = args.data_count
    TEST_FONT = args.test_font
    FONT_SIZE = args.font_size
    NUM_WORDS = args.num_words
    HEIGHT_PADING = args.height_padding
    WIDTH_PADING = args.width_padding
    BASE_X = args.base_x
    BASE_Y = args.base_y
    BASE_X_PADING = args.base_x_padding
    BASE_Y_PADING = args.base_y_padding
    OUTPUT_PATH = args.output_path
    INPUT_FILE = args.input_file
    TEXT_MODE = args.text_mode
    BG_COLOR = args.bg_color
    TEXT_COLOR = args.text_color
    OUTLINE_THICKNESS = args.outline_thickness
    OUTLINE_COLOR = args.outline_color

    r = RandomWords()

    print(f"\nGenerating {DATA_COUNT} items using font: {TEST_FONT}, text mode: {TEXT_MODE}")

    if(not os.path.exists(OUTPUT_PATH)):
        os.mkdir(OUTPUT_PATH)
        
    for i in range(DATA_COUNT):

        # Create a temporary image to get the size of the text
        tmp = Image.new(mode="RGB", size=(200, 200))
        d = ImageDraw.Draw(tmp)

        try:
            font = ImageFont.truetype(TEST_FONT, FONT_SIZE)
        except IOError:
            font = ImageFont.load_default()
        
        text = ""
        for j in range(NUM_WORDS):
            text += r.get_random_word() + " "
        
        text = text.strip()

        match(TEXT_MODE):
        
            case "DEFINED_LIST":
                text = get_words_from_file(INPUT_FILE,NUM_WORDS)

            case "DEFINED_LIST_LINES":
                text = get_words_from_file(INPUT_FILE,NUM_WORDS,lines=True,line_index=i)

            case "DEFINED_LIST_RANDOM":
                text = get_words_from_file(INPUT_FILE,NUM_WORDS,randomWords=True)

            case "DEFINED_LIST_RANDOM_LINE":
                text = get_words_from_file(INPUT_FILE,NUM_WORDS,lines=True,randomWords=True)

            case "RANDOM_LOWER":
                text = text
            
            case "RANDOM_UPPER":
                text = text.upper()

            case "RANDOM_CASE":
                text = list(text)

                for j in range(len(text)):

                    if(random.randint(0,1)):
                        text[j] = text[j].upper()

                text = "".join(text)

        __,__,width,height = d.textbbox((0,0), text, font=font, align="left")

        # Create image with padding and background
        img = Image.new('RGB', (width + WIDTH_PADING, height + HEIGHT_PADING), color=BG_COLOR)
        d = ImageDraw.Draw(img)

        x = BASE_X + BASE_X_PADING
        y = BASE_Y + BASE_Y_PADING

        if(OUTLINE_THICKNESS > 0):                                              # Draw outline first (all surrounding pixels)
            for dx in range(-OUTLINE_THICKNESS, OUTLINE_THICKNESS + 1):
                for dy in range(-OUTLINE_THICKNESS, OUTLINE_THICKNESS + 1):
                    if dx != 0 or dy != 0:
                        d.text((x + dx, y + dy), text, font=font, fill=OUTLINE_COLOR)

        d.text((x, y), text, font=font, fill=TEXT_COLOR)

        img.save(f"{OUTPUT_PATH}/generated_data{str(i)}.png")

        with open(f"{OUTPUT_PATH}/generated_data{str(i)}.gt.txt", "w") as file:
            file.write(text)

        # print(f"Generated Data #{str(i)}")

    print("done")
