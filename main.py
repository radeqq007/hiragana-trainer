from rich.console import Console
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from InquirerPy import inquirer
from gtts import gTTS
from pygame import mixer
from io import BytesIO
import os
import json
import random
import time

console = Console()

chars = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "ka": "か",
    "ki": "き",
    "ku": "く",
    "ke": "け",
    "ko": "こ",
    "sa": "さ",
    "shi": "し",
    "su": "す",
    "se": "せ",
    "so": "そ",
    "ta": "た",
    "chi": "ち",
    "tsu": "つ",
    "te": "て",
    "to": "と",
    "na": "な",
    "ni": "に",
    "nu": "ぬ",
    "ne": "ね",
    "no": "の",
    "ha": "は",
    "hi": "ひ",
    "fu": "ふ",
    "he": "へ",
    "ho": "ほ",
    "ma": "ま",
    "mi": "み",
    "mu": "む",
    "me": "め",
    "mo": "も",
    "ya": "や",
    "yu": "ゆ",
    "yo": "よ",
    "ra": "ら",
    "ri": "り",
    "ru": "る",
    "re": "れ",
    "ro": "ろ",
    "wa": "わ",
    "wo": "を",
    "n": "ん"
}

enabled_chars = list()

STORAGE_FILE = "enabled_chars.json"


def save_state():
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(enabled_chars, f, ensure_ascii=False, indent=2)


def load_state():
    global enabled_chars
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            enabled_chars = json.load(f)


def start():
    if not enabled_chars:
        console.print("[red]No characters are enabled![/red]")
        pause()
        menu()
        return
    
    console.clear()

    option = inquirer.select(
        message="Select the mode: ",
        choices=[
            "Single Character",
            "Multiple Characters"
        ],
        cycle=True
    ).execute()

    if option == "Single Character":
        main_loop(1)
    elif option == "Multiple Characters":
        try:
            length_input = console.input("How many characters should be in one quiz question?\n> ")
            length = int(length_input)
            if length < 1 or length > len(enabled_chars):
                console.print(f"[red]Please enter a number between 1 and {len(enabled_chars)}.[/red]")
                pause()
                menu()
                return
            main_loop(length)
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
            pause()
            menu()
    else:
        console.print("Invalid option")
        pause()
        menu()

def main_loop(length: int):
    console.clear()

    correct = 0
    total = 0

    mixer.init()

    while True:
        char = random.sample(enabled_chars, length)

        cols = Columns(
            [f"What is the romaji for {''.join([chars[c] for c in char])}?",
             Align.right(f"{correct}/{total} ({(correct/total*100) if total > 0 else 0:.2f}%)")],
            equal=True,
            expand=True,
        )
        console.print(cols)
        console.print("> ", end="")

        answer = console.input()
        if answer == "".join(char):
            console.print("Correct!")
            correct += 1
        else:
            console.print(f"Wrong! The correct answer is {''.join([c for c in char])}")

        tts = gTTS(''.join([chars[c] for c in char]), lang="ja")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        mixer.music.load(fp)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.1)

        total += 1

        pause()

        console.clear()

def display_hiragana_table():
    table = Table()
    table.add_column("Hiragana")
    table.add_column("Romanji")
    for char in chars:
        table.add_row(chars[char], char)
    console.print(table)
    pause()
    menu()


def enabled_characters():
    global enabled_chars
    choices = [
        {"name": f"{chars[c]} ({c})", "value": c,
         "enabled": c in enabled_chars}
        for c in chars.keys()
    ]
    selected = inquirer.checkbox(
        message="Select enabled characters:",
        choices=choices,
        instruction="Use arrows + space to toggle, Enter to confirm",
        cycle=True
    ).execute()

    enabled_chars = [c for c in chars.keys() if c in selected]

    save_state()

    console.print(f"[green]Enabled characters updated![/green]")
    
    pause()

    menu()


def menu():
    console.clear()
    option = inquirer.select(
        message="Select an option: ",
        choices=[
            "Start",
            "Change Enabled Characters",
            "Display Hiragana Table",
            "Exit"
        ],
        cycle=True
    ).execute()

    if option == "Start":
        start()
    elif option == "Change Enabled Characters":
        enabled_characters()
    elif option == "Display Hiragana Table":
        display_hiragana_table()
    elif option == "Exit":
        exit()
    else:
        console.print("Invalid option")

def pause():
    console.print("Press any key to continue...", style="dim")
    console.input()

def main():
    global enabled_chars
    if os.path.exists(STORAGE_FILE):
        try:
            load_state()
        except json.JSONDecodeError:
            enabled_chars = list(chars.keys())
    else:
        enabled_chars = list(chars.keys())

    menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/red]")
