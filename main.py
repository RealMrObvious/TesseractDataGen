from PIL import Image, ImageDraw, ImageFont
from random_word import RandomWords
import random, argparse, os, time, subprocess

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

    parser.add_argument("--count", type=int, default=1, help="Number of data items to generate")
    parser.add_argument("--font-path", type=str, required=True, help="Path to the font file")
    parser.add_argument("--font-size", type=int, default=72, help="Font size in points")
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
    parser.add_argument("--char-spacing", type=int, default=0, help="Extra spacing between characters in pixels")
    parser.add_argument("--dpi", type=int, default=300, help="DPI of the image in pixels")
    parser.add_argument("--gen-boxes", type=bool, default=True, help="Generate .box files for the images?")
    
    return parser.parse_args()

import random

def get_words_from_file(filepath, count, lines=False, line_index=0, randomWords=False):
    with open(filepath, "r", encoding="utf-8") as file:
        if lines:
            all_lines = [line.strip() for line in file if line.strip()]

            if(randomWords):
                line_index =  random.randint(0,len(all_lines))
                selected = all_lines[line_index]
                return "".join(selected)
            
            if 0 < line_index < len(all_lines):
                selected = all_lines[line_index]
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

def draw_text_with_spacing(draw, position, text, font, fill, spacing, outline=0, outline_color=None):
    x, y = position
    for char in text:
        if outline > 0:
            for dx in range(-outline, outline + 1):
                for dy in range(-outline, outline + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), char, font=font, fill=outline_color)

        draw.text((x, y), char, font=font, fill=fill)
        char_width = draw.textlength(char, font=font)
        x += char_width + spacing

def generate_boxes(text, font, draw, image_height, base_x, base_y, spacing=0, outline=0):
    x_cursor = base_x
    y_baseline = base_y
    boxes = []

    for char in text:
        bbox = font.getbbox(char)
        char_width = draw.textlength(char, font=font)

        x1 = x_cursor
        y1 = image_height - (y_baseline + bbox[3])  # bottom
        x2 = x_cursor + char_width
        y2 = image_height - (y_baseline + bbox[1])  # top

        boxes.append(f"{char} {int(x1)} {int(y1) - outline} {int(x2) + outline} {int(y2) + outline} 0")

        x_cursor += char_width + spacing

    return boxes
    # Returns:        list[str]: Box lines in Tesseract format: char x1 y1 x2 y2 0


if __name__ == "__main__":
    args = parse_args()

    if args.text_mode in ["DEFINED_LIST", "DEFINED_LIST_RANDOM"] and not args.input_file:
        print("--input-file is required when --text-mode is DEFINED_LIST or DEFINED_LIST_RANDOM")
        exit(1)

    COUNT = args.count
    FONT_PATH = args.font_path
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
    CHARACTER_SPACING = args.char_spacing
    DPI = args.dpi
    GEN_BOXES = args.gen_boxes  

    r = RandomWords()

    start_time = time.time()
    print(f"\nGenerating {COUNT} items using font: {FONT_PATH}, text mode: {TEXT_MODE}")

    if(not os.path.exists(OUTPUT_PATH)):
        os.mkdir(OUTPUT_PATH)
        
    for i in range(COUNT):

        NUM_WORDS = random.randint(1,20)

        # Create a temporary image to get the size of the text
        tmp = Image.new(mode="RGB", size=(200, 200))
        d = ImageDraw.Draw(tmp)

        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except IOError:

            answers = ["Y","N"]
            answer = None
            while(answer == None):
                answer = input(f"\nThe current font path [{FONT_PATH}] isn't valid, use default font? (Y/N): ").upper().strip()
                if(answer not in answers):
                    answer = None
                
                if(answer == "Y"):
                    font = ImageFont.load_default()
                if(answer == "N"):
                    print("Exiting... (please fix your path)")
                    exit(1)
        
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

        #Calculate the width for dynamic character spacing
        __,__,width,height = d.textbbox((0,0), text, font=font, align="left")

        width += (len(text)-1) * CHARACTER_SPACING

        img = Image.new('RGB', (int(width + (2*WIDTH_PADING)), int(height + (2*HEIGHT_PADING))), color=BG_COLOR)
        d = ImageDraw.Draw(img)

        draw_text_with_spacing(
            d,
            (BASE_X + BASE_X_PADING, BASE_Y + BASE_Y_PADING),
            text,
            font,
            fill=TEXT_COLOR,
            spacing=CHARACTER_SPACING,
            outline=OUTLINE_THICKNESS,
            outline_color=OUTLINE_COLOR
        )

        image_path = f"{OUTPUT_PATH}/generated_word_data{str(i)}.png"


        img.save(image_path, dpi=(300, 300))


        if(GEN_BOXES):
            boxes = generate_boxes(
                        text=text,
                        font=font,
                        draw=d,
                        image_height=img.height,
                        base_x=BASE_X,
                        base_y=BASE_Y,
                        spacing=CHARACTER_SPACING,
                        outline=OUTLINE_THICKNESS
                    )

        with open(image_path.replace(".png", ".box"), "w", encoding="utf-8") as f:
            f.write("\n".join(boxes))
        

        with open(image_path.replace(".png", ".gt.txt"), "w") as file:
            file.write(text)

    elapsed_time = time.time() - start_time
    print(f"Generated {str(COUNT)} items in: {elapsed_time} seconds")
