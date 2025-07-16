# Tesseract Data Generator Tool     


This is a simple tool/script to generates synthetic text image data for training or testing Tesseract OCR models. It allows you to control font style, padding, color, and text generation mode through command-line arguments. 

I haven't tested it to a great extent so Im not sure if it'll play nicely with every font, but I have yet to run into a problem. If you find a font that doesn't work well, please lmk.

---

## Requirements

- Python 3.7+
- [Pillow](https://pypi.org/project/Pillow/) – `pip install pillow`
- [Random-word](https://pypi.org/project/random-word/) – `pip install random-word`

---

## Usage

```bash
python main.py --test-font <path to test font> [options]
````

---

## Arguments / Options

| Argument           | Type  | Default         | Description                                                                                                             |
| ------------------ | ----- | --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `--test-font`      | str   | *(required)*    | Path to the `.ttf` font file                                                                                            |
| `--data-count`     | int   | `1`             | Number of samples to generate                                                                                           |
| `--num-words`      | int   | `1`             | Number of words generated per image (**Note:** increasing word count can *significantly* increases generation time)                                                                                     |
| `--font-size`      | int   | `45`            | Font size in points                                                                                                     |
| `--height-padding` | float | `5`             | Vertical padding around the text                                                                                        |
| `--width-padding`  | float | `5`             | Horizontal padding around the text                                                                                      |
| `--base-x`         | int   | `0`             | Base X offset for text rendering                                                                                        |
| `--base-y`         | int   | `0`             | Base Y offset for text rendering                                                                                        |
| `--base-x-padding` | float | `2.5`           | Additional X padding offset                                                                                             |
| `--base-y-padding` | float | `0`             | Additional Y padding offset                                                                                             |
| `--output-path`    | str   | `GeneratedData` | Directory where output images will be saved                                                                             |
| `--text-mode`      | str   | `RANDOM_LOWER`  | Text generation mode. Options:<br> `DEFINED_LIST`, `DEFINED_LIST_RANDOM`, `RANDOM_LOWER`, `RANDOM_UPPER`, `RANDOM_CASE` |
| `--input-file`     | str   | `None`          | **Required** if using `DEFINED_LIST` or `DEFINED_LIST_RANDOM`. Path to file with source words                           |
| `--text-color`     | str   | `#000000`       | Text color in HEX format (e.g., `#000000` for black)                                                                    |
| `--bg-color`       | str   | `#ffffff`       | Background color in HEX format (e.g., `#ffffff` for white)                                                              |
| `--outline-thickness`     | int   | `0`       | Thickness of the outline around text (0 = no outline)                                                                    |
| `--bg-color`       | str   | `#000000`       | Outline color in HEX format (e.g., `#000000` for black)                                                              |


---


## Example

```bash
python main.py \
  --data-count 100 \
  --test-font "C:/Windows/Fonts/Arial.ttf" \
  --font-size 28 \
  --output-path "./output" \
  --text-mode RANDOM_UPPER \
  --text-color "#000000" \
  --bg-color "#ffffff"
```

---

## Input File Requirement

If `--text-mode` is set to either `DEFINED_LIST` or `DEFINED_LIST_RANDOM`, you **must** provide an `--input-file` containing words (one per line or space-separated).

```bash
python main.py --text-mode DEFINED_LIST --input-file wordlist.txt ...
```
---
## Output

Each generated sample will be saved to the specified `--output-path` directory as an image (`.png`) with a configured text file (`.gt.txt`).

---

## Text Modes

* `DEFINED_LIST` — Uses words sequentially from a provided file.
* `DEFINED_LIST_RANDOM` — Randomly selects words from a provided file.
* `RANDOM_LOWER` — Random lowercase words (e.g., `hello world`).
* `RANDOM_UPPER` — Random uppercase words (e.g., `HELLO WORLD`).
* `RANDOM_CASE` — Random mixed-case words (e.g., `HEllO worlD`).

---
